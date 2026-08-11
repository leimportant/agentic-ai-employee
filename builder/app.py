import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash"
)

from commands.create_product_manager import COMMAND as PRODUCT_MANAGER_COMMAND
from commands.create_architect import COMMAND as ARCHITECT_COMMAND
from commands.create_backend_engineer import COMMAND as BACKEND_ENGINEER_COMMAND
from commands.create_frontend_engineer import COMMAND as FRONTEND_ENGINEER_COMMAND
from commands.create_qa import COMMAND as QA_COMMAND
from commands.create_documentation import COMMAND as DOCUMENTATION_COMMAND
from commands.create_devops import COMMAND as DEVOPS_COMMAND
from commands.create_marketing import COMMAND as MARKETING_COMMAND
from commands.create_ceo import COMMAND as CEO_COMMAND

commands = {
    "product_manager.py": PRODUCT_MANAGER_COMMAND,
    "architect.py": ARCHITECT_COMMAND,
    "backend_engineer.py": BACKEND_ENGINEER_COMMAND,
    "frontend_engineer.py": FRONTEND_ENGINEER_COMMAND,
    "qa.py": QA_COMMAND,
    "documentation.py": DOCUMENTATION_COMMAND,
    "devops.py": DEVOPS_COMMAND,
    "marketing.py": MARKETING_COMMAND,
    "ceo.py": CEO_COMMAND,
}

os.makedirs("agents", exist_ok=True)

for filename, command in commands.items():

    print(f"Generating {filename}...")

    response = llm.invoke(command)

    code = response.content
    code = code.replace("```python", "")
    code = code.replace("```", "")

    with open(
        f"agents/{filename}",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(code)

    print(f"{filename} generated successfully.")

print("All AI Employees created.")