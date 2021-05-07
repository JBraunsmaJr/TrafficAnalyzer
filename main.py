import sys

from PyQt5.QtWidgets import QApplication

from analyzers.BasicAnalyzer import BasicAnalyzer
from analyzers.ArgumentParser import analyzer_cli
import os

from ui.AppWindow import AppWindow


def main():
    config = analyzer_cli()
    analyzer = BasicAnalyzer(config)

    if os.path.exists(f"{config.session_name}.gv") and config.render_only:
        analyzer.display_as_static_graph()
        exit(0)

    if os.path.isdir(config.path):
        for file in os.listdir(config.path):
            if file.endswith(".pcap"):
                analyzer.parse_file(os.path.join(config.path, file))
    elif os.path.isfile(config.path):
        analyzer.parse_file(config.path)

    if config.use_app:
        app = QApplication([])
        window = AppWindow()
        window.consumePCAPResults(analyzer)
        sys.exit(app.exec_())


if __name__ == '__main__':
    main()
