# Launch the scqo-agent server against the QBLOX deployment (chipA/qblox).
# HARDWARE: runs execute on the Qblox cluster. Operator supervision required
# for first use (Phase C); make sure no notebook kernel holds the cluster.

$repo = Split-Path -Parent $PSScriptRoot

$env:SCQO_AGENT_CONFIG = Join-Path $repo "configs\config.qblox.toml"
$env:SCQO_USER_CONFIG  = Join-Path $repo "configs\user.qblox.toml"
$env:SCQO_AGENT_PYTHON = "D:\github\.venv-qblox\Scripts\python.exe"
$env:SCQO_AGENT_TIMEOUT_S = "1800"
# kill is safe for Qblox: process exit releases the cluster sockets.
$env:SCQO_AGENT_TIMEOUT_POLICY = "kill"

# ---- LLM brain -------------------------------------------------------------
if (-not $env:QCA_MODEL) { $env:QCA_MODEL = "anthropic:claude-opus-5" }
# Lab Ising endpoint alternative:
# $env:QCA_MODEL = "openai:nvidia/NVIDIA-Ising-Calibration-1"
# $env:OPENAI_API_KEY = "dummy"
# $env:OPENAI_API_BASE = "http://10.21.19.201:28000/v1"
# ---------------------------------------------------------------------------

& (Join-Path $repo ".venv\Scripts\python.exe") (Join-Path $repo "server.py")
