"""Offline numeric-input regressions; never connect to speakers."""

import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import Mock, patch


SPEC = importlib.util.spec_from_file_location(
    "khtool_under_test", Path(__file__).resolve().parents[1] / "khtool.py"
)
khtool = importlib.util.module_from_spec(SPEC)
with patch.dict(sys.modules, {"pyssc": types.ModuleType("pyssc")}), patch(
    "signal.signal"
):
    SPEC.loader.exec_module(khtool)


class LevelTests(unittest.TestCase):
    def run_cli(self, option, value):
        backend = Mock()
        # Reaching discovery means validation accepted the input. No network is used.
        backend.scan.side_effect = RuntimeError("discovery reached")
        output = io.StringIO()
        with patch.object(khtool, "ssc", backend), patch.object(
            khtool.os.path, "exists", return_value=False
        ), patch.object(
            sys, "argv", ["khtool.py", "-i", "en0", f"{option}={value}"]
        ), contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            try:
                khtool.main()
            except SystemExit as exc:
                return exc.code, output.getvalue(), backend
            except RuntimeError as exc:
                if str(exc) != "discovery reached":
                    raise
                return 0, output.getvalue(), backend
        self.fail("CLI unexpectedly returned")

    def test_nonfinite_values_are_rejected_before_discovery(self):
        for option in ("--level", "--dimm"):
            for value in ("nan", "NaN", "+nan", "-nan", "inf", "-inf", "1e999"):
                with self.subTest(option=option, value=value):
                    code, output, backend = self.run_cli(option, value)
                    self.assertNotEqual(code, 0)
                    self.assertIn("finite", output)
                    backend.scan.assert_not_called()
                    backend.Ssc_device_setup.assert_not_called()

    def test_finite_out_of_range_values_remain_rejected(self):
        for option, values in (("--level", ("-0.1", "120.1")),
                               ("--dimm", ("-120.1", "0.1"))):
            for value in values:
                with self.subTest(option=option, value=value):
                    code, _, backend = self.run_cli(option, value)
                    self.assertNotEqual(code, 0)
                    backend.scan.assert_not_called()

    def test_valid_bounds_and_fractional_values_are_unchanged(self):
        for option, values in (("--level", ("0", "120", "85.5", "-0")),
                               ("--dimm", ("-120", "0", "-12.5", "-0"))):
            for value in values:
                with self.subTest(option=option, value=value):
                    code, _, backend = self.run_cli(option, value)
                    self.assertEqual(code, 0)
                    backend.scan.assert_called_once_with(scan_time_seconds=10)


if __name__ == "__main__":
    unittest.main()
