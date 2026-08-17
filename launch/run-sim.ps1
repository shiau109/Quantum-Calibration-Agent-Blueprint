# Launch the scqo-agent server against the SIMULATED deployment (chipA/simulated).
# Safe to run anywhere: no hardware is touched, runs persist to D:\qpu_data_dev
# under the chipA `simulated` setup context, tagged "qca".

$repo = Split-Path -Parent $PSScriptRoot

$env:SCQO_AGENT_CONFIG = Join-Path $repo "configs\config.sim.toml"
$env:SCQO_USER_CONFIG  = Join-Path $repo "configs\user.sim.toml"
$env:SCQO_AGENT_PYTHON = "D:\github\.venv-view\Scripts\python.exe"
$env:SCQO_AGENT_TIMEOUT_S = "900"
$env:SCQO_AGENT_TIMEOUT_POLICY = "kill"

# ---- LLM brain -------------------------------------------------------------
# Default: Anthropic (needs ANTHROPIC_API_KEY in the environment or .env).
if (-not $env:QCA_MODEL) { $env:QCA_MODEL = "anthropic:claude-opus-5" }

# Alternative: the lab's self-hosted Ising endpoint (no key, on-LAN).
# Uncomment the three lines below to switch (and comment nothing else out —
# QCA_MODEL wins because it is set explicitly here).
# $env:QCA_MODEL = "openai:nvidia/NVIDIA-Ising-Calibration-1"
# $env:OPENAI_API_KEY = "dummy"
# $env:OPENAI_API_BASE = "http://10.21.19.201:28000/v1"
# ---------------------------------------------------------------------------

& (Join-Path $repo ".venv\Scripts\python.exe") (Join-Path $repo "server.py")
