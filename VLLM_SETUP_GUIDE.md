# 🚀 vLLM + Qwen Setup Guide

This guide will help you set up and run the Autonomous Incident Diagnosis & Resolution AI Tool with vLLM and the Qwen3-30B-A3B model.

## 📋 Prerequisites

### System Requirements
- **GPU**: AMD GPU with ROCm support OR NVIDIA GPU with CUDA
- **Memory**: At least 32GB RAM
- **GPU Memory**: At least 24GB VRAM for Qwen3-30B-A3B
- **Python**: 3.9 or higher
- **OS**: Windows, Linux, or macOS

### Software Requirements
1. **Python Packages**:
   ```bash
   pip install vllm openai langgraph python-dotenv chromadb sentence-transformers
   ```

2. **For AMD GPUs**:
   - ROCm 5.7+ installed
   - HIP-compatible PyTorch

3. **For NVIDIA GPUs**:
   - CUDA 11.8+ or 12.1+
   - CUDA-compatible PyTorch

## 🔧 Step-by-Step Setup

### Step 1: Install Dependencies

```bash
# Navigate to project directory
cd AUTONOMOUS_INCIDENT_DIAGNOSIS_RESOLUTION_AI_TOOL

# Install Python packages
pip install -r requirements.txt

# Or install individually:
pip install vllm openai langgraph python-dotenv chromadb sentence-transformers
```

### Step 2: Configure Environment Variables

The `.env` file is already configured with default settings:
- **LLM_BASE_URL**: `http://localhost:8000/v1` (vLLM server endpoint)
- **LLM_MODEL**: `Qwen3-30B-A3B` (model name)
- **LLM_API_KEY**: `abc-123` (authentication key)

**No changes needed unless you want to customize the port or API key.**

### Step 3: Start vLLM Server

⚠️ **IMPORTANT**: You must start the vLLM server BEFORE running main.py

#### Option A: Use the Provided Scripts

**Windows PowerShell** (Recommended for Windows):
```powershell
.\start_vllm.ps1
```

**Windows Command Prompt**:
```cmd
start_vllm.bat
```

**Linux/Mac**:
```bash
chmod +x start_vllm.sh
./start_vllm.sh
```

#### Option B: Manual Start

```bash
# For AMD GPUs:
VLLM_USE_TRITON_FLASH_ATTN=0 vllm serve Qwen/Qwen3-30B-A3B \
    --served-model-name Qwen3-30B-A3B \
    --api-key abc-123 \
    --port 8000 \
    --enable-auto-tool-choice \
    --tool-call-parser hermes \
    --trust-remote-code

# For NVIDIA GPUs (remove the VLLM_USE_TRITON_FLASH_ATTN line):
vllm serve Qwen/Qwen3-30B-A3B \
    --served-model-name Qwen3-30B-A3B \
    --api-key abc-123 \
    --port 8000 \
    --enable-auto-tool-choice \
    --tool-call-parser hermes \
    --trust-remote-code
```

#### What to Expect:
1. vLLM will download the Qwen3-30B-A3B model (if not already cached)
2. Model loading will take 2-5 minutes
3. You'll see: `INFO: Application startup complete.`
4. Server will be accessible at `http://localhost:8000`

**Keep this terminal open!** The server must remain running.

### Step 4: Verify vLLM Server

Open a new terminal and test the connection:

```bash
# Test if server is running
curl http://localhost:8000/v1/models -H "Authorization: Bearer abc-123"
```

You should see a response listing available models.

### Step 5: Run the AI Tool

In a **NEW terminal** (while vLLM server is still running):

```bash
# Navigate to project directory
cd AUTONOMOUS_INCIDENT_DIAGNOSIS_RESOLUTION_AI_TOOL

# Run the main script
python main.py
```

## 🎯 Expected Output

### Successful Connection
```
[CONFIG] LLM Configuration:
   Base URL: http://localhost:8000/v1
   Model: Qwen3-30B-A3B
   API Key: ***-123
   Connection: ✓ OK (models available: 1)
```

### Failed Connection
If you see:
```
   Connection: ✗ FAILED
   Error: Connection refused
```

**This means the vLLM server is not running!** Go back to Step 3.

## 🔍 Troubleshooting

### Problem: "Connection refused" or "Connection failed"
**Solution**: The vLLM server is not running. Start it using Step 3.

### Problem: "vllm: command not found"
**Solution**: vLLM is not installed.
```bash
pip install vllm
```

