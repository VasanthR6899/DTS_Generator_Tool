
import os
import tkinter as tk
from tkinter import ttk
from baseboards import list_folders, list_baseboards  # Assume these return list[str]

KERNEL_PATH = "/home/vasanth/Desktop/personal/linux-at91"

class DTSApp:
    def __init__(self, root):
        self.root = root
        root.title("DTS Tool")
        root.geometry("600x400")

        self.board_var = tk.StringVar()
        self.board_file_var = tk.StringVar()

        # Label for manufacturer
        ttk.Label(self.root, text="Select the baseboard Manufacturer:", font=("Arial", 12, "bold")).pack(pady=10)

        folder_frame = ttk.Frame(self.root)
        folder_frame.pack()

        manufacturers = list_folders(os.path.join(KERNEL_PATH, "arch/arm/boot/dts"))
        self.manufacturer_combo = ttk.Combobox(folder_frame, values=manufacturers, textvariable=self.board_var, state="readonly")
        self.manufacturer_combo.pack()
        self.manufacturer_combo.bind("<<ComboboxSelected>>", self.manufacturer_selected)

        # Label for board name
        ttk.Label(self.root, text="Select the baseboard name:", font=("Arial", 12, "bold")).pack(pady=10)

        board_frame = ttk.Frame(self.root)
        board_frame.pack()

        self.board_name_combo = ttk.Combobox(board_frame, textvariable=self.board_file_var, state="readonly")
        self.board_name_combo.pack()

    def manufacturer_selected(self, event):
        selected_manufacturer = self.board_var.get()
        baseboard_path = os.path.join(KERNEL_PATH, "arch/arm/boot/dts", selected_manufacturer)

        # Get DTS files in selected folder
        boards = list_baseboards(baseboard_path)
        self.board_name_combo['values'] = boards

if __name__ == "__main__":
    root = tk.Tk()
    app = DTSApp(root)
    root.mainloop()
