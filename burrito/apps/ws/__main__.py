import multiprocessing

from burrito.apps.ws.utils import run_websocket_server


multiprocessing.Process(target=run_websocket_server).start()
