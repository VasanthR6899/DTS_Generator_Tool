import tkinter as tk
from tkinter import ttk, messagebox
import yaml
import os
from jinja2 import Template
from baseboards import list_folders,list_baseboards
from sensor_schema import get_vendor_chipsets

# --- CONFIG ---
KERNEL_PATH = "/home/vasanth/Desktop/personal/linux-at91"
SENSOR_BINDINGS_PATH = os.path.join(KERNEL_PATH, "Documentation/devicetree/bindings/net/wireless/microchip,wilc1000.yaml")
BASEBOARD_DTS_PATH = os.path.join(KERNEL_PATH, "arch/arm/boot/dts/microchip/at91-sama5d27_som1_ek.dts")
OUTPUT_DTS_PATH = "output/custom_sama5d27.dts"
TEMPLATE_PATH = "templates/wilc1000_template.dts.j2"

# --- PARSE YAML BINDINGS ---
def parse_yaml_bindings(path):
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    required = data.get('required', [])
    optional = list(data.get('properties', {}).keys())
    return required, [o for o in optional if o not in required]

# --- DTS MODIFIER ---
def inject_sensor_node(base_dts_path, output_path, rendered_node):
    with open(base_dts_path, 'r') as f:
        lines = f.readlines()

    insert_index = None
    for i, line in enumerate(lines):
        if line.strip() == "/ {":
            insert_index = i + 1
            break

    if insert_index is not None:
        lines.insert(insert_index, f"\n{rendered_node}\n")
        with open(output_path, 'w') as f:
            f.writelines(lines)
        return True
    else:
        return False

# --- GUI TOOL ---

class DTSApp:
    def __init__(self, root):
        self.root = root
        root.title("DTS Generator Tool")
        root.geometry("600x500")
        root.resizable(False, False)

        # Parse YAML and store properties
        self.required, self.optional = parse_yaml_bindings(SENSOR_BINDINGS_PATH)

        # Pin variables
        self.cs_var = tk.StringVar()
        self.irq_var = tk.StringVar()
        self.reset_var = tk.StringVar()

        # Manufacturer and board selection variables
        self.manufacturer_var = tk.StringVar()
        self.baseboard_var = tk.StringVar()
        self.sensor_var=tk.StringVar()

        self.build_ui()

    def build_ui(self):
        # --- Manufacturer Dropdown ---
        ttk.Label(self.root, text="Select the baseboard Manufacturer:", font=("Arial", 12, "bold")).pack(pady=10)
        folder_frame = ttk.Frame(self.root)
        folder_frame.pack()

        manufacturers = list_folders(os.path.join(KERNEL_PATH, "arch/arm/boot/dts"))
        self.manufacturer_combo = ttk.Combobox(folder_frame, values=manufacturers, textvariable=self.manufacturer_var, state="readonly")
        self.manufacturer_combo.pack()
        self.manufacturer_combo.bind("<<ComboboxSelected>>", self.on_manufacturer_selected)

        # --- Baseboard Dropdown ---
        ttk.Label(self.root, text="Select the baseboard name:", font=("Arial", 12, "bold")).pack(pady=10)
        board_frame = ttk.Frame(self.root)
        board_frame.pack()

        self.baseboard_combo = ttk.Combobox(board_frame, textvariable=self.baseboard_var, state="readonly")
        self.baseboard_combo.pack()

        #---Sensor select Dropdown---

        ttk.Label(self.root, text="Select the Sensor name:", font=("Arial", 12, "bold")).pack(pady=10)
        sensor_frame = ttk.Frame(self.root)
        sensor_frame.pack()

        self.sensor_combo = ttk.Combobox(sensor_frame, textvariable=self.sensor_var, state="readonly")
        self.sensor_combo.pack()

        """For complexity purposes, I am adding only the wireless sensors in the mainline kernel in here"""
        self.populate_sensor_dropdown()

    def populate_sensor_dropdown(self):
        vendor_chipsets = get_vendor_chipsets()

        sensor_options = []
        for vendor in sorted(vendor_chipsets):
            for chip in sorted(vendor_chipsets[vendor]):
                sensor_options.append(f"{vendor},{chip}")

        self.sensor_combo['values'] = sensor_options

        if sensor_options:
            self.sensor_combo.current(0)  # Optional: pre-select first item

    



        """# --- Pin Entries ---
        frame = ttk.Frame(self.root)
        frame.pack(pady=15)

        ttk.Label(frame, text="CS Pin:").grid(row=0, column=0, sticky='e')
        ttk.Entry(frame, textvariable=self.cs_var).grid(row=0, column=1)

        ttk.Label(frame, text="IRQ Pin:").grid(row=1, column=0, sticky='e')
        ttk.Entry(frame, textvariable=self.irq_var).grid(row=1, column=1)

        ttk.Label(frame, text="Reset Pin:").grid(row=2, column=0, sticky='e')
        ttk.Entry(frame, textvariable=self.reset_var).grid(row=2, column=1)"""

        # --- Generate Button ---
        #ttk.Button(self.root, text="Generate DTS", command=self.generate_dts).pack(pady=20)

        # --- Optional Properties Display ---
        opt_frame = ttk.Frame(self.root)
        opt_frame.pack(pady=10)
        ttk.Label(opt_frame, text="Optional Properties:", font=("Arial", 10, "bold")).pack()

        for prop in self.optional:
            ttk.Label(opt_frame, text=prop).pack()

    def on_manufacturer_selected(self, event):
        manufacturer = self.manufacturer_var.get()
        baseboard_path = os.path.join(KERNEL_PATH, "arch/arm/boot/dts", manufacturer)
        baseboards = list_baseboards(baseboard_path)
        self.baseboard_combo['values'] = baseboards

    """def generate_dts(self):
        pins = {
            "cs_pin": self.cs_var.get(),
            "irq_pin": self.irq_var.get(),
            "reset_pin": self.reset_var.get(),
        }

        # You can update this if you want to dynamically use selected baseboard file
        selected_board = self.baseboard_var.get()
        full_baseboard_path = os.path.join(KERNEL_PATH, "arch/arm/boot/dts", self.manufacturer_var.get(), selected_board)

        try:
            with open(TEMPLATE_PATH, 'r') as f:
                template = Template(f.read())

            rendered = template.render(**pins)

            success = inject_sensor_node(full_baseboard_path, OUTPUT_DTS_PATH, rendered)
            if success:
                messagebox.showinfo("Success", f"DTS generated at {OUTPUT_DTS_PATH}")
            else:
                messagebox.showerror("Error", "Failed to inject device node into DTS")
        except Exception as e:
            messagebox.showerror("Error", f"Exception occurred: {e}")"""


if __name__ == "__main__":
    root = tk.Tk()
    app = DTSApp(root)
    root.mainloop()
