"""Provide a swagger model for mashumaru."""
# /// script
# dependencies = [
#   "camel-converter",
#   "python-slugify",
#   "PyYAML",
#   "types-PyYAML",
# ]
# ///

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from camel_converter import to_snake  # type: ignore[import-not-found]
from slugify import slugify  # type: ignore[import-untyped]
from yaml import CSafeLoader as SafeLoader  # type: ignore[import-untyped]
from yaml import load

PATH_TYPE_MAP = {"string": "str"}
PATH_METHOD_MAP = {"get": "GET", "put": "PUT", "delete": "DELETE"}

DEFINITION_NESTED_MAP = {
    ("ArrayOfHomeAppliances", "homeappliances"): "HomeAppliance",
    ("ArrayOfEvents", "items"): "Event",
    ("Program", "options"): "Option",
    ("Program", "constraints"): "ProgramConstraints",
    ("ArrayOfAvailablePrograms", "programs"): "EnumerateAvailableProgram",
    (
        "EnumerateAvailableProgram",
        "constraints",
    ): "EnumerateAvailableProgramConstraints",
    ("EnumerateAvailableProgramConstraints", "execution"): "Execution",
    ("ArrayOfPrograms", "programs"): "EnumerateProgram",
    ("ArrayOfPrograms", "active"): "Program",
    ("ArrayOfPrograms", "selected"): "Program",
    ("EnumerateProgram", "constraints"): "EnumerateProgramConstraints",
    ("EnumerateProgramConstraints", "execution"): "Execution",
    ("ProgramDefinition", "options"): "ProgramDefinitionOption",
    ("ProgramDefinitionOption", "constraints"): "ProgramDefinitionConstraints",
    ("ArrayOfOptions", "options"): "Option",
    ("ArrayOfImages", "images"): "Image",
    ("ArrayOfSettings", "settings"): "GetSetting",
    ("GetSetting", "constraints"): "SettingConstraints",
    ("PutSettings", "data"): "PutSetting",
    ("ArrayOfStatus", "status"): "Status",
    ("Status", "constraints"): "StatusConstraints",
    ("ArrayOfCommands", "commands"): "Command",
    ("PutCommands", "data"): "PutCommand",
}
PARAMETER_ENUM_MAP = {
    "Accept": "ContentType",
    "Accept-Language": "Language",
}


@dataclass
class Parameter:
    """Represent a path parameter."""

    name: str
    in_: str
    code_name: str = field(init=False)
    description: str | None = None
    required: bool = False
    type_: str | None = None
    enum: list[str] | None = None
    code_type: str = field(init=False)
    definition: str | None = None

    def __post_init__(self) -> None:
        """Initialize instance."""
        if self.type_ is None and self.definition is None:
            raise ValueError("Missing type or definition")
        code_name = self.definition or self.name
        self.code_name = f"{slugify(to_snake(code_name), separator='_')}"
        if self.enum:
            self.code_type = PARAMETER_ENUM_MAP[self.name]
        elif self.type_:
            self.code_type = PATH_TYPE_MAP[self.type_]
        elif definition := self.definition:
            self.code_type = definition
        else:
            self.code_type = ""


