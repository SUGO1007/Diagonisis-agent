# 🚀 Quick Start: vLLM + Qwen Setup

## Two-Step Setup

### 1️⃣ Start vLLM Server (First Terminal)

```powershell
# Windows PowerShell (Recommended)
.\start_vllm.ps1

# Windows CMD
start_vllm.bat

# Linux/Mac
./start_vllm.sh
```

**Wait for**: `Application startup complete.` ✅

### 2️⃣ Run the AI Tool (Second Terminal)

```bash
python main.py
```

**Look for**: `Connection: ✓ OK` ✅

---

## That's It! 🎉

Your AI agents will now use **real Qwen model responses** instead of fallbacks.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Connection: ✗ FAILED` | vLLM server not running → Go to Step 1 |
| `vllm: command not found` | Install vLLM: `pip install vllm` |
| `CUDA/HIP out of memory` | GPU too small for Qwen3-30B-A3B |

---

## Full Documentation

See [VLLM_SETUP_GUIDE.md](VLLM_SETUP_GUIDE.md) for detailed instructions.

---

## Configuration (`.env` file)

Already configured! No changes needed for default setup:
- Server: `http://localhost:8000/v1`
- Model: `Qwen3-30B-A3B`
- API Key: `abc-123`
