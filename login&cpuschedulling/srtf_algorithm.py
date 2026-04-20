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

def srtf_gui():

    window = tk.Toplevel()
    window.title("SJF Scheduling (Non-Preemptive)")
    window.geometry("600x600")

    # =========================
    # VARIABLES
    # =========================
    arrival_entries = []
    burst_entries = []

    # =========================
    # STEP 1: PROCESS COUNT
    # =========================
    tk.Label(window, text="Enter Process Count").pack()

    process_entry = tk.Entry(window)
    process_entry.pack()

    input_frame = tk.Frame(window)
    input_frame.pack(pady=10)

    output_box = tk.Text(window, height=15, width=70)
    output_box.pack(pady=10)

    # =========================
    # GENERATE INPUT FIELDS
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

        prev_entry = None

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
            if prev_entry:
                prev_entry.bind("<Return>", lambda e, nxt=at: nxt.focus())
            at.bind("<Return>", lambda e, nxt=bt: nxt.focus())

            prev_entry = bt

    tk.Button(window, text="Set Processes", command=generate_fields, **BUTTON_STYLE).pack(pady=5)

    # =========================
    # RUN ALGORITHM
    # =========================
    def run_sjf():
        output_box.delete("1.0", tk.END)

        try:
            process_count = len(arrival_entries)

            arrival_time = [int(e.get()) for e in arrival_entries]
            burst_time = [int(e.get()) for e in burst_entries]

        except:
            messagebox.showerror("Error", "Invalid input")
            return

        # ===== ORIGINAL LOGIC (UNCHANGED) =====
        completed = [False] * process_count
        start_time = [0] * process_count
        finish_time = [0] * process_count

        current_time = 0
        done = 0

        gantt_chart = []
        gantt_time = [0]
        cpu_idle_time = 0

        while done < process_count:
            idx = -1
            min_burst = float('inf')

            for i in range(process_count):
                if arrival_time[i] <= current_time and not completed[i]:
                    if burst_time[i] < min_burst:
                        min_burst = burst_time[i]
                        idx = i

            if idx == -1:
                gantt_chart.append("Idle")
                gantt_time.append(current_time)
                cpu_idle_time += 1
                current_time += 1
                continue

            start_time[idx] = current_time
            gantt_chart.append(f"P{idx+1}")

            current_time += burst_time[idx]

            finish_time[idx] = current_time
            gantt_time.append(current_time)

            completed[idx] = True
            done += 1

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

        cpu_busy_time = sum(burst_time)
        total_time = gantt_time[-1]

        cpu_util = (cpu_busy_time / total_time) * 100
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
        output_box.insert(tk.END, f"CPU Utilization: {cpu_util}\n")
        output_box.insert(tk.END, f"Throughput: {throughput}\n")
        output_box.insert(tk.END, f"Average Waiting Time: {total_waiting/process_count}\n")
        output_box.insert(tk.END, f"Average Turnaround Time: {total_turnaround/process_count}\n")

    tk.Button(window, text="Run SJF", command=run_sjf, **BUTTON_STYLE).pack(pady=5)

    tk.Button(window, text="Exit", bg="red", fg="white",
              width=30, height=2,
              command=window.destroy).pack(pady=10)


# =========================
# RUN DIRECTLY
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    srtf_gui()
    root.mainloop()