# 🚀 Running the Agentic AI Platform

This guide explains how to run the system in different ways.

---

## 1️⃣ Quick Start: Run the POC Simulation (5 minutes)

The fastest way to see the entire 5-agent system in action.

### Windows

```bash
# Navigate to the project directory
cd d:\AI experiment\AUTONOMOUS_INCIDENT_DIAGNOSIS_RESOLUTION_AI_TOOL

# Option A: Direct Python
python main.py

# Option B: Using the convenience script
run.bat
```

### Unix/Mac/Linux

```bash
cd AUTONOMOUS_INCIDENT_DIAGNOSIS_RESOLUTION_AI_TOOL

# Option A: Direct Python
python main.py

# Option B: Using the convenience script
bash run.sh
```

### What You'll See

The simulation demonstrates a complete incident response workflow:

```
1. ✅ Data Ingestion Pipeline
   • Collect 20 metric events
   • Enrich with CMDB context
   • Detect 6 anomalies

2. 📨 MonitorAgent
   • Receives raw CPU alert
   • Enriches with service context

3. 🧠 DiagnosisAgent
   • Analyzes root cause
   • Initial confidence: 72%
   • Vector DB finds 3 similar incidents

4. 🔄 InformationGatheringAgent
   • Runs ReAct loop (3 iterations)
   • Improves confidence: 72% → 96%

5. 🔧 RemediationAgent
   • Performs compliance check
   • Pre-flight validation
   • Executes remediation: kill -9 8421
   • Post-flight validation
   • Success! ✅

6. 🧠 LearnerAgent
   • Captures human feedback
   • Learns new pattern
   • Updates Vector DB
   • Generates runbook

📊 Final Statistics
   • 1 alert processed
   • 96% final confidence
   • 3 ReAct iterations
   • 1 pattern learned
```

**Runtime**: ~5 seconds
**Output**: Full incident resolution trace

---

## 2️⃣ Production Usage: Import as Library

Use the agents in your own code:

```python
from agentic_ai_platform.orchestration import AgentOrchestrator
from agentic_ai_platform.mcp import MCPClient
from agentic_ai_platform.core import get_config

# Initialize
config = get_config()
mcp_client = MCPClient(config)
orchestrator = AgentOrchestrator(mcp_client, config)

# Process alert
raw_alert = {
    "alert": "HighCPU",
    "server": "prod-web-07",
    "cpu_percent": 98.5,
    "duration": "30m",
}

result = orchestrator.process_alert(raw_alert)
print(f"Final confidence: {result['final_confidence']:.0%}")
print(f"Action taken: {result['action']}")
```

---

## 3️⃣ REST API Server (Planned)

```bash
python -m agentic_ai_platform.apps.api
```

Will start a FastAPI server on `http://localhost:8000`

POST `/incidents` - Process an incident
GET `/incidents/{id}` - Get incident status
GET `/statistics` - View system statistics

---

## 4️⃣ CLI Interface (Planned)

```bash
python -m agentic_ai_platform.apps.cli process --alert "cpu_high" --server "prod-01"
```

---

## 5️⃣ Background Worker (Planned)

```bash
python -m agentic_ai_platform.apps.worker
```

Continuously processes incidents from a message queue.

---

## 📋 Configuration

### Environment Variables

Create `.env.local` with:

```bash
# LLM Configuration
LLM_PROVIDER=mistralai          # or openai, anthropic
LLM_MODEL=mistral-large-latest
LLM_TEMPERATURE=0.1
MISTRAL_API_KEY=sk-xxx...

# Vector DB Configuration
VECTOR_DB_PROVIDER=pinecone     # or weaviate, chromadb
VECTOR_DB_INDEX=incidents
PINECONE_API_KEY=xxx...
PINECONE_ENVIRONMENT=production

# MCP Configuration
MCP_TELEMETRY_SERVER=http://localhost:9001
MCP_SSH_SERVER=http://localhost:9002
MCP_CMDB_SERVER=http://localhost:9003
MCP_ALERTING_SERVER=http://localhost:9004
MCP_RUNBOOK_SERVER=http://localhost:9005

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/agentic-ai.log

# Agent Thresholds
DIAGNOSIS_CONFIDENCE_THRESHOLD=0.80
GATHERING_CONFIDENCE_THRESHOLD=0.85
GATHERING_MAX_ITERATIONS=10

# Timeouts (seconds)
MCP_TOOL_TIMEOUT=30
REMEDIATION_EXECUTION_TIMEOUT=60
GATHERING_LOOP_TIMEOUT=300
```

