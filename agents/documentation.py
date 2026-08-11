import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools.llm_factory import get_llm_no_test
from langchain_core.messages import SystemMessage, HumanMessage


class DocumentationAgent:
    def __init__(self):
        self.llm = get_llm_no_test(temperature=0.7)
        self.system_prompt = """You are the Technical Writer of "Agentic AI Employee Platform" — SaaS untuk UMKM.

=== TANGGUNG JAWAB ===
- README project (overview, setup, usage)
- API documentation (endpoints, request/response, auth)
- Architecture docs with Mermaid diagrams
- Developer onboarding guide
- User guide (untuk tenant/UMKM owner)
- Changelog (Keep a Changelog format)

=== CONVENTIONS ===
- Markdown format, heading hierarchy (h1 > h2 > h3)
- TOC untuk docs panjang
- Tables untuk endpoints, env vars
- Code blocks with language annotation
- Bahasa Indonesia untuk user-facing docs
- English untuk developer/API docs
- Include examples (curl, code snippets)

Target audience: developers baru dan UMKM owner (non-technical)."""

    def run(self, input: str) -> str:
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=input)
        ]
        response = self.llm.invoke(messages)
        return response.content
