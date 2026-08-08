import socket


class ChatClient:

    def __init__(self):

        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.callback = None


    def connect(self, host, port):

        self.socket.connect(
            (host, port)
        )
        
    def send_username(self, username):

        self.socket.send(
            username.encode()
        )
    


    def send_message(self, message):

        self.socket.send(
            message.encode()
        )


    def receive_messages(self):

        while True:

            try:

                message = self.socket.recv(1024).decode()

                if not message:
                    break


                if self.callback:

                    self.callback(message)


            except:

                break


    def set_callback(self, callback):

        self.callback = callback


    def close(self):

        self.socket.close()

