#!/usr/bin/env python3
"""
Agent 管理脚本
用法: python3 agent-manager.py <command> [args]

Commands:
    list              列出所有Agent
    status <agent>   查看Agent状态
    restart <agent>   重启Agent
    logs <agent>      查看Agent日志
"""

import json
import sys
import os
import subprocess

CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def list_agents():
    config = load_config()
    print("\n=== Agent 列表 ===")
    for agent in config.get("agents", {}).get("list", []):
        aid = agent.get("id", "unknown")
        workspace = agent.get("workspace", "N/A")
        print(f"  • {aid} → {workspace}")
    print()

def status_agent(agent_id):
    config = load_config()
    for agent in config.get("agents", {}).get("list", []):
        if agent.get("id") == agent_id:
            print(f"\n=== {agent_id} ===")
            print(f"Workspace: {agent.get('workspace')}")
            print(f"Model: {agent.get('model', 'default')}")
            subs = agent.get("subagents", {}).get("allowAgents", [])
            print(f"可调度: {', '.join(subs) if subs else '(无)'}")
            print()
            return
    print(f"Agent '{agent_id}' not found")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        list_agents()
    elif cmd == "status" and len(sys.argv) > 2:
        status_agent(sys.argv[2])
    else:
        print(__doc__)
