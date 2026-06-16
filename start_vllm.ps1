# ═══════════════════════════════════════════════════════════════
# vLLM Server Startup Script for Qwen3-30B-A3B Model (PowerShell)
# ═══════════════════════════════════════════════════════════════
#
# This script starts the vLLM server with Qwen3-30B-A3B model
# using OpenAI-compatible API for the Autonomous Incident AI Tool.
#
# Usage:
#   .\start_vllm.ps1
#   or right-click and "Run with PowerShell"
#
# Requirements:
#   - vLLM installed: pip install vllm
#   - AMD GPU with ROCm support (or NVIDIA GPU with CUDA)
#   - Sufficient GPU memory for Qwen3-30B-A3B model
#
# ═══════════════════════════════════════════════════════════════

Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Starting vLLM Server for Autonomous Incident AI Tool" -ForegroundColor Cyan
Write-Host "  Model: Qwen/Qwen3-30B-A3B" -ForegroundColor Cyan
Write-Host "  Port: 8000" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Check if vLLM is installed
$vllmInstalled = Get-Command vllm -ErrorAction SilentlyContinue
if (-not $vllmInstalled) {
    Write-Host "ERROR: vLLM is not installed!" -ForegroundColor Red
    Write-Host "Install it with: pip install vllm" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Set environment variables for AMD GPUs (comment out if using NVIDIA)
$env:VLLM_USE_TRITON_FLASH_ATTN = "0"

Write-Host "Starting vLLM server..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start vLLM server with Qwen3-30B-A3B
# Parameters explained:
#   --served-model-name: Name exposed via API (must match LLM_MODEL in .env)
#   --api-key: Authentication key (must match LLM_API_KEY in .env)
#   --port: Server port (default 8000)
#   --enable-auto-tool-choice: Enable automatic tool selection
#   --tool-call-parser: Parser for function calling (hermes format)
#   --trust-remote-code: Allow custom model code execution

vllm serve Qwen/Qwen3-30B-A3B `
    --served-model-name Qwen3-30B-A3B `
    --api-key abc-123 `
    --port 8000 `
    --enable-auto-tool-choice `
    --tool-call-parser hermes `
    --trust-remote-code

# Note: The server will run in the foreground.
# Press Ctrl+C to stop the server.
