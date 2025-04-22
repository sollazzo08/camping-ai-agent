from generate_checklist import generate_checklist

def main():

    trip_data = {
        "location": "Little Pond Campground, NY",
        "latitude": 42.0132,
        "longitude": -74.5938,
        "start_date": "2025-06-15",
        "end_date": "2025-06-17",
        "group_size": 2,
        "has_dog": True,
        "activities": ["hiking", "campfire cooking"]
}

    checklist = generate_checklist(trip_data)
    print(checklist)


if __name__ == "__main__":
    main()
