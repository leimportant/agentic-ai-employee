
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables from .env file
load_dotenv()

class CEOAgent:
    """
    The CEOAgent defines the product vision, sets business goals, prioritizes the roadmap,
    and coordinates other AI employees.
    """
    def __init__(self):
        """
        Initializes the CEOAgent with a Google Generative AI model and sets up
        the system prompt defining its responsibilities and persona.
        """
        # Initialize the LLM with a suitable model
        # Ensure GOOGLE_API_KEY is set in your environment or .env file
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY environment variable not set. Please set it in your .env file or environment.")
        
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash") # Using gemini-2.5-flash as a capable model
        
        self.system_prompt = (
            "You are a CEO and Founder of an AI Employee Platform.\n\n"
            "Your responsibilities:\n"
            "- Define long-term vision.\n"
            "- Break down ideas into actionable tasks.\n"
            "- Prioritize MVP features.\n"
            "- Coordinate AI employees (Product Manager, Architect, Backend Engineer, Frontend Engineer, QA, Documentation, DevOps).\n"
            "- Think like a startup founder.\n"
            "- Focus on business value.\n"
            "- Avoid overengineering."
        )

    def run(self, question: str) -> str:
        """
        Processes a question using the CEO's persona and returns a strategic response.

        Args:
            question: The question or task for the CEO.

        Returns:
            The CEO's strategic response as a string.
        """
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=question),
        ]
        
        response = self.llm.invoke(messages)
        return response.content

# Example usage (optional, for testing purposes, would not be in the final return)
if __name__ == "__main__":
    # Ensure GOOGLE_API_KEY is set in your .env file or environment
    # Example .env content:
    # GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    
    ceo = CEOAgent()
    
    # Test case 1: Define product vision and initial goals
    q1 = "We need to build an AI Employee Platform. What's our MVP vision and first steps? Who should lead what?"
    print("--- Question 1 ---")
    print(f"CEO: {ceo.run(q1)}\n")
    
    # Test case 2: Prioritize roadmap
    q2 = "We have ideas for 'Automated HR onboarding', 'AI-driven code generation', and 'Intelligent customer support bots'. Which should be our MVP focus?"
    print("--- Question 2 ---")
    print(f"CEO: {ceo.run(q2)}\n")

    # Test case 3: Strategic decision
    q3 = "Competitor X just launched a similar platform. How should we react strategically?"
    print("--- Question 3 ---")
    print(f"CEO: {ceo.run(q3)}\n")
