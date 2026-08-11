"""
Code Writer — Parse LLM output and save code blocks to actual project files.

Supported formats:
1. ```filepath:backend/app/modules/auth/router.py
2. ```python\n# file: backend/app/modules/auth/router.py
3. ### `path/to/file.ext` followed by code block
4. ```path/to/file.ext  (most common from LLM)
"""

import os
import re

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def parse_code_blocks(llm_output: str) -> list[dict]:
    """Extract code blocks with file paths from LLM output."""
    blocks = []

    # Pattern: ```[optional_lang_or_path]\ncontent\n```
    # Capture everything between ``` markers
    all_blocks = re.findall(
        r"```([^\n]*)\n(.*?)```",
        llm_output, re.DOTALL
    )

    for header, code in all_blocks:
        header = header.strip()
        filepath = None

        # Check if header is a file path (has extension like .py, .tsx, .ts, .sql, .yaml, etc)
        if re.match(r"^(filepath:)?[\w/.()\-]+\.\w+$", header):
            filepath = header.replace("filepath:", "")

        # Check for # file: comment on first line
        if not filepath:
            file_match = re.match(r"#\s*file:\s*([\w/.()\-]+\.\w+)", code.strip())
            if file_match:
                filepath = file_match.group(1)
                code = re.sub(r"#\s*file:.*\n", "", code, count=1)

        if filepath:
            # Normalize: add backend/app/ prefix if starts with modules/ or models/ or services/
            if re.match(r"^(modules|models|services|middleware)/", filepath):
                filepath = "backend/app/" + filepath

            blocks.append({"path": filepath.strip(), "code": code.strip()})

    # Also try: ### `path/to/file` pattern
    heading_blocks = re.findall(
        r"###?\s*`([\w/.()\-]+\.\w+)`\s*\n+```\w*\s*\n(.*?)```",
        llm_output, re.DOTALL
    )
    for filepath, code in heading_blocks:
        if not any(b["path"] == filepath for b in blocks):
            blocks.append({"path": filepath.strip(), "code": code.strip()})

    return blocks


def write_files(blocks: list[dict], dry_run: bool = False) -> list[str]:
    """Write parsed code blocks to actual files."""
    written = []

    for block in blocks:
        filepath = os.path.join(PROJECT_ROOT, block["path"])
        dirpath = os.path.dirname(filepath)

        if dry_run:
            print(f"  [DRY RUN] {block['path']}")
            written.append(block["path"])
            continue

        os.makedirs(dirpath, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(block["code"])

        written.append(block["path"])
        print(f"  >> {block['path']}")

    return written


def process_llm_output(llm_output: str, dry_run: bool = False) -> list[str]:
    """Full pipeline: parse + write."""
    blocks = parse_code_blocks(llm_output)

    if not blocks:
        print("  No code blocks with file paths found.")
        return []

    print(f"\n  Found {len(blocks)} file(s) to write:")
    return write_files(blocks, dry_run)
