import tkinter as tk
from tkinter import ttk, messagebox
import yaml
import os
from jinja2 import Template

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
        root.geometry("600x400")
        root.resizable(False, False)

        self.cs_var = tk.StringVar()
        self.irq_var = tk.StringVar()
        self.reset_var = tk.StringVar()

        self.required, self.optional = parse_yaml_bindings(SENSOR_BINDINGS_PATH)

        self.build_ui()

    def build_ui(self):
        ttk.Label(self.root, text="Required DTS Properties", font=("Arial", 12, "bold")).pack(pady=10)

        frame = ttk.Frame(self.root)
        frame.pack(pady=5)

        ttk.Label(frame, text="CS Pin:").grid(row=0, column=0, sticky='e')
        ttk.Entry(frame, textvariable=self.cs_var).grid(row=0, column=1)

        ttk.Label(frame, text="IRQ Pin:").grid(row=1, column=0, sticky='e')
        ttk.Entry(frame, textvariable=self.irq_var).grid(row=1, column=1)

        ttk.Label(frame, text="Reset Pin:").grid(row=2, column=0, sticky='e')
        ttk.Entry(frame, textvariable=self.reset_var).grid(row=2, column=1)

        ttk.Button(self.root, text="Generate DTS", command=self.generate_dts).pack(pady=20)

        opt_frame = ttk.Frame(self.root)
        opt_frame.pack(pady=10)
        ttk.Label(opt_frame, text="Optional Properties:").pack()
        for prop in self.optional:
            ttk.Label(opt_frame, text=prop).pack()

    def generate_dts(self):
        pins = {
            "cs_pin": self.cs_var.get(),
            "irq_pin": self.irq_var.get(),
            "reset_pin": self.reset_var.get(),
        }
        with open(TEMPLATE_PATH, 'r') as f:
            template = Template(f.read())
        rendered = template.render(**pins)

        success = inject_sensor_node(BASEBOARD_DTS_PATH, OUTPUT_DTS_PATH, rendered)
        if success:
            messagebox.showinfo("Success", f"DTS generated at {OUTPUT_DTS_PATH}")
        else:
            messagebox.showerror("Error", "Failed to inject device node into DTS")

if __name__ == "__main__":
    root = tk.Tk()
    app = DTSApp(root)
    root.mainloop()
