import socket
import threading

# إنشاء Socket للعميل
# AF_INET = IPv4
# SOCK_STREAM = TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# عنوان السيرفر الذي نريد الاتصال به
# هنا السيرفر موجود على نفس الجهاز
HOST = "127.0.0.1"
PORT = 5000


client_socket.connect((HOST, PORT))

print("Connected to server")
username = input("Enter your username: ")

client_socket.send(username.encode())

# دالة تستقبل الرسائل من السيرفر بشكل مستمر
def receive_messages():

    while True:

        try:
            message = client_socket.recv(1024).decode()

            if not message:
                break

            print("\n" + message)

        except ConnectionAbortedError:
            break

# إنشاء Thread خاص بالاستقبال
receive_thread = threading.Thread(
    target=receive_messages
)

# تشغيل Thread الاستقبال
receive_thread.start()

# متغير يدل على أن الاتصال ما زال قائمًا
connected = True

# طالما الاتصال قائم نستمر في إرسال واستقبال الرسائل
while connected:

    # قراءة رسالة من المستخدم
    message = input("Client: ")

    # إذا كتب المستخدم exit نخرج من الحلقة
    if message == "exit":

        client_socket.send("exit".encode())

        connected = False
    break

    # إرسال الرسالة إلى السيرفر
    client_socket.send(message.encode())


# بعد انتهاء الحلقة نغلق الاتصال
client_socket.close()