### Load Configuration

```python
from agentic_ai_platform.core import ConfigManager

config = ConfigManager.load_from_env()
```

---

## 🧪 Testing

### Run Unit Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/agents/test_diagnosis_agent.py -v

# With coverage
pytest tests/ --cov tests/
```

### Run Integration Tests

```bash
pytest tests/workflows/ -v
```

### Run MCP Tests

```bash
pytest tests/mcp/ -v
```

---

## 📊 Understanding the Output

When you run `python main.py`, you'll see:

### 1. Data Ingestion Pipeline

```
📡 Running Data Ingestion Pipeline...
────────────────────────────────────────────────────────────
  [COLLECT]  20 raw metric events ingested
  [ENRICH]   16/20 events enriched with CMDB data
  [DETECT]   6 anomalies detected
────────────────────────────────────────────────────────────
🚨 ANOMALIES REQUIRING INVESTIGATION:
   [CRITICAL] prod-web-07: cpu_percent=98.5% | tier=critical
   [WARNING ] prod-db-01: memory_percent=88.5% | tier=unknown
   ...
```

**What it means:**
- System collected metrics from 5 servers
- Enriched them with CMDB data (service owner, tier, dependencies)
- Detected 6 anomalies (3 critical, 3 warning)

### 2. MonitorAgent Output

```
📨 MONITOR AGENT — Alert Ingestion & Enrichment
Raw Alert Received:
   Server: prod-web-07
   Metric: CPU 98.5% (threshold: 80.0%)
   Duration: 30m
   Severity: warning
```

**What it means:**
- Agent received a raw CPU spike alert
- Alert shows CPU at 98.5% for 30 minutes
- Severity classified as "warning"

### 3. DiagnosisAgent Output

```
🧠 DIAGNOSIS AGENT — Root Cause Analysis (Vector DB RAG)
Root Cause: ETL batch job deadlock in data transformation
Confidence: 72%
Vector DB Matches: 3 similar incidents
Recommended Actions: kill_process, restart_service
→ Requires more information gathering
```

**What it means:**
- Agent analyzed 3 similar incidents from Vector DB
- Diagnosis is ETL deadlock with 72% confidence
- 72% < 80% threshold, so more info needed

### 4. InformationGatheringAgent Output

```
🔄 INFORMATION GATHERING AGENT — ReAct Loop

   Iteration 1:
      REASON: Determine which tool to call
      ACT: Execute ps -aux on prod-batch-01
      OBSERVE: Process 5510 using 95% CPU for 45+ minutes
      UPDATE: Confidence improved to 80%

   Iteration 2:
      REASON: Determine which tool to call
      ACT: Execute ps -aux on prod-batch-01
      OBSERVE: Process 5510 using 95% CPU for 45+ minutes
      UPDATE: Confidence improved to 88%

   Iteration 3:
      REASON: Determine which tool to call
      ACT: Execute ps -aux on prod-batch-01
      OBSERVE: Process 5510 using 95% CPU for 45+ minutes
      UPDATE: Confidence improved to 96%
```

**What it means:**
- Agent ran 3 ReAct iterations
- Each iteration: picked a tool → executed → processed result → recalculated confidence
- Confidence improved from 72% → 96% (above 85% threshold)

### 5. RemediationAgent Output

```
🔧 REMEDIATION AGENT — Compliance & Execution

✅ PRE-FLIGHT CHECKS:
   ✓ Backup created
   ✓ Rollback plan available

⚙️  EXECUTING: kill -9 8421
   Process terminated successfully

✅ POST-FLIGHT CHECKS:
   ✓ CPU returned to 12% (from 98%)
   ✓ No related services affected

✅ ROLLBACK READY: Available for 24 hours
```

**What it means:**
- Agent validated safety before execution
- Executed the action (kill process 8421)
- CPU dropped from 98% to 12%
- Ready to rollback if needed

### 6. LearnerAgent Output

```
🧠 LEARNER AGENT — Capturing Feedback & Learning

📋 Feedback Captured:
   Incident: HighCPU
   AI Decision: kill_process (confidence: 96%)
   Human Decision: kill_process
   Expert Notes: This pattern has occurred 3 times this month...

