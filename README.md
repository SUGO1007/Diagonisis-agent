# Autonomous Incident Diagnosis & Resolution AI Tool

**Multi-Agent LangGraph System with Real Vector DB RAG & Schema-Aware Tool Selection**

A production-ready multi-agent AI system that autonomously diagnoses and resolves infrastructure incidents using LangGraph orchestration, ChromaDB semantic search, and Qwen LLM reasoning.

---

## Architecture

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         LangGraph StateGraph (13 Nodes)                     │
│                                                                            │
│  START → Monitor → Diagnose → [Gather Info] → Plan → Comply → Execute     │
│              │          │           │                      │                │
│              ▼          ▼           ▼                      ▼                │
│           MCP Tools  ChromaDB    RAG + LLM             MCP Tools           │
│                      55 chunks   Schema-Aware                              │
│                                  Tool Selection                            │
│                                       │                                    │
│              → Validate → Learn & Close → END                              │
└────────────────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology | Role |
|-----------|-----------|------|
| Orchestrator | **LangGraph** StateGraph | 13-node workflow with conditional routing |
| LLM | **Qwen3-30B-A3B** via vLLM | Agent reasoning, root cause analysis, tool selection |
| Vector DB | **ChromaDB** (persistent) | 55-chunk knowledge base with cosine similarity |
| Embeddings | **sentence-transformers** (all-MiniLM-L6-v2) | 384-dimensional vectors, ~15ms latency |
| MCP Server | Simulated stdio-based | 12 infrastructure tools |
| Data Pipeline | Custom Python | Metric collection → CMDB enrichment → Anomaly detection |

---

## Key Features

### 1. Schema-Aware Tool Selection (Latest)

Instead of hardcoded tool lists, TOOL_REGISTRY schemas are embedded into Vector DB:

```
Agent Goal: "investigate high CPU process on prod-web-07"
    ↓ RAG semantic search on tool_schema docs
Best Match: get_process_list (score: 0.78)
    ↓ Returns full parameter schema
Schema: { host: string (REQUIRED), ... }
    ↓ LLM generates arguments from context
Arguments: { "host": "prod-web-07" }
    ↓ Validated against schema
Execute: get_process_list(host="prod-web-07")
```

### 2. Real Vector DB RAG (ChromaDB)

55 indexed chunks across 7 categories:
- **Incident History** (7 chunks) — Past incidents for pattern matching
- **Runbooks** (5 chunks) — Operational procedures
- **Service Catalog** (6 chunks) — Service tiers, SLAs, owners
- **Infrastructure** (5 chunks) — Server specs and status
- **System Topology** (8 chunks) — Dependency graphs
- **Tool Knowledge** (12 chunks) — MCP API documentation
- **Tool Schemas** (12 chunks) — TOOL_REGISTRY with parameter definitions

### 3. LangGraph Workflow (13 Nodes)

```
monitor_node        → Enriches raw alert with CMDB context
diagnose_node       → RAG-powered root cause analysis (confidence scoring)
gather_info_node    → ReAct loop with schema-aware tool selection
plan_remediation    → LLM creates remediation plan with rollback steps
check_compliance    → Service-tier policy enforcement
execute_fix_node    → Pre/post-flight checks + MCP tool execution
validate_node       → Verifies fix effectiveness
learn_and_close     → Pattern extraction + Vector DB update
```

Conditional routing based on:
- Confidence thresholds (< 85% → gather more info)
- Service tier compliance (critical → always needs approval)
- Validation results (failed → rollback)

### 4. 5 Specialized Agents

| Agent | Role | Key Capability |
|-------|------|---------------|
| Monitor | Alert enrichment | MCP calls for server metadata, service info |
| Diagnosis | Root cause analysis | 4 parallel RAG searches + LLM reasoning |
| Gathering | Evidence collection | ReAct loop with RAG tool schema selection |
| Remediation | Safe execution | Pre/post checks, compliance, rollback |
| Learner | Pattern extraction | Stores new patterns back in Vector DB |

### 5. Simulated MCP Server (12 Tools)

