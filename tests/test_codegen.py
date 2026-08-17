# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Census gate for the generated SCQO wrappers.

Runs without scqo installed: it only asserts what QCA's own discovery sees
in the committed scripts/scqo_*.py files. Regenerating the wrappers
(codegen/generate_wrappers.py, under an SCQO venv) is what keeps them in
sync with the live catalog; this gate keeps broken output from landing.
"""

import py_compile
from pathlib import Path

from core.discovery import discover_experiments

REPO = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO / "scripts"

EXPECTED_WRAPPERS = 37
LEGAL_TYPES = {"int", "float", "str", "bool", "list", "dict"}


def _scqo_experiments():
    return [
        e for e in discover_experiments(SCRIPTS_DIR) if e.name.startswith("scqo_")
    ]


class TestWrapperCensus:
    def test_expected_count(self):
        assert len(_scqo_experiments()) == EXPECTED_WRAPPERS

    def test_targets_is_the_only_required_param(self):
        for exp in _scqo_experiments():
            required = [p.name for p in exp.parameters if p.required]
            assert required == ["targets"], f"{exp.name}: required={required}"

    def test_all_types_legal(self):
        for exp in _scqo_experiments():
            for p in exp.parameters:
                assert p.type in LEGAL_TYPES, f"{exp.name}.{p.name}: {p.type!r}"
            targets = next(p for p in exp.parameters if p.name == "targets")
            assert targets.type == "list"

    def test_every_wrapper_has_description(self):
        for exp in _scqo_experiments():
            assert exp.description, f"{exp.name} has an empty description"

    def test_wrappers_compile(self):
        for path in sorted(SCRIPTS_DIR.glob("scqo_*.py")):
            py_compile.compile(str(path), doraise=True)

    def test_api_doc_generated(self):
        doc = REPO / "data" / "knowledge" / "documents" / "03_Experiment_API.md"
        assert doc.is_file()
        text = doc.read_text(encoding="utf-8")
        for exp in _scqo_experiments():
            assert f"## {exp.name}" in text, f"{exp.name} missing from API doc"
