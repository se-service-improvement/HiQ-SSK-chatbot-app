import os
import pytest
import sys

from subprocess import Popen, TimeoutExpired
from time import sleep


script_base_path = os.path.dirname(
***REMOVED***os.path.dirname(
***REMOVED***os.path.dirname(__file__)
***REMOVED***)
)

script_timeout = 240

@pytest.fixture(scope="function")
def script_command():
***REMOVED***if sys.platform.startswith("linux"):
***REMOVED***return "./start.sh"
***REMOVED***
***REMOVED***else:
***REMOVED***return "./start.cmd"


def test_startup_script(script_command):
***REMOVED***stdout = None
***REMOVED***try:
***REMOVED***p = Popen([script_command], cwd=script_base_path)
***REMOVED***stdout, _ = p.communicate(timeout=script_timeout)
***REMOVED***
***REMOVED***except TimeoutExpired:
***REMOVED***assert isinstance(stdout, str)
***REMOVED***assert "127.0.0.1:50505" in stdout
***REMOVED***p.terminate()

***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***