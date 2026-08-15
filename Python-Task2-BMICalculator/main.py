from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox, ttk
from database import create_database, save_record, get_all_records
from bmi import calculate_bmi, get_category



def calculate():
    try:
        user_name = name_entry.get().strip()
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if not user_name:
            messagebox.showerror(
                "Invalid Input",
                "Please enter your name."
            )
            return

        if weight <= 0 or height <= 0:
            messagebox.showerror(
                "Invalid Input",
                "Weight and height must be positive values."
            )
            return

        bmi = calculate_bmi(weight, height)
        category = get_category(bmi)

        if category == "Normal":
            result_color = "green"
        elif category == "Obese":
            result_color = "red"
        else:
            result_color = "orange"

        result_label.config(
            text=f"BMI: {bmi}\nCategory: {category}",
            fg=result_color
        )

        save_record(
            user_name,
            weight,
            height,
            bmi,
            category
        )

        messagebox.showinfo(
            "Success",
            "BMI record saved successfully."
        )

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter numeric values only."
        )

def show_history():
    history_window = tk.Toplevel(root)

    history_window.title("BMI History")
    history_window.geometry("800x400")

    title = tk.Label(
        history_window,
        text="BMI History",
        font=("Arial", 18, "bold")
    )
    title.pack(pady=10)

    columns = (
        "Name",
        "Weight",
        "Height",
        "BMI",
        "Category",
        "Date & Time"
    )

    table = ttk.Treeview(
        history_window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        table.heading(column, text=column)
        table.column(column, width=120)

    table.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    records = get_all_records()

    for record in records:
        table.insert("", "end", values=record)

def show_bmi_graph():
    records = get_all_records()

    if not records:
        messagebox.showinfo(
            "BMI Graph",
            "No BMI records available."
        )
        return

    bmi_values = []
    dates = []

    # Reverse so graph shows oldest → newest
    for record in reversed(records):
        bmi_values.append(record[3])
        dates.append(record[5])

    graph_window = tk.Toplevel(root)
    graph_window.title("BMI Trend")
    graph_window.geometry("800x500")

    figure = Figure(figsize=(8, 4), dpi=100)

    axis = figure.add_subplot(111)

    axis.plot(
        dates,
        bmi_values,
        marker="o"
    )

    axis.set_title("BMI Trend")
    axis.set_xlabel("Date & Time")
    axis.set_ylabel("BMI")

    axis.tick_params(
        axis="x",
        rotation=45
    )

    figure.tight_layout()

    canvas = FigureCanvasTkAgg(
        figure,
        master=graph_window
    )

    canvas.draw()

    canvas.get_tk_widget().pack(
        fill=tk.BOTH,
        expand=True
    )

    
# Main window
create_database()
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("500x600")
root.resizable(False, True)


# Title
title_label = tk.Label(
    root,
    text="BMI Calculator",
    font=("Arial", 22, "bold")
)
title_label.pack(pady=20)

name_label = tk.Label(
    root,
    text="User Name",
    font=("Arial", 12)
)
name_label.pack()

name_entry = tk.Entry(
    root,
    width=25,
    font=("Arial", 12)
)
name_entry.pack(pady=5)

# Weight
weight_label = tk.Label(
    root,
    text="Weight (kg)",
    font=("Arial", 12)
)
weight_label.pack()

weight_entry = tk.Entry(
    root,
    width=25,
    font=("Arial", 12)
)
weight_entry.pack(pady=5)


# Height
height_label = tk.Label(
    root,
    text="Height (m)",
    font=("Arial", 12)
)
height_label.pack()

height_entry = tk.Entry(
    root,
    width=25,
    font=("Arial", 12)
)
height_entry.pack(pady=5)


# Calculate button
calculate_button = tk.Button(
    root,
    text="Calculate BMI",
    command=calculate,
    font=("Arial", 12)
)
calculate_button.pack(pady=20)

history_button = tk.Button(
    root,
    text="View BMI History",
    command=show_history,
    font=("Arial", 12)
)

history_button.pack(pady=5)

graph_button = tk.Button(
    root,
    text="View BMI Trend",
    command=show_bmi_graph,
    font=("Arial", 12)
)

graph_button.pack(pady=5)

# Result
result_label = tk.Label(
    root,
    text="Enter your details",
    font=("Arial", 16, "bold"),
    justify="center"
)
result_label.pack(pady=20)

root.mainloop()