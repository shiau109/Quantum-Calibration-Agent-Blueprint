# Launch the scqo-agent server against the QM deployment (chipA/qm_OPX1000).
# HARDWARE: runs execute on the OPX1000. Operator supervision required.
#
# QM DISCIPLINE: a killed experiment child can orphan the gateway-side job
# and wedge the cluster for every later run (the vendor session helper waits
# 120 s then times out; only an operator cluster restart clears a wedge).
# That is why this deployment uses the DETACH timeout policy: on timeout the
# agent reports failure and walks away, but the child finishes on its own.

$repo = Split-Path -Parent $PSScriptRoot

$env:SCQO_AGENT_CONFIG = Join-Path $repo "configs\config.qm.toml"
$env:SCQO_USER_CONFIG  = Join-Path $repo "configs\user.qm.toml"
$env:SCQO_AGENT_PYTHON = "D:\github\.venv-qm\Scripts\python.exe"
$env:SCQO_AGENT_TIMEOUT_S = "3600"
$env:SCQO_AGENT_TIMEOUT_POLICY = "detach"

# ---- LLM brain -------------------------------------------------------------
if (-not $env:QCA_MODEL) { $env:QCA_MODEL = "anthropic:claude-opus-5" }
# Lab Ising endpoint alternative:
# $env:QCA_MODEL = "openai:nvidia/NVIDIA-Ising-Calibration-1"
# $env:OPENAI_API_KEY = "dummy"
# $env:OPENAI_API_BASE = "http://10.21.19.201:28000/v1"
# ---------------------------------------------------------------------------

& (Join-Path $repo ".venv\Scripts\python.exe") (Join-Path $repo "server.py")
