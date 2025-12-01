from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from tools.tech_tools import run_diagnostics
from tools.kb_search import google_search
from config import GOOGLE_MODEL

tech_agent = Agent(
    name="tech_agent",
    description="Helps resolve technical issues & device diagnostics.",
    instruction="""
    You are the Tech Support Agent. Diagnose device issues using diagnostics
    tools and provide steps to fix problems.
    """,
    output_key="tech_response",
    model=Gemini(model=GOOGLE_MODEL),
    tools=[run_diagnostics],
)
