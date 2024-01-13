import requests
import json
import logging

class UTPayClient:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.api_key}'}
        logging.basicConfig(level=logging.ERROR)  # Set the desired log level
        self.logger = logging.getLogger(__name__)

    def handle_request(self, method, endpoint, data=None):
        try:
            response = requests.request(method, f'{self.base_url}/{endpoint}', headers=self.headers, data=json.dumps(data))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_message = f"Error during {method} {endpoint}: {e}"
            self.logger.error(error_message)
            return {'error': error_message}

    def create_order(self, order_data):
        # Validate input data
        if not all(key in order_data for key in ('currency', 'amount', 'customerId')):
            raise ValueError('Missing required parameters in order data.')

        return self.handle_request('POST', 'orders', order_data)

    def get_order_details(self, order_id):
        return self.handle_request('GET', f'orders/{order_id}')

    def list_orders(self):
        return self.handle_request('GET', 'orders')

    def update_order(self, order_id, order_data):
        return self.handle_request('PUT', f'orders/{order_id}', order_data)

    def cancel_order(self, order_id):
        return self.handle_request('DELETE', f'orders/{order_id}')

# Usage example
try:
    utpay_client = UTPayClient('your_api_key', 'https://api.utpay.com')

    # Create an order
    order_data = {'currency': 'USD', 'amount': 100, 'customerId': '123456789'}
    order_response = utpay_client.create_order(order_data)
    print("Created Order:", order_response)

    # Get order details
    order_id = order_response.get('orderId')
    if order_id:
        order_details = utpay_client.get_order_details(order_id)
        print("Order Details:", order_details)

    # List all orders
    all_orders = utpay_client.list_orders()
    print("All Orders:", all_orders)

    # Update an order (assuming 'order_id' is valid)
    if order_id:
        update_data = {'amount': 150}
        updated_order = utpay_client.update_order(order_id, update_data)
        print("Updated Order:", updated_order)

    # Cancel an order (assuming 'order_id' is valid)
    if order_id:
        cancellation_result = utpay_client.cancel_order(order_id)
        print("Cancellation Result:", cancellation_result)

except ValueError as ve:
    print(f"ValueError: {ve}")
