import tkinter as tk
from tkinter import ttk, filedialog

length_units = {'Meter': 1, 'Kilometer': 1000, 'Centimeter': 0.01, 'Mile': 1609.34}
weight_units = {'Gram': 1, 'Kilogram': 1000, 'Pound': 453.592}
temperature_units = ['Celsius', 'Fahrenheit', 'Kelvin']

history = []

def convert():
    try:
        val = float(value_entry.get())
        cat = cat_combo.get()
        from_u, to_u = from_combo.get(), to_combo.get()
        if cat == "Length":
            res = val * length_units[from_u] / length_units[to_u]
        elif cat == "Weight":
            res = val * weight_units[from_u] / weight_units[to_u]
        else:
            c = (val if from_u == "Celsius" else (val-32)*5/9 if from_u == "Fahrenheit" else val-273.15)
            res = c if to_u == "Celsius" else c*9/5+32 if to_u == "Fahrenheit" else c+273.15
        r = f"{val} {from_u} = {res:.2f} {to_u}"
        result_var.set(r)
        history_list.insert('end', r)
        history.append(r)
    except Exception:
        result_var.set("Invalid input!")

def update_units(_=None):
    cat = cat_combo.get()
    units = list(length_units) if cat=="Length" else list(weight_units) if cat=="Weight" else temperature_units
    from_combo['values'] = to_combo['values'] = units
    from_combo.set(units[0])
    to_combo.set(units[1])

def clear_history():
    history_list.delete(0, 'end')
    history.clear()

def save_history():
    filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text Files", "*.txt")],
                                            title="Save History As")
    if filename:
        with open(filename, 'w') as f:
            for item in history:
                f.write(item + '\n')

def view_history():
    win = tk.Toplevel(root)
    win.title("View History")
    tk.Label(win, text="Conversion History:").pack()
    history_box = tk.Listbox(win, width=40, height=12)
    history_box.pack(padx=8, pady=8)
    for item in history:
        history_box.insert('end', item)
    tk.Button(win, text="Close", command=win.destroy).pack(pady=5)

root = tk.Tk()
root.title("Unit Converter")

tk.Label(root, text="Value:").grid(row=0, column=0)
value_entry = tk.Entry(root)
value_entry.grid(row=0, column=1)

tk.Label(root, text="Category:").grid(row=1, column=0)
cat_combo = ttk.Combobox(root, values=["Length","Weight","Temperature"], state='readonly')
cat_combo.grid(row=1, column=1)
cat_combo.set("Length")
cat_combo.bind("<<ComboboxSelected>>", update_units)

from_combo = ttk.Combobox(root, state='readonly')
from_combo.grid(row=2, column=1)
to_combo = ttk.Combobox(root, state='readonly')
to_combo.grid(row=3, column=1)

tk.Label(root, text="From:").grid(row=2, column=0)
tk.Label(root, text="To:").grid(row=3, column=0)

result_var = tk.StringVar()
tk.Label(root, textvariable=result_var).grid(row=4, columnspan=2)

tk.Button(root, text="Convert", command=convert).grid(row=5, columnspan=2)
tk.Button(root, text="Clear History", command=clear_history).grid(row=6, column=0)
tk.Button(root, text="Save History", command=save_history).grid(row=6, column=1)
tk.Button(root, text="View History", command=view_history).grid(row=7, column=0, columnspan=2)

history_list = tk.Listbox(root, width=36, height=6)
history_list.grid(row=8, column=0, columnspan=2)

update_units()
root.mainloop()
