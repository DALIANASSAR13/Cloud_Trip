from flask import Blueprint, request, jsonify
#from flights_data import flights

selected_flight_bp = Blueprint('flight_bp', __name__)
# i will add here the real data or the api
flights =[


]
@selected_flight_bp.route('/selected-flight', methods=['POST'])

def selected_flight():
    
    "return the flight chosen by the user"
    data = request.json
    flight_name = data.get("flight_name")

    if not flight_name:
        return jsonify({"success": False, "message": "Missing required fields"}), 400
    
    # replace with the real data 
    flight = next((f for f in flights if f["flight_name"] == flight_name), None)
    
    if not flight:
         return jsonify({"success": False, "message": "Missing required fields"}), 400
    

    return jsonify({"success": True, "flights": flight})
