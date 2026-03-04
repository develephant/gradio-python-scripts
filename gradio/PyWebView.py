# PyWebView

import webview
import threading

threading.Thread(target=demo.launch, kwargs={"prevent_thread_lock": True}).start()
webview.create_window("My App", "http://localhost:7860")
webview.start()
