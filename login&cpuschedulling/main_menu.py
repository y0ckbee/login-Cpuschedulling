import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import fcfs_algorithm
import srtf_algorithm
import round_robin_algorithm
import np_priosched_algorithm
import pre_priosched_algorithm
import sjf_algorithm

# =========================
# BUTTON STYLE
# =========================
BUTTON_STYLE = {
    "bg": "#add8e6",   # light blue
    "width": 30,
    "height": 2
}


# =========================
# NON-PREEMPTIVE FUNCTIONS
# =========================
def run_fcfs():
    fcfs_algorithm.fcfs_gui()

def run_sjf_np():
    sjf_algorithm.sjf_gui()

def run_priority_np():
    np_priosched_algorithm.priority_gui()


# =========================
# PREEMPTIVE FUNCTIONS
# =========================
def run_sjf_preemptive():
    srtf_algorithm.srtf_gui()
    
def run_priority_preemptive():
    pre_priosched_algorithm.priority_preemptive_gui()
def run_rr():
    round_robin_algorithm.round_robin_gui()


# =========================
# MAIN MENU (TABBED GUI)
# =========================
def open_main_menu():
    menu = tk.Toplevel()
    menu.title("CPU Scheduling Simulator")
    menu.geometry("450x400")

    title = tk.Label(menu, text="CPU SCHEDULING SIMULATOR",
                     font=("Arial", 14, "bold"))
    title.pack(pady=10)

    notebook = ttk.Notebook(menu)
    notebook.pack(expand=True, fill="both")


    # =========================
    # NON-PREEMPTIVE TAB
    # =========================
    non_preemptive_tab = tk.Frame(notebook)
    notebook.add(non_preemptive_tab, text="Non-Preemptive")

    tk.Label(non_preemptive_tab, text="Non-Preemptive Algorithms",
             font=("Arial", 12, "bold")).pack(pady=10)

    tk.Button(non_preemptive_tab, text="First Come First Serve",
              command=run_fcfs, **BUTTON_STYLE).pack(pady=5)

    tk.Button(non_preemptive_tab, text="Shortest Job First",
              command=run_sjf_np, **BUTTON_STYLE).pack(pady=5)

    tk.Button(non_preemptive_tab, text="Priority Scheduling",
              command=run_priority_np, **BUTTON_STYLE).pack(pady=5)


    # =========================
    # PREEMPTIVE TAB
    # =========================
    preemptive_tab = tk.Frame(notebook)
    notebook.add(preemptive_tab, text="Preemptive")

    tk.Label(preemptive_tab, text="Preemptive Algorithms",
             font=("Arial", 12, "bold")).pack(pady=10)

    tk.Button(preemptive_tab, text="Shortest Remaining Time First",
              command=run_sjf_preemptive, **BUTTON_STYLE).pack(pady=5)

    tk.Button(preemptive_tab, text="Priority Scheduling",
              command=run_priority_preemptive, **BUTTON_STYLE).pack(pady=5)

    tk.Button(preemptive_tab, text="Round Robin",
              command=run_rr, **BUTTON_STYLE).pack(pady=5)


    # =========================
    # EXIT
    # =========================
    tk.Button(menu, text="Exit", bg="red", fg="white",
              width=30, height=2,
              command=menu.destroy).pack(pady=10)


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_main_menu()
    root.mainloop()