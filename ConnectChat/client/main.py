import threading

from network_client import ChatClient
from gui import ChatGUI
from config import HOST, PORT



client = ChatClient()


client.connect(
    HOST,
    PORT
)



gui = ChatGUI(client)



# ربط الرسائل القادمة بالواجهة
client.set_callback(
    gui.display_message
)



# Thread لاستقبال الرسائل
receive_thread = threading.Thread(
    target=client.receive_messages
)

receive_thread.start()



# تشغيل الواجهة
gui.start()