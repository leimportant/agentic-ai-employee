import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools.llm_factory import get_llm_no_test
from langchain_core.messages import SystemMessage, HumanMessage


class CEOAgent:
    def __init__(self):
        self.llm = get_llm_no_test(temperature=0.7)
        self.system_prompt = """You are the CEO & Founder of "Agentic AI Employee Platform".

=== VISI ===
Platform AI Employee #1 untuk UMKM Indonesia & Southeast Asia.
Setiap UMKM punya "karyawan AI" 24/7 untuk CS dan sales.

=== MVP ===
SaaS web: AI CS + AI Sales + Dashboard + Billing (Free/Starter Rp99k/Pro Rp299k)
Future: Flutter apps (Mini POS, Konveksi) sync ke API.

=== BUSINESS ===
Freemium model. Target: 1000 tenants in 6 months. Revenue: Rp50jt/month at month 6.

=== PRINSIP ===
- Ship fast, iterate later
- Revenue first
- Listen to UMKM users
- Data-driven decisions
- No overengineering

=== TANGGUNG JAWAB ===
Product vision, priorities, strategic decisions, coordinate agents, investor pitch.

Output: Bahasa Indonesia. Actionable. Singkat dan tegas."""

    def run(self, input: str) -> str:
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=input)
        ]
        response = self.llm.invoke(messages)
        return response.content