@dataclass(kw_only=True)
class SwaggerPathModel:
    """Represent a Swagger model."""

    path: str
    method: str
    summary: str
    operation_id: str
    headers: str = ""
    responses: dict[int, dict[str, Any]]
    description: str | None = None
    path_parameters: list[Parameter] | None = None
    body_parameter: Parameter | None = None
    data_parameter: str = ""
    docstring: str = ""
    signature: str = ""
    return_type: str = ""
    return_value: str = ""

    def __post_init__(self) -> None:
        """Initialize instance."""
        if self.path_parameters:
            headers = {
                param.name: param.code_name
                for param in self.path_parameters
                if param.in_ == "header"
            }
            items = ", ".join(f"'{key}': {val}" for key, val in headers.items())
            if items:
                self.headers = f"{{{items}}}"
            else:
                self.headers = "None"
        else:
            self.headers = "None"

        parameters = self.path_parameters or []
        if body_parameter := self.body_parameter:
            parameters.append(body_parameter)

        parameters_code = ", ".join(
            f"{param.code_name}: "
            f"{param.code_type}"
            f"{' | None = None' if not param.required else ''}"
            for param in sorted(parameters, key=lambda x: not x.required)
        ).strip()

        self.data_parameter = (
            f"\n            data={body_parameter.code_name}.to_dict(),"
            if body_parameter
            else ""
        )
        if self.description:
            description_lines = self.description.splitlines()
            description = "\n        ".join(description_lines)
        else:
            description = ""
        docstring = f"{self.summary.strip()}.\n\n        {description}".strip()
        docstring_ending = "\n        " if "\n" in docstring else ""
        self.docstring = f"{docstring}{docstring_ending}"
        self.signature = f"self, {parameters_code}".strip(", ")

        if (response := self.responses.get(200)) and (schema := response.get("schema")):
            self.return_type = schema["$ref"].split("/")[-1]
            self.return_value = (
                f"\n        return {self.return_type}"
                '.from_dict(response.json()["data"])'
            )
        else:
            self.return_type = "None"
            self.return_value = ""

    def generate_code(self) -> str:
        """Return the Python code as a string for this model."""
        return f"""
    async def {self.operation_id}({self.signature}) -> {self.return_type}:
        \"""{self.docstring}\"""
        {'response = ' if self.return_value != '' else ''}await self._auth.request(
            "{PATH_METHOD_MAP[self.method]}",
            f"{self.path.replace('haId', 'ha_id')}",
            headers={self.headers},{self.data_parameter}
        ){self.return_value}
"""


@dataclass(kw_only=True)
class DefinitionModelBase(ABC):
    """Represent a base definition model."""

    definition: str
    all_definitions: list[str]
    description: str | None = None
    generated_classes: set[str] = field(default_factory=set)

    @abstractmethod
    def generate_code(
        self, definition: str, *, generate_class: bool = False, required: bool = False
    ) -> str:
        """Return the Python code as a string for this model."""

    @staticmethod
    def generate_class(definition: str, description: str | None = None) -> str:
        """Return the Python code as a string for this model."""
        docstring = description or f"Represent {definition}"
        suffix = f'    """{docstring.strip()}."""\n' if docstring else ""
        return f"""
@dataclass
class {definition}(DataClassJSONMixin):
{suffix}
"""


@dataclass(kw_only=True)
class DefinitionModelUnknown(DefinitionModelBase):
    """Represent a string type model."""

    def generate_code(
        self, definition: str, *, generate_class: bool = False, required: bool = False
    ) -> str:
        """Return the Python code as a string for this model."""
        suffix = "" if required else " | None = None"
        return f"Any{suffix}"


@dataclass(kw_only=True)
class DefinitionModelString(DefinitionModelBase):
    """Represent a string type model."""

    def generate_code(
        self, definition: str, *, generate_class: bool = False, required: bool = False
    ) -> str:
        """Return the Python code as a string for this model."""
        suffix = "" if required else " | None = None"
        return f"str{suffix}"


@dataclass(kw_only=True)
class DefinitionModelStringEnum(DefinitionModelBase):
    """Represent a StrEnum type model."""

    enum: list[str]

    def generate_code(
        self, definition: str, *, generate_class: bool = False, required: bool = False
    ) -> str:
        """Return the Python code as a string for this model."""
        if (description := self.description) is None:
            raise ValueError("Missing description")
        suffix = "" if required else " | None = None"
        if generate_class:
            code_enum = "\n    ".join(
                f'{enum.upper()} = "{enum}"' for enum in self.enum
            )
            self.generated_classes.add(
                "\n\n"
                f"class {definition.capitalize()}(StrEnum):\n"
                f'    """{description.strip()}."""\n\n    '
                f"{code_enum}"
                "\n\n"
            )
        return f"{definition.capitalize()}{suffix}"


@dataclass(kw_only=True)
class DefinitionModelInteger(DefinitionModelBase):
    """Represent a integer type model."""

    format_: str | None = None

    def generate_code(
        self, definition: str, *, generate_class: bool = False, required: bool = False
    ) -> str:
        """Return the Python code as a string for this model."""
        suffix = "" if required else " | None = None"
        return f"int{suffix}"


