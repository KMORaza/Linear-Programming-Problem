import tkinter as tk
from tkinter import messagebox
from pulp import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
def solve_lp():
    prob = LpProblem("Maximize_Profit", LpMaximize)
    obj_coefficients = []
    for var in obj_vars:
        try:
            obj_coefficients.append(float(var.get()))
        except ValueError:
            messagebox.showerror("Error", "Invalid input for objective function coefficients")
            return
    variables = [LpVariable(f"x{i+1}", lowBound=0) for i in range(len(obj_coefficients))]
    prob += lpSum([obj_coefficients[i] * variables[i] for i in range(len(obj_coefficients))]), "Profit"
    constraints_coeffs = []
    bounds = []
    for i in range(len(constraint_entries)):
        coefficients = []
        for entry in constraint_entries[i]:
            try:
                coefficients.append(float(entry.get()))
            except ValueError:
                messagebox.showerror("Error", f"Invalid input for constraint {i+1} coefficients")
                return
        bound = bound_entries[i].get()
        try:
            bounds.append(float(bound))
        except ValueError:
            messagebox.showerror("Error", f"Invalid input for constraint {i+1} bound")
            return
        constraints_coeffs.append(coefficients)
        prob += lpSum([coefficients[j] * variables[j] for j in range(len(obj_coefficients))]) <= bounds[-1]
    prob.solve()
    x_values = np.linspace(0, 10, 400)
    plt.figure(figsize=(8, 6))
    for i in range(len(constraints_coeffs)):
        y_values = [(bounds[i] - constraints_coeffs[i][0] * x) / constraints_coeffs[i][1] for x in x_values]
        plt.plot(x_values, y_values, label=f"Constraint {i+1}", linestyle='--')
    plt.fill_between(x_values, 0, 10, color='gray', alpha=0.3, label='Feasible Region')
    z_values = [(value(prob.objective) - obj_coefficients[0] * x) / obj_coefficients[1] for x in x_values]
    plt.plot(x_values, z_values, label='Objective Function')
    plt.xlabel('x', fontname='Verdana', fontsize=10, color='#FFFFCC')
    plt.ylabel('y', fontname='Verdana', fontsize=10, color='#FFFFCC')
    plt.title('Feasible Region and Objective Function', fontname='Consolas', fontsize=12, color='#000000')
    plt.legend()
    plt.grid(True)
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=3, rowspan=6)
    status_label.config(text="Status: " + LpStatus[prob.status], font=('Verdana', 10), fg='#FFFFCC', bg='black')
    values_label.config(text="Optimal values:\n" + '\n'.join([v.name + " = " + str(v.varValue) for v in prob.variables()]), font=('Verdana', 10), fg='#FFFFCC', bg='black')
    obj_value_label.config(text="Optimal value of the objective function: " + str(value(prob.objective)), font=('Verdana', 10), fg='#FFFFCC', bg='black')
root = tk.Tk()
root.title("LPP Solver")
root.configure(bg='black')
root.resizable(False, False)
obj_vars = []
obj_label = tk.Label(root, text="Objective function coefficients:", font=('Verdana', 10), fg='#FFFFCC', bg='black')
obj_label.grid(row=0, column=0)
for i in range(2):
    obj_var = tk.Entry(root, width=5, bg='#003366', fg='white', insertbackground='#FFFFCC', relief='flat', highlightbackground='#FFFFCC', highlightthickness=1,)
    obj_var.grid(row=0, column=i+1)
    obj_vars.append(obj_var)
constraint_entries = []
bound_entries = []
constraint_label = tk.Label(root, text="Constraints (A*x + B*y ≤ C):", font=('Verdana', 10), fg='#FFFFCC', bg='black')
constraint_label.grid(row=1, column=0)
for i in range(2):
    constraint_vars = []
    for j in range(2):
        constraint_var = tk.Entry(root, width=5, bg='#003366', fg='#FFFFCC', insertbackground='#FFFFCC', relief='flat', highlightbackground='#FFFFCC', highlightthickness=1)
        constraint_var.grid(row=i+1, column=j+1)
        constraint_vars.append(constraint_var)
    constraint_entries.append(constraint_vars)
    bound_entry = tk.Entry(root, width=5, bg='#003366', fg='#FFFFCC', insertbackground='#FFFFCC', relief='flat', highlightbackground='#FFFFCC', highlightthickness=1)
    bound_entry.grid(row=i+1, column=3)
    bound_entries.append(bound_entry)
solve_button = tk.Button(root, text="Solve", command=solve_lp, font=('Verdana', 10), bg='#00CCCC', fg='#000000')
solve_button.grid(row=3, column=0, columnspan=3)
status_label = tk.Label(root, text="", font=('Verdana', 10), fg='#FFFFCC', bg='black')
status_label.grid(row=4, column=0, columnspan=3)
values_label = tk.Label(root, text="", font=('Verdana', 10), fg='#FFFFCC', bg='black')
values_label.grid(row=5, column=0, columnspan=3)
obj_value_label = tk.Label(root, text="", font=('Verdana', 10), fg='#FFFFCC', bg='black')
obj_value_label.grid(row=6, column=0, columnspan=3)
def on_closing():
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
