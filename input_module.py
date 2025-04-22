
from matrix import is_deadlocked as banker_deadlock
from rag_wfg import run_deadlock_detection as wfg_deadlock

def load_static_inputs():
    available = [0, 0, 0]
    allocation = [
        [1, 0, 0],  # P0 holds R0
        [0, 1, 0],  # P1 holds R1
        [0, 0, 1],  # P2 holds R2
    ]
    request = [
        [0, 1, 0],  # P0 requests R1
        [0, 0, 1],  # P1 requests R2
        [1, 0, 0],  # P2 requests R0
    ]
    return available, allocation, request

def main():
    print("=== Deadlock Detection Tool ===")
    print("Choose method:")
    print("1. Banker's Algorithm (Matrix-Based)")
    print("2. Wait-For Graph (WFG)")

    while True:
        method = input("Enter choice (1 or 2): ").strip()
        if method in ("1", "2"):
            break
        print("Invalid input. Please enter 1 or 2.")

    available, allocation, request = load_static_inputs()

    if method == "1":
        if banker_deadlock(available, allocation, request):
            print("🔴 Deadlock detected.")
        else:
            print("✅ No deadlock detected.")
    else:
        print("\n[Using Wait-For Graph (RAG to WFG)]")
        wfg_deadlock(available, allocation, request)

if __name__ == "__main__":
    main()

"""
    n = int(input("Enter the number of processes: "))
    m = int(input("Enter the number of resource types: "))

    available = get_int_list(f"Enter {m} available resource instances: ")
    allocation = get_matrix("Enter the Allocation Matrix:", n)
    request = get_matrix("Enter the Request Matrix:", n)
    """
