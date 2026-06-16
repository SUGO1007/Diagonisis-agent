# Deployment Guide

Deploy the Autonomous Incident Diagnosis & Resolution AI Tool on a Jupyter Notebook instance (JupyterHub, Google Colab, AWS SageMaker, or local Jupyter).

---

## Prerequisites

- Python 3.10+ (3.12 recommended)
- 4GB+ RAM (for embedding model)
- 2GB+ disk space (for PyTorch CPU + models)
- Internet access (for first-time model download from HuggingFace)

---

## Step 1: Clone or Upload the Project

### Option A: Git Clone

```bash
!git clone <your-repo-url> AUTONOMOUS_INCIDENT_DIAGNOSIS_RESOLUTION_AI_TOOL
%cd AUTONOMOUS_INCIDENT_DIAGNOSIS_RESOLUTION_AI_TOOL
```

### Option B: Upload ZIP

Upload your project zip to the Jupyter instance, then:

```bash
!unzip AUTONOMOUS_INCIDENT_DIAGNOSIS_RESOLUTION_AI_TOOL.zip
%cd AUTONOMOUS_INCIDENT_DIAGNOSIS_RESOLUTION_AI_TOOL
```

---

## Step 2: Install Dependencies

Run these cells in order. Each group handles a specific dependency layer.

### 2.1 Core Dependencies (Required)

```python
# LangGraph orchestration + LLM client
!pip install langgraph>=0.2.0 langchain-core>=0.3.0 openai>=1.30.0

# Configuration and HTTP
!pip install python-dotenv>=1.0.0 requests>=2.31.0 httpx>=0.25.0 pydantic>=2.0
```

### 2.2 Vector DB & Embeddings (Required)

```python
# ChromaDB vector database
!pip install chromadb>=0.4.0

# Sentence-transformers for embeddings
!pip install sentence-transformers>=2.2.0

# PyTorch CPU-only (saves ~1.5GB vs full CUDA version)
!pip install torch --index-url https://download.pytorch.org/whl/cpu

# Required transitive dependencies
!pip install transformers huggingface_hub jsonschema tokenizers
```

### 2.3 Verify Installation

```python
# Verify all imports work
import langgraph
print(f"langgraph: {langgraph.__version__}")

import chromadb
print(f"chromadb: {chromadb.__version__}")

from sentence_transformers import SentenceTransformer
print("sentence-transformers: OK")

import openai
print(f"openai: {openai.__version__}")

import torch
print(f"torch: {torch.__version__} (CPU)")

print("\n All dependencies installed successfully!")
```

---

## Step 3: Environment Configuration

```python
# Create .env file (or set environment variables)
import os

# LLM Configuration
# Option 1: Use local vLLM server (if available)
os.environ["LLM_BASE_URL"] = "http://localhost:8000/v1"
os.environ["LLM_MODEL"] = "Qwen3-30B-A3B"
os.environ["LLM_API_KEY"] = "abc-123"

# Option 2: System works WITHOUT LLM server (uses intelligent fallbacks)
# Just leave the defaults and skip the vLLM setup

# General config
os.environ["ENVIRONMENT"] = "development"
os.environ["DEBUG"] = "false"
```

---

## Step 4: Run the Full Workflow

### 4.1 Quick Test (RAG Only)

```python
%cd AUTONOMOUS_INCIDENT_DIAGNOSIS_RESOLUTION_AI_TOOL

# Test RAG search quality
!python test_rag.py
```

Expected output:
```
[RAG] Indexed 43 chunks into ChromaDB
Query: "high CPU ETL batch deadlock process stuck"
  [1] score=0.858 | infrastructure | prod-batch-01
  [2] score=0.817 | incident_history | INC-2024-0891
  [3] score=0.752 | runbook | RB-005: Data Transform ETL Deadlocks
```

### 4.2 Full End-to-End Workflow

```python
# Run complete incident response workflow
!python main.py
```

Expected output:
```
[AGENT-1] MONITOR AGENT - Alert: HighCPU 98.5% on prod-web-07
[AGENT-2] DIAGNOSIS AGENT - Root Cause: ETL deadlock (72% confidence)
[RAG] 55 chunks indexed (43 knowledge + 12 tool schemas)
[AGENT-3] GATHERING - Schema-aware tool selection (72% → 88%)
[AGENT-4] REMEDIATION - kill_process(prod-web-07, 5510) → SUCCESS
[SUMMARY] RESOLVED in ~15s | Confidence: 88%
```

### 4.3 Run Inside a Notebook Cell

```python
import sys
sys.path.insert(0, '.')

from orchestrator import build_incident_response_graph
from data_ingestion import DataIngestionPipeline, SERVERS, SERVICES

# Data ingestion
pipeline = DataIngestionPipeline(SERVERS, SERVICES)
results = pipeline.run_pipeline()
print(f"Anomalies detected: {results['anomalies']}")

# Get top critical alert
critical = [a for a in results['anomaly_details'] if a['severity'] == 'critical']
alert = {
    "alert_type": "HighCPU",
    "server": critical[0]['server'],
    "metric": critical[0]['metric'],
    "value": critical[0]['value'],
    "threshold": critical[0]['threshold'],
    "duration_minutes": 47,
    "service": "data-transform",
    "severity": "critical",
}

# Build and run LangGraph workflow
graph = build_incident_response_graph()
initial_state = {
    "raw_alert": alert,
    "enriched_alert": {},
    "diagnosis": {},
    "confidence": 0.0,
    "gathering_iterations": [],
    "gathered_info": {},
    "remediation_plan": {},
    "execution_result": {},
    "validation_result": {},
    "learning_result": {},
    "outcome": "",
    "messages": [],
}

final_state = graph.invoke(initial_state)
print(f"\nOutcome: {final_state['outcome']}")
print(f"Confidence: {final_state['confidence']:.0%}")
```

