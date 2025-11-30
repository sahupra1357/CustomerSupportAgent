import time
import random
import json
import os
import re
from typing import List, Dict, Any, Optional
from core.toolbox import ToolBox
import google.generativeai as genai
from models import AgentResponse

class DepartmentAgent:
    def __init__(self, name: str, department: str, sub_depts: List[str]):
        self.name = name
        self.department = department
        self.sub_depts = sub_depts
        self.tools = ToolBox()
        
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp') 

    def process_task(self, task: Dict, user_context: Dict) -> AgentResponse:
        print(f"\n🤖 [{self.department} AGENT] Processing: {task['intent']}")
        
        # 1. Gather Context
        search_data = ""
        if task.get('requires_search'):
            search_data = self.tools.google_search(f"{self.department} {task['intent']}")

        # 2. Construct Prompt for the AI
        prompt = f"""
        You are the {self.department} Agent. 
        User Context: {json.dumps(user_context)}
        Knowledge Base Info: {search_data}
        Task: {task['intent']}
        
        Your Goal: Resolve the issue autonomously if possible.
        Rules:
        - If 'Refund' and User is 'Premium', approve it.
        - If 'Technical' and requires physical hardware fix, you CANNOT solve it (return success=False).
        - If 'Tracking', provide the status.
        
        Output strictly valid JSON:
        {{ "success": boolean, "message": "string response to user", "action_taken": "string" }}
        """

        # 3. Generate Decision
        try:
            # Call Google Gemini API
            response = self.model.generate_content(prompt)
            # Clean up json markdown if present
            clean_json = response.text.replace("```json", "").replace("```", "")
            decision = json.loads(clean_json)

            return AgentResponse(decision['success'], decision['message'], decision.get('action_taken'))

        except Exception as e:
            print(f"  [Error] Agent crashed: {e}")
            return AgentResponse(False, "Internal Agent Error")

    def _mock_decision(self, task, user_context):
        # Fallback logic for demo purposes
        intent = task['intent'].lower()
        if "refund" in intent and user_context['tier'] == "Premium":
            return {"success": True, "message": "Refund processed for Premium member.", "action_taken": "refund_api"}
        if "broken" in intent:
            return {"success": False, "message": "Physical damage requires human inspection.", "action_taken": "escalate"}
        return {"success": True, "message": "I have logged your request.", "action_taken": "log"}
