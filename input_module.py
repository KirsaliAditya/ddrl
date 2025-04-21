from rag_wfg import run_deadlock_detection # type: ignore

def load_inputs():
    """
    Static input version (example for quick testing)
    """
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
    available, allocation, request = load_inputs()
    run_deadlock_detection(available, allocation, request)


if __name__ == "__main__":
    main()

'''
    try:
        num_processes = int(input("Enter the number of processes: "))
        num_resources = int(input("Enter the number of resource types: "))
    except ValueError:
        print("Invalid input. Please enter integers.")
        exit(1)

    allocation = get_matrix_input("Enter the Allocation Matrix", num_processes, num_resources)
    request = get_matrix_input("Enter the Request Matrix", num_processes, num_resources)

    while True:
        try:
            available = list(map(int, input(f"Enter the Available Resources (space-separated {num_resources} integers): ").strip().split()))
            if len(available) != num_resources:
                raise ValueError
            break
        except ValueError:
            print(f"Please enter exactly {num_resources} integers.")

    return available, allocation, request
    '''