import pydotplus
from TrafficItem import TrafficItem


def render(ipmap_dict, name):
    # argument type checks
    if not isinstance(ipmap_dict, dict):
        print("Render requires an argument of type 'dict'")
        exit(1)

    if not isinstance(name, str):
        print("Name requires an argument of type 'str'")
        exit(1)

    g = pydotplus.Dot()

    nodes = {}
    edges = {}

    for item in ipmap_dict.items():
        if not isinstance(item, TrafficItem):
            continue

        if not nodes.get(item.source, None):
            nodes[item.source] = g.node(item.source,
                                        label=item.source_name if item.source_name else item.source)

        if not nodes.get(item.destination, None):
            nodes[item.destination] = g.node(item.destination,
                                             label=item.destination_name if item.destination_name else item.destination)

        key = f"{item.source} {item.destination}"
        if not edges.get(key, None):
            edges[key] = g.edge(item.source, item.destination, label=f"{item.counter}")

    g.write("test.png", format="png")