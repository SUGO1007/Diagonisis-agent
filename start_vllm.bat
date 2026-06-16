# ═══════════════════════════════════════════════════════════════
# vLLM Server Startup Script for Qwen3-30B-A3B Model (Windows)
# ═══════════════════════════════════════════════════════════════
#
# This script starts the vLLM server with Qwen3-30B-A3B model
# using OpenAI-compatible API for the Autonomous Incident AI Tool.
#
# Usage:
#   .\start_vllm.bat
#   or double-click the file
#
# Requirements:
#   - vLLM installed: pip install vllm
#   - AMD GPU with ROCm support (or NVIDIA GPU with CUDA)
#   - Sufficient GPU memory for Qwen3-30B-A3B model
#
# ═══════════════════════════════════════════════════════════════

@echo off
echo ═══════════════════════════════════════════════════════════════
echo   Starting vLLM Server for Autonomous Incident AI Tool
echo   Model: Qwen/Qwen3-30B-A3B
echo   Port: 8000
echo ═══════════════════════════════════════════════════════════════
echo.

REM Check if vLLM is installed
where vllm >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: vLLM is not installed!
    echo Install it with: pip install vllm
    pause
    exit /b 1
)

REM Set environment variables for AMD GPUs (comment out if using NVIDIA)
set VLLM_USE_TRITON_FLASH_ATTN=0

echo Starting vLLM server...
echo Press Ctrl+C to stop the server
echo.

REM Start vLLM server with Qwen3-30B-A3B
REM Parameters explained:
REM   --served-model-name: Name exposed via API (must match LLM_MODEL in .env)
REM   --api-key: Authentication key (must match LLM_API_KEY in .env)
REM   --port: Server port (default 8000)
REM   --enable-auto-tool-choice: Enable automatic tool selection
REM   --tool-call-parser: Parser for function calling (hermes format)
REM   --trust-remote-code: Allow custom model code execution

vllm serve Qwen/Qwen3-30B-A3B --served-model-name Qwen3-30B-A3B --api-key abc-123 --port 8000 --enable-auto-tool-choice --tool-call-parser hermes --trust-remote-code

REM Note: The server will run in the foreground.
REM Press Ctrl+C to stop the server.

pause
