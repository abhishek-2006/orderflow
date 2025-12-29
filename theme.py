import tkinter as tk

# Default Light Theme
THEME = {
    "BG": "#f5f5f5",
    "TEXT": "#2c3e50",
    "BOX": "#ffffff"
}

def enable_dark():
    THEME["BG"] = "#1e1e1e"
    THEME["TEXT"] = "#ffffff"
    THEME["BOX"] = "#2b2b2b"

def enable_light():
    THEME["BG"] = "#f5f5f5"
    THEME["TEXT"] = "#2c3e50"
    THEME["BOX"] = "#ffffff"

def styled_button(master, text, command, color, hover_color):
    return tk.Button(
        master, text=text, command=command,
        bg=color, fg="white",
        activebackground=hover_color, activeforeground="white",
        relief="flat", font=("Segoe UI", 10, "bold"),
        padx=12, pady=6, cursor="hand2"
    )

def styled_label(master, text, size=11, bold=False):
    font_style = ("Segoe UI", size, "bold" if bold else "normal")
    return tk.Label(master, text=text, fg=THEME["TEXT"], bg=THEME["BG"], font=font_style)
