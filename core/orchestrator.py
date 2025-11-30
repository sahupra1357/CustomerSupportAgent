import time
import random
import json
import os
import re
from typing import List, Dict, Any, Optional

from core.department import DepartmentAgent
from data.organization_data import OrganizationData
import google.generativeai as genai

class Orchestrator:
    def __init__(self):
        self.data = OrganizationData()
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Initialize Agents
        self.agents = {
            name: DepartmentAgent(f"{name}Bot", name, subs) 
            for name, subs in self.data.departments.items()
        }

    def analyze_and_route(self, user_query: str) -> List[Dict]:
        print(f"🧠 [ORCHESTRATOR] Analyzing: \"{user_query}\"")
        
        # Prompt for the Router Agent
        prompt = f"""
        You are a Customer Support Router.
        Available Departments: {json.dumps(self.data.departments)}
        
        User Query: "{user_query}"
        
        Instructions:
        1. Break the query into distinct tasks (multi-intent support).
        2. Assign each task to a Department and Sub-Department.
        3. Determine if external info search is needed.
        
        Output strictly valid JSON list:
        [
            {{ "dept": "DEPT_NAME", "sub_dept": "Sub_Name", "intent": "summary", "requires_search": bool }}
        ]
        """

        try:
            response = self.model.generate_content(prompt)
            clean_text = response.text.replace("```json", "").replace("```", "")
            tasks = json.loads(clean_text)
            
            print(f"🧠 [ORCHESTRATOR] Routing {len(tasks)} tasks.")
            return tasks

        except Exception as e:
            print(f"  [Error] Orchestrator failed: {e}")
            return []

    def _mock_routing(self, query):
        # Fallback mock routing
        tasks = []
        q = query.lower()
        if "refund" in q:
            tasks.append({"dept": "BILLING", "sub_dept": "Refunds", "intent": "Process Refund", "requires_search": True})
        if "broken" in q:
            tasks.append({"dept": "TECH_SUPPORT", "sub_dept": "Hardware", "intent": "Hardware Issue", "requires_search": True})
        return tasks

    def generate_ticket(self, task, reason, assigned_to):
        tid = f"TKT-{random.randint(10000,99999)}"
        print(f"  🎫 [TICKET] {tid} assigned to {assigned_to} ({reason})")
        return tid
