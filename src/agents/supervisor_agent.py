from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from config import GOOGLE_MODEL

supervisor_agent = Agent(
    name="supervisor_agent",
    description="Ensures correctness, compliance, and tone.",
    instruction="""
    You are the Supervisor Agent.
    Review the agent response for:
      - factuality
      - policy compliance
      - friendly tone
      - clear steps

    If acceptable: output {"approved": true, "final": "<message>"}
    If not acceptable: rewrite the message.
    """,
    model=Gemini(model=GOOGLE_MODEL),
)
