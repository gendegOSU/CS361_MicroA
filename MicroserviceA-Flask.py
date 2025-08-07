from flask import Flask, request, jsonify
import requests


app = Flask(__name__)

# Define API constants
API_url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
API_headers = {
    "x-app-id": "f826a32d",
    "x-app-key": "022895198af401c5af931eb5a9db45da",
    "x-remote-user-id": "0"
}

def food_format(food):
    return {
        "food_name": food["food_name"],
        "serving_size": food["serving_qty"],
        "serving_unit": food["serving_unit"],
        "calories": food["nf_calories"],
        "total_fat": food["nf_total_fat"],
        "saturated_fat": food["nf_saturated_fat"],
        "cholesterol": food["nf_cholesterol"],
        "sodium": food["nf_sodium"],
        "carbohydrates": food["nf_total_carbohydrate"],
        "fiber": food["nf_dietary_fiber"],
        "sugar": food["nf_sugars"],
        "protein": food["nf_protein"]
    }

@app.route('/nutrition', methods=['POST'])
def get_nutrition():
    data = request.get_json()
    return_result = {"success": False, "data": "", "message":""}

    # Extract search terms
    search_term = data["search_term"]
    req_list = data["ingredients"]

    # Build API query
    API_query = search_term
    for item in req_list:
        if item == "":
            continue
        API_query += " " + item
    if API_query == "":
        print("Request does not have any search terms")
        #send_response(server, False, [{"message": "Request must contain search term or ingredient list"}])
        return_result["message"] = "Request must contain search term or ingredient list"
        return jsonify(return_result),400


    API_payload = {"query": API_query}

    # Send API request
    print("Requesting data from API")
    API_response = requests.post(API_url, headers=API_headers, data=API_payload)
    response = API_response.json()
    response_status = API_response.status_code

    # Check if request failed and send failure response
    if response_status != 200:
        print("API request failed, status: " + str(response_status) + ", message: " + response["message"])
        #send_response(server, False, )
        return_result["message"] = response["message"]
        return jsonify(return_result), 400

    # Send response back
    data = []
    for food in response["foods"]:
        data.append(food_format(food))
    print("API request succeeded!  Response sent back to client!")
    #send_response(server, True, data)
    return_result["data"] = data
    return jsonify(return_result),200


if __name__ == '__main__':
    app.run(port=6000)