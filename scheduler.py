import heapq
import random
import sys

# Define a Process class
class Process:
    def __init__(self, pid, arrival_time, deadline, period):
        self.pid = pid
        self.initial_arrival = arrival_time
        self.arrival_time = arrival_time
        self.relative_deadline = deadline
        self.period = period
        self.absolute_deadline = arrival_time + deadline
        self.remaining_time = 0
        self.service_time = 0
        self.finish_times = []

# Define an Event class
class Event:
    def __init__(self, time, process, event_type):
        self.time = time
        self.process = process
        self.event_type = event_type  # "arrival" or "completion"

    def __lt__(self, other):
        return self.time < other.time

# Read processes from input file
def read_input(filename):
    processes = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        num_processes, switch_time = map(int, lines[0].strip().split())
        for line in lines[1:]:
            pid, arrival, deadline, period = map(int, line.strip().split())
            processes.append(Process(pid, arrival, deadline, period))
    return processes, switch_time

# Select next process based on scheduler
def select_next_process(ready_queue, method):
    if method == 'RM':
        ready_queue.sort(key=lambda p: p.period)
    elif method == 'DM':
        ready_queue.sort(key=lambda p: p.relative_deadline)
    elif method == 'EDF':
        ready_queue.sort(key=lambda p: p.absolute_deadline)
    return ready_queue[0] if ready_queue else None

def simulate(processes, switch_time, method, simulation_end_time=1500):
    clock = 0
    cpu_busy_time = 0
    event_queue = []
    ready_queue = []
    deadline_miss = None

    # Initialize events (all arrivals at 0)
    for process in processes:
        service_time = {
            'EDF': random.randint(0, 500),
            'DM': random.randint(0, 413),
            'RM': random.randint(0, 101)
        }[method]
        process.remaining_time = service_time
        process.service_time = service_time
        heapq.heappush(event_queue, Event(process.arrival_time, process, 'arrival'))

    current_process = None

    while event_queue and clock <= simulation_end_time:
        event = heapq.heappop(event_queue)
        clock = event.time

        if event.event_type == 'arrival':
            ready_queue.append(event.process)

            if current_process:
                candidate = select_next_process(ready_queue, method)
                if candidate and candidate != current_process:
                    ready_queue.append(current_process)
                    current_process = None

        if not current_process and ready_queue:
            current_process = select_next_process(ready_queue, method)
            ready_queue.remove(current_process)
            completion_time = clock + current_process.remaining_time
            heapq.heappush(event_queue, Event(completion_time, current_process, 'completion'))
            cpu_busy_time += current_process.remaining_time

        elif event.event_type == 'completion':
            if clock > current_process.absolute_deadline:
                deadline_miss = (current_process.pid, clock)
                break
            current_process.finish_times.append(clock)
            # Reschedule the process for its next period
            current_process.arrival_time += current_process.period
            current_process.absolute_deadline = current_process.arrival_time + current_process.relative_deadline
            heapq.heappush(event_queue, Event(current_process.arrival_time, current_process, 'arrival'))
            current_process = None

    # ✅ Final additional check if no miss was found inside loop
    if not deadline_miss:
        for p in processes:
            if not p.finish_times:
                deadline_miss = (p.pid, clock)
                break

    return deadline_miss, cpu_busy_time, clock, processes


def main():
    # Open file to save output
    output_file = open('output.txt', 'w')
    sys.stdout = output_file  # Redirect prints to the file

    input_file = 'input.txt'
    processes, switch_time = read_input(input_file)

    for method in ['RM', 'DM', 'EDF']:
        fresh_processes = [Process(p.pid, p.initial_arrival, p.relative_deadline, p.period) for p in processes]
        deadline_miss, cpu_time, end_time, finished_processes = simulate(fresh_processes, switch_time, method)

        print(f"\n{method} Results:")

        if deadline_miss:
            pid, miss_time = deadline_miss
            print(f"Schedule feasible from 0 to {miss_time} units.")
            print(f"At {miss_time}, process {pid} did not meet deadline.")
        else:
            print(f"Schedule feasible from 0 to {end_time} units.")

        print(f"CPU time took {cpu_time} units.")

        for p in finished_processes:
            if p.finish_times:
                finish_times_str = ', '.join(map(str, p.finish_times))
            else:
                finish_times_str = 'Not finished (missed deadline)'
            print(f"Process {p.pid}: Arrival Time: {p.initial_arrival}, Service: {p.service_time}, Period: {p.period}, finish: {finish_times_str}")

    output_file.close()

if __name__ == "__main__":
    main()