### Problem: "CUDA out of memory" or "HIP out of memory"
**Solution**: Your GPU doesn't have enough memory for Qwen3-30B-A3B.
- Try a smaller model like `Qwen/Qwen2-7B-Instruct`
- Or use quantized versions

### Problem: "ModuleNotFoundError: No module named 'openai'"
**Solution**: Install missing packages:
```bash
pip install openai langgraph python-dotenv chromadb sentence-transformers
```

### Problem: vLLM server starts but model doesn't load
**Solution**: 
1. Check your GPU memory: `nvidia-smi` (NVIDIA) or `rocm-smi` (AMD)
2. Ensure you have at least 24GB VRAM
3. Try using `--tensor-parallel-size 2` if you have multiple GPUs

### Problem: Model is loading very slowly
**Solution**: 
- First-time download of Qwen3-30B-A3B can take 15-30 minutes
- The model is ~30GB and will be cached in `~/.cache/huggingface/`
- Subsequent runs will be much faster

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     main.py (Python)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  LangGraph Multi-Agent Orchestrator                  │  │
│  │  - Monitor Agent                                     │  │
│  │  - Diagnosis Agent                                   │  │
│  │  - Gathering Agent                                   │  │
│  │  - Remediation Agent                                 │  │
│  │  - Learner Agent                                     │  │
│  └──────────────────────────────────────────────────────┘  │
│                            │                                │
│                            ↓                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  OpenAI Client (Python SDK)                          │  │
│  │  - Sends prompts to vLLM                             │  │
│  │  - Receives AI responses                             │  │
│  │  - Handles function calling                          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP (OpenAI API format)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  vLLM Server (Port 8000)                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Qwen3-30B-A3B Model                                 │  │
│  │  - Hosted on GPU                                     │  │
│  │  - OpenAI-compatible API                             │  │
│  │  - Function calling support                          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 🎨 Architecture Comparison with MCP-Airbnb-Agent

Both projects follow the same pattern:

1. **vLLM Server**: Serves Qwen model with OpenAI-compatible API
2. **Python Client**: Uses OpenAI SDK to communicate with vLLM
3. **Function Calling**: LLM can call tools/functions during reasoning
4. **Agent Framework**: 
   - MCP-Airbnb: Uses pydantic-ai
   - This project: Uses LangGraph

### Key Configuration (Both Projects)
```python
# MCP-Airbnb-Agent setup
provider = OpenAIProvider(
    base_url="http://localhost:8000/v1",
    api_key="abc-123"
)
model = OpenAIChatModel("Qwen3-30B-A3B", provider=provider)

# This project's setup (in nodes.py)
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="abc-123"
)
response = client.chat.completions.create(
    model="Qwen3-30B-A3B",
    messages=[...],
    tools=[...]
)
```

## ⚙️ Advanced Configuration

### Using a Different Port
Edit `.env`:
```bash
LLM_BASE_URL=http://localhost:9000/v1
```

Then start vLLM with `--port 9000`

### Using a Different Model
Edit `.env`:
```bash
LLM_MODEL=Qwen/Qwen2-7B-Instruct
```

Then start vLLM with that model name

### Adjusting LLM Parameters
Edit `.env`:
```bash
LLM_TEMPERATURE=0.2    # Higher = more creative
LLM_MAX_TOKENS=4000    # More tokens = longer responses
```

## 📚 Additional Resources

- **vLLM Documentation**: https://docs.vllm.ai/
- **Qwen Models**: https://huggingface.co/Qwen
- **LangGraph**: https://python.langchain.com/docs/langgraph
- **OpenAI API**: https://platform.openai.com/docs/api-reference

## 🆘 Getting Help

If you encounter issues not covered here:

1. Check the vLLM server logs for errors
2. Verify GPU availability: `nvidia-smi` or `rocm-smi`
3. Check Python package versions: `pip list | grep -E "vllm|openai|langgraph"`
4. Ensure port 8000 is not blocked by firewall

## ✅ Quick Start Checklist

- [ ] Install Python 3.9+
- [ ] Install GPU drivers (ROCm or CUDA)
- [ ] Install Python packages: `pip install vllm openai langgraph python-dotenv chromadb sentence-transformers`
- [ ] Review `.env` configuration
- [ ] Start vLLM server: `./start_vllm.ps1` (or .bat/.sh)
- [ ] Wait for "Application startup complete"
- [ ] Test connection: `curl http://localhost:8000/v1/models -H "Authorization: Bearer abc-123"`
- [ ] Run main.py: `python main.py`
- [ ] Verify you see "Connection: ✓ OK" in output

---

**🎉 You're all set! The AI agents will now use real Qwen model responses instead of fallbacks.**
