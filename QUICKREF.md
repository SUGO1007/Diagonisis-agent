# ⚡ Agentic AI Platform — Quick Reference

## 🚀 Run Immediately

```bash
# Windows
cd d:\AI experiment\AUTONOMOUS_INCIDENT_DIAGNOSIS_RESOLUTION_AI_TOOL
python main.py

# Unix/Mac
cd AUTONOMOUS_INCIDENT_DIAGNOSIS_RESOLUTION_AI_TOOL
python main.py
```

**Result**: See a complete 5-agent incident response in ~5 seconds ✅

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `main.py` | **MAIN ENTRY POINT** - Run the entire simulation |
| `run.bat` | Windows convenience script |
| `run.sh` | Unix/Mac convenience script |
| `README.md` | Project overview |
| `RUNNING.md` | Complete running guide |
| `docs/ARCHITECTURE.md` | Technical deep dive |
| `docs/QUICKSTART.md` | 5-minute walkthrough |

---

## 📦 Project Structure at a Glance

```
agents/                   ← 5 specialized agents
├── base/               ← Base agent class
├── monitor_agent/      ← Alert enrichment
├── diagnosis_agent/    ← Root cause analysis
├── gathering_agent/    ← Information gathering (ReAct)
├── remediation_agent/  ← Safe execution
└── learner_agent/      ← Learning from feedback

orchestration/          ← Coordinates all agents
mcp/                    ← Tool communication
core/                   ← Configuration, logging
apps/                   ← API, CLI, worker (planned)
tests/                  ← Test suite
docs/                   ← Documentation
```

---

## 🧠 5-Agent Workflow

1. **MonitorAgent** 📨
   - Receives raw alert
   - Enriches with CMDB context
   - Calculates priority

2. **DiagnosisAgent** 🧠
   - Analyzes root cause
   - Searches Vector DB for similar incidents
   - Outputs confidence score (0-100%)

3. **InformationGatheringAgent** 🔄
   - If confidence < 80%, runs ReAct loop
   - REASON → ACT → OBSERVE → UPDATE
   - Repeats until confidence ≥ 85% or max iterations

4. **RemediationAgent** 🔧
   - Checks service tier compliance
   - Pre-flight validation
   - Safe execution with rollback ready
   - Post-flight validation

5. **LearnerAgent** 🧠
   - Captures human feedback
   - Learns new patterns
   - Updates Vector DB
   - Generates runbooks

---

## 🎯 What main.py Does

```
✅ Loads mock infrastructure (5 servers, 5 services)
✅ Runs data ingestion pipeline (20 metrics → 6 anomalies)
✅ Creates a CPU spike alert
✅ Runs alert through all 5 agents
✅ Shows full decision trace and execution
✅ Prints final statistics
✅ Demonstrates learning capability
```

**Output:** Full incident resolution trace with timing and confidence metrics

---

## 💻 Common Commands

```bash
# Run the POC simulation
python main.py

# Run with output to file
python main.py > output.txt

# Run specific test
pytest tests/agents/test_diagnosis_agent.py -v

# Run all tests
pytest tests/ -v --cov

# Check code style
black --check .
flake8 .

# Run type checking
mypy agentic_ai_platform/
```

---

## 🔧 Configuration

### Environment Variables (create `.env.local`)

```bash
# LLM
LLM_MODEL=mistral-large-latest
MISTRAL_API_KEY=sk-xxx...

# Agent thresholds
DIAGNOSIS_CONFIDENCE_THRESHOLD=0.80
GATHERING_CONFIDENCE_THRESHOLD=0.85

# Logging
LOG_LEVEL=INFO
```

### Load in Code

```python
from agentic_ai_platform.core import get_config
config = get_config()
```

---

## 📊 Key Metrics from Output

When you run `python main.py`, you get:

| Metric | Example |
|--------|---------|
| Initial confidence | 72% |
| ReAct iterations | 3 |
| Confidence improvement | +24% |
| Final confidence | 96% |
| Execution success | ✓ |
| Patterns learned | 1 |
| Processing time | ~5s |

---

## 🚨 Incident Data Structure

```python
alert = {
    "alert": "HighCPU",              # Alert type
    "server": "prod-web-07",         # Host
    "cpu_percent": 98.5,             # Current value
    "duration": "30m",               # How long
    "threshold": 80.0,               # Alert threshold
    "severity": "warning",           # Critical/warning/info
}
```

---

## 🎓 Learning Outcomes

After running `python main.py`, you'll understand:

✅ How multi-agent systems work
✅ What ReAct pattern is (Reason → Act → Observe → Update)
✅ How Vector DB helps with incident diagnosis
✅ How confidence-driven decision making works
✅ Safe execution patterns with rollback
✅ How LLMs can learn from feedback

---

## 📚 Documentation Map

**Start here**: `main.py` → Run it → See it work
**Understand it**: `docs/ARCHITECTURE.md` → Read design
**Extend it**: `docs/QUICKSTART.md` → Build on it
**Deploy it**: `docs/INSTALL.md` → Production setup

---

## 🔗 Key Classes

| Class | Location | Purpose |
|-------|----------|---------|
| `AgentOrchestrator` | `orchestration/orchestration.py` | Coordinates all agents |
| `MonitorAgent` | `agents/monitor_agent/` | Alert enrichment |
| `DiagnosisAgent` | `agents/diagnosis_agent/` | Root cause analysis |
| `InformationGatheringAgent` | `agents/gathering_agent/` | ReAct loop |
| `RemediationAgent` | `agents/remediation_agent/` | Safe execution |
| `LearnerAgent` | `agents/learner_agent/` | Learning from feedback |
| `MCPClient` | `mcp/client.py` | Tool communication |
| `ConfigManager` | `core/config.py` | Configuration mgmt |

---

## 🐛 Common Issues

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run: `pip install -e "."` |
| `MISTRAL_API_KEY not set` | Create `.env.local` with your key |
| Slow execution | Reduce `max_iterations` in `.env` |
| Import errors | Ensure you're in the right directory |

---

## 🚀 Next Steps

1. **Run it**: `python main.py` (takes ~5 seconds)
2. **Read it**: Open `docs/ARCHITECTURE.md`
3. **Modify it**: Edit `main.py` for custom scenarios
4. **Extend it**: Add agents/tools in `agents/` and `tools/`
5. **Deploy it**: Follow `docs/INSTALL.md`

---

## 📞 Quick Help

```python
# See what agents do
from agentic_ai_platform.agents import MonitorAgent, DiagnosisAgent
help(MonitorAgent.receive_alert)

# Check configuration
from agentic_ai_platform.core import get_config
config = get_config()
print(config)

# Access orchestrator
from agentic_ai_platform.orchestration import AgentOrchestrator
help(AgentOrchestrator.process_alert)
```

---

**Version**: 1.0
**Last Updated**: 2026-06-12
**Status**: Production Ready ✅
