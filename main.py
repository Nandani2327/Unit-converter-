import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# --- Data dictionaries for categories ---
length_units = {
    'Meter': 1,
    'Kilometer': 1000,
    'Centimeter': 0.01,
    'Millimeter': 0.001,
    'Mile': 1609.34,
    'Yard': 0.9144,
    'Foot': 0.3048,
    'Inch': 0.0254
}
weight_units = {
    'Gram': 1,
    'Kilogram': 1000,
    'Milligram': 0.001,
    'Ton': 1e6,
    'Pound': 453.592,
    'Ounce': 28.3495
}
temperature_units = ['Celsius', 'Fahrenheit', 'Kelvin', 'Rankine']
area_units = {
    'Square Meter': 1,
    'Square Kilometer': 1e6,
    'Square Centimeter': 0.0001,
    'Square Millimeter': 0.000001,
    'Square Mile': 2.59e6,
    'Square Yard': 0.836127,
    'Square Foot': 0.092903,
    'Square Inch': 0.00064516,
    'Hectare': 10000,
    'Acre': 4046.86
}
volume_units = {
    'Cubic Meter': 1,
    'Liter': 0.001,
    'Milliliter': 0.000001,
    'Cubic Centimeter': 0.000001,
    'Cubic Inch': 0.0000163871,
    'Cubic Foot': 0.0283168,
    'Cubic Yard': 0.764555,
    'US Gallon': 0.00378541,
    'Imperial Gallon': 0.00454609,
    'Quart': 0.000946353,
    'Pint': 0.000473176
}
speed_units = {
    'Meter/Second': 1,
    'Kilometer/Hour': 0.277778,
    'Mile/Hour': 0.44704,
    'Foot/Second': 0.3048,
    'Knot': 0.514444
}
time_units = {
    'Second': 1,
    'Minute': 60,
    'Hour': 3600,
    'Day': 86400,
    'Week': 604800
}

# --- Conversion functions ---
def convert_length(val, from_unit, to_unit):
    return val * length_units[from_unit] / length_units[to_unit]

def convert_weight(val, from_unit, to_unit):
    return val * weight_units[from_unit] / weight_units[to_unit]

def convert_temperature(val, from_unit, to_unit):
    if from_unit == 'Celsius':
        c = val
    elif from_unit == 'Fahrenheit':
        c = (val - 32) * 5/9
    elif from_unit == 'Kelvin':
        c = val - 273.15
    elif from_unit == 'Rankine':
        c = (val - 491.67) * 5/9
    else:
        raise ValueError("Unsupported temperature unit")
    if to_unit == 'Celsius':
        return c
    elif to_unit == 'Fahrenheit':
        return c * 9/5 + 32
    elif to_unit == 'Kelvin':
        return c + 273.15
    elif to_unit == 'Rankine':
        return (c + 273.15) * 9/5
    else:
        raise ValueError("Unsupported temperature unit")

def convert_area(val, from_unit, to_unit):
    return val * area_units[from_unit] / area_units[to_unit]

def convert_volume(val, from_unit, to_unit):
    return val * volume_units[from_unit] / volume_units[to_unit]

def convert_speed(val, from_unit, to_unit):
    return val * speed_units[from_unit] / speed_units[to_unit]

def convert_time(val, from_unit, to_unit):
    return val * time_units[from_unit] / time_units[to_unit]

