import requests
from concurrent.futures import ThreadPoolExecutor

class MessagingHandler:
    def __init__(self, backend_url, on_message):
        """
        Initialize the messaging handler.

        Args:
            backend_url (str): URL of the backend API.
            on_message (callable): Callback function to add messages to the UI.
        """
        self.backend_url = backend_url
        self.executor = ThreadPoolExecutor()  # For non-blocking backend calls
        self.on_message = on_message  # Callback for adding messages to the UI

    def send_data_to_backend(self, user_message):
        """
        Handle sending a message to the backend and updating the UI.
        Args:
            user_message (str): The user's message.
        """
        # Add the user's message to the UI
        self.on_message(user_message, is_user=True)

        # Add a loading bubble for the AI response
        loading_bubble = self.on_message("Typing...", is_user=False, is_loading=True)

        def backend_call():
            """Perform the backend request."""
            try:
                response = requests.post(self.backend_url, json={"query": user_message})
                if response.status_code == 200:
                    data = response.json()
                    return data
                else:
                    return f"Error: {response.status_code}", []
            except Exception as e:
                return f"Connection error: {e}", []

        def handle_response(future):
            try:
                data = future.result()  # Now receives the entire JSON object
                print("Backend data received:", data)  # Debug
                bot_message = data.get("response", "")
                citations = data.get("citations", [])
                loading_bubble.set_message(bot_message, citations)
            except Exception as e:
                print(f"Error updating message: {e}")
                loading_bubble.set_message(f"Error: {str(e)}")

        # Execute the backend call
        future = self.executor.submit(backend_call)
        future.add_done_callback(handle_response)
