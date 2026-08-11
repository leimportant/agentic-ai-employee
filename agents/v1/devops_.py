
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

class DevOpsAgent:
    """
    A DevOpsAgent powered by Google's Generative AI, specialized in Docker,
    Docker Compose, Nginx, Deployment, and VPS management.
    """

    def __init__(self, model_name: str = "gemini-2.5-flash", api_key: str = None):
        """
        Initializes the DevOpsAgent.

        Args:
            model_name (str): The name of the Google Generative AI model to use (e.g., "gemini-2.5-flash").
            api_key (str, optional): Your Google API key. If not provided, the agent
                                     will attempt to load it from the GOOGLE_API_KEY
                                     environment variable.
        Raises:
            ValueError: If the API key is neither provided nor found in environment variables.
        """
        if api_key is None:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError(
                    "Google API Key not provided and GOOGLE_API_KEY environment "
                    "variable not set. Please provide an API key or set the environment variable."
                )

        self.llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)
        self.responsibilities = [
            "Docker",
            "Docker Compose",
            "Nginx",
            "Deployment",
            "VPS"
        ]
        self.system_prompt = (
            f"You are a highly skilled DevOps Agent. Your core expertise areas include: "
            f"{', '.join(self.responsibilities)}. "
            f"Provide clear, concise, and accurate advice, explanations, and solutions "
            f"related to these topics. Focus on practical and actionable guidance."
        )

    def run(self, question: str) -> str:
        """
        Processes a question using the underlying generative AI model,
        acting as a DevOps expert.

        Args:
            question (str): The question related to DevOps topics.

        Returns:
            str: The AI's response to the question. Returns an error message if an issue occurs.
        """
        full_prompt = f"{self.system_prompt}\n\nQuestion: {question}"
        try:
            response = self.llm.invoke([HumanMessage(content=full_prompt)])
            return response.content
        except Exception as e:
            return f"An error occurred while processing your request: {e}"
