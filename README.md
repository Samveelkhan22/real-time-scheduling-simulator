# Real-Time Scheduling Simulator

This project simulates real-time job scheduling using three classical algorithms:

- **RM (Rate Monotonic Scheduling)**
- **DM (Deadline Monotonic Scheduling)**
- **EDF (Earliest Deadline First)**

The simulator is event-driven and models periodic tasks with service times, deadlines, and periods. It tracks schedule feasibility, missed deadlines, CPU usage, and per-process finish times.

---

## 📂 Input Format

The simulator reads input from a file named `input.txt`.


---

## ⚙️ How It Works

- Each process runs periodically based on its **period**.
- Service time is **randomly assigned** as per method-specific ranges:
  - **RM**: 0–101
  - **DM**: 0–413
  - **EDF**: 0–500
- Simulation is event-driven and only progresses on arrivals or completions.
- If a process misses its deadline, the simulation reports the failure time.
- Output is written to `output.txt`.

---

## 📤 Output Example

- RM Results: Schedule feasible from 0 to 650 units. CPU time took 408 units. Process 1: Arrival Time: 0, Service: 62, Period: 650, finish: 62 Process 2: Arrival Time: 0, Service: 11, Period: 750, finish: 62

---

## 📎 Files

- scheduler.py	Main Python script with simulation logic
- input.txt	Input file with 5+ periodic process definitions
- output.txt	Captured simulation results
