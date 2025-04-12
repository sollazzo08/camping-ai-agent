from agents.extract_trip import extract_trip_info

def run_trip_agent():
    user_input = input("Tell me about your camping trip: ")
    try:
        trip = extract_trip_info(user_input)
        print("\nTrip Info Extracted:")
        print(trip.model_dump_json(indent=2))
    except Exception as e:
        print(f"\n Error: {e}")

if __name__ == "__main__":
    run_trip_agent()
