from pathlib import Path
from typing import List, Optional
from qgis.PyQt.QtCore import QObject, QProcess, pyqtSignal


class RTKLIBRunner(QObject):
    started = pyqtSignal(str)
    log_received = pyqtSignal(str)
    finished = pyqtSignal(int)

    def __init__(self, rnx2rtkp_path: Optional[str] = None, parent=None):
        super().__init__(parent)
        self.rnx2rtkp_path = rnx2rtkp_path or "rnx2rtkp"
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self._stdout)
        self.process.readyReadStandardError.connect(self._stderr)
        self.process.finished.connect(self.finished.emit)

    def run(self, config_path: str, output_pos: str, input_files: List[str]):
        args = ["-k", config_path, "-o", output_pos] + input_files
        self.started.emit(f"{self.rnx2rtkp_path} {' '.join(args)}")
        self.process.start(self.rnx2rtkp_path, args)

    def cancel(self):
        if self.process.state() != QProcess.NotRunning:
            self.process.kill()

    def _stdout(self):
        self.log_received.emit(bytes(self.process.readAllStandardOutput()).decode("utf-8", errors="ignore"))

    def _stderr(self):
        self.log_received.emit(bytes(self.process.readAllStandardError()).decode("utf-8", errors="ignore"))
