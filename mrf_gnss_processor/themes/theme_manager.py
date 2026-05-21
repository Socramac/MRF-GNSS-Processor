from pathlib import Path


class ThemeManager:
    def apply(self, widget, theme_name="light"):
        qss_path = Path(__file__).parent / f"{theme_name}.qss"
        if qss_path.exists():
            widget.setStyleSheet(qss_path.read_text(encoding="utf-8"))