@dataclass(kw_only=True)
class DefinitionModelBoolean(DefinitionModelBase):
    """Represent a boolean type model."""

    def generate_code(
        self, definition: str, *, generate_class: bool = False, required: bool = False
    ) -> str:
        """Return the Python code as a string for this model."""
        suffix = "" if required else " | None = None"
        return f"bool{suffix}"


@dataclass(kw_only=True)
class DefinitionModelStringNumberBoolean(DefinitionModelBase):
    """Represent a union of string number and boolean type model."""

    def generate_code(
        self, definition: str, *, generate_class: bool = False, required: bool = False
    ) -> str:
        """Return the Python code as a string for this model."""
        suffix = "" if required else " | None = None"
        return f"str | float | bool{suffix}"


@dataclass(kw_only=True)
class DefinitionModelArray(DefinitionModelBase):
    """Represent a array type model."""

    items: DefinitionModelBase = field(init=False)
    raw_items: dict[str, Any]

    def __post_init__(self) -> None:
        """Initialize instance."""
        self.items = create_definition_model(
            definition=self.definition,
            all_definitions=self.all_definitions,
            data=self.raw_items,
        )

    def generate_code(
        self, definition: str, *, generate_class: bool = False, required: bool = False
    ) -> str:
        """Return the Python code as a string for this model."""
        suffix = "" if required else " | None = None"
        if definition != self.definition and generate_class:
            item = definition
            if definition not in self.all_definitions:
                self.generated_classes.add(
                    "\n\n"
                    f"{self.generate_class(definition)}    "
                    f"{self.items.generate_code(definition)}"
                    "\n\n"
                )
        else:
            item = self.items.generate_code(definition, required=True)

        self.generated_classes.update(self.items.generated_classes)
        self.items.generated_classes.clear()
        return f"list[{item}]{suffix}"


@dataclass(kw_only=True)
class DefinitionModelObject(DefinitionModelBase):
    """Represent a object type model."""

    properties: dict[str, DefinitionModelBase] = field(init=False)
    raw_properties: dict[str, Any]
    required: list[str] | None = None

    def __post_init__(self) -> None:
        """Initialize instance."""
        properties: dict[str, DefinitionModelBase] = {}
        for property_name, data in self.raw_properties.items():
            properties[property_name] = create_definition_model(
                definition=self.definition,
                all_definitions=self.all_definitions,
                data=data,
            )

        self.properties = properties

    def generate_code(
        self, definition: str, *, generate_class: bool = False, required: bool = False
    ) -> str:
        """Return the Python code as a string for this model."""
        if definition != self.definition and generate_class:
            suffix = "" if required else " | None = None"
            if definition not in self.all_definitions:
                self.generated_classes.add(
                    "\n\n"
                    f"{self.generate_class(definition)}    "
                    f"{self.generate_code(definition)}"
                    "\n\n"
                )
            return f"{definition}{suffix}"
        properties = ""
        sorted_properties = {}
        if required_properties := self.required:
            for prop in required_properties:
                sorted_properties[prop] = self.properties[prop]
        sorted_properties.update(self.properties)

        generate_class = False
        original_definition = definition
        for prop, model in sorted_properties.items():
            required_property = bool(
                required_properties and prop in required_properties
            )
            if nested_definition := DEFINITION_NESTED_MAP.get((definition, prop)):
                definition = nested_definition
                generate_class = True
            if prop in ("data", "error") and definition == self.definition:
                model_code = model.generate_code(definition, required=required_property)
                properties += f"    {model_code}\n"
            else:
                prop_code = model.generate_code(
                    definition,
                    generate_class=generate_class,
                    required=required_property,
                )
                properties += f"    {prop}: {prop_code}\n"
            definition = original_definition
            self.generated_classes.update(model.generated_classes)
            model.generated_classes.clear()
        suffix = (
            "".join(self.generated_classes)
            if self.definition == original_definition
            else ""
        )
        return f"{properties}{suffix}".strip()


