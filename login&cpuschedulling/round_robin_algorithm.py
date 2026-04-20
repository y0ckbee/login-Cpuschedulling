import tkinter as tk
from tkinter import messagebox

# =========================
# BUTTON STYLE
# =========================
BUTTON_STYLE = {
    "bg": "#add8e6",
    "width": 30,
    "height": 2
}

def round_robin_gui():

    window = tk.Toplevel()
    window.title("Round Robin Scheduling")
    window.geometry("650x650")

    arrival_entries = []
    burst_entries = []

    # =========================
    # PROCESS COUNT
    # =========================
    tk.Label(window, text="Enter Process Count").pack()

    process_entry = tk.Entry(window)
    process_entry.pack()

    input_frame = tk.Frame(window)
    input_frame.pack(pady=10)

    # Time Quantum
    tk.Label(window, text="Time Quantum").pack()
    quantum_entry = tk.Entry(window)
    quantum_entry.pack(pady=5)

    output_box = tk.Text(window, height=18, width=75)
    output_box.pack(pady=10)

    # =========================
    # GENERATE FIELDS
    # =========================
    def generate_fields():
        for widget in input_frame.winfo_children():
            widget.destroy()

        arrival_entries.clear()
        burst_entries.clear()

        try:
            process_count = int(process_entry.get())
        except:
            messagebox.showerror("Error", "Invalid process count")
            return

        prev_entry = process_entry

        tk.Label(input_frame, text="Arrival Times").grid(row=0, column=0)
        tk.Label(input_frame, text="Burst Times").grid(row=0, column=1)

        for i in range(process_count):
            at = tk.Entry(input_frame)
            bt = tk.Entry(input_frame)

            at.grid(row=i+1, column=0, padx=5, pady=5)
            bt.grid(row=i+1, column=1, padx=5, pady=5)

            arrival_entries.append(at)
            burst_entries.append(bt)

            # ENTER navigation
            prev_entry.bind("<Return>", lambda e, nxt=at: nxt.focus())
            at.bind("<Return>", lambda e, nxt=bt: nxt.focus())

            prev_entry = bt

        # Last burst → time quantum
        prev_entry.bind("<Return>", lambda e: quantum_entry.focus())

    tk.Button(window, text="Set Processes", command=generate_fields, **BUTTON_STYLE).pack(pady=5)

    # =========================
    # RUN ROUND ROBIN
    # =========================
    def run_rr():
        output_box.delete("1.0", tk.END)

        try:
            process_count = len(arrival_entries)
            arrival_time = [int(e.get()) for e in arrival_entries]
            burst_time = [int(e.get()) for e in burst_entries]
            time_quantum = int(quantum_entry.get())
        except:
            messagebox.showerror("Error", "Invalid input")
            return

        # ===== ORIGINAL LOGIC =====
        remaining_burst = burst_time.copy()

        start_time = [-1] * process_count
        finish_time = [0] * process_count

        current_time = 0

        queue = []
        in_queue = [False] * process_count

        gantt_chart = []
        gantt_time = [0]

        completed = 0
        cpu_idle_time = 0

        while completed < process_count:

            for i in range(process_count):
                if arrival_time[i] <= current_time and i not in queue and remaining_burst[i] > 0:
                    queue.append(i)

            if not queue:
                gantt_chart.append("Idle")
                current_time += 1
                gantt_time.append(current_time)
                cpu_idle_time += 1
                continue

            current = queue.pop(0)
            in_queue[current] = False

            if start_time[current] == -1:
                start_time[current] = current_time

            execute_time = min(time_quantum, remaining_burst[current])

            gantt_chart.append(f"P{current+1}")

            current_time += execute_time
            remaining_burst[current] -= execute_time

            gantt_time.append(current_time)

            for i in range(process_count):
                if arrival_time[i] <= current_time and i not in queue and remaining_burst[i] > 0 and i != current:
                    queue.append(i)

            if remaining_burst[current] > 0:
                queue.append(current)
                in_queue[current] = True
            else:
                finish_time[current] = current_time
                completed += 1

        turnaround_time = []
        waiting_time = []

        total_turnaround = 0
        total_waiting = 0

        for i in range(process_count):
            tat = finish_time[i] - arrival_time[i]
            wt = tat - burst_time[i]

            turnaround_time.append(tat)
            waiting_time.append(wt)

            total_turnaround += tat
            total_waiting += wt

        avg_waiting_time = total_waiting / process_count
        avg_turnaround_time = total_turnaround / process_count

        cpu_busy_time = sum(burst_time)
        total_time = gantt_time[-1]

        cpu_idle_time = total_time - cpu_busy_time
        cpu_utilization = (cpu_busy_time / total_time) * 100
        throughput = process_count / total_time

        # ===== OUTPUT =====
        output_box.insert(tk.END, "GANTT CHART:\n")
        for p in gantt_chart:
            output_box.insert(tk.END, f"| {p} ")
        output_box.insert(tk.END, "|\n")

        for t in gantt_time:
            output_box.insert(tk.END, f"{t}    ")

        output_box.insert(tk.END, "\n\nPROCESS TABLE\n")
        output_box.insert(tk.END, "Process\tTurnaround\tWaiting\n")

        for i in range(process_count):
            output_box.insert(tk.END, f"P{i+1}\t{turnaround_time[i]}\t\t{waiting_time[i]}\n")

        output_box.insert(tk.END, "\nSYSTEM PERFORMANCE\n")
        output_box.insert(tk.END, f"CPU Busy Time: {cpu_busy_time}\n")
        output_box.insert(tk.END, f"CPU Idle Time: {cpu_idle_time}\n")
        output_box.insert(tk.END, f"CPU Utilization: {cpu_utilization}\n")
        output_box.insert(tk.END, f"Throughput: {throughput}\n")
        output_box.insert(tk.END, f"Average Waiting Time: {avg_waiting_time}\n")
        output_box.insert(tk.END, f"Average Turnaround Time: {avg_turnaround_time}\n")

    tk.Button(window, text="Run Round Robin", command=run_rr, **BUTTON_STYLE).pack(pady=5)

    tk.Button(window, text="Exit", bg="red", fg="white",
              width=30, height=2,
              command=window.destroy).pack(pady=10)


# =========================
# RUN DIRECTLY
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    round_robin_gui()
    root.mainloop()