| Tool | Category | Parameters |
|------|----------|-----------|
| `query_metrics` | Telemetry | host (R), metric (R), time_range |
| `get_application_logs` | Telemetry | host (R), level, last_n, service |
| `get_process_list` | Execution | host (R) |
| `kill_process` | Execution | host (R), pid (R), signal |
| `execute_command` | Execution | host (R), command (R) |
| `get_server_metadata` | CMDB | hostname (R) |
| `get_service_info` | CMDB | service_name (R) |
| `get_recent_changes` | CMDB | target (R), hours |
| `get_dependencies` | CMDB | service_name (R) |
| `check_service_health` | Health | service_name (R) |
| `create_incident` | Management | title (R), severity (R), description |
| `send_notification` | Management | channel (R), message (R), severity |

---

## Project Structure

```
AUTONOMOUS_INCIDENT_DIAGNOSIS_RESOLUTION_AI_TOOL/
├── main.py                          # Entry point - full LangGraph workflow
├── test_rag.py                      # RAG search quality verification
├── .env                             # Config (LLM_BASE_URL, LLM_MODEL, etc.)
│
├── orchestrator/                    # LangGraph Workflow Engine
│   ├── __init__.py                  # Exports build_incident_response_graph
│   ├── state.py                     # IncidentState TypedDict (shared state)
│   ├── graph.py                     # StateGraph with 13 nodes + conditional edges
│   └── nodes.py                     # All node functions + helpers (~1200 lines)
│       ├── monitor_node()           # Agent 1: Alert enrichment
│       ├── diagnose_node()          # Agent 2: RAG-powered diagnosis
│       ├── gather_info_node()       # Agent 3: Schema-aware ReAct loop
│       ├── plan_remediation_node()  # Agent 4: LLM remediation planning
│       ├── check_compliance_node()  # Service-tier policy check
│       ├── execute_fix_node()       # Pre/post-flight + MCP execution
│       ├── validate_node()          # Fix verification
│       ├── learn_and_close_node()   # Agent 5: Pattern learning
│       └── _select_and_execute_tool_with_schema()  # RAG tool selection
│
├── rag/                             # Vector DB & Knowledge Base
│   ├── __init__.py
│   ├── vector_store.py              # RAGVectorStore (ChromaDB + embeddings)
│   │   ├── load_and_index()         # Loads 6 txt files + 12 tool schemas
│   │   ├── search()                 # Cosine similarity with metadata filters
│   │   ├── search_tool_schemas()    # Find tools by natural language
│   │   └── get_tool_schema_and_args()  # Schema + auto-suggested arguments
│   ├── tool_schema_loader.py        # TOOL_REGISTRY → Vector DB documents
│   │   ├── tool_registry_to_documents()  # Convert schemas to embeddings
│   │   ├── validate_tool_arguments()     # Validate args against schema
│   │   └── get_tool_schema()             # Get schema for specific tool
│   ├── incident_history.txt         # 7 past incidents
│   ├── runbooks.txt                 # 5 operational runbooks
│   ├── service_catalog.txt          # 6 services with SLA tiers
│   ├── infrastructure_inventory.txt # 5 server specifications
│   ├── system_topology.txt          # Dependency graphs
│   └── tool_knowledge.txt           # 12 MCP tool documentation
│
├── mcp/                             # Model Context Protocol (Simulated)
│   ├── __init__.py
│   ├── incident_mcp_server.py       # 12 tools + TOOL_REGISTRY dict (~600 lines)
│   ├── schemas.py                   # ToolDefinition, ToolCall, ToolResult dataclasses
│   ├── client.py                    # MCP client connector
│   └── server.py                    # MCP server base
│
├── data_ingestion/                  # Metric Collection & Anomaly Detection
│   ├── __init__.py                  # Exports Pipeline, SERVERS, SERVICES
│   ├── pipeline.py                  # DataIngestionPipeline class
│   ├── mock_data.py                 # 5 servers, 5 services, thresholds
│   └── models.py                    # MetricEvent, Anomaly dataclasses
│
├── agents/                          # Agent class definitions (legacy/reference)
├── core/                            # Config, constants, exceptions, logging
├── prompts/                         # Agent prompt templates
├── docs/                            # Architecture and migration docs
└── tests/                           # Test suite
```