def load_yaml(path: str = "hcsdk-production.yaml") -> dict[str, Any]:
    """Load yaml."""
    raw = Path(path).read_text(encoding="utf-8")
    return load(raw, Loader=SafeLoader)


def create_definition_model(
    *,
    definition: str,
    all_definitions: list[str],
    data: dict[str, Any],
) -> DefinitionModelBase:
    """Return a definition model from data."""
    type_ = data.get("type")
    if type_ is None:
        return DefinitionModelUnknown(
            definition=definition,
            all_definitions=all_definitions,
            description=data.get("description"),
        )
    match type_:
        case "string":
            if enum := data.get("enum"):
                return DefinitionModelStringEnum(
                    definition=definition,
                    all_definitions=all_definitions,
                    description=data.get("description"),
                    enum=enum,
                )
            return DefinitionModelString(
                definition=definition,
                all_definitions=all_definitions,
                description=data.get("description"),
            )
        case "integer":
            return DefinitionModelInteger(
                definition=definition,
                all_definitions=all_definitions,
                format_=data.get("format"),
                description=data.get("description"),
            )
        case "boolean":
            return DefinitionModelBoolean(
                definition=definition,
                all_definitions=all_definitions,
                description=data.get("description"),
            )
        case "array":
            return DefinitionModelArray(
                definition=definition,
                all_definitions=all_definitions,
                raw_items=data["items"],
            )
        case "object":
            return DefinitionModelObject(
                definition=definition,
                all_definitions=all_definitions,
                required=data.get("required"),
                raw_properties=data["properties"],
                description=data.get("description"),
            )
        case ["string", "number", "boolean"]:
            return DefinitionModelStringNumberBoolean(  # type: ignore[unreachable]
                definition=definition,
                all_definitions=all_definitions,
                description=data.get("description"),
            )
        case _:
            raise ValueError(f"Missing model: {type_}")


def get_parameters(parameters: list[dict[str, Any]]) -> list[Parameter]:
    """Return parsed parameters."""
    return [
        Parameter(
            name=p_data["name"],
            in_=p_data["in"],
            description=p_data.get("description"),
            required=p_data.get("required", False),
            type_=p_data.get("type"),
            enum=p_data.get("enum"),
            definition=p_data.get("schema", {}).get("$ref", "").split("/")[-1],
        )
        for p_data in parameters
    ]


def run() -> None:
    """Run script."""
    swagger = load_yaml()
    content = """
\"""Provide a model for the Home Connect API.\"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from mashumaro.mixins.json import DataClassJSONMixin


class ContentType(StrEnum):
    \"""Represent the content type for the response.\"""

    APPLICATION_JSON = "application/vnd.bsh.sdk.v1+json"
    EVENT_STREAM = "text/event-stream"


class Language(StrEnum):
    \"""Represent the language for the response.\"""

    DE = "de-DE"
    EN = "en-US"
    EN_GB = "en-GB"

"""
    output = Path("output.py")

    all_definitions = list(swagger["definitions"])
    for definition, data in swagger["definitions"].items():
        definition_model = create_definition_model(
            definition=definition,
            all_definitions=all_definitions,
            data=data,
        )
        header = definition_model.generate_class(
            definition,
            definition_model.description,
        )
        body = definition_model.generate_code(definition)
        content += f"{header}    {body}\n"

    content += """

class Client:
    \"""Represent a client for the Home Connect API.\"""

    def __init__(self, auth: AbstractAuth) -> None:
        \"""Initialize the client.\"""
        self._auth = auth

"""

    for path, data in swagger["paths"].items():
        path_parameters: list[Parameter] | None = None
        for method, method_model in data.items():
            if method == "parameters":
                path_parameters = get_parameters(method_model)
            else:
                parameters = get_parameters(method_model.get("parameters", []))
                path_model = SwaggerPathModel(
                    path=path,
                    method=method,
                    summary=method_model["summary"],
                    operation_id=method_model["operationId"],
                    responses=method_model["responses"],
                    description=method_model.get("description"),
                    path_parameters=path_parameters,
                    body_parameter=parameters[0] if parameters else None,
                )
                content += path_model.generate_code()

    output.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    run()
