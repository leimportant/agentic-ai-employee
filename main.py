import os
import sys
import ast
import time
import argparse
from dotenv import load_dotenv

load_dotenv()

# =========================
# LLM INIT (multi-provider fallback)
# =========================
sys.path.insert(0, os.path.dirname(__file__))
from tools.llm_factory import get_llm

llm = get_llm(temperature=0.7)

# =========================
# GLOBAL PROMPT (INDONESIA + SAAS STANDARD)
# =========================
GLOBAL_PROMPT = """
# ROLE
Kamu adalah code generator untuk "Agentic AI Employee Platform" — SaaS yang mensimulasikan tim engineering startup menggunakan AI agents.

# KONTEKS
- Setiap agent = "digital employee" dengan role spesifik
- User = CEO / Product Owner yang memberi instruksi
- Platform ini multi-agent system di mana agent saling berkolaborasi

# STRICT OUTPUT RULES (WAJIB DIPATUHI)

1. Output HANYA Python code — tanpa markdown fence, tanpa penjelasan
2. Class-based architecture dengan format EXACT ini:

```
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools.llm_factory import get_llm_no_test
from langchain_core.messages import SystemMessage, HumanMessage

class {AgentName}Agent:
    def __init__(self):
        self.llm = get_llm_no_test(temperature=0.7)
        self.system_prompt = "..."  # role-specific

    def run(self, input: str) -> str:
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=input)
        ]
        response = self.llm.invoke(messages)
        return response.content
```

3. HANYA gunakan library berikut (JANGAN import library lain):
   - os, sys, langchain_core.messages, tools.llm_factory
4. JANGAN generate: placeholder comments, TODO, pseudo code, atau "pass"
5. system_prompt dalam __init__ HARUS detail dan spesifik sesuai role
6. Bahasa di system_prompt: Bahasa Inggris
7. Jika agent butuh method tambahan selain run(), boleh ditambah

# QUALITY CHECKLIST
- [ ] Class name sesuai role + suffix "Agent" (e.g. ArchitectAgent)
- [ ] __init__ ada self.llm dan self.system_prompt
- [ ] run() menerima str, return str
- [ ] Tidak ada import yang tidak digunakan
- [ ] Code bisa langsung dieksekusi tanpa error
"""

# =========================
# ROLE COMMANDS
# =========================
from commands.create_product_manager import COMMAND as PRODUCT_MANAGER_COMMAND
from commands.create_architect import COMMAND as ARCHITECT_COMMAND
from commands.create_backend_engineer import COMMAND as BACKEND_ENGINEER_COMMAND
from commands.create_frontend_engineer import COMMAND as FRONTEND_ENGINEER_COMMAND
from commands.create_qa import COMMAND as QA_COMMAND
from commands.create_documentation import COMMAND as DOCUMENTATION_COMMAND
from commands.create_devops import COMMAND as DEVOPS_COMMAND
from commands.create_marketing import COMMAND as MARKETING_COMMAND
from commands.create_ceo import COMMAND as CEO_COMMAND
from commands.create_ui_ux import COMMAND as UI_UX_COMMAND
from commands.create_database_engineer import COMMAND as DATABASE_ENGINEER_COMMAND

# =========================
# AGENT REGISTRY (output tanpa _ suffix, file *_.py = backup)
# =========================
ALL_COMMANDS = {
    "product_manager": PRODUCT_MANAGER_COMMAND,
    "architect": ARCHITECT_COMMAND,
    "backend_engineer": BACKEND_ENGINEER_COMMAND,
    "frontend_engineer": FRONTEND_ENGINEER_COMMAND,
    "qa": QA_COMMAND,
    "documentation": DOCUMENTATION_COMMAND,
    "devops": DEVOPS_COMMAND,
    "marketing": MARKETING_COMMAND,
    "ceo": CEO_COMMAND,
    "ui_ux": UI_UX_COMMAND,
    "database_engineer": DATABASE_ENGINEER_COMMAND,
}

# =========================
# CONFIG
# =========================
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


def validate_python(code: str) -> bool:
    """Validate generated code is valid Python syntax."""
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


def clean_code(raw: str) -> str:
    """Strip markdown code fences from LLM output."""
    code = raw.replace("```python", "").replace("```", "").strip()
    return code


def generate_agent(name: str, command: str) -> str | None:
    """Generate agent code with retry logic."""
    full_prompt = f"{GLOBAL_PROMPT}\n\n=========================\nROLE TASK:\n=========================\n{command}"

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = llm.invoke(full_prompt)
            code = clean_code(response.content)

            if validate_python(code):
                return code

            print(f"  ⚠️  [{name}] Attempt {attempt}: Output bukan valid Python, retrying...")
        except Exception as e:
            print(f"  ❌ [{name}] Attempt {attempt}: API error - {e}")

        if attempt < MAX_RETRIES:
            time.sleep(RETRY_DELAY)

    return None


def parse_args():
    parser = argparse.ArgumentParser(description="Agentic AI Employee Generator")
    parser.add_argument(
        "--agent", "-a",
        type=str,
        nargs="*",
        help="Specific agent(s) to generate (e.g. architect backend_engineer). Default: all",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available agents",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.list:
        print("Available agents:")
        for name in ALL_COMMANDS:
            print(f"  - {name}")
        return

    # Determine which agents to generate
    if args.agent:
        commands = {}
        for name in args.agent:
            key = name.rstrip("_")
            if key in ALL_COMMANDS:
                commands[key] = ALL_COMMANDS[key]
            else:
                print(f"❌ Unknown agent: {name}")
                print(f"   Available: {', '.join(ALL_COMMANDS.keys())}")
                sys.exit(1)
    else:
        commands = ALL_COMMANDS

    os.makedirs("agents", exist_ok=True)

    total = len(commands)
    success = 0
    failed = []

    print(f"🏗️  Generating {total} agent(s)...\n")

    for i, (name, command) in enumerate(commands.items(), 1):
        filename = f"{name}.py"
        print(f"[{i}/{total}] 🚀 Generating {filename}...")

        code = generate_agent(name, command)

        if code is None:
            print(f"[{i}/{total}] ❌ FAILED {filename} after {MAX_RETRIES} attempts\n")
            failed.append(filename)
            continue

        file_path = os.path.join("agents", filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

        success += 1
        print(f"[{i}/{total}] ✅ {filename} generated successfully\n")

    # Summary
    print("=" * 40)
    print(f"🎉 Done! {success}/{total} agents generated.")
    if failed:
        print(f"❌ Failed: {', '.join(failed)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
