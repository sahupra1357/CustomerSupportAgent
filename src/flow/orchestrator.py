from agents.router_agent import router_agent
from agents.single.billing_agent import billing_agent
from agents.single.tech_agent import tech_agent
from agents.single.sales_agent import sales_agent
from agents.single.misc_agent import misc_agent
from agents.supervisor_agent import supervisor_agent
from flow.executor import FlowExecutor
from utils import trim_back_ticks
from agents.multiple.parallel import create_root_agent
import json

class CustomerSupportFlow:

    def __init__(self, api_key: str, model: str="gemini-2.5-flash-lite", user_id: str="user123", session_id: str="session123"):
        self.api_key = api_key
        self.model = model
        self.user_id = user_id
        self.session_id = session_id
        self.flow_executor = FlowExecutor(user_id=self.user_id, session_id=self.session_id)

    async def run(self, user_input):
        # 1. Route intent
        
        runner = await self.flow_executor.agent_runner(router_agent)
        route_event = await self.flow_executor.run_session(runner, user_input, session_name="routing")
        
        # Extract the route from the response text
        if route_event and route_event.content and route_event.content.parts:
            response_text = route_event.content.parts[0].text
            print("Router Agent Response:", response_text)
            # Try to parse JSON response
            try:
                if response_text.strip().startswith("```"):
                    response_text = trim_back_ticks(response_text)
                route_data = json.loads(response_text)
                route = route_data.get("route", "misc")
                print("Parsed route data:", route, route_data)
            except:
                # Fallback: check if keywords are in the response
                response_lower = response_text.lower()
                print("Fallback response lower:", response_lower)
                if "billing" in response_lower:
                    route = "billing"
                elif "tech" in response_lower:
                    route = "tech"
                elif "sales" in response_lower:
                    route = "sales"
                else:
                    route = "misc"
        else:
            route = "misc"

        print(f"Determined route: {route}")
        # 2. Select specialist agent
        agent_list = []

        for spl in route if isinstance(route, list) else [route]:
            if spl == "billing":
                agent_list.append(billing_agent)
            elif spl == "tech":
                agent_list.append(tech_agent)
            elif spl == "sales":
                agent_list.append(sales_agent)
            else:
                agent_list.append(misc_agent)

        print(f"Routed to {[agent.name for agent in agent_list]} agents.")

        # 3 - Run all selected agents in parallel

        root_agent = create_root_agent(agent_list)
        root_runner = await self.flow_executor.agent_runner(root_agent)
        root_event = await self.flow_executor.run_session(root_runner, user_input, session_name="processing")

        if root_event and root_event.content and root_event.content.parts:
            root_response = root_event.content.parts[0].text
            print("Final Agent Response:", root_response)
            try:
                if root_response.strip().startswith("```"):
                    root_response = trim_back_ticks(root_response)
                root_response_data = json.loads(root_response)
                print("Parsed final response data:", root_response_data)
            except:
                print("Root response:", root_response)
        else:
            root_response = "I'm sorry, I couldn't process your request at this time."

        # 4. Supervisor validates / enhances
        # Pass the aggregated response to the supervisor for final review
        supervisor_input = f"Review and enhance this customer support response:\n\n{root_response}"
        
        supervisor_runner = await self.flow_executor.agent_runner(supervisor_agent)
        supervisor_event = await self.flow_executor.run_session(supervisor_runner, supervisor_input, session_name="final_review")

        if supervisor_event and supervisor_event.content and supervisor_event.content.parts:
            supervisor_response = supervisor_event.content.parts[0].text
            print("Supervisor Agent Response:", supervisor_response)
            try:
                if supervisor_response.strip().startswith("```"):
                    supervisor_response = trim_back_ticks(supervisor_response)
                supervisor_response_data = json.loads(supervisor_response)
                final_response = supervisor_response_data.get("final", supervisor_response)
            except:
                print("Supervisor response:", supervisor_response)
                final_response = supervisor_response
        else:
            final_response = root_response  # Fall back to aggregated response if supervisor fails

        return final_response

if __name__ == "__main__":
    import asyncio

    async def test_flow():
        flow = CustomerSupportFlow()
        user_question = "I need help with my billing statement and my laptop is not working."
        response = await flow.run(user_question)
        print("Final Response:", response)

    asyncio.run(test_flow())