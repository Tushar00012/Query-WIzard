import os
import threading
import time
import webbrowser

from werkzeug.serving import make_server

from backend.app import create_app


class ServerThread(threading.Thread):
    def __init__(self, host: str, port: int):
        super().__init__(daemon=True)
        self.host = host
        self.port = port
        self.app = create_app()
        self.server = make_server(self.host, self.port, self.app)

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()


def main():
    host = os.getenv("APP_HOST", "127.0.0.1")
    port = int(os.getenv("APP_PORT", "5000"))
    open_browser = os.getenv("OPEN_BROWSER", "1") == "1"

    server = ServerThread(host, port)
    server.start()

    url = f"http://{host}:{port}"
    if open_browser:
        # Delay avoids race where browser opens before server bind completes.
        time.sleep(0.6)
        webbrowser.open(url)

    try:
        while server.is_alive():
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
