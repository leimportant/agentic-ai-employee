"""Shared runner logic for all runtime scripts."""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.code_writer import process_llm_output

CODE_MODE_SUFFIX = """

PENTING: Format output WAJIB seperti ini untuk SETIAP file:

```backend/app/modules/auth/router.py
kode lengkap di sini
```

```backend/app/modules/auth/schemas.py
kode lengkap di sini
```

```frontend/app/(dashboard)/billing/page.tsx
kode lengkap di sini
```

Rules:
- Satu code block per file
- Baris pertama setelah ``` HARUS path file relatif (dari project root)
- JANGAN tulis penjelasan di dalam code block
- Path harus ada extension (.py, .tsx, .ts, .sql, .yaml, dll)
- Prefix path: backend/app/... untuk FastAPI, frontend/... untuk Next.js"""


def run_agent(agent, agent_name: str, output_prefix: str):
    """Run agent with optional --code flag."""
    code_mode = "--code" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--code"]

    question = input(f"{agent_name} > ") if not args else " ".join(args)

    # Append code mode instruction
    if code_mode:
        question += CODE_MODE_SUFFIX

    result = agent.run(question)

    # Save markdown doc
    os.makedirs("docs/v1", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    md_file = f"docs/v1/{output_prefix}_{timestamp}.md"
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(result)

    print(result)
    print(f"\nOutput saved: {md_file}")

    # Code mode: also write files
    if code_mode:
        print("\n--- CODE MODE: Writing files ---")
        written = process_llm_output(result)
        if written:
            print(f"\n{len(written)} file(s) written to project.")
        else:
            print("\nNo files extracted. LLM mungkin belum pakai format yang benar.")
