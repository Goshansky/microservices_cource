import requests


class OrderService:
    def __init__(self, base_url):
        self.base_url = base_url

    def accept_order(self, order_id):
        url = f"{self.base_url}/orders/{order_id}/status"
        data = {"status": "in_work"}
        response = requests.put(url, json=data)
        return response.json()

    def cancel_order(self, order_id):
        url = f"{self.base_url}/orders/{order_id}/status"
        data = {"status": "cancel"}
        response = requests.put(url, json=data)
        return response.json()

    def complete_order(self, order_id):
        url = f"{self.base_url}/orders/{order_id}/status"
        data = {"status": "done"}
        response = requests.put(url, json=data)
        return response.json()
