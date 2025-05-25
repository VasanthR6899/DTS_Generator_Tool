import os
import yaml
from collections import defaultdict

BINDINGS_DIR = "/home/vasanth/Desktop/personal/linux-at91/Documentation/devicetree/bindings/net/wireless"

def get_vendor_chipsets():
    vendor_chipsets = defaultdict(list)

    for root, _, files in os.walk(BINDINGS_DIR):
        for file in files:
            if file.endswith(".yaml") or file.endswith(".yml"):
                if "," in file:
                    vendor, chipset_ext = file.split(",", 1)
                    chipset = chipset_ext.rsplit(".", 1)[0]
                    vendor_chipsets[vendor].append(chipset)

    return vendor_chipsets

"""if __name__ == "__main__":
    schema = get_vendor_chipsets(BINDINGS_DIR)
    for vendor in sorted(schema.keys()):
        print(f"{vendor}:")
        for chip in sorted(schema[vendor]):
            print(f"  - {chip}")"""

