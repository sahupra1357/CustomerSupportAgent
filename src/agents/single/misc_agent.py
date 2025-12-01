from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from config import GOOGLE_MODEL

misc_agent = Agent(
    name="misc_agent",
    description="Handles miscellanous issue and esclate to human if needed.",
    instruction="""
    You are the Misc Agent. Handle miscellanous inquiries and issues. If unable to resolve,
    escalate to human support. 
    """,
    output_key="misc_response",
    model=Gemini(model=GOOGLE_MODEL),
    tools=[],
)

