"""Provide a swagger model for mashumaru."""  # noqa: INP001
# /// script
# dependencies = [
#   "PyYAML",
#   "types-PyYAML",
# ]
# ///

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from yaml import CSafeLoader as SafeLoader  # type: ignore[import-untyped]
from yaml import load

PATH_TYPE_MAP = {"string": "str"}
PATH_METHOD_MAP = {"get": "GET", "put": "PUT", "delete": "DELETE"}

DEFINITION_NESTED_MAP = {
    ("ArrayOfHomeAppliances", "homeappliances"): "HomeAppliance",
    ("ArrayOfEvents", "items"): "Event",
    ("Program", "options"): "Option",
    ("ArrayOfAvailablePrograms", "programs"): "EnumerateAvailableProgram",
    (
        "EnumerateAvailableProgram",
        "constraints",
    ): "EnumerateAvailableProgramConstraints",
    ("ArrayOfPrograms", "programs"): "EnumerateProgram",
    ("EnumerateProgram", "constraints"): "EnumerateProgramConstraints",
    ("ProgramDefinition", "options"): "ProgramDefinitionOption",
    ("ProgramDefinitionOption", "constraints"): "ProgramDefinitionConstraints",
    ("ArrayOfOptions", "options"): "Option",
    ("ArrayOfImages", "images"): "Image",
    ("ArrayOfSettings", "settings"): "GetSetting",
    ("GetSetting", "constraints"): "SettingConstraints",
    ("PutSettings", "data"): "PutSetting",
    ("ArrayOfStatus", "status"): "Status",
    ("Status", "constraints"): "StatusConstraints",
}


@dataclass
class Parameter:
    """Represent a path parameter."""

    name: str
    in_: str
    description: str | None
    required: bool
    type_: str


@dataclass
class SwaggerPathModel:
    """Represent a Swagger model."""

    path: str
    method: str
    summary: str
    operation_id: str
    description: str | None = None
    path_parameters: list[Parameter] | None = None
    method_parameters: list[Parameter] | None = None

    def generate_code(self) -> str:
        """Return the Python code as a string for this model."""
        path_parameters = self.path_parameters or []
        path_parameters_code = ", ".join(
            f"{param.name}: {PATH_TYPE_MAP[param.type_]}"
            for param in path_parameters
            if param.in_ == "path"
        ).strip()
        docstring = f"{self.summary}.\n\n    {self.description or ''}".strip()
        signature = f"self, {path_parameters_code}".strip(", ")
        return f"""
async def {self.operation_id}({signature}) -> None:
    \"""{docstring}\"""
    response = await self._auth.request({PATH_METHOD_MAP[self.method]}, {self.path})
    return response.json()
"""


@dataclass(kw_only=True)
class DefinitionModelBase(ABC):
    """Represent a base definition model."""

    definition: str
    all_definitions: list[str]
    description: str | None = None

    @abstractmethod
    def generate_code(self, definition: str, *, generate_class: bool = False) -> str:
        """Return the Python code as a string for this model."""

    @staticmethod
    def generate_class(definition: str, description: str | None = None) -> str:
        """Return the Python code as a string for this model."""
        docstring = description or f"Represent {definition}"
        suffix = f'    """{docstring.strip()}."""\n' if docstring else ""
        return f"""
@dataclass
class {definition}:
{suffix}
"""


@dataclass(kw_only=True)
class DefinitionModelUnknown(DefinitionModelBase):
    """Represent a string type model."""

    def generate_code(self, definition: str, *, generate_class: bool = False) -> str:
        """Return the Python code as a string for this model."""
        return "unknown"


@dataclass(kw_only=True)
class DefinitionModelString(DefinitionModelBase):
    """Represent a string type model."""

    def generate_code(self, definition: str, *, generate_class: bool = False) -> str:
        """Return the Python code as a string for this model."""
        return "str"


@dataclass(kw_only=True)
class DefinitionModelInteger(DefinitionModelBase):
    """Represent a integer type model."""

    format_: str | None = None

    def generate_code(self, definition: str, *, generate_class: bool = False) -> str:
        """Return the Python code as a string for this model."""
        return "int"


@dataclass(kw_only=True)
class DefinitionModelBoolean(DefinitionModelBase):
    """Represent a boolean type model."""

    def generate_code(self, definition: str, *, generate_class: bool = False) -> str:
        """Return the Python code as a string for this model."""
        return "bool"


@dataclass(kw_only=True)
class DefinitionModelStringNumberBoolean(DefinitionModelBase):
    """Represent a union of string number and boolean type model."""

    def generate_code(self, definition: str, *, generate_class: bool = False) -> str:
        """Return the Python code as a string for this model."""
        return "str | Number | bool"


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

    def generate_code(self, definition: str, *, generate_class: bool = False) -> str:
        """Return the Python code as a string for this model."""
        suffix = ""
        if definition != self.definition and generate_class:
            item = definition
            if definition not in self.all_definitions:
                suffix = (
                    "\n\n"
                    f"{self.generate_class(definition)}    "
                    f"{self.items.generate_code(definition)}"
                    "\n\n"
                )
        else:
            item = self.items.generate_code(definition)
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

    def generate_code(self, definition: str, *, generate_class: bool = False) -> str:
        """Return the Python code as a string for this model."""
        if definition != self.definition and generate_class:
            suffix = ""
            if definition not in self.all_definitions:
                suffix = (
                    "\n\n"
                    f"{self.generate_class(definition)}    "
                    f"{self.generate_code(definition)}"
                    "\n\n"
                )
            return f"{definition}{suffix}"
        properties = ""
        sorted_properties = {}
        if required := self.required:
            for prop in required:
                sorted_properties[prop] = self.properties[prop]
        sorted_properties.update(self.properties)

        generate_class = False
        original_definition = definition
        for prop, data in self.properties.items():
            if nested_definition := DEFINITION_NESTED_MAP.get((definition, prop)):
                definition = nested_definition
                generate_class = True
            if prop in ("data", "error") and definition == self.definition:
                properties += f"    {data.generate_code(definition)}\n"
            else:
                properties += (
                    f"    {prop}: "
                    f"{data.generate_code(definition, generate_class=generate_class)}\n"
                )
            definition = original_definition

        return f"{properties}".strip()


def load_yaml() -> dict[str, Any]:
    """Load yaml."""
    raw = Path("hcsdk.yaml").read_text(encoding="utf-8")
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


def run() -> None:
    """Run script."""
    swagger = load_yaml()
    for path, data in swagger["paths"].items():
        path_parameters: list[Parameter] | None = None
        for method, method_model in data.items():
            if method == "parameters":
                path_parameters = [
                    Parameter(
                        name=m_model["name"],
                        in_=m_model["in"],
                        description=m_model.get("description"),
                        required=m_model.get("required", False),
                        type_=m_model["type"],
                    )
                    for m_model in method_model
                ]
            else:
                path_model = SwaggerPathModel(
                    path=path,
                    method=method,
                    summary=method_model["summary"],
                    operation_id=method_model["operationId"],
                    description=method_model.get("description"),
                    path_parameters=path_parameters,
                )
                print(path_model.generate_code())

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
        print(f"{header}    {body}\n")


if __name__ == "__main__":
    run()
