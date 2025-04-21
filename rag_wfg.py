from collections import defaultdict

def get_matrix_input(prompt, rows, cols):
    matrix = []
    print(f"{prompt} (Enter {cols} space-separated integers per row):")
    for i in range(rows):
        while True:
            try:
                row = list(map(int, input(f"Row {i}: ").strip().split()))
                if len(row) != cols:
                    raise ValueError
                matrix.append(row)
                break
            except ValueError:
                print(f"Please enter exactly {cols} integers.")
    return matrix

def build_rag(allocation, request, num_processes, num_resources):
    rag = defaultdict(set)

    for i in range(num_processes):
        for j in range(num_resources):
            if allocation[i][j] > 0:
                resource_node = f"R{j}"
                process_node = f"P{i}"
                rag[resource_node].add(process_node)

            if request[i][j] > 0:
                resource_node = f"R{j}"
                process_node = f"P{i}"
                rag[process_node].add(resource_node)

    return rag

def convert_rag_to_wfg(rag):
    wfg = defaultdict(set)

    for node in rag:
        if node.startswith('P'):
            for neighbor in rag[node]:
                if neighbor.startswith('R'):
                    for holder in rag.get(neighbor, []):
                        if holder != node:
                            wfg[node].add(holder)

    return wfg

def detect_cycle(wfg):
    visited = set()
    rec_stack = set()

    def dfs(process):
        visited.add(process)
        rec_stack.add(process)
        for neighbor in wfg.get(process, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
        rec_stack.remove(process)
        return False

    for process in wfg:
        if process not in visited:
            if dfs(process):
                return True
    return False

def is_deadlocked(allocation, request, available):
    num_processes = len(allocation)
    num_resources = len(available)

    rag = build_rag(allocation, request, num_processes, num_resources)
    print("\nResource Allocation Graph (RAG):")
    for node, edges in rag.items():
        print(f"{node} -> {list(edges)}")

    wfg = convert_rag_to_wfg(rag)
    print("\nWait-For Graph (WFG):")
    for node, edges in wfg.items():
        print(f"{node} -> {list(edges)}")

    return detect_cycle(wfg)

def run_deadlock_detection(available, allocation, request):
    print("\nInputs:")
    print("Available:", available)
    print("Allocation Matrix:")
    for row in allocation:
        print(row)
    print("Request Matrix:")
    for row in request:
        print(row)

    if is_deadlocked(allocation, request, available):
        print("\n⚠️  Deadlock detected.")
    else:
        print("\n✅ No deadlock detected.")
