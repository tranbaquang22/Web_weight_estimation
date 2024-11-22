import requests

API_URL = 'http://vn-07.fpt.ai.vn:8082/weight_estimation/predict'  # URL API

def call_api(image_link, name_product, name_level_1, name_level_2, name_level_3, price_product):
    """Gọi API dự đoán trọng lượng"""
    payload = {
        "image_link": image_link,
        "name_product": name_product,
        "name_level_1": name_level_1,
        "name_level_2": name_level_2,
        "name_level_3": name_level_3,
        "price_product": float(price_product)
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(API_URL, json=payload, headers=headers)
    
    print("Payload sent:", payload)  # Debug payload
    print("Response status:", response.status_code)  # Debug status code
    print("Response body:", response.text)  # Debug response body

    if response.status_code == 200: 
        return response.json()
    else:
        print("API Error:", response.text)
        return {"error": f"API call failed with status code {response.status_code}"}

