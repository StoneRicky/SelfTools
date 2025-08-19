import json


data = []
# china 3-54,73-134
# japan 29-46,124-146
# usa 25-50,-125--66
for lat in range(-89, 89):
    for lng in range(-179, 179):
        data.append({
        "type": "marker",
        "latLng": {
            "lat": lat , 
            "lng": lng
        },
        "color": "#4aa8c3"
    })

json_str = json.dumps(data, indent=4)
with open('iitc/intGps/global.json', 'w') as f:
    f.write(json_str)