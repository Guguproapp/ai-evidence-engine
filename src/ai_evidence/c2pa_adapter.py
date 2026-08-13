import json
import shutil
import subprocess
from pathlib import Path


class C2paError(RuntimeError):
    pass


class C2paTool:
    def __init__(self, executable="c2patool"):
        resolved = shutil.which(executable)
        if not resolved:
            raise C2paError("official c2patool is not installed")
        self.executable = resolved

    def version(self):
        return self._run(["-V"]).strip()

    def sign(self, source, output, manifest, parent=None, create_type=None):
        command = [str(source), "--manifest", str(manifest), "--output", str(output), "--force"]
        if parent:
            command.extend(["--parent", str(parent)])
        if create_type:
            command.extend(["--create", create_type])
        raw = self._run(command)
        return json.loads(raw)

    def read(self, asset):
        return json.loads(self._run([str(asset)]))

    def info(self, asset):
        return self._run([str(asset), "--info"])

    def _run(self, args):
        result = subprocess.run([self.executable, *args], capture_output=True, text=True)
        if result.returncode != 0:
            raise C2paError(result.stderr.strip() or result.stdout.strip())
        return result.stdout

