"""Notification handler"""
from tornado import websocket

sessions = {}


class WebsocketHandler(websocket.WebSocketHandler):
    """Web socket handler"""
    def open(self, customer_id):
        """Open connection"""
        self.customer_id = int(customer_id)
        sessions[self.customer_id] = self

    def on_close(self, code=None, reason=None):
        """Close"""
        del sessions[self.customer_id]

    def on_message(self, message):
        """On message"""
        print('message', message)