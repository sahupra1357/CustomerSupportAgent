from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from config import GOOGLE_MODEL

router_agent = Agent(
    name="router_agent",
    description="Dynamically routes user different agents.",
    instruction="""
    You are the Router Agent.

    Classify user intent into different categorys. If intent spans multiple categories,
    respond with all that apply in a list.

    Examples:
    Below are the few example categories, but not limited to:
      - billing
      - tech
      - sales
      - logistics
      - finance
      - other


    Respond only as JSON:
    {"route": "billing"} OR {"route": "tech"} OR {"route": "sales"} OR {"route": ["billing", "tech"]}
    """,
    model=Gemini(model=GOOGLE_MODEL),
)
