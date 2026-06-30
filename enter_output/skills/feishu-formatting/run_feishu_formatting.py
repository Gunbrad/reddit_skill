from __future__ import annotations

import subprocess
import sys
from pathlib import Path


STAGE = "feishu-formatting"
# Delegates to enter_output/runtime/run_stage.py.
RUN_STAGE = Path(__file__).resolve().parents[2] / "runtime" / "run_stage.py"


if __name__ == "__main__":
    raise SystemExit(subprocess.call([sys.executable, str(RUN_STAGE), "--stage", STAGE, *sys.argv[1:]]))
