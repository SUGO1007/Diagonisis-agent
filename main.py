#!/usr/bin/env python3
"""
Autonomous Incident Diagnosis & Resolution AI Tool

LangGraph-based Multi-Agent Orchestrator with Qwen LLM and Simulated MCP Server.

Architecture:
    - LangGraph StateGraph for workflow orchestration
    - Qwen model (via vLLM OpenAI-compatible API) for agent reasoning
    - Simulated MCP Server (stdio) for infrastructure tool calls
    - 5 Specialized Agents: Monitor, Diagnosis, Gathering, Remediation, Learner

Usage:
    # Step 1: Start vLLM server first (in a separate terminal):
    # 
    # On Windows PowerShell:
    #   .\start_vllm.ps1
    # 
    # On Windows CMD:
    #   start_vllm.bat
    # 
    # On Linux/Mac:
    #   ./start_vllm.sh
    #
    # Or manually:
    #   vllm serve Qwen/Qwen3-30B-A3B --served-model-name Qwen3-30B-A3B --api-key abc-123 --port 8000 --enable-auto-tool-choice --tool-call-parser hermes --trust-remote-code
    #
    # Step 2: Wait for vLLM to load (you'll see "Application startup complete" message)
    #
    # Step 3: Run this script:
    #   python main.py
    #
    # Configuration:
    #   Edit .env file to customize settings (LLM_BASE_URL, LLM_MODEL, etc.)
    #   Or use environment variables:
    #   LLM_BASE_URL=http://localhost:8000/v1 LLM_MODEL=Qwen3-30B-A3B python main.py
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from orchestrator import build_incident_response_graph, visualize_graph
from data_ingestion import DataIngestionPipeline, SERVERS, SERVICES


def create_sample_alert() -> dict:
    """
    Create a sample alert from the data ingestion pipeline.

    In production, this would come from Prometheus/Datadog/CloudWatch.
    """
    pipeline = DataIngestionPipeline(SERVERS, SERVICES)
    results = pipeline.run_pipeline()

    print(f"\n{'='*70}")
    print(f"  AUTONOMOUS INCIDENT DIAGNOSIS & RESOLUTION AI TOOL")
    print(f"  LangGraph Orchestrator | Qwen LLM | MCP Tools")
    print(f"{'='*70}")

    print(f"\n[DATA INGESTION] Pipeline Results:")
    print(f"   Events collected: {results['total_events']}")
    print(f"   Events enriched: {results['enriched']}")
    print(f"   Anomalies detected: {results['anomalies']}")
    print(f"   Critical: {results['critical']} | Warning: {results['warning']}")

    # Get top critical anomaly
    critical_anomalies = pipeline.get_critical_anomalies()
    if critical_anomalies:
        top = critical_anomalies[0]
        raw_alert = {
            "alert": "HighCPU",
            "server": top.host,
            "service": "data-transform",
            "cpu_percent": top.metric_value,
            "threshold": top.threshold,
            "duration": "47m",
            "severity": top.severity,
            "source": top.source,
            "metric": top.metric_name,
            "timestamp": datetime.now().isoformat(),
        }
    else:
        raw_alert = {
            "alert": "HighCPU",
            "server": "prod-web-07",
            "service": "data-transform",
            "cpu_percent": 98.5,
            "threshold": 95.0,
            "duration": "47m",
            "severity": "critical",
            "source": "prometheus",
            "metric": "cpu_percent",
            "timestamp": datetime.now().isoformat(),
        }

    print(f"\n[ALERT] Triggering incident response for:")
    print(f"   Server: {raw_alert['server']}")
    print(f"   Metric: CPU {raw_alert['cpu_percent']}% (threshold: {raw_alert['threshold']}%)")
    print(f"   Duration: {raw_alert['duration']}")
    print(f"   Severity: {raw_alert['severity']}")

    return raw_alert


def run_langgraph_workflow(raw_alert: dict) -> dict:
    """
    Execute the full LangGraph incident response workflow.

    This builds and runs the StateGraph, passing the alert through
    all agent nodes following the Graph_flow 2.txt architecture.
    """
    print(f"\n{'='*70}")
    print(f"[LANGGRAPH] Building incident response graph...")
    print(f"{'='*70}")

    # Build the compiled graph
    graph = build_incident_response_graph()

    # Initialize state
    initial_state = {
        "raw_alert": raw_alert,
        "enriched_alert": {},
        "diagnosis": {},
        "confidence": 0.0,
        "gathering_iterations": [],
        "gathered_info": {},
        "remediation_plan": {},
        "compliance_result": {},
        "approval_needed": False,
        "human_approval": None,
        "execution_result": {},
        "validation_result": {},
        "learning_result": {},
        "outcome": "pending",
        "escalation_reason": "",
        "messages": [],
    }

    print(f"[LANGGRAPH] Executing workflow...")
    print(f"[LANGGRAPH] Nodes: monitor -> diagnose -> [gather_info] -> plan -> comply -> execute -> validate -> learn")

    start_time = time.time()

    # Execute the graph
    final_state = graph.invoke(initial_state)

    elapsed = time.time() - start_time

    return final_state, elapsed


def print_summary(final_state: dict, elapsed: float):
    """Print execution summary and statistics."""
    print(f"\n{'='*70}")
    print(f"[SUMMARY] WORKFLOW COMPLETE")
    print(f"{'='*70}")

    outcome = final_state.get("outcome", "unknown")
    confidence = final_state.get("confidence", 0)
    iterations = len(final_state.get("gathering_iterations", []))
    diagnosis = final_state.get("diagnosis", {})
    learning = final_state.get("learning_result", {})

    print(f"\n   Outcome: {outcome.upper()}")
    print(f"   Total Time: {elapsed:.1f}s")
    print(f"   Final Confidence: {confidence:.0%}")
    print(f"   Root Cause: {diagnosis.get('root_cause', 'N/A')[:80]}")
    print(f"   Gathering Iterations: {iterations}")
    print(f"   Approval Needed: {final_state.get('approval_needed', False)}")

    if learning:
        pattern = learning.get("pattern", {})
        print(f"\n   Pattern Learned:")
        print(f"      Trigger: {pattern.get('trigger', 'N/A')}")
        print(f"      Category: {pattern.get('root_cause_category', 'N/A')}")

        lessons = learning.get("lessons_learned", [])
        if lessons:
            print(f"\n   Lessons Learned:")
            for lesson in lessons[:3]:
                print(f"      - {lesson}")

    print(f"\n{'='*70}")
    print(f"[DONE] LangGraph workflow finished with outcome: {outcome}")
    print(f"{'='*70}\n")


def check_prerequisites():
    """Check that required services and dependencies are available."""
    issues = []

    # Check for required packages
    try:
        import langgraph
    except ImportError:
        issues.append("langgraph not installed. Run: pip install langgraph")

    try:
        import openai
    except ImportError:
        issues.append("openai not installed. Run: pip install openai")

    try:
        from dotenv import load_dotenv
    except ImportError:
        issues.append("python-dotenv not installed. Run: pip install python-dotenv")

    # Check LLM server connectivity
    base_url = os.environ.get("LLM_BASE_URL", "http://localhost:8000/v1")
    model = os.environ.get("LLM_MODEL", "Qwen3-30B-A3B")

    print(f"\n[CONFIG] LLM Configuration:")
    print(f"   Base URL: {base_url}")
    print(f"   Model: {model}")
    print(f"   API Key: {'***' + os.environ.get('LLM_API_KEY', 'abc-123')[-4:]}")

    if issues:
        print(f"\n[WARNING] Prerequisites issues:")
        for issue in issues:
            print(f"   ! {issue}")
        print(f"\n   Install all: pip install langgraph openai python-dotenv")
        return False

    # Test LLM connection
    try:
        from openai import OpenAI
        client = OpenAI(base_url=base_url, api_key=os.environ.get("LLM_API_KEY", "abc-123"))
        models = client.models.list()
        print(f"   Connection: ✓ OK (models available: {len(models.data)})")
        return True
    except Exception as e:
        error_msg = str(e)
        print(f"   Connection: ✗ FAILED")
        print(f"   Error: {error_msg[:100]}")
        print(f"\n{'='*70}")
        print(f"[ERROR] LLM Server Connection Failed")
        print(f"{'='*70}")
        print(f"\nThe vLLM server is not running at {base_url}")
        print(f"\nTo fix this issue:")
        print(f"\n1. Open a NEW terminal/command prompt")
        print(f"\n2. Start the vLLM server using one of these methods:")
        print(f"   ")
        print(f"   Windows PowerShell:")
        print(f"     .\\start_vllm.ps1")
        print(f"   ")
        print(f"   Windows CMD:")
        print(f"     start_vllm.bat")
        print(f"   ")
        print(f"   Linux/Mac:")
        print(f"     ./start_vllm.sh")
        print(f"   ")
        print(f"   Or manually:")
        print(f"     vllm serve Qwen/Qwen3-30B-A3B \\")
        print(f"       --served-model-name Qwen3-30B-A3B \\")
        print(f"       --api-key abc-123 \\")
        print(f"       --port 8000 \\")
        print(f"       --enable-auto-tool-choice \\")
        print(f"       --tool-call-parser hermes \\")
        print(f"       --trust-remote-code")
        print(f"\n3. Wait for the message: 'Application startup complete'")
        print(f"\n4. Run this script again: python main.py")
        print(f"\n{'='*70}")
        print(f"\nNote: The workflow will continue with simulated/fallback responses.")
        print(f"      For REAL AI responses, you must start the vLLM server first.")
        print(f"{'='*70}\n")
        return False


def main():
    """Main entry point - run the LangGraph incident response workflow."""

    # Check prerequisites
    check_prerequisites()

    # Create alert from data ingestion pipeline
    raw_alert = create_sample_alert()

    # Run the LangGraph workflow
    final_state, elapsed = run_langgraph_workflow(raw_alert)

    # Print summary
    print_summary(final_state, elapsed)

    return final_state


if __name__ == "__main__":
    main()
