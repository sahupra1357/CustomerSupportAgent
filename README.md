# Customer Support Agent System

An intelligent multi-agent customer support system built with Google ADK that routes, processes, and responds to customer inquiries across multiple departments (Billing, Technical Support, Sales).

## 🏗️ Architecture Overview

The system uses a sophisticated multi-agent architecture with routing, parallel processing, aggregation, and supervision layers.

## 🔄 Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INPUT                                  │
│            "I need help with billing and my laptop"                 │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    STEP 1: ROUTER AGENT                             │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │ • Analyzes user intent                                        │  │
│  │ • Classifies into categories: billing, tech, sales, misc     │  │
│  │ • Supports multi-category routing                            │  │
│  │ • Returns: {"route": ["billing", "tech"]}                    │  │
│  └───────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  STEP 2: AGENT SELECTION                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │ Maps routes to specialist agents:                            │  │
│  │  • "billing"  → Billing Agent                                │  │
│  │  • "tech"     → Tech Support Agent                           │  │
│  │  • "sales"    → Sales Agent                                  │  │
│  │  • other      → Misc Agent                                   │  │
│  └───────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│           STEP 3: PARALLEL PROCESSING (Root Agent)                  │
│                                                                     │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │             PARALLEL AGENT EXECUTION                        │   │
│  │                                                             │   │
│  │  ┌──────────────────┐    ┌──────────────────┐            │   │
│  │  │  Billing Agent   │    │ Tech Support     │            │   │
│  │  │                  │    │    Agent         │            │   │
│  │  │ • get_invoice()  │    │ • run_diagnostics│            │   │
│  │  │ • initiate_refund│    │ • google_search()│            │   │
│  │  │                  │    │                  │            │   │
│  │  │ Output:          │    │ Output:          │            │   │
│  │  │ ${billing_resp}  │    │ ${tech_response} │            │   │
│  │  └──────────────────┘    └──────────────────┘            │   │
│  │           │                        │                      │   │
│  └───────────┼────────────────────────┼──────────────────────┘   │
│              │                        │                          │
│              └────────────┬───────────┘                          │
│                           ▼                                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              AGGREGATOR AGENT                              │ │
│  │                                                            │ │
│  │ • Collects outputs from all parallel agents               │ │
│  │ • Synthesizes into a coherent executive summary           │ │
│  │ • References: ${billing_response}, ${tech_response}       │ │
│  │ • Creates unified customer response                       │ │
│  │                                                            │ │
│  │ Output: ${executive_support_summary}                      │ │
│  └────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│               STEP 4: SUPERVISOR AGENT                              │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │ Final Quality Assurance:                                      │  │
│  │  • Reviews aggregated response                                │  │
│  │  • Checks for factuality and accuracy                         │  │
│  │  • Ensures policy compliance                                  │  │
│  │  • Validates friendly and professional tone                   │  │
│  │  • Verifies clear actionable steps                            │  │
│  │  • Rewrites if necessary                                      │  │
│  │                                                               │  │
│  │ Returns: {"approved": true, "final": "<enhanced_message>"}   │  │
│  └───────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     FINAL RESPONSE TO USER                          │
│              Complete, validated, enhanced answer                   │
└─────────────────────────────────────────────────────────────────────┘
```

## 🧩 Component Details

### 1. **Router Agent**
- **Purpose**: Intent classification and routing
- **Model**: Gemini (configurable)
- **Output**: JSON with route(s) - supports multi-category routing
- **Example**: `{"route": ["billing", "tech"]}`

### 2. **Specialist Agents**

#### Billing Agent
- Handles billing inquiries, refunds, invoices
- **Tools**: 
  - `get_invoice(customer_id)` - Fetches customer invoices
  - `initiate_refund(invoice_id, amount)` - Processes refunds
- **Output Key**: `billing_response`

#### Tech Support Agent
- Diagnoses device issues and provides solutions
- **Tools**: 
  - `run_diagnostics(device_id)` - Runs system diagnostics
  - `google_search(query)` - Searches knowledge base
- **Output Key**: `tech_response`

#### Sales Agent
- Provides plan upgrades, pricing, comparisons
- **Tools**: 
  - `fetch_plan_options()` - Gets available plans
  - `google_search(query)` - Searches product info
- **Output Key**: `sales_response`

#### Misc Agent
- Handles miscellaneous inquiries
- Escalates to human support when needed
- **Output Key**: `misc_response`

### 3. **Root Agent (Sequential Agent)**
Combines parallel execution with aggregation:

#### a. Parallel Support Agent
- Executes multiple specialist agents simultaneously
- Each agent processes the user query independently
- Outputs are stored in session state with unique keys

#### b. Aggregator Agent
- Synthesizes all specialist outputs
- Creates coherent executive summary
- Uses template variables to reference agent outputs: `${billing_response}`, `${tech_response}`, etc.
- **Output Key**: `executive_support_summary`

### 4. **Supervisor Agent**
- Final quality control layer
- Reviews for:
  - ✅ Factual accuracy
  - ✅ Policy compliance
  - ✅ Professional tone
  - ✅ Clear action steps
- Can rewrite/enhance responses
- **Output**: JSON with approval status and final message

## 🔧 Technology Stack

- **Framework**: Google ADK (Agent Development Kit)
- **LLM**: Google Gemini (2.0-flash-exp for function calling support)
- **Language**: Python 3.12+
- **Session Management**: SQLite with async support (aiosqlite)
- **Environment**: python-dotenv for configuration

## 📁 Project Structure

```
CustomerSupportAgent/
├── src/
│   ├── config.py                    # Global configuration & env loading
│   ├── main.py                      # Entry point
│   ├── utils.py                     # Helper functions
│   ├── agents/
│   │   ├── router_agent.py          # Intent classification
│   │   ├── supervisor_agent.py      # Quality assurance
│   │   ├── single/
│   │   │   ├── billing_agent.py     # Billing specialist
│   │   │   ├── tech_agent.py        # Tech support specialist
│   │   │   ├── sales_agent.py       # Sales specialist
│   │   │   └── misc_agent.py        # Miscellaneous handler
│   │   └── multiple/
│   │       └── parallel.py          # Root agent with parallel execution
│   ├── flow/
│   │   ├── executor.py              # Flow execution engine
│   │   └── orchestrator.py          # Main orchestration logic
│   └── tools/
│       ├── billing_tools.py         # Billing functions
│       ├── tech_tools.py            # Tech support functions
│       ├── sales_tools.py           # Sales functions
│       └── kb_search.py             # Knowledge base search
├── db/                              # SQLite session database
├── .env                             # Environment variables (not in git)
├── .env.example                     # Environment template
├── pyproject.toml                   # Dependencies
└── README.md                        # This file
```

## 🚀 Setup & Installation

### 1. Clone Repository
```bash
git clone https://github.com/sahupra1357/CustomerSupportAgent.git
cd CustomerSupportAgent
```

### 2. Install Dependencies
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### 3. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your Google AI API key
# Get key from: https://aistudio.google.com/app/apikey
```

