from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from tools.billing_tools import get_invoice, initiate_refund
from config import GOOGLE_MODEL

billing_agent = Agent(
    name="billing_agent",
    description="Handles billing issues, refunds, and invoices.",
    instruction="""
    You are the Billing Agent. Resolve billing inquiries, explain charges,
    fetch invoices, and issue refunds using available tools.
    """,
    output_key="billing_response",
    model=Gemini(model=GOOGLE_MODEL),
    tools=[get_invoice, initiate_refund],
)