# --- GUI Setup & Logic ---
class UnitConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ultimate Unit Converter")
        self.geometry("600x400")
        self.configure(bg="#f5f5f5")
        self.dark_mode = False
        self.create_widgets()
        self.history = []

    def create_widgets(self):
        # Input fields and dropdowns
        self.label_val = tk.Label(self, text="Value:", bg="#f5f5f5")
        self.label_val.grid(row=0, column=0, padx=8, pady=8, sticky="e")
        self.entry_value = tk.Entry(self)
        self.entry_value.grid(row=0, column=1, padx=8, pady=8)
        self.label_cat = tk.Label(self, text="Category:", bg="#f5f5f5")
        self.label_cat.grid(row=1, column=0, padx=8, pady=8, sticky="e")

        self.cat_list = ["Length", "Weight", "Temperature", "Area", "Volume", "Speed", "Time"]
        self.combo_category = ttk.Combobox(self, values=self.cat_list, state='readonly', width=16)
        self.combo_category.grid(row=1, column=1, padx=8, pady=8)
        self.combo_category.current(0)
        self.combo_category.bind("<<ComboboxSelected>>", self.update_units)

        self.label_from = tk.Label(self, text="From Unit:", bg="#f5f5f5")
        self.label_from.grid(row=2, column=0, padx=8, pady=8, sticky="e")
        self.combo_from = ttk.Combobox(self, state='readonly', width=16)
        self.combo_from.grid(row=2, column=1, padx=8, pady=8)

        self.label_to = tk.Label(self, text="To Unit:", bg="#f5f5f5")
        self.label_to.grid(row=3, column=0, padx=8, pady=8, sticky="e")
        self.combo_to = ttk.Combobox(self, state='readonly', width=16)
        self.combo_to.grid(row=3, column=1, padx=8, pady=8)

        # Buttons
        self.btn_convert = tk.Button(self, text="Convert", command=self.convert, bg="#388e3c", fg="white", width=12)
        self.btn_convert.grid(row=4, column=0, columnspan=2, pady=8)

        self.btn_clear = tk.Button(self, text="Clear History", command=self.clear_history, bg="#d32f2f", fg="white", width=12)
        self.btn_clear.grid(row=5, column=0, pady=8)

        self.btn_export = tk.Button(self, text="Export History", command=self.export_history, bg="#1976d2", fg="white", width=12)
        self.btn_export.grid(row=5, column=1, pady=8)

        self.btn_theme = tk.Button(self, text="Dark Mode", command=self.toggle_theme, bg="#212121", fg="white", width=12)
        self.btn_theme.grid(row=6, column=0, pady=8)

        # Result and history
        self.label_result = tk.Label(self, text="", font=("Arial", 12, "bold"), fg="#1a237e", bg="#f5f5f5")
        self.label_result.grid(row=4, column=2, rowspan=2, padx=8, pady=8, sticky="n")
        self.history_box = tk.Listbox(self, width=40, height=12)
        self.history_box.grid(row=0, column=2, rowspan=4, padx=8, pady=8)
        self.update_units()

    def update_units(self, event=None):
        cat = self.combo_category.get()
        if cat == "Length":
            units = list(length_units.keys())
        elif cat == "Weight":
            units = list(weight_units.keys())
        elif cat == "Temperature":
            units = temperature_units
        elif cat == "Area":
            units = list(area_units.keys())
        elif cat == "Volume":
            units = list(volume_units.keys())
        elif cat == "Speed":
            units = list(speed_units.keys())
        elif cat == "Time":
            units = list(time_units.keys())
        else:
            units = []
        self.combo_from['values'] = units
        self.combo_to['values'] = units
        if units:
            self.combo_from.current(0)
            self.combo_to.current(1 if len(units) > 1 else 0)

    def convert(self):
        try:
            val = float(self.entry_value.get())
            from_unit = self.combo_from.get()
            to_unit = self.combo_to.get()
            cat = self.combo_category.get()
            if not from_unit or not to_unit:
                raise ValueError("Select both units.")
            if cat == "Length":
                result = convert_length(val, from_unit, to_unit)
            elif cat == "Weight":
                result = convert_weight(val, from_unit, to_unit)
            elif cat == "Temperature":
                result = convert_temperature(val, from_unit, to_unit)
            elif cat == "Area":
                result = convert_area(val, from_unit, to_unit)
            elif cat == "Volume":
                result = convert_volume(val, from_unit, to_unit)
            elif cat == "Speed":
                result = convert_speed(val, from_unit, to_unit)
            elif cat == "Time":
                result = convert_time(val, from_unit, to_unit)
            else:
                raise ValueError("Invalid category.")
            disp = f"{val} {from_unit} = {result:.4f} {to_unit}"
            self.label_result.config(text=disp)
            self.history.append(disp)
            self.history_box.insert(tk.END, disp)
            self.history_box.see(tk.END)
        except Exception as e:
            messagebox.showerror("Conversion Error", str(e))

    def clear_history(self):
        self.history = []
        self.history_box.delete(0, tk.END)

    def export_history(self):
        if not self.history:
            messagebox.showinfo("Export", "No history to export.")
            return
        file = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv")])
        if file:
            with open(file, "w") as f:
                for line in self.history:
                    f.write(line + "\n")
            messagebox.showinfo("Export", f"History saved to {file}")

    def toggle_theme(self):
        if self.dark_mode:
            # Light mode
            bg, fg = "#f5f5f5", "#1a237e"
            self.dark_mode = False
            self.btn_theme.config(text="Dark Mode")
        else:
            # Dark mode
            bg, fg = "#212121", "#ffeb3b"
            self.dark_mode = True
            self.btn_theme.config(text="Light Mode")
        # Apply theme
        self.configure(bg=bg)
        widgets = [self.label_val, self.label_cat, self.label_from, self.label_to, self.label_result]
        for w in widgets:
            w.config(bg=bg, fg=fg)
        self.history_box.config(bg="#333", fg="#fff" if self.dark_mode else "#000")
        for btn in [self.btn_convert, self.btn_clear, self.btn_export, self.btn_theme]:
            btn.config(bg="#333" if self.dark_mode else btn["bg"], fg="#fff" if self.dark_mode else btn["fg"])

if __name__ == "__main__":
    app = UnitConverterApp()
    app.mainloop()