📖 Generated Runbook from Pattern:
   Trigger: HighCPU + OOMKilled
   Resolution: kill_process
   Confidence: 89%

🔄 Updating Vector DB with new pattern...
```

**What it means:**
- Agent captured that human approved the AI decision
- Learned a new pattern: HighCPU + OOMKilled → kill_process
- Generated a runbook for future incidents
- Updated Vector DB so next similar incident will diagnose faster

### 7. Statistics

```
📊 MULTI-AGENT PERFORMANCE STATISTICS

📡 MonitorAgent:
   Alerts received: 1
   Alerts enriched: 1

🧠 DiagnosisAgent:
   Diagnoses performed: 1
   Vector DB queries: 1
   Final diagnosis confidence: 72%

🔄 InformationGatheringAgent:
   ReAct iterations: 3
   Initial confidence: 72%
   Final confidence: 96%
   Confidence improvement: +24%

🔧 RemediationAgent:
   Executions: 1
   Success Rate: 0.98

🧠 LearnerAgent:
   Feedback Captured: 1
   Patterns Learned: 1
   Approval Rate: 0.92
   Runbooks Generated: 1
```

**What it means:**
- Complete system metrics for this incident response
- Shows how effective each agent was
- Tracks improvement over time

---

## 🐛 Troubleshooting

### Error: ModuleNotFoundError: No module named 'autonomous_incident_ai'

**Solution:**
```bash
# Install the package in development mode
cd AUTONOMOUS_INCIDENT_DIAGNOSIS_RESOLUTION_AI_TOOL
pip install -e "."
```

### Error: MISTRAL_API_KEY not set

**Solution:**
```bash
# Create .env.local
cp .env .env.local

# Edit .env.local and add your key
# Then run with environment variable:
export MISTRAL_API_KEY=sk-xxx...
python main.py
```

### Slow execution

**Possible causes:**
- Network latency to MCP servers
- Large Vector DB queries
- Many ReAct iterations

**Solutions:**
- Use smaller Vector DB (POC uses simulated data)
- Reduce max_iterations in .env
- Run on faster network

---

## 📚 Next Steps

1. **Read the docs**
   - [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Deep technical dive
   - [QUICKSTART.md](docs/QUICKSTART.md) - 5-minute walkthrough

2. **Customize the system**
   - Create custom agents in `agents/`
   - Add custom tools in `tools/`
   - Implement real MCP servers

3. **Deploy to production**
   - Connect to real monitoring systems
   - Set up actual Vector DB (Pinecone/Weaviate)
   - Configure authentication and logging
   - Deploy as Docker containers

---

## 💡 Examples

### Example 1: Process CPU Spike

```python
from main import main

# main.py handles this scenario by default
python main.py
```

### Example 2: Custom Incident

```python
# Create custom_incident.py
from agentic_ai_platform.orchestration import AgentOrchestrator

orchestrator = AgentOrchestrator(mcp_client, config)

# Your custom incident
incident = {
    "alert": "MemoryLeak",
    "server": "prod-cache-02",
    "memory_percent": 92.0,
    "duration": "2h",
}

result = orchestrator.process_alert(incident)
print(result)
```

### Example 3: Multiple Incidents (Batch)

```python
from agentic_ai_platform.orchestration import AgentOrchestrator

incidents = [
    {"alert": "HighCPU", "server": "prod-web-07", "cpu_percent": 98.5},
    {"alert": "HighMemory", "server": "prod-cache-02", "memory_percent": 92.0},
    {"alert": "DiskFull", "server": "prod-db-01", "disk_percent": 95.0},
]

for incident in incidents:
    result = orchestrator.process_alert(incident)
    print(f"✅ {incident['alert']}: {result['final_confidence']:.0%}")
```

---

## 🎯 Performance Expectations

| Metric | Value |
|--------|-------|
| Simulation runtime | 5-10 seconds |
| Diagnosis confidence | 72% initial, 96% after gathering |
| ReAct iterations | 3 (configurable 1-10) |
| Pre-flight checks | ~100ms |
| Post-flight checks | ~100ms |
| Rollback ready | Instant |
| Pattern learning | 1-2ms |

---

## 📞 Support

- **Questions?** Check [README.md](README.md)
- **Technical details?** See [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Migration from notebook?** See [MIGRATION.md](docs/MIGRATION.md)
- **File structure?** See [INDEX.md](docs/INDEX.md)

---

**Happy incident solving! 🚀**
