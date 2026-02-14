#!/usr/bin/env python3
"""
Generate TypeScript types from Pydantic models
Ensures frontend and backend types stay in sync
"""

import json
from pathlib import Path
from typing import get_type_hints, get_origin, get_args
from datetime import datetime
from enum import Enum
import sys
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from models import types as model_types


def python_type_to_typescript(py_type) -> str:
    """Convert Python type to TypeScript type"""

    # Handle None/Optional
    if py_type is type(None):
        return "null"

    # Handle primitives
    if py_type is str:
        return "string"
    if py_type in (int, float):
        return "number"
    if py_type is bool:
        return "boolean"
    if py_type is datetime:
        return "Date"

    # Handle Optional (Union with None)
    origin = get_origin(py_type)
    if origin is type(None):
        return "null"

    # Handle Union types (including Optional)
    if origin in (type("|"), type(None)):
        args = get_args(py_type)
        if len(args) == 2 and type(None) in args:
            # Optional type
            non_none = [a for a in args if a is not type(None)][0]
            return f"{python_type_to_typescript(non_none)} | null"
        else:
            # Union type
            return " | ".join(python_type_to_typescript(arg) for arg in args)

    # Handle List
    if origin is list:
        args = get_args(py_type)
        if args:
            return f"Array<{python_type_to_typescript(args[0])}>"
        return "Array<any>"

    # Handle Dict
    if origin is dict:
        args = get_args(py_type)
        if len(args) == 2:
            return f"Record<{python_type_to_typescript(args[0])}, {python_type_to_typescript(args[1])}>"
        return "Record<string, any>"

    # Handle Literal
    if hasattr(py_type, "__origin__") and str(py_type.__origin__) == "typing.Literal":
        args = get_args(py_type)
        return " | ".join(f'"{arg}"' if isinstance(arg, str) else str(arg) for arg in args)

    # Handle Enums
    if isinstance(py_type, type) and issubclass(py_type, Enum):
        return py_type.__name__

    # Handle Pydantic models
    if hasattr(py_type, "__annotations__"):
        return py_type.__name__

    # Default
    return "any"


def generate_enum(enum_class) -> str:
    """Generate TypeScript enum"""
    lines = [f"export enum {enum_class.__name__} {{"]
    for member in enum_class:
        lines.append(f"  {member.name} = \"{member.value}\",")
    lines.append("}")
    return "\n".join(lines)


def generate_interface(model_class) -> str:
    """Generate TypeScript interface from Pydantic model"""
    lines = [f"export interface {model_class.__name__} {{"]

    # Get field annotations
    if hasattr(model_class, "model_fields"):
        # Pydantic v2
        for field_name, field_info in model_class.model_fields.items():
            ts_type = python_type_to_typescript(field_info.annotation)
            optional = "?" if not field_info.is_required() else ""
            lines.append(f"  {field_name}{optional}: {ts_type};")
    else:
        # Fallback to __annotations__
        annotations = getattr(model_class, "__annotations__", {})
        for field_name, field_type in annotations.items():
            ts_type = python_type_to_typescript(field_type)
            lines.append(f"  {field_name}: {ts_type};")

    lines.append("}")
    return "\n".join(lines)


def generate_typescript_file():
    """Generate complete TypeScript file"""
    output = []

    # Header
    output.append("/**")
    output.append(" * PedalBuild Type Definitions")
    output.append(" * AUTO-GENERATED from Python Pydantic models")
    output.append(" * DO NOT EDIT MANUALLY - Run: npm run generate:types")
    output.append(" */")
    output.append("")

    # Enums
    output.append("// ============================================================================")
    output.append("// ENUMS")
    output.append("// ============================================================================")
    output.append("")

    enums = [
        model_types.ComponentType,
        model_types.PedalCategory,
        model_types.DifficultyLevel,
        model_types.WorkflowStage,
        model_types.ProjectStatus,
        model_types.StageStatus,
    ]

    for enum_class in enums:
        output.append(generate_enum(enum_class))
        output.append("")

    # Interfaces
    output.append("// ============================================================================")
    output.append("// INTERFACES")
    output.append("// ============================================================================")
    output.append("")

    # Get all Pydantic models from types module
    models = []
    for name in dir(model_types):
        obj = getattr(model_types, name)
        if (isinstance(obj, type) and
            hasattr(obj, "model_fields") and
            not name.startswith("_")):
            models.append(obj)

    # Sort models for consistent output
    models.sort(key=lambda m: m.__name__)

    for model_class in models:
        output.append(generate_interface(model_class))
        output.append("")

    # Union types for stage data
    output.append("// ============================================================================")
    output.append("// UNION TYPES")
    output.append("// ============================================================================")
    output.append("")
    output.append("export type StageData =")
    output.append("  | InspirationData")
    output.append("  | SpecDownloadData")
    output.append("  | SchematicAnalysisData")
    output.append("  | InventoryCheckData")
    output.append("  | BOMGenerationData")
    output.append("  | BreadboardLayoutData")
    output.append("  | PrototypeTestingData")
    output.append("  | FinalAssemblyData")
    output.append("  | GraphicsDesignData")
    output.append("  | ShowcaseData;")
    output.append("")

    return "\n".join(output)


def main():
    """Main function"""
    print("🔄 Generating TypeScript types from Python Pydantic models...")

    # Generate TypeScript
    ts_content = generate_typescript_file()

    # Write to file
    output_path = Path(__file__).parent.parent / "src" / "models" / "types.generated.ts"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(ts_content)

    # Count lines
    line_count = len(ts_content.split("\n"))

    print(f"✅ Generated {line_count} lines of TypeScript")
    print(f"📝 Output: {output_path}")
    print("\n💡 Next step: Review and copy to types.ts if correct")


if __name__ == "__main__":
    main()