---

## Step 5: (Optional) LLM Server Setup

The system works without an LLM server using intelligent fallbacks. For full LLM-powered reasoning:

### Option A: vLLM (GPU required, 24GB+ VRAM)

```bash
# Install vLLM (requires CUDA GPU)
!pip install vllm

# Start server (in a separate terminal or background)
!vllm serve Qwen/Qwen3-30B-A3B \
    --served-model-name Qwen3-30B-A3B \
    --api-key abc-123 \
    --port 8000 &
```

### Option B: Use Any OpenAI-Compatible API

```python
# Works with any OpenAI-compatible endpoint
os.environ["LLM_BASE_URL"] = "https://api.openai.com/v1"  # or any compatible API
os.environ["LLM_MODEL"] = "gpt-4o-mini"
os.environ["LLM_API_KEY"] = "your-api-key"
```

### Option C: Ollama (Local, CPU-friendly)

```bash
# Install Ollama
!curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
!ollama pull qwen2.5:14b

# Start server (serves on localhost:11434)
!ollama serve &
```

```python
os.environ["LLM_BASE_URL"] = "http://localhost:11434/v1"
os.environ["LLM_MODEL"] = "qwen2.5:14b"
os.environ["LLM_API_KEY"] = "ollama"
```

---

## Complete pip Install (One-Liner)

For quick deployment, install everything in a single command:

```bash
pip install langgraph langchain-core openai python-dotenv requests httpx pydantic chromadb sentence-transformers transformers huggingface_hub jsonschema tokenizers && pip install torch --index-url https://download.pytorch.org/whl/cpu
```

---

## Package Versions (Tested)

| Package | Version | Purpose |
|---------|---------|---------|
| langgraph | 0.2.0+ | StateGraph orchestration |
| langchain-core | 0.3.0+ | LangGraph dependency |
| openai | 1.30.0+ | LLM client (OpenAI-compatible) |
| chromadb | 0.4.0+ (tested 1.5.9) | Vector database |
| sentence-transformers | 2.2.0+ (tested 5.5.1) | Embedding model |
| torch | 2.0+ (CPU) | Model inference backend |
| transformers | 4.0+ (tested 5.12.0) | HuggingFace model loading |
| huggingface_hub | 0.20+ | Model downloads |
| tokenizers | 0.15+ | Fast tokenization |
| jsonschema | 4.0+ | ChromaDB dependency |
| python-dotenv | 1.0.0+ | .env file loading |
| pydantic | 2.0+ | Data validation |
| requests | 2.31.0+ | HTTP client |
| httpx | 0.25.0+ | Async HTTP |

---

## Troubleshooting

### ChromaDB Import Error

```
ModuleNotFoundError: No module named 'jsonschema'
```

Fix: `!pip install jsonschema`

### sentence-transformers Import Error

```
ModuleNotFoundError: No module named 'transformers'
```

Fix: `!pip install transformers huggingface_hub tokenizers`

### Model Download Slow/Fails

```python
# Pre-download the embedding model
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model downloaded successfully")
```

### HuggingFace Symlink Warning (Windows)

```
UserWarning: huggingface_hub cache-system uses symlinks...
```

This is harmless — ignore it or set:
```python
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
```

### LLM Server Not Reachable

```
[WARNING] LLM server not reachable at http://localhost:8000/v1
```

This is expected if you don't have a vLLM server running. The system uses intelligent fallbacks and the full workflow still completes successfully.

### ChromaDB Metadata Error

```
ValueError: Expected metadata list value for key ... to be non-empty
```

Fix: Clear the ChromaDB cache and re-run:
```python
import shutil
shutil.rmtree('rag/.chromadb', ignore_errors=True)
!python main.py
```

---

## Jupyter Notebook Deployment (Full Cell Sequence)

Copy these cells into a new Jupyter notebook for one-click deployment:

```
Cell 1: !pip install langgraph langchain-core openai python-dotenv requests httpx pydantic
Cell 2: !pip install chromadb sentence-transformers transformers huggingface_hub jsonschema tokenizers
Cell 3: !pip install torch --index-url https://download.pytorch.org/whl/cpu
Cell 4: %cd AUTONOMOUS_INCIDENT_DIAGNOSIS_RESOLUTION_AI_TOOL
Cell 5: !python test_rag.py
Cell 6: !python main.py
```

---

## Resource Requirements

| Environment | RAM | Disk | GPU | Notes |
|-------------|-----|------|-----|-------|
| Local Jupyter | 4GB+ | 2GB | None | CPU-only PyTorch |
| Google Colab (Free) | 12GB | 15GB | Optional | Works on CPU runtime |
| AWS SageMaker (ml.t3.medium) | 4GB | 5GB | None | Sufficient for POC |
| JupyterHub (shared) | 4GB+ | 2GB | None | Check pip permissions |

**Note**: The embedding model (all-MiniLM-L6-v2) is only 80MB. The main disk usage is PyTorch (~700MB CPU-only).
