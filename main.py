from workflows.trip_workflow import run_trip_agent

def main():
    user_input = input("Tell me about your camping trip: ")
    result = run_trip_agent(user_input)

    print("\nTrip Info:")
    print(result["trip"])

    print("\nLocation Lookup:")
    print(result["location"])

if __name__ == "__main__":
    main()
