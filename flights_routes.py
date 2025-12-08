from flask import Blueprint, request, jsonify
#from flights_data import flights

flight_bp = Blueprint('flight_bp', __name__)

@flight_bp.route('/search-flights', methods=['POST'])

def search_flights():
    data = request.json

    departure = data.get("departure")
    arrival = data.get("arrival")
    dates = data.get("dates")           # list of dates
    trip_type = data.get("trip_type") 
    travellers_number = data.get("travellers_number")
    class_type = data.get("class_type")

      # "one-way", "round-trip", "multi-trip"

    # Validate required fields
    if not departure or not arrival or not dates or not trip_type or not travellers_number or not class_type:
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    # Check dates based on trip type
    if trip_type == "one-way" and len(dates) != 1:
        return jsonify({"success": False, "message": "One-way trip must have 1 date"}), 400
    elif trip_type == "round-trip" and len(dates) != 2:
        return jsonify({"success": False, "message": "Round-trip must have 2 dates"}), 400
    elif trip_type == "multi-trip" and (len(dates) < 2 or len(dates) > 4):
        return jsonify({"success": False, "message": "Multi-trip must have 2 to 4 dates"}), 400

    # results will come from flights_data later
    results = []

    # Example: for testing, return a dummy flight for each date this is will be deleted when we enter real data
    for date in dates:
        results.append({
            "flight_name": "DUMMY001",
            "from": departure,
            "to": arrival,
            "date": date,
            "trip_type": trip_type,
            "airline": "Example Air",
            "departure_time": "09:00 AM",
            "arrival_time": "12:00 PM",
            "duration": "3h",
            "price": 100
        })

    return jsonify({"success": True, "flights": results})
