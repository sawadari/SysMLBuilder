from __future__ import annotations

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sysml_builder.suite import run_suite


class GfseStrictSuiteTest(unittest.TestCase):
    def test_gfse_strict_suite(self) -> None:
        self.assertEqual(run_suite(ROOT), 0)


if __name__ == "__main__":
    unittest.main()
