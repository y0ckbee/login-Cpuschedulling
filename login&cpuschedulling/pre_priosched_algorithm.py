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

def priority_preemptive_gui():

    window = tk.Toplevel()
    window.title("Priority Scheduling (Preemptive)")
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

    output_box = tk.Text(window, height=18, width=75)
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

        prev = None

        tk.Label(input_frame, text="Arrival").grid(row=0, column=0)
        tk.Label(input_frame, text="Burst").grid(row=0, column=1)
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
            if prev:
                prev.bind("<Return>", lambda e, nxt=at: nxt.focus())

            at.bind("<Return>", lambda e, nxt=bt: nxt.focus())
            bt.bind("<Return>", lambda e, nxt=pr: nxt.focus())

            prev = pr

    tk.Button(window, text="Set Processes", command=generate_fields, **BUTTON_STYLE).pack(pady=5)

    # =========================
    # RUN PREEMPTIVE PRIORITY
    # =========================
    def run_priority():
        output_box.delete("1.0", tk.END)

        try:
            n = len(arrival_entries)

            arrival_time = [int(e.get()) for e in arrival_entries]
            burst_time = [int(e.get()) for e in burst_entries]
            priority_list = [int(e.get()) for e in priority_entries]

        except:
            messagebox.showerror("Error", "Invalid input")
            return

        # ===== PREEMPTIVE LOGIC =====
        remaining_bt = burst_time[:]
        completed = [False] * n

        current_time = 0
        done = 0

        finish_time = [0] * n

        gantt_chart = []
        gantt_time = [0]

        while done < n:

            idx = -1
            best_priority = float('inf')

            for i in range(n):
                if arrival_time[i] <= current_time and not completed[i]:
                    if priority_list[i] < best_priority:
                        best_priority = priority_list[i]
                        idx = i

            if idx == -1:
                gantt_chart.append("IDLE")
                current_time += 1
                gantt_time.append(current_time)
                continue

            # execute 1 unit (preemptive!)
            gantt_chart.append(f"P{idx+1}")
            remaining_bt[idx] -= 1
            current_time += 1
            gantt_time.append(current_time)

            if remaining_bt[idx] == 0:
                completed[idx] = True
                finish_time[idx] = current_time
                done += 1

        # =========================
        # CALCULATIONS
        # =========================
        turnaround_time = []
        waiting_time = []

        total_tat = 0
        total_wt = 0

        for i in range(n):
            tat = finish_time[i] - arrival_time[i]
            wt = tat - burst_time[i]

            turnaround_time.append(tat)
            waiting_time.append(wt)

            total_tat += tat
            total_wt += wt

        cpu_busy_time = sum(burst_time)
        total_time = gantt_time[-1]

        cpu_idle_time = total_time - cpu_busy_time
        cpu_util = (cpu_busy_time / total_time) * 100
        throughput = n / total_time

        # =========================
        # OUTPUT
        # =========================
        output_box.insert(tk.END, "GANTT CHART:\n")
        for p in gantt_chart:
            output_box.insert(tk.END, f"| {p} ")
        output_box.insert(tk.END, "|\n")

        for t in gantt_time:
            output_box.insert(tk.END, f"{t}    ")

        output_box.insert(tk.END, "\n\nPROCESS TABLE\n")
        output_box.insert(tk.END, "Process\tTurnaround\tWaiting\n")

        for i in range(n):
            output_box.insert(tk.END, f"P{i+1}\t{turnaround_time[i]}\t\t{waiting_time[i]}\n")

        output_box.insert(tk.END, "\nSYSTEM PERFORMANCE\n")
        output_box.insert(tk.END, f"CPU Busy Time: {cpu_busy_time}\n")
        output_box.insert(tk.END, f"CPU Idle Time: {cpu_idle_time}\n")
        output_box.insert(tk.END, f"CPU Utilization: {cpu_util}\n")
        output_box.insert(tk.END, f"Throughput: {throughput}\n")
        output_box.insert(tk.END, f"Average Waiting Time: {total_wt/n}\n")
        output_box.insert(tk.END, f"Average Turnaround Time: {total_tat/n}\n")

    tk.Button(window, text="Run Priority (Preemptive)", command=run_priority, **BUTTON_STYLE).pack(pady=5)

    tk.Button(window, text="Exit", bg="red", fg="white",
              width=30, height=2,
              command=window.destroy).pack(pady=10)


# =========================
# RUN DIRECTLY
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    priority_preemptive_gui()
    root.mainloop()