"""Provide a swagger model for mashumaru."""  # noqa: INP001
# /// script
# dependencies = [
#   "PyYAML",
#   "types-PyYAML",
# ]
# ///

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from yaml import CSafeLoader as SafeLoader  # type: ignore[import-untyped]
from yaml import load

TYPE_MAP = {"string": "str"}
METHOD_MAP = {"get": "GET", "put": "PUT", "delete": "DELETE"}


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
            f"{param.name}: {TYPE_MAP[param.type_]}"
            for param in path_parameters
            if param.in_ == "path"
        ).strip()
        docstring = f"{self.summary}.\n\n    {self.description or ''}".strip()
        signature = f"self, {path_parameters_code}".strip(", ")
        return f"""
async def {self.operation_id}({signature}) -> None:
    \"""{docstring}\"""
    response = await self._auth.request({METHOD_MAP[self.method]}, {self.path})
    return response.json()
"""


def load_yaml() -> dict[str, Any]:
    """Load yaml."""
    raw = Path("hcsdk.yaml").read_text(encoding="utf-8")
    return load(raw, Loader=SafeLoader)


def run() -> None:
    """Run script."""
    swagger = load_yaml()
    for path, model in swagger["paths"].items():
        path_parameters: list[Parameter] | None = None
        for method, method_model in model.items():
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
                sw = SwaggerPathModel(
                    path=path,
                    method=method,
                    summary=method_model["summary"],
                    operation_id=method_model["operationId"],
                    description=method_model.get("description"),
                    path_parameters=path_parameters,
                )
                print(sw.generate_code())


if __name__ == "__main__":
    run()
