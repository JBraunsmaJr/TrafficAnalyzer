from TrafficAnalyzer import TrafficAnalyzer
import argparse
import os


def main(file):
    analyzer = TrafficAnalyzer()
    analyzer.parse_pcap(file, display_text=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Analyze Traffic via PCAP files and display basic metrics")
    parser.add_argument("file", help="Path to PCAP file to process")
    args = parser.parse_args()

    # argument validation
    if not args.file:
        print("Requires pcap_file to process")
        exit(1)

    if not os.path.exists(args.file):
        print(f"PCAP File: {args.file} does not exist")
        exit(1)

    main(args.file)
