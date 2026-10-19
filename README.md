# SSH Log Agent

An AI agent that answers natural-language questions about SSH logs, using a local LLM and tool calling.

## How it works

1. User asks a question
2. Model decides if it needs a tool
3. Python runs a tool
4. Result goes back to the model
5. Model answers or asks for another tool. The agent stops after 5 rounds.

## Example

```
Put the message in here: Find the IP with the most failed attempts, then tell me which accounts that IP attacked.
get_failed_attempts
{'filename': 'logs.txt'}
{'192.168.1.50': 1, '10.0.0.7': 2, '172.16.5.9': 1}
get_users_for_ip
{'ip': '10.0.0.7', 'filename': 'logs.txt'}
{'root': 2}
The IP with the most failed attempts is **10.0.0.7**, and it attacked the account **root**.

```

## Tools

| Tool | What it does |
|---|---|
| `get_failed_attempts` | Count failed SSH login attempts for every IP address in a log file |
| `get_targeted_users` | Count failed SSH login attempts for every username in a log file |
| `get_users_for_ip` | Count failed SSH login attempts for every account attacked by one IP address |

## Tech stack

Python 3.14.4, Ollama, Qwen3 14B - running locally on GPU, pytest

## Setup

1. Install [Ollama](https://ollama.com) and download the model:
```
ollama pull qwen3:14b
```
2. Create a virtual environment and install dependencies:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
3. Run the agent:
```
python agent.py
```

## Tests

```
python -m pytest test_agent.py
```
Tests cover all three tools, including an edge case: `10.0.0.7` must not count attacks from `10.0.0.70`


## Design decisions

- **Tools take a filename, not log lines:** the model can't see the disk or open files — it only knows the conversation. So it passes the filename from the user's question, and the tool opens the file in Python.
- **System prompt:** with two similar tools, the model kept asking which one to use. A system prompt with clear rules made it pick a tool and answer directly.
- **Round limit:** the agent stops after 5 rounds to prevent an infinite loop.
- **`extract_ip` instead of `ip in line`:** a simple substring check counted attacks from `10.0.0.70` as attacks from `10.0.0.7`. Comparing the exact extracted IP fixes that (covered by a test).