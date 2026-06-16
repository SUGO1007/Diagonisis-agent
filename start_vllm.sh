#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# vLLM Server Startup Script for Qwen3-30B-A3B Model
# ═══════════════════════════════════════════════════════════════
#
# This script starts the vLLM server with Qwen3-30B-A3B model
# using OpenAI-compatible API for the Autonomous Incident AI Tool.
#
# Usage:
#   ./start_vllm.sh
#
# Requirements:
#   - vLLM installed: pip install vllm
#   - AMD GPU with ROCm support (or NVIDIA GPU with CUDA)
#   - Sufficient GPU memory for Qwen3-30B-A3B model
#
# ═══════════════════════════════════════════════════════════════

echo "═══════════════════════════════════════════════════════════════"
echo "  Starting vLLM Server for Autonomous Incident AI Tool"
echo "  Model: Qwen/Qwen3-30B-A3B"
echo "  Port: 8000"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Check if vLLM is installed
if ! command -v vllm &> /dev/null; then
    echo "ERROR: vLLM is not installed!"
    echo "Install it with: pip install vllm"
    exit 1
fi

# Set environment variables for AMD GPUs (comment out if using NVIDIA)
export VLLM_USE_TRITON_FLASH_ATTN=0

# Start vLLM server with Qwen3-30B-A3B
# Parameters explained:
#   --served-model-name: Name exposed via API (must match LLM_MODEL in .env)
#   --api-key: Authentication key (must match LLM_API_KEY in .env)
#   --port: Server port (default 8000)
#   --enable-auto-tool-choice: Enable automatic tool selection
#   --tool-call-parser: Parser for function calling (hermes format)
#   --trust-remote-code: Allow custom model code execution
vllm serve Qwen/Qwen3-30B-A3B \
    --served-model-name Qwen3-30B-A3B \
    --api-key abc-123 \
    --port 8000 \
    --enable-auto-tool-choice \
    --tool-call-parser hermes \
    --trust-remote-code

# Note: The server will run in the foreground.
# Press Ctrl+C to stop the server.
#
# To run in the background, use:
#   nohup ./start_vllm.sh > vllm.log 2>&1 &
