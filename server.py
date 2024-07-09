import http.server
import socketserver
import threading
import websockets
import asyncio
import cv2
from sqldb import db
from functools import partial


PORT = 8000
WS_PORT = 8765
dbe = db()


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


def start_http_server():
    handler = MyHttpRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving HTTP on port {PORT}")
        httpd.serve_forever()


def capture_image(x, y):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    ret, frame = cap.read()
    if ret:
        i = dbe.get_last_id() + 1
        cv2.imwrite(f'img/captured_image{i}.jpg', frame)
        dbe.insert_data(f'img/captured_image{i}.jpg', x, y)
        print(f"Image captured and saved as captured_image{i}.jpg")
    else:
        print("Error: Could not capture image.")
    cap.release()


async def capture_image_async(x, y):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, partial(capture_image, x, y))


async def websocket_handler(websocket):
    async for message in websocket:
        c, x, y = message.split(',')
        if c == 'Click':
            print("click")
            asyncio.create_task(capture_image_async(x, y))
        elif c == 'NoClick':
            print(f"Received mouse data: x={x}, y={y}")


async def start_websocket_server():
    async with websockets.serve(websocket_handler, "localhost", WS_PORT):
        print(f"Serving WebSocket on port {WS_PORT}")
        try:
            await asyncio.Future()  # Run forever
        except asyncio.CancelledError:
            dbe.close_table()
            print("WebSocket server is shutting down...")

# Run both servers concurrently
if __name__ == "__main__":
    try:
        # Start the HTTP server in a new thread
        http_thread = threading.Thread(target=start_http_server)
        http_thread.daemon = True
        http_thread.start()

        # Start the WebSocket server in the main thread
        asyncio.run(start_websocket_server())
    except KeyboardInterrupt:
        dbe.close_table()
        print("Server is shutting down...")
