import random
from typing import List, Dict, Any, Optional

class OrganizationData:
    def __init__(self):
        self.departments = {
            "BILLING": ["Refunds", "Invoicing", "Payment Methods"],
            "TECH_SUPPORT": ["Hardware", "Software", "Network"],
            "SALES": ["New Business", "Upgrades", "Enterprise"],
            "LOGISTICS": ["Order Tracking", "Returns", "Shipping"],
        }
        
        self.staff_db = [
            {"id": "S01", "name": "Alice Chen", "dept": "BILLING", "sub": "Refunds", "available": True},
            {"id": "S02", "name": "Bob Smith", "dept": "TECH_SUPPORT", "sub": "Hardware", "available": False}, 
            {"id": "S03", "name": "Charlie Kim", "dept": "TECH_SUPPORT", "sub": "Software", "available": True},
            {"id": "S04", "name": "Diana Prince", "dept": "SALES", "sub": "New Business", "available": True},
            {"id": "S05", "name": "Evan Wright", "dept": "LOGISTICS", "sub": "Order Tracking", "available": True},
        ]

    def get_available_staff(self, department: str, sub_department: str) -> Optional[Dict]:
        candidates = [
            s for s in self.staff_db 
            if s['dept'] == department and s['sub'] == sub_department and s['available']
        ]
        return random.choice(candidates) if candidates else None
