import os
import argparse
import json
from models.FlagRule import FlagRule
from models.RenderRule import RenderRule


class AnalyzerConfig:
    """
    Data Structure to store configuration values from CLI or JSON

    Can be passed around the application
    """
    def __init__(self):
        self.render_rules: dict = dict()
        self.render_flags: list = []
        self.render_labels: dict = dict()
        self.session_name: str = None
        self.path: str = None
        self.render_only: bool = False
        self.use_app: bool = False


def consume_args(args) -> AnalyzerConfig:
    """
    Consumes CLI arguments and condenses them into a usable Configuration instance
    :param args: CLI arguments provided by argparse
    :return: AnalyzerConfig with populated values
    """
    config = AnalyzerConfig()

    if args.use_app:
        config.use_app = True

    if not args.path:
        if os.environ["TEST_PCAP"]:
            args.path = os.environ["TEST_PCAP"]
        else:
            print("Traffic Analyzer requires a PCAP file, or directory of PCAPS")
            exit(1)

    if os.path.isdir(args.path) or os.path.isfile(args.path):
        config.path = args.path
    else:
        print(f"{args.path} could not be located")
        exit(1)

    if args.name:
        config.session_name = args.name

    if args.render_only:
        config.render_only = args.render_only

    # Parse through CLI labels (if applicable)
    for entry in args.label if args.label else []:
        split = entry.split("=")

        if len(split) != 2:
            print(f"Invalid label provided via CLI. '{entry}' must use format \"x.x.x.x=your awesome label\"")
            continue

        config.render_labels[split[0]] = split[1]

    # Parse through CLI flags (if applicable)
    for entry in args.flag if args.flag else []:
        values = entry.split(",")

        if len(values) > 3:
            print(f"Invalid flag format provided. Expected no more than 3 values. \"{entry}\"\n"
                  "\tFormat should be \"origin=x.x.x.x|y.y.y.y,destination=a.a.a.a|b.b.b.b,color=black\"")
            continue

        color = "black"
        origin = []
        destinations = []

        for item in values:
            if "color=" in item:
                color = item.split("=")[1]
            elif "origin=" in item:
                addresses = item.split("=")[1]
                origin = addresses.split("|") if "|" in addresses else [addresses]
            elif "destination=" in item:
                addresses = item.split("=")[1]
                destinations = addresses.split("|") if "|" in addresses else [addresses]

        config.render_flags.append(FlagRule(origin, destinations, color))

    # Parse through CLI rules (if applicable)
    for entry in args.rule if args.rule else []:
        values = split(",")

        if len(values) > 3:
            print(f"Invalid render rule format. Should have no more than 3 parameters. '{entry}'\n"
                  f"\t--flag=\"color=red,shape=oval,target=x.x.x.x\"")

        color = "black"
        shape = "ellipse"
        target = None

        for item in values:
            if "color=" in item:
                color = item.split("=")[1]
            elif "shape=" in item:
                shape = item.split("=")[1]
            elif "target=" in item:
                target = item.split("=")[1]

        config.render_rules[target] = RenderRule(target, shape, color)

    # if the configuration value was provided AND
    # the config path exists
    if args.config and os.path.exists(args.config):
        try:
            with open(args.config, "r") as file:
                config_json = json.load(file)

                for item in config_json["labels"] if config_json["labels"] else []:
                    config.render_labels[item["address"]] = item["label"]

                for item in config_json["rules"] if config_json["rules"] else []:
                    config.render_rules[item["target"]] = RenderRule(item["target"],
                                                                     item["shape"] if item["shape"] else "ellipse",
                                                                     item["color"] if item["color"] else "black")

                for item in config_json["flags"] if config_json["flags"] else []:
                    config.render_flags.append(FlagRule(item["origin"], item["destination"], item["color"]))
        except Exception as ex:
            print(f"Issue loading JSON config file: {args.config}", ex)
            exit(1)

    # if the user flagged to save arguments
    if args.save:
        # If a config was provided -- we'll simply overwrite the config
        # to be a combination of all CLI arguments and JSON values
        if args.config:
            with open(args.config, "w") as json_config:
                json_config.write(json.dumps(config))
        # Otherwise -- output everything to the default "traffic_analyzer.json" file
        else:
            with open("traffic_analyzer.json", "w") as json_config:
                json_config.write(json.dumps(config))

    return config


def analyzer_cli():
    """
    One stop shop for all cli arguments / parsing
    :return: Populated AnalyzerConfig instance
    """
    parser = argparse.ArgumentParser(description="Analyze Traffic via PCAPs and display various metrics")
    parser.add_argument("-p", "--path", help="PCAP File OR Directory to consume (must have .pcap extension)")
    parser.add_argument("-c", "--config", help="Path to Traffic Analyzer JSON config to use for this session")
    parser.add_argument("--save", action="store_true", help="Instead of remembering CLI arguments such as labels "
                                                            "or flags you can optionally have it saved to a JSON"
                                                            "file. If used in conjunction with --config it will"
                                                            "combine values and save to the specified config path")
    parser.add_argument("-l", "--label", action="append", help="Map an IP Address to a label to use for rendering.\n"
                                                               "\t--label=\"x.x.x.x=my awesome label\"")
    parser.add_argument("-f", "--flag", action="append",
                        help="When specific traffic between devices warrants emphasis.\n"
                             "\t--flag=\"origin=x.x.x.x,destination=a.a.a.a,color=red\"\n"
                             "\t--flag=\"origin=a.a.a.a|b.b.b.b,destination=c.c.c.c|d.d.d.d,color=red\"\n"
                             "\t\tTo specify more than one host use a pipe '|' as the delimiter")
    parser.add_argument("-r", "--rule", action="append",
                        help="Give emphasis to particular IPs / IP Ranges. From coloration to the shape used during "
                             "rendering\n"
                             "\t--rule=\"color=red,target=x.x.x,shape=rectangle\"\n"
                             "\t\tcolor -> visual color to use when IP meets target criteria\n"
                             "\t\tshape -> shape to render on graph (default is ellipse)\n"
                             "\t\ttarget -> IP prefix / range / CIDR")

    parser.add_argument("--render-only", action="store_true", help="Only render output (or from saved file)")
    parser.add_argument("--name", default="TrafficAnalyzer", help="Name of session. Used for session "
                                                                  "identification purposes")

    parser.add_argument("--use_app", action="store_true", help="Display Interactive Application")

    return consume_args(parser.parse_args())
