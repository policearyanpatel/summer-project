
import customtkinter as ctk
from tkinter import messagebox, filedialog
import pyperclip
from datetime import datetime

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class TemperatureConverterPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Temperature Converter Pro+")
        try:
            self.root.state("zoomed")
        except:
            self.root.geometry("1400x800")

        self.root.configure(fg_color="#F5F5F5")

        self.history = []
        self.values = []
        self.result_text = ""

        self.build_ui()
        self.update_clock()

    def build_ui(self):
        self.header = ctk.CTkLabel(
            self.root,
            text="🌡 TEMPERATURE CONVERTER PRO+ 🌡",
            font=("Segoe UI", 34, "bold"),
            text_color="#0F172A"
        )
        self.header.pack(pady=(15, 5))

        self.subtitle = ctk.CTkLabel(
            self.root,
            text="Convert Between Celsius • Fahrenheit • Kelvin",
            font=("Segoe UI", 14),
            text_color="#6B7280"
        )
        self.subtitle.pack()

        self.clock_label = ctk.CTkLabel(self.root, text="")
        self.clock_label.place(relx=0.97, rely=0.03, anchor="ne")

        self.main = ctk.CTkFrame(self.root, fg_color="#F5F5F5")
        self.main.pack(fill="both", expand=True, padx=15, pady=15)

        self.left = ctk.CTkFrame(self.main, fg_color="white", corner_radius=20)
        self.left.pack(side="left", fill="y", padx=10)

        ctk.CTkLabel(self.left, text="📜 Conversion History",
                     font=("Segoe UI", 20, "bold")).pack(pady=10)

        self.search = ctk.CTkEntry(self.left, placeholder_text="Search history")
        self.search.pack(fill="x", padx=10, pady=5)

        self.history_box = ctk.CTkTextbox(self.left, width=280, height=500)
        self.history_box.pack(padx=10, pady=10)

        ctk.CTkButton(self.left, text="📤 Export History",
                      command=self.export_history).pack(pady=10)

        self.center = ctk.CTkFrame(self.main, fg_color="white", corner_radius=20)
        self.center.pack(side="left", fill="both", expand=True, padx=10)

        ctk.CTkLabel(self.center, text="🔥 Converter Dashboard",
                     font=("Segoe UI", 24, "bold")).pack(pady=15)

        self.from_unit = ctk.CTkOptionMenu(self.center, values=["Celsius", "Fahrenheit", "Kelvin"])
        self.from_unit.pack(pady=8)

        self.to_unit = ctk.CTkOptionMenu(self.center, values=["Celsius", "Fahrenheit", "Kelvin"])
        self.to_unit.pack(pady=8)

        self.temp_entry = ctk.CTkEntry(self.center, width=350, placeholder_text="Enter temperature")
        self.temp_entry.pack(pady=15)

        preset = ctk.CTkFrame(self.center, fg_color="transparent")
        preset.pack(pady=5)

        for val in [0, 25, 37, 100]:
            ctk.CTkButton(
                preset, text=f"{val}°C", width=70,
                command=lambda v=val: self.set_preset(v)
            ).pack(side="left", padx=5)

        btns = ctk.CTkFrame(self.center, fg_color="transparent")
        btns.pack(pady=15)

        ctk.CTkButton(btns, text="⚡ Convert", command=self.convert).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="🔄 Swap", command=self.swap_units).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="🗑 Clear", command=self.clear).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="📋 Copy", command=self.copy_result).pack(side="left", padx=5)

        self.result_frame = ctk.CTkFrame(self.center, fg_color="white")
        self.result_frame.pack(fill="x", padx=25, pady=15)

        ctk.CTkLabel(self.result_frame, text="RESULT",
                     font=("Segoe UI", 18, "bold")).pack(pady=5)

        self.result_label = ctk.CTkLabel(
            self.result_frame,
            text="--",
            font=("Segoe UI", 54, "bold"),
            text_color="#2563EB"
        )
        self.result_label.pack()

        self.status_label = ctk.CTkLabel(
            self.result_frame,
            text="🌡 Waiting for Conversion",
            font=("Segoe UI", 16, "bold")
        )
        self.status_label.pack(pady=8)

        ctk.CTkLabel(self.center, text="🌡 Temperature Meter").pack()
        self.meter = ctk.CTkProgressBar(self.center, width=600)
        self.meter.pack(pady=10)
        self.meter.set(0)

        self.right = ctk.CTkFrame(self.main, fg_color="white", corner_radius=20)
        self.right.pack(side="right", fill="y", padx=10)

        ctk.CTkLabel(self.right, text="📊 Statistics",
                     font=("Segoe UI", 20, "bold")).pack(pady=10)

        self.total_lbl = ctk.CTkLabel(self.right, text="Total Conversions: 0")
        self.total_lbl.pack(pady=8)

        self.high_lbl = ctk.CTkLabel(self.right, text="Highest Temp: --")
        self.high_lbl.pack(pady=8)

        self.low_lbl = ctk.CTkLabel(self.right, text="Lowest Temp: --")
        self.low_lbl.pack(pady=8)

        self.avg_lbl = ctk.CTkLabel(self.right, text="Average Temp: --")
        self.avg_lbl.pack(pady=8)

        ctk.CTkLabel(
            self.root,
            text="Temperature Converter Pro+ | Internship Project",
            text_color="#6B7280"
        ).pack(side="bottom", pady=5)

    def update_clock(self):
        self.clock_label.configure(text="🕒 " + datetime.now().strftime("%I:%M:%S %p"))
        self.root.after(1000, self.update_clock)

    def set_preset(self, value):
        self.temp_entry.delete(0, "end")
        self.temp_entry.insert(0, str(value))

    def convert(self):
        try:
            temp = float(self.temp_entry.get())
        except:
            messagebox.showerror("Error", "Enter a valid number")
            return

        f = self.from_unit.get()
        t = self.to_unit.get()

        c = temp
        if f == "Fahrenheit":
            c = (temp - 32) * 5 / 9
        elif f == "Kelvin":
            c = temp - 273.15

        if t == "Celsius":
            result = c
            unit = "°C"
        elif t == "Fahrenheit":
            result = (c * 9 / 5) + 32
            unit = "°F"
        else:
            result = c + 273.15
            unit = "K"

        self.result_text = f"{result:.2f}{unit}"
        self.result_label.configure(text=self.result_text)

        if c < 0:
            status = "❄ Freezing"
            color = "#3B82F6"
        elif c < 25:
            status = "🌤 Cool"
            color = "#22C55E"
        elif c < 50:
            status = "☀ Warm"
            color = "#F59E0B"
        else:
            status = "🔥 Hot"
            color = "#EF4444"

        self.status_label.configure(text=status, text_color=color)
        self.result_label.configure(text_color=color)

        self.meter.set(min(max((c + 50) / 150, 0), 1))

        entry = f"{temp} {f} → {result:.2f} {t}"
        self.history.append(entry)
        self.history_box.insert("end", entry + "\n")

        self.values.append(c)
        self.update_stats()

    def update_stats(self):
        self.total_lbl.configure(text=f"Total Conversions: {len(self.values)}")
        self.high_lbl.configure(text=f"Highest Temp: {max(self.values):.2f}°C")
        self.low_lbl.configure(text=f"Lowest Temp: {min(self.values):.2f}°C")
        self.avg_lbl.configure(text=f"Average Temp: {sum(self.values)/len(self.values):.2f}°C")

    def swap_units(self):
        a = self.from_unit.get()
        b = self.to_unit.get()
        self.from_unit.set(b)
        self.to_unit.set(a)

    def clear(self):
        self.temp_entry.delete(0, "end")
        self.result_label.configure(text="--", text_color="#2563EB")
        self.status_label.configure(text="🌡 Waiting for Conversion")

    def copy_result(self):
        if self.result_text:
            pyperclip.copy(self.result_text)
            messagebox.showinfo("Copied", "Result copied to clipboard")

    def export_history(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.history))
        messagebox.showinfo("Success", "History exported")

if __name__ == "__main__":
    root = ctk.CTk()
    app = TemperatureConverterPro(root)
    root.mainloop()
