import socket
import threading
clients = []
avatars = [
    "😀",
    "😎",
    "🐱",
    "🐼",
    "🐸",
    "🦊",
    "🐻",
    "🐧",
    "🐨",
    "🦁",
    "🐯"
]
# يمرعلى كلالعملاء ليرسل لهم ما عدا المرسل
def broadcast(message, sender_socket):
    for username, avatar, client_socket in clients:
        # لا نرسل الرسالة للمرسل نفسه
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode())

            except:
                pass
def send_users_list():

    users = []

    for username, avatar, client_socket in clients:
        users.append(
            avatar + " " + username
        )

    message = "USERS:" + ",".join(users)
    print(message)
    broadcast_all(message)
# إرسال رسالة لجميع العملاء بدون استثناء
def broadcast_all(message):

    for username, avatar, client_socket in clients:

        try:
            client_socket.send(message.encode())

        except:
            pass

# حلقة مستمرة لاستقبال وإرسال الرسائل
# تستمر طالما الاتصال موجود
def handle_client(client_socket, address, username, avatar):

    print(f"{address} connected")

    try:
        while True:
            #يستقبل الرسالة
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
# اذا اغلق الاتصال فجاة 
#حماية استقبال الرسائل في السيرفر
            except (ConnectionResetError, ConnectionAbortedError):

                print(f"{username} connection lost")
                break

            if not message:
                break


            print(f"{username}: {message}")
            # تجهيز الرسالة مع اسم المستخدم
            full_message = f"\t{avatar} {username}: {message}"
            broadcast(full_message, client_socket)

    finally:
        # حذف العميل عندما يغلق الاتصال
        # التاكد من ان العميل موجود قبل حذفه
        if (username, client_socket) in clients:
            clients.remove((username, client_socket))
            send_users_list()
        broadcast_all(f"\t{username} left the chat")
        # إغلاق الـ socket
        client_socket.close()

        print(f"{address} \tdisconnected")
# قبول اتصال من Client
# البرنامج يتوقف هنا حتى يأتي Client
# يرجع لنا Socket خاص بالعميل + عنوان العميل

# إنشاء Socket للسيرفر
# AF_INET = استخدام IPv4
# SOCK_STREAM = استخدام TCP (اتصال موثوق)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# تحديد عنوان السيرفر والمنفذ
# 127.0.0.1 يعني نفس الجهاز (Localhost)
# 5000 هو رقم الـ Port الذي سيستقبل عليه السيرفر الاتصالات
HOST = "127.0.0.1"
PORT = 5000


# ربط الـ Socket بالـ IP والـ Port
# بعد هذه الخطوة يصبح السيرفر مرتبطًا بهذا العنوان
server_socket.bind((HOST, PORT))


# جعل السيرفر في وضع الاستماع لطلبات الاتصال
# يعني أنه ينتظر أي Client يريد الاتصال
server_socket.listen()

print("Server is running and waiting for connection...")


server_running = True

while server_running:

    client_socket, address = server_socket.accept()
    username = client_socket.recv(1024).decode()
    avatar = avatars[len(clients) % len(avatars)]
    clients.append(
        (username, avatar, client_socket)
    )
    send_users_list()
    print(username, avatar)
    # إخبار الجميع بدخول المستخدم
    broadcast_all(f"\t{username} joined the chat")
    thread = threading.Thread(
    target=handle_client,
    args=(
        client_socket,
        address,
        username,
        avatar
    )

    )
    thread.start()


# إغلاق Socket السيرفر
server_socket.close()