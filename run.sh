#!/bin/bash
# 🤖 Agentic AI Platform — Run Script
# Executes the 5-agent incident response simulation

cd "$(dirname "$0")" || exit
python main.py "$@"
