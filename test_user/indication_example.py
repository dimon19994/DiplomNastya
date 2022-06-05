import requests

data = {
    'kilowatts_count': 10
}

r = requests.post("http://192.168.50.239:5130/indication/1/2", json=data)
