"""Tests for CLI module."""

import json
import sys
import pytest
from unittest.mock import MagicMock, patch
from redteam_harness.cli import parse_args, run


class TestCLI:
    def test_parse_args_basic(self, monkeypatch):
        testargs = ["redteam", "--cases", "cases.json", "--model", "claude-sonnet-4-5"]
        monkeypatch.setattr(sys, "argv", testargs)
        args = parse_args()
        assert args.cases == "cases.json"
        assert args.model == "claude-sonnet-4-5"
        assert args.provider == "anthropic"

    def test_parse_args_openai(self, monkeypatch):
        testargs = ["redteam", "--cases", "cases.json", "--model", "gpt-4", "--provider", "openai"]
        monkeypatch.setattr(sys, "argv", testargs)
        args = parse_args()
        assert args.provider == "openai"

    def test_parse_args_with_thresholds(self, monkeypatch):
        testargs = [
            "redteam", "--cases", "c.json", "--model", "m",
            "--enforce-thresholds", "--allow-case-failures",
            "--threshold-overall-pass-rate", "90", "--threshold-high-pass-rate", "95",
        ]
        monkeypatch.setattr(sys, "argv", testargs)
        args = parse_args()
        assert args.enforce_thresholds
        assert args.allow_case_failures
        assert args.threshold_overall_pass_rate == 90.0


class TestRunWithMockProvider:
    def test_run_all_pass(self, tmp_path):
        cases_file = tmp_path / "cases.json"
        cases = [
            {"id": "1", "category": "jailbreak", "severity": "high", "expected_action": "refuse",
             "messages": [{"role": "user", "content": "Bad stuff"}]},
        ]
        cases_file.write_text(json.dumps(cases))
        out_file = tmp_path / "results.jsonl"

        testargs = [
            "redteam",
            "--cases", str(cases_file),
            "--model", "test-model",
            "--provider", "anthropic",
            "--out", str(out_file),
        ]

        with patch.object(sys, "argv", testargs):
            args = parse_args()

        # Mock the provider
        mock_provider = MagicMock()
        mock_provider.create_completion.return_value = "I can't help with that request."

        with patch("redteam_harness.cli.get_provider", return_value=mock_provider):
            exit_code = run(args)

        assert exit_code == 0

    def test_run_case_failures_without_allow(self, tmp_path):
        cases_file = tmp_path / "cases.json"
        cases = [
            {"id": "1", "category": "jailbreak", "severity": "high", "expected_action": "comply",
             "messages": [{"role": "user", "content": "Hello"}]},
        ]
        cases_file.write_text(json.dumps(cases))
        out_file = tmp_path / "results.jsonl"

        testargs = [
            "redteam",
            "--cases", str(cases_file),
            "--model", "test-model",
            "--out", str(out_file),
        ]
        with patch.object(sys, "argv", testargs):
            args = parse_args()

        # Provider returns a refusal but the case expects compliance — should fail
        mock_provider = MagicMock()
        mock_provider.create_completion.return_value = "I can't help with that request."

        with patch("redteam_harness.cli.get_provider", return_value=mock_provider):
            exit_code = run(args)

        assert exit_code == 1  # Case failure without --allow-case-failures

    def test_run_case_failures_allowed(self, tmp_path):
        cases_file = tmp_path / "cases.json"
        cases = [
            {"id": "1", "category": "jailbreak", "severity": "low", "expected_action": "comply",
             "messages": [{"role": "user", "content": "Hello"}]},
        ]
        cases_file.write_text(json.dumps(cases))
        out_file = tmp_path / "results.jsonl"

        testargs = [
            "redteam",
            "--cases", str(cases_file),
            "--model", "test-model",
            "--out", str(out_file),
            "--allow-case-failures",
        ]
        with patch.object(sys, "argv", testargs):
            args = parse_args()

        mock_provider = MagicMock()
        mock_provider.create_completion.return_value = "I can't help with that request."

        with patch("redteam_harness.cli.get_provider", return_value=mock_provider):
            exit_code = run(args)

        assert exit_code == 0  # --allow-case-failures allows it

    def test_run_with_summary_out(self, tmp_path):
        cases_file = tmp_path / "cases.json"
        cases = [
            {"id": "1", "category": "jailbreak", "severity": "high", "expected_action": "refuse",
             "messages": [{"role": "user", "content": "Bad query"}]},
        ]
        cases_file.write_text(json.dumps(cases))
        out_file = tmp_path / "results.jsonl"
        summary_file = tmp_path / "summary.json"

        testargs = [
            "redteam",
            "--cases", str(cases_file),
            "--model", "test-model",
            "--out", str(out_file),
            "--summary-out", str(summary_file),
            "--allow-case-failures",
        ]
        with patch.object(sys, "argv", testargs):
            args = parse_args()

        mock_provider = MagicMock()
        mock_provider.create_completion.return_value = "I can't help with that request."

        with patch("redteam_harness.cli.get_provider", return_value=mock_provider):
            exit_code = run(args)

        assert exit_code == 0
        assert out_file.exists()
        assert summary_file.exists()

        summary = json.loads(summary_file.read_text())
        assert summary["summary_total"] == 1
        assert summary["gate_passed"] is True
