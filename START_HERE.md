# ⚠️ IMPORTANT: Before Running main.py

## The vLLM Server MUST Be Running First! 🚨

This project uses **vLLM** to serve the **Qwen3-30B-A3B** model for all AI agents. Without the vLLM server running, you will get connection errors and only receive fallback responses.

---

## ✅ Quick Setup (2 Steps)

### Step 1: Start vLLM Server

**Open a terminal** and run:

```powershell
# Windows PowerShell
.\start_vllm.ps1

# Windows CMD
start_vllm.bat

# Linux/Mac
./start_vllm.sh
```

**Wait for this message**: `Application startup complete.`

**Keep this terminal open!** The server must stay running.

---

### Step 2: Run the AI Tool

**Open a NEW terminal** and run:

```bash
python main.py
```

**Look for**: `Connection: ✓ OK (models available: 1)`

---

## 📚 Documentation

- **Quick Start**: [QUICKSTART_VLLM.md](QUICKSTART_VLLM.md)
- **Full Guide**: [VLLM_SETUP_GUIDE.md](VLLM_SETUP_GUIDE.md)
- **Project README**: [README.md](README.md)

---

## 🆘 Getting Connection Errors?

If you see `Connection: ✗ FAILED`, the vLLM server is not running.

**Solution**: Go back to Step 1 and start the vLLM server.

---

## 📦 First-Time Setup

If you haven't installed dependencies yet:

```bash
pip install -r requirements.txt
```

This installs:
- vLLM (for model serving)
- OpenAI (for API client)
- LangGraph (for orchestration)
- ChromaDB (for vector storage)
- And other dependencies

---

**🎯 Remember**: vLLM server first, then main.py!