---

## How It Works

### End-to-End Workflow

```
1. DATA INGESTION
   20 raw metrics → CMDB enrichment → 6 anomalies → Top critical alert

2. MONITOR AGENT
   Alert: HighCPU 98.5% on prod-web-07 (47 minutes)
   Enrichment: get_server_metadata + get_service_info + get_recent_changes

3. DIAGNOSIS AGENT (Vector DB RAG)
   4 parallel searches: incidents(5) + runbooks(3) + services(2) + tools(3)
   Root Cause: ETL batch deadlock, PID 5510, connection pool exhaustion
   Confidence: 72% → Needs more info

4. GATHERING AGENT (Schema-Aware ReAct Loop)
   Iter 1: RAG → get_process_list(host="prod-web-07") → Confidence 80%
   Iter 2: RAG → query_metrics(host="prod-web-07", metric="memory_percent") → Confidence 88%

5. REMEDIATION AGENT
   Plan: kill_process(host="prod-web-07", pid=5510)
   Compliance: batch tier + low risk = auto-approved
   Pre-checks: 3 passed → Execute → Post-checks: 4 passed

6. VALIDATION
   Service health confirmed → RESOLVED

7. LEARNER AGENT
   Pattern: "High CPU + ETL + deployment → kill stuck process"
   Stored in Vector DB for future RAG
```

### Performance

| Metric | Value |
|--------|-------|
| Total workflow time | ~15-18 seconds |
| RAG query latency | ~15ms per search |
| Similarity scores | 0.60 - 0.86 |
| Confidence progression | 72% → 88% (2 iterations) |
| Vector DB chunks | 55 (43 knowledge + 12 tool schemas) |

---

## Quick Start

```bash
# 1. Install core dependencies
pip install langgraph langchain-core openai python-dotenv requests httpx pydantic

# 2. Install Vector DB + embeddings
pip install chromadb sentence-transformers
pip install torch --index-url https://download.pytorch.org/whl/cpu

# 3. (Optional) Start Qwen LLM — system works without it using fallbacks
vllm serve Qwen/Qwen3-30B-A3B --served-model-name Qwen3-30B-A3B --api-key abc-123 --port 8000

# 4. Run
python main.py
```

### Configuration (.env)

```env
LLM_BASE_URL=http://localhost:8000/v1
LLM_MODEL=Qwen3-30B-A3B
LLM_API_KEY=abc-123
ENVIRONMENT=development
```

---

## Data Flow: Schema-Aware Tool Selection

```python
# 1. Tool schemas from TOOL_REGISTRY are embedded into ChromaDB at startup
#    Each tool becomes a searchable document with:
#    - Natural language description
#    - Full parameter schema (names, types, required/optional)
#    - Usage examples

# 2. During gathering, the agent searches for tools by goal
result = store.search_tool_schemas("investigate CPU process list", top_k=1)
# Returns: get_process_list with schema {host: string (REQUIRED)}

# 3. LLM fills in arguments from context
arguments = llm_generate_args(schema, context={"host": "prod-web-07"})
# Returns: {"host": "prod-web-07"}

# 4. Arguments validated before execution
is_valid, error = validate_tool_arguments("get_process_list", arguments)

# 5. Tool executed via MCP server
result = execute_mcp_tool("get_process_list", {"host": "prod-web-07"})
```

---

## References

- [LangGraph](https://langchain-ai.github.io/langgraph/) — State machine orchestration
- [ChromaDB](https://www.trychroma.com/) — Vector database
- [sentence-transformers](https://www.sbert.net/) — Embedding models
- [vLLM](https://vllm.readthedocs.io/) — LLM serving
- [Model Context Protocol](https://modelcontextprotocol.io/) — Tool integration standard
- [ReAct Pattern](https://arxiv.org/abs/2210.03629) — Reason + Act in LLMs
