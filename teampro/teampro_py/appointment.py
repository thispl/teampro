import frappe
@frappe.whitelist()
def calculate_distance(docname):
    doc = frappe.get_doc('Appointment', docname)

    origin_lat = float(doc.custom_checkin_latitude)
    origin_lon = float(doc.custom_checkin_longitude)
    destination_lat = float(doc.custom_checkout_latitude)
    destination_lon = float(doc.custom_checkout_longitude)
    if destination_lat == origin_lat and destination_lon == origin_lon:
        distance = 0
    else:
        distance = get_road_distance_graphhopper(origin_lat, origin_lon, destination_lat, destination_lon)
    distance = float(distance)
    return distance


import requests
def get_road_distance_graphhopper(origin_lat, origin_lon, destination_lat, destination_lon):
    api_key = "f0801316-68c4-43b8-8c19-788ebff443df"
    url = f"https://graphhopper.com/api/1/route?point={origin_lat},{origin_lon}&point={destination_lat},{destination_lon}&vehicle=car&locale=en&key={api_key}&calc_points=false"

    response = requests.get(url)
    data = response.json()

    if 'paths' in data:
        distance_in_meters = data['paths'][0]['distance']
        distance_in_km = distance_in_meters / 1000
        return distance_in_km
    else:
        return "Error calculating distance"
