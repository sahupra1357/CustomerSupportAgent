from typing import Any, Dict
import os
from pathlib import Path

from google.adk.agents import Agent, LlmAgent
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.models.google_llm import Gemini
from google.adk.sessions import DatabaseSessionService
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from config import DB_PATH

print("✅ ADK components imported successfully.")

class FlowExecutor:
    def __init__(
        self,
        user_id: str,
        session_id: str,
        app_name: str = "customer_support_app",
        model_name: str = "gemini-2.5-flash-lite"
    ):
        self.app_name = app_name
        self.user_id = user_id  
        self.session_id = session_id
        self.model_name = model_name
        
        # Ensure db directory exists before creating database
        db_path = Path(DB_PATH).parent
        db_path.mkdir(parents=True, exist_ok=True)
        
        #self.session_service = InMemorySessionService()
        self.session_service = DatabaseSessionService(
            db_url=f"sqlite+aiosqlite:///{DB_PATH}",
        )
        print("✅ FlowExecutor initialized.")
    async def agent_runner(
        self,
        agent: Agent,
    ) -> Runner:
        return Runner(
            agent=agent,
            app_name=self.app_name,
            session_service=self.session_service)

    # Define helper functions that will be reused throughout the notebook
    async def run_session(self,
        runner_instance: Runner,
        user_queries: list[str] | str = None,
        session_name: str = "default",
    ):
        print(f"\n ### Session: {session_name}")

        # Get app name from the Runner
        app_name = runner_instance.app_name

        # Attempt to create a new session or retrieve an existing one
        try:
            session = await self.session_service.create_session(
                app_name=self.app_name, user_id=self.user_id, session_id=session_name
            )
        except:
            session = await self.session_service.get_session(
                app_name=self.app_name, user_id=self.user_id, session_id=session_name
            )

        # Process queries if provided
        last_event = None
        if user_queries:
            # Convert single query to list for uniform processing
            if type(user_queries) == str:
                user_queries = [user_queries]

            # Process each query in the list sequentially
            for query in user_queries:
                print(f"\nUser > {query}")

                # Convert the query string to the ADK Content format
                query = types.Content(role="user", parts=[types.Part(text=query)])

                # Stream the agent's response asynchronously
                async for event in runner_instance.run_async(
                    user_id=self.user_id, session_id=session.id, new_message=query
                ):
                    last_event = event
                    # Check if the event contains valid content
                    if event.content and event.content.parts:
                        # Filter out empty or "None" responses before printing
                        if (
                            event.content.parts[0].text != "None"
                            and event.content.parts[0].text
                        ):
                            print(f"{self.model_name} > ", event.content.parts[0].text)
        else:
            print("No queries!")
        
        return last_event


print("✅ Helper functions defined.")