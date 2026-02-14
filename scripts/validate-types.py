#!/usr/bin/env python3
"""
Validate TypeScript types match generated types
Ensures types haven't drifted or been manually edited
"""

import difflib
from pathlib import Path
import sys


def validate_types():
    """Check that committed types match generated types"""

    base_path = Path(__file__).parent.parent / "src" / "models"
    generated_path = base_path / "types.generated.ts"
    committed_path = base_path / "types.ts"

    if not generated_path.exists():
        print("❌ Generated types file not found!")
        print(f"   Run: python scripts/generate-types.py")
        return False

    if not committed_path.exists():
        print("⚠️  types.ts not found, copying generated version...")
        committed_path.write_text(generated_path.read_text())
        print("✅ Created types.ts from generated types")
        return True

    # Compare files
    generated = generated_path.read_text()
    committed = committed_path.read_text()

    if generated == committed:
        print("✅ TypeScript types are in sync with Python models")
        return True
    else:
        print("❌ TypeScript types are out of sync!")
        print("\nDifferences:")
        print("=" * 80)

        diff = difflib.unified_diff(
            committed.splitlines(keepends=True),
            generated.splitlines(keepends=True),
            fromfile="types.ts (committed)",
            tofile="types.generated.ts (from Python)",
            lineterm=""
        )

        diff_lines = list(diff)
        for line in diff_lines[:50]:  # Show first 50 lines
            if line.startswith('+'):
                print(f"\033[92m{line}\033[0m", end="")  # Green
            elif line.startswith('-'):
                print(f"\033[91m{line}\033[0m", end="")  # Red
            else:
                print(line, end="")

        if len(diff_lines) > 50:
            print(f"\n... and {len(diff_lines) - 50} more lines")

        print("=" * 80)
        print("\n💡 To fix:")
        print("   1. Run: python scripts/generate-types.py")
        print("   2. Review: src/models/types.generated.ts")
        print("   3. Copy: cp src/models/types.generated.ts src/models/types.ts")
        return False


if __name__ == "__main__":
    success = validate_types()
    sys.exit(0 if success else 1)