**`.env` file:**
```env
GOOGLE_API_KEY=your_api_key_here
GOOGLE_MODEL=gemini-2.0-flash-exp
DB_URL=sqlite+aiosqlite:///./db/adk_sessions.db
```

### 4. Run the Application
```bash
python ./src/main.py
```

## 💬 Example Interactions

### Single Category Query
```
User: "I need help with my billing statement"

Flow:
1. Router → {"route": "billing"}
2. Billing Agent → Processes query with get_invoice tool
3. Aggregator → Formats response
4. Supervisor → Validates and enhances
5. Output → Customer receives billing information
```

### Multi-Category Query
```
User: "I need help with my billing and my laptop is not working"

Flow:
1. Router → {"route": ["billing", "tech"]}
2. Parallel Execution:
   - Billing Agent → Handles billing inquiry
   - Tech Agent → Diagnoses laptop issue
3. Aggregator → Combines both responses into executive summary
4. Supervisor → Reviews and enhances
5. Output → Unified response addressing both concerns
```

## 🔑 Key Features

- ✅ **Multi-Agent Architecture**: Specialized agents for different domains
- ✅ **Parallel Processing**: Handles multiple concerns simultaneously
- ✅ **Tool Integration**: Function calling for actions (invoices, diagnostics, etc.)
- ✅ **Quality Assurance**: Supervisor layer ensures response quality
- ✅ **Session Management**: Persistent conversations with SQLite
- ✅ **Flexible Routing**: Supports single and multi-category routing
- ✅ **Centralized Configuration**: Single source for all settings
- ✅ **Error Handling**: Robust fallbacks and error recovery

## 🛠️ Configuration

All configuration is centralized in `src/config.py`:

```python
# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash-exp")

# Database Configuration
DB_URL = os.getenv("DB_URL", "sqlite+aiosqlite:///./db/adk_sessions.db")

# App Configuration
APP_NAME = "customer_support_app"
```

### Important Notes:
- **Model Selection**: Use models that support function calling (e.g., `gemini-2.0-flash-exp`, `gemini-1.5-pro`)
- **Lite Models**: Models like `gemini-2.5-flash-lite` do NOT support function calling/tools
- **Session Database**: Automatically created in `./db/adk_sessions.db`

## 🔍 Session Management

Each request creates isolated sessions:
- **routing**: Router agent classification
- **processing**: Parallel agent execution and aggregation
- **final_review**: Supervisor validation

This prevents state conflicts and ensures clean execution.

## 📝 Adding New Agents

1. Create agent in `src/agents/single/new_agent.py`:
```python
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from config import GOOGLE_MODEL

new_agent = Agent(
    name="new_agent",
    description="Handles new category",
    instruction="Your instructions here",
    output_key="new_response",
    model=Gemini(model=GOOGLE_MODEL),
    tools=[],  # Add your tools
)
```

2. Update router instruction to include new category
3. Add mapping in `orchestrator.py`:
```python
elif spl == "new_category":
    agent_list.append(new_agent)
```

## 🐛 Troubleshooting

### Error: "Tool use with function calling is unsupported"
- **Cause**: Using a model that doesn't support function calling
- **Solution**: Change `GOOGLE_MODEL` to `gemini-2.0-flash-exp` or `gemini-1.5-pro`

### Error: "Agent already has a parent"
- **Cause**: Trying to reuse agents in multiple ParallelAgent instances
- **Solution**: Create agents only once, don't recreate root_agent

### Error: "Missing key inputs argument"
- **Cause**: Google API key not set
- **Solution**: Set `GOOGLE_API_KEY` in `.env` file

### Warning: "App name mismatch"
- **Cause**: ADK internal warning (can be ignored)
- **Impact**: None - system works correctly

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue on GitHub.
