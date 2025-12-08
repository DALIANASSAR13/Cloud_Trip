from flask import Blueprint, request, jsonify
#from flights_data import flights

ticket_bp = Blueprint('ticket_bp', __name__)

# hina ha7ot el data el real b3d keda
flights =[


]

@ticket_bp.route('/ticket-summary', methods=['POST'])

def summary():
    data = request.json 
    flight_name = data.get("flight_name")
    payment_method = data.get("payment_method")
    total_amount = data.get("total_amount")
    travellers_number = data.get("travellers_number")
    dates = data.get("dates")           # list of dates
    trip_type = data.get("trip_type") 
    departure = data.get("departure")
    arrival = data.get("arrival")

    if not flight_name or not payment_method or not total_amount or not travellers_number or not dates or not trip_type or not departure or not arrival:
        return jsonify({"success": False, "message": "Missing required fields"}), 400
    

    # hina b validate el flight mawgoda sah
    flight = next((f for f in flights if f["flight_name"] == flight_name), None)
    if not flight:
        return jsonify({"success": False, "message": "Flight not found"}), 404
    

    # hina b check eno el total amount by match el flight price wla la 

    expected_amount = flight["price"] * travellers_number
    if total_amount != expected_amount:
        return jsonify({"success": False, "message": "Amount does not match flight price"}), 400
    
    
    #hina b validate eno el payment method sah
    if payment_method not in ["paypal","stripe"]:
        return jsonify({"success": False, "message": "Amount does not match flight price"}), 400
    

    # this is the data of the ticket summary 

    ticket_summary = {
        "flight_name": flight["flight_name"],
        "from": flight["from"],
        "to": flight["to"],
        "dates": dates,
        "trip_type": trip_type,
        "airline": flight["airline"],
        "departure_time": flight["departure_time"],
        "arrival_time": flight["arrival_time"],
        "duration": flight["duration"],
        "travellers_number": travellers_number,
        "total_amount": total_amount,
        "payment_method": payment_method,
        "payment_status": "Paid via " + payment_method.capitalize()
    }



    return jsonify({"success": True, "ticket_summary": ticket_summary})
    


    


