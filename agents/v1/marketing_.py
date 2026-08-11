
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

class MarketingAgent:
    """
    A sophisticated Marketing Agent designed to assist with various marketing responsibilities
    using Google's Generative AI models.

    Responsibilities:
    - SEO (Search Engine Optimization)
    - Landing page copy creation
    - Blog idea generation
    - Marketing strategy development
    """

    def __init__(self, model_name: str = "gemini-2.5-flash", temperature: float = 0.7):
        """
        Initializes the MarketingAgent with a specific Google Generative AI model.

        Args:
            model_name (str): The name of the generative model to use (e.g., "gemini-2.5-flash", "gemini-1.5-pro-latest").
                              Ensure you have access to the specified model.
            temperature (float): Controls the randomness of the output. Higher values (e.g., 0.8)
                                 make the output more creative, while lower values (e.g., 0.2)
                                 make it more focused and deterministic.
        
        Note:
            Ensure the GOOGLE_API_KEY environment variable is set with your Google API key
            before initializing this agent.
            Example: export GOOGLE_API_KEY="your_api_key_here"
        """
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError(
                "GOOGLE_API_KEY environment variable not set. "
                "Please set it to your Google API key before initializing MarketingAgent."
            )
        
        self.llm = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)
        self.system_prompt = (
            "You are a highly skilled Marketing Agent. Your expertise covers a wide range of marketing "
            "disciplines. When a user asks a question, provide detailed, actionable, and insightful "
            "responses tailored to their marketing needs. Your core responsibilities include:\n"
            "- **SEO Expert:** Provide comprehensive SEO recommendations, keyword analysis, content optimization "
            "strategies, and technical SEO advice.\n"
            "- **Landing Page Copywriter:** Craft compelling, high-converting landing page copy that drives "
            "user action and aligns with marketing goals.\n"
            "- **Blog Idea Generator:** Brainstorm creative, engaging, and relevant blog post ideas, including "
            "potential titles, outlines, and target audiences.\n"
            "- **Marketing Strategist:** Develop holistic marketing strategies, campaign plans, target audience "
            "segmentation, competitive analysis, and performance measurement frameworks.\n\n"
            "Always aim to provide practical advice and clear explanations."
        )

    def run(self, question: str) -> str:
        """
        Processes a marketing-related question or request using the configured LLM
        and returns a comprehensive response.

        Args:
            question (str): The user's marketing question or request (e.g., "Suggest 5 blog ideas for a SaaS product.",
                            "Write landing page copy for a new productivity app.",
                            "What's an SEO strategy for a local bakery?",
                            "Develop a marketing strategy for launching a new e-commerce store.").

        Returns:
            str: A detailed and actionable response from the Marketing Agent.
                 Returns an error message if the LLM call fails.
        """
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=question)
        ]

        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return (f"An error occurred while processing your request: {e}\n"
                    f"Please ensure your GOOGLE_API_KEY is valid and the model '{self.llm.model}' is accessible.")

# Example Usage (uncomment to run):
# if __name__ == "__main__":
#     # Make sure to set your GOOGLE_API_KEY environment variable
#     # For example: export GOOGLE_API_KEY="YOUR_API_KEY"
#
#     try:
#         agent = MarketingAgent(model_name="gemini-2.5-flash") # You can try "gemini-1.5-pro-latest" if available
#
#         print("--- Testing SEO Request ---")
#         seo_question = "What are the key SEO factors for a small business website targeting local customers?"
#         seo_response = agent.run(seo_question)
#         print(f"Question: {seo_question}\nResponse:\n{seo_response}\n")
#
#         print("--- Testing Landing Page Copy Request ---")
#         lp_question = "Write compelling landing page copy for a new online course on 'Mastering Python for Data Science'. Focus on benefits, urgency, and a clear call to action."
#         lp_response = agent.run(lp_question)
#         print(f"Question: {lp_question}\nResponse:\n{lp_response}\n")
#
#         print("--- Testing Blog Ideas Request ---")
#         blog_question = "Generate 5 engaging blog post ideas for a healthy food blog, targeting busy professionals."
#         blog_response = agent.run(blog_question)
#         print(f"Question: {blog_question}\nResponse:\n{blog_response}\n")
#
#         print("--- Testing Marketing Strategy Request ---")
#         strategy_question = "Outline a marketing strategy for launching a new sustainable clothing brand targeting Gen Z."
#         strategy_response = agent.run(strategy_question)
#         print(f"Question: {strategy_question}\nResponse:\n{strategy_response}\n")
#
#     except ValueError as e:
#         print(f"Error: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
