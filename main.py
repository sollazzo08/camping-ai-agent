from workflows.trip_workflow import run_trip_agent

def main():
    user_input = input("Tell me about your camping trip: ")
    result = run_trip_agent(user_input)

    print("\n Trip Info:")
    print(result.get("trip"))

    print("\n Weather Info:")
    print(result.get("weather"))



if __name__ == "__main__":
    main()
