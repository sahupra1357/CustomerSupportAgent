import time
import random
import json
import os
import re
from typing import List, Dict, Any, Optional

class AgentResponse:
    def __init__(self, success: bool, message: str, data: Any = None):
        self.success = success
        self.message = message
        self.data = data