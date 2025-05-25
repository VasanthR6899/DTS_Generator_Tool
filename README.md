📟 DTS Generator Tool

A graphical Python-based utility to help embedded Linux developers generate and inject device tree snippets for custom sensor nodes into an existing baseboard DTS (Device Tree Source) file.

This tool is especially helpful for quickly customizing DTS files based on hardware pin configurations, saving time during board bring-up or peripheral integration in embedded Linux environments.
🛠 Features

    ✅ Tkinter-based GUI – Simple and intuitive interface for developers.

    🔍 Auto-detect baseboard folders under the Linux kernel source.

    📂 Select manufacturer & board files from dropdowns.

    ✏️ Input CS, IRQ, and Reset pin names.

    📄 Injects a rendered DTS snippet into the selected baseboard .dts.

    📑 Displays optional sensor properties parsed from a YAML file.

    🧩 Jinja2 templating allows reusable sensor node templates.