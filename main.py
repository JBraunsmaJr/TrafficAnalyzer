from analyzers.BasicAnalyzer import BasicAnalyzer
from ArgumentParser import analyzer_cli
import os


def main():
    config = analyzer_cli()
    analyzer = BasicAnalyzer(config)

    if os.path.isdir(config.path):
        for file in os.listdir(config.path):
            if file.endswith(".pcap"):
                analyzer.parse_file(os.path.join(config.path, file))
    elif os.path.isfile(config.path):
        analyzer.parse_file(config.path)

    analyzer.display_as_static_graph()


if __name__ == '__main__':
    main()
