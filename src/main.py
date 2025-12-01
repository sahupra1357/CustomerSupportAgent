import asyncio
from config import GOOGLE_API_KEY, GOOGLE_MODEL  # This imports and loads .env automatically
from flow.orchestrator import CustomerSupportFlow

async def main():
    flow = CustomerSupportFlow(api_key=GOOGLE_API_KEY, model=GOOGLE_MODEL, user_id="user123", session_id="session123")

    print("Type your question:")
    while True:
        user = input("> ")
        if user.lower() in ["x", "q"]:
            break

        response = await flow.run(user)
        print("\nAI:", response, "\n")

if __name__ == "__main__":
    asyncio.run(main())
