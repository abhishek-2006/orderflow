import tkinter as tk
from logic import *
from tkinter import messagebox
from theme import THEME, styled_button, styled_label, enable_dark, enable_light

def build_ui(root):
    root.title("🍔 Restaurant Manager")
    root.geometry("900x600")

    # --- Theme Application ---
    def apply_theme():
        root.config(bg=THEME["BG"])
        header.config(bg=THEME["BG"], fg=THEME["TEXT"])
        input_container.config(bg=THEME["BG"])
        main_content.config(bg=THEME["BG"])
        
        # Style the LabelFrames
        for frame in [queue_frame, history_frame]:
            frame.config(bg=THEME["BG"], fg=THEME["TEXT"], font=("Segoe UI", 10, "bold"))

        queue_display.config(bg=THEME["BOX"], fg=THEME["TEXT"], insertbackground=THEME["TEXT"])
        stack_display.config(bg=THEME["BOX"], fg=THEME["TEXT"], insertbackground=THEME["TEXT"])

    # --- Header ---
    header_frame = tk.Frame(root, pady=20)
    header_frame.pack(fill="x")
    header = styled_label(root, "RESTAURANT ORDER SYSTEM", 18, True)
    header.pack()

    # --- Input Section ---
    input_container = tk.Frame(root, padx=20, pady=10)
    input_container.pack(fill="x")
    
    input_inner = tk.Frame(input_container) # Centering helper
    input_inner.pack()

    styled_label(input_inner, "Customer:").grid(row=0, column=0, padx=5)
    customer_entry = tk.Entry(input_inner, width=15, font=("Segoe UI", 11))
    customer_entry.grid(row=0, column=1, padx=5)
    customer_entry.focus_set()

    styled_label(input_inner, "Order Items:").grid(row=0, column=2, padx=5)
    items_entry = tk.Entry(input_inner, width=25, font=("Segoe UI", 11))
    items_entry.grid(row=0, column=3, padx=5)

    def add_order(event=None): # Added event support for Enter key
        if not customer_entry.get() or not items_entry.get():
            toast(root, "Please fill all fields", "warning")
            return
        add_order_logic(customer_entry.get(), items_entry.get())
        customer_entry.delete(0, tk.END)
        items_entry.delete(0, tk.END)
        customer_entry.focus_set()
        toast(root, "Order added to queue", "success")
        update_display()
        update_button_states()

    root.bind('<Return>', add_order) # Press Enter to add
    styled_button(input_inner, "➕ Add Order", add_order, "#27ae60", "#1e8449").grid(row=0, column=4, padx=10)

    # --- Main Display Area ---
    main_content = tk.Frame(root, padx=20, pady=10)
    main_content.pack(expand=True, fill="both")

    # Left Column: Active Queue
    queue_frame = tk.LabelFrame(main_content, text=" Pending Orders (FIFO) ", padx=10, pady=10)
    queue_frame.pack(side="left", expand=True, fill="both", padx=10)

    queue_display = tk.Text(queue_frame, height=12, width=35, state="disabled", font=("Consolas", 10))
    queue_display.pack(pady=10)

    btn_grid_left = tk.Frame(queue_frame)
    btn_grid_left.pack()
    serve_btn = styled_button(btn_grid_left, "✅ Serve Next", lambda: serve(),"#f39c12", "#d68910")
    serve_btn.pack(side="left", padx=5)
    undo_btn = styled_button(btn_grid_left, "↩️ Undo Serve", lambda: undo(),"#9b59b6", "#8e44ad")
    undo_btn.pack(side="left", padx=5)

    # Right Column: Order History
    history_frame = tk.LabelFrame(main_content, text=" Recent History (LIFO) ", padx=10, pady=10)
    history_frame.pack(side="right", expand=True, fill="both", padx=10)

    stack_display = tk.Text(history_frame, height=12, width=35, state="disabled", font=("Consolas", 10))
    stack_display.pack(pady=10)

    btn_grid_right = tk.Frame(history_frame)
    btn_grid_right.pack()
    export_btn = styled_button(btn_grid_right, "📊 Export CSV", lambda: export(),"#3498db", "#2980b9")
    export_btn.pack(side="left", padx=5)
    clear_btn = styled_button(btn_grid_right, "🗑️ Clear All", lambda: clear_all(),"#e74c3c", "#c0392b")
    clear_btn.pack(side="left", padx=5)

    # --- Footer / Settings ---
    footer = tk.Frame(root, pady=10)
    footer.pack(fill="x", side="bottom")

    styled_button(footer, "🌙 Dark", lambda: [enable_dark(), apply_theme()], "#333", "#111").pack(side="left", padx=20)
    styled_button(footer, "☀️ Light", lambda: [enable_light(), apply_theme()], "#32E65E", "#1CC74A").pack(side="right", padx=20)

    # --- Logic Connectors ---
    def update_display():
        for disp, func in [(queue_display, get_queue), (stack_display, get_stack)]:
            disp.config(state="normal")
            disp.delete(1.0, tk.END)
            data = func()
            disp.insert(tk.END, "\n".join(data) if data else "--- No orders ---")
            disp.config(state="disabled")

    def serve():
        serve_order_logic()
        toast(root, "Order moved to history", "success")
        update_display()
        update_button_states()
    
    def undo():
        undo_served_logic()
        toast(root, "Order returned to queue", "info")
        update_display()
        update_button_states()

    def clear_all():
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all data?"):
            clear_all_logic()
            toast(root, "System Reset", "warning")
            update_display()
            update_button_states

    def export():
        export_report_logic()
        toast(root, "Report saved to file", "success")
        update_button_states

    def toast(root, msg, type="info", duration=2000):
        colors = {
            "success": {"bg": "#2ECC71", "fg": "black"},   # Green
            "error":   {"bg": "#E74C3C", "fg": "white"},   # Red
            "info":    {"bg": "#3498DB", "fg": "white"},   # Blue
            "warning": {"bg": "#F1C40F", "fg": "black"},   # Yellow
        }

        color = colors.get(type, colors["info"])

        toast_win = tk.Toplevel(root)
        toast_win.overrideredirect(True)
        toast_win.attributes("-topmost", True)

        frame = tk.Frame(
            toast_win,
            bg=color["bg"],
            padx=16,
            pady=10,
            highlightthickness=0,
            bd=0
        )
        frame.pack()

        label = tk.Label(
            frame,
            text=msg,
            fg=color["fg"],
            bg=color["bg"],
            font=("Segoe UI", 10, "bold")
        )
        label.pack()

        # Position bottom-center
        toast_win.update_idletasks()
        x = root.winfo_x() + (root.winfo_width() // 2) - (toast_win.winfo_width() // 2)
        y = root.winfo_y() + root.winfo_height() - 90
        toast_win.geometry(f"+{x}+{y}")

        # Fade animation
        toast_win.attributes("-alpha", 0.0)
        fade_steps = 10

        def fade_in(step=0):
            if step <= fade_steps:
                toast_win.attributes("-alpha", step / fade_steps)
                toast_win.after(18, fade_in, step + 1)

        def fade_out(step=fade_steps):
            if step >= 0:
                toast_win.attributes("-alpha", step / fade_steps)
                toast_win.after(18, fade_out, step - 1)
            else:
                toast_win.destroy()

        fade_in()
        toast_win.after(duration, fade_out)

    def update_button_states():
        q = get_queue()
        s = get_stack()

        # Serve only if queue has data
        serve_btn.config(state="normal" if q else "disabled")

        # Undo only if history has data
        undo_btn.config(state="normal" if s else "disabled")

        # Clear only if something exists
        clear_btn.config(
            state="normal" if (q or s) else "disabled"
        )

    update_display()
    apply_theme()