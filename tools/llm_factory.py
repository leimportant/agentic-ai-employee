"""
LLM Factory with multi-provider fallback.
Order: Groq → Gemini → OpenAI → Kiro (Anthropic)
"""

import os
from dotenv import load_dotenv

load_dotenv()


def _get_providers(temperature):
    """Return list of available (name, llm) tuples."""
    providers = []

    if os.getenv("GROQ_API_KEY", "").strip():
        from langchain_groq import ChatGroq
        providers.append(("Groq", ChatGroq(model="llama-3.3-70b-versatile", temperature=temperature)))

    if os.getenv("GOOGLE_API_KEY", "").strip():
        from langchain_google_genai import ChatGoogleGenerativeAI
        providers.append(("Gemini", ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=temperature)))

    if os.getenv("OPENAI_API_KEY", "").strip():
        from langchain_openai import ChatOpenAI
        providers.append(("OpenAI", ChatOpenAI(model="gpt-4o-mini", temperature=temperature)))

    if os.getenv("KIRO_API_KEY", "").strip():
        from langchain_anthropic import ChatAnthropic
        providers.append(("Kiro", ChatAnthropic(model="claude-sonnet-4-20250514", temperature=temperature, api_key=os.getenv("KIRO_API_KEY"))))

    if os.getenv("Z_API_KEY", "").strip():
        from langchain_openai import ChatOpenAI
        providers.append(("Z.AI", ChatOpenAI(
            model="glm-5.2",
            temperature=temperature,
            api_key=os.getenv("Z_API_KEY"),
            base_url="https://api.z.ai/api/paas/v4/"
        )))

    if not providers:
        raise RuntimeError("No API keys found. Set GROQ_API_KEY, GOOGLE_API_KEY, OPENAI_API_KEY, KIRO_API_KEY, or Z_API_KEY in .env")

    return providers


class FallbackLLM:
    """LLM wrapper that tries multiple providers on failure."""

    def __init__(self, temperature=0.7):
        self.providers = _get_providers(temperature)

    def invoke(self, messages, **kwargs):
        last_error = None
        for name, llm in self.providers:
            try:
                response = llm.invoke(messages, **kwargs)
                return response
            except Exception as e:
                print(f"⚠️  {name} failed: {e}")
                last_error = e
                continue
        raise RuntimeError(f"All LLM providers failed. Last error: {last_error}")


def get_llm(temperature=0.7):
    return FallbackLLM(temperature)


get_llm_no_test = get_llm
