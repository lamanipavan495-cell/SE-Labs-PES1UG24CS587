
def parse_request(text):
    try:
        if not isinstance(text, str):
            return None

        if text.count('->') != 1:
            return None

        start, end = text.split('->')

        start = start.strip()
        end = end.strip()

        if not start or not end:
            return None

        return int(start), int(end)

    except (ValueError, TypeError, OverflowError):
        return None


def total_travel(floors_csv):
    try:
        if not isinstance(floors_csv, str):
            return None

        if not floors_csv.strip():
            return None

        floor_values = floors_csv.split(',')

        if any(not f.strip() for f in floor_values):
            return None

        floors = [int(f.strip()) for f in floor_values]

        return sum(
            abs(floors[i + 1] - floors[i])
            for i in range(len(floors) - 1)
        )

    except (ValueError, TypeError, OverflowError):
        return None


def load_percent(text):
    try:
        if not isinstance(text, str):
            return None

        if text.count(' of ') != 1:
            return None

        load, capacity = text.split(' of ')

        load = int(load.strip())
        capacity = int(capacity.strip())

        if capacity <= 0:
            return None

        if load < 0 or load > capacity:
            return None

        return load * 100 // capacity

    except (ValueError, TypeError, OverflowError):
        return None


def main():
    print("==== Running parse_request ====")
    user_input = input(
        "Enter a request as FROM->TO (e.g. 5->9): "
    )
    result = parse_request(user_input)
    print("From and To:", result)

    print("\n==== Running total_travel ====")
    user_input = input(
        "Enter floors visited as CSV (e.g. 1,5,3,9): "
    )
    result = total_travel(user_input)
    print("Floors Travelled:", result)

    print("\n==== Running load_percent ====")
    user_input = input(
        "Enter load as 'X of Y' (e.g. 450 of 630): "
    )
    result = load_percent(user_input)
    print("Load Percent:", result)


if __name__ == "__main__":
    main()
