from flask import Blueprint, request, jsonify
#from flights_data import flights

payment_bp = Blueprint('payment_bp', __name__)

# hina ha7ot el data el real b3d keda
flights =[


]

@payment_bp.route('/process_payment', methods=['POST'])

def process_payment():

    data = request.json 

    flight_name = data.get("flight_name")
    payment_method = data.get("payment_method")
    total_amount = data.get("total_amount")


    if not flight_name or not payment_method or not total_amount:
        return jsonify({"success": False, "message": "Missing required fields"}), 400
    

     # hina ana bat2ked eno el flight de aslun mawgoda abl ma adf3ha 

    flight = next((f for f in flights if f["flight_name"] == flight_name), None)
    if not flight:
        return jsonify({"success": False, "message": "Flight not found"}), 404
    

    
    # hina b check eno el total amount by match el flight price wla la 
    if total_amount != flight["price"]:
        return jsonify({"success": False, "message": "Amount does not match flight price"}), 400
    
    
    if payment_method not in ["paypal","stripe"]:
        return jsonify({"success": False, "message": "Amount does not match flight price"}), 400
    
    if payment_method == "paypal":
        payment_status = "paid via paypal"
        # hina hn integrate el api beta3 el paypal method

    elif payment_method == "stripe":
        payment_method = "paid via stripe"

        # hina hn integrate el api beta3 el stripe method

    
     
     # hina barg3 el ticket summary le el selected flight bas law 3mltha flights 8alt htgeb keda kol el flights
    ticket_summary ={
        "flight": flight,
        "payment_status": payment_status
    }

    
    return jsonify({"success": True, "ticket_summary": ticket_summary})


