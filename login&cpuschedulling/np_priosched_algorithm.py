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

def priority_gui():

    window = tk.Toplevel()
    window.title("Priority Scheduling (Non-Preemptive)")
    window.geometry("650x650")

    arrival_entries = []
    burst_entries = []
    priority_entries = []

    # =========================
    # PROCESS COUNT
    # =========================
    tk.Label(window, text="Enter Process Count").pack()

    process_entry = tk.Entry(window)
    process_entry.pack()

    input_frame = tk.Frame(window)
    input_frame.pack(pady=10)

    output_box = tk.Text(window, height=15, width=75)
    output_box.pack(pady=10)

    # =========================
    # GENERATE INPUT FIELDS
    # =========================
    def generate_fields():
        for widget in input_frame.winfo_children():
            widget.destroy()

        arrival_entries.clear()
        burst_entries.clear()
        priority_entries.clear()

        try:
            process_count = int(process_entry.get())
        except:
            messagebox.showerror("Error", "Invalid process count")
            return

        prev_entry = None

        tk.Label(input_frame, text="Arrival Time").grid(row=0, column=0)
        tk.Label(input_frame, text="Burst Time").grid(row=0, column=1)
        tk.Label(input_frame, text="Priority").grid(row=0, column=2)

        for i in range(process_count):
            at = tk.Entry(input_frame)
            bt = tk.Entry(input_frame)
            pr = tk.Entry(input_frame)

            at.grid(row=i+1, column=0, padx=5, pady=5)
            bt.grid(row=i+1, column=1, padx=5, pady=5)
            pr.grid(row=i+1, column=2, padx=5, pady=5)

            arrival_entries.append(at)
            burst_entries.append(bt)
            priority_entries.append(pr)

            # ENTER navigation
            if prev_entry:
                prev_entry.bind("<Return>", lambda e, nxt=at: nxt.focus())

            at.bind("<Return>", lambda e, nxt=bt: nxt.focus())
            bt.bind("<Return>", lambda e, nxt=pr: nxt.focus())

            prev_entry = pr

    tk.Button(window, text="Set Processes", command=generate_fields, **BUTTON_STYLE).pack(pady=5)

    # =========================
    # RUN ALGORITHM
    # =========================
    def run_priority():
        output_box.delete("1.0", tk.END)

        try:
            process_count = len(arrival_entries)

            arrival_time = [int(e.get()) for e in arrival_entries]
            burst_time = [int(e.get()) for e in burst_entries]
            priority_list = [int(e.get()) for e in priority_entries]

        except:
            messagebox.showerror("Error", "Invalid input")
            return

        # ===== ORIGINAL LOGIC (UNCHANGED) =====
        completed = [False] * process_count
        current_time = 0

        start_time = [0] * process_count
        finish_time = [0] * process_count

        gantt_chart = []
        gantt_time = [0]

        done = 0

        while done < process_count:

            ready = []

            for i in range(process_count):
                if arrival_time[i] <= current_time and not completed[i]:
                    ready.append(i)

            if len(ready) == 0:
                gantt_chart.append("IDLE")
                current_time += 1
                gantt_time.append(current_time)
                continue

            idx = ready[0]

            for i in ready:
                if priority_list[i] < priority_list[idx]:
                    idx = i

            start_time[idx] = current_time
            gantt_chart.append(f"P{idx+1}")

            current_time += burst_time[idx]
            finish_time[idx] = current_time
            gantt_time.append(current_time)

            completed[idx] = True
            done += 1

        # ===== OUTPUT =====
        output_box.insert(tk.END, "GANTT CHART:\n")
        for p in gantt_chart:
            output_box.insert(tk.END, f"| {p} ")
        output_box.insert(tk.END, "|\n")

        for t in gantt_time:
            output_box.insert(tk.END, f"{t}    ")

        output_box.insert(tk.END, "\n\nPROCESS TABLE\n")
        output_box.insert(tk.END, "Process\tTurnaround\tWaiting\n")

        total_turnaround = 0
        total_waiting = 0

        for i in range(process_count):
            tat = finish_time[i] - arrival_time[i]
            wt = tat - burst_time[i]

            total_turnaround += tat
            total_waiting += wt

            output_box.insert(tk.END, f"P{i+1}\t{tat}\t\t{wt}\n")

        cpu_busy_time = sum(burst_time)
        total_time = gantt_time[-1]

        cpu_idle_time = total_time - cpu_busy_time
        cpu_utilization = (cpu_busy_time / total_time) * 100
        throughput = process_count / total_time

        avg_waiting_time = total_waiting / process_count
        avg_turnaround_time = total_turnaround / process_count

        output_box.insert(tk.END, "\nSYSTEM PERFORMANCE\n")
        output_box.insert(tk.END, f"CPU Busy Time: {cpu_busy_time}\n")
        output_box.insert(tk.END, f"CPU Idle Time: {cpu_idle_time}\n")
        output_box.insert(tk.END, f"CPU Utilization: {cpu_utilization}\n")
        output_box.insert(tk.END, f"Throughput: {throughput}\n")
        output_box.insert(tk.END, f"Average Waiting Time: {avg_waiting_time}\n")
        output_box.insert(tk.END, f"Average Turnaround Time: {avg_turnaround_time}\n")

    tk.Button(window, text="Run Priority Scheduling", command=run_priority, **BUTTON_STYLE).pack(pady=5)

    tk.Button(window, text="Exit", bg="red", fg="white",
              width=30, height=2,
              command=window.destroy).pack(pady=10)


# =========================
# RUN DIRECTLY
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    priority_gui()
    root.mainloop()