from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from tools.sales_tools import fetch_plan_options
from tools.kb_search import google_search
from config import GOOGLE_MODEL

sales_agent = Agent(
    name="sales_agent",
    description="Provides plan upgrades, discounts, and comparisons.",
    instruction="""
    You are the Sales/Upgrade Agent. Help customers pick a plan, upsell
    when appropriate, and explain pricing clearly.
    """,
    output_key="sales_response",
    model=Gemini(model=GOOGLE_MODEL),
    tools=[fetch_plan_options, google_search],
)
