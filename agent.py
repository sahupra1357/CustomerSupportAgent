import time
import random
import json
import os
import re
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from core.orchestrator import Orchestrator
from core.toolbox import ToolBox
from core.department import DepartmentAgent
from data.organization_data import OrganizationData
from models import AgentResponse

from dotenv import load_dotenv
load_dotenv()


# 🔑 TODO: Replace with your actual API key or set GOOGLE_API_KEY env variable
API_KEY = os.getenv("GOOGLE_API_KEY", "YOUR_API_KEY_HERE")


def main():
    orchestrator = Orchestrator()
    tools = ToolBox()

    # User Simulation
    user_id = "U-8823"
    user_context = tools.crm_lookup(user_id)
    user_query = "I bought a laptop that is physically broken and I want a refund immediately."

    # 1. Orchestration
    tasks = orchestrator.analyze_and_route(user_query)

    # 2. Execution
    for task in tasks:
        dept = task.get('dept')
        agent = orchestrator.agents.get(dept)
        
        if not agent:
            print(f"❌ Unknown Dept: {dept}")
            continue

        # Agent tries to solve
        response = agent.process_task(task, user_context)

        # 3. Scheduler / Escalation Logic
        if response.success:
            print(f"✅ [SOLVED] {response.message}")
        else:
            print(f"⚠️ [ESCALATING] Reason: {response.message}")
            human = orchestrator.data.get_available_staff(dept, task.get('sub_dept'))
            
            if human:
                orchestrator.generate_ticket(task, "Agent Escalation", human['name'])
            else:
                orchestrator.generate_ticket(task, "No Staff Available", "BACKLOG")

if __name__ == "__main__":
    main()