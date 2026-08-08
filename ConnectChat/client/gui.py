import tkinter as tk
import threading

class ChatGUI:

    def __init__(self, client):

        self.client = client

        # إنشاء النافذة
        self.window = tk.Tk()
        self.window.configure(bg="#F5F7FA")

        self.window.title("ConnectChat")

        self.window.geometry("1000x550")

        self.window.resizable(False, False)

        # إنشاء الصفحتين
        self.create_login_frame()

        self.create_chat_frame()

    def create_login_frame(self):

        self.login_frame = tk.Frame(
            self.window,
            bg="#F5F7FA"
        )

        self.login_frame.pack(
            expand=True
        )


        title = tk.Label(

            self.login_frame,

            text="ConnectChat",

            font=("Arial", 20),
            bg="#F5F7FA",
            fg="#1F2937"

        )

        title.pack(
            pady=20
        )


        username_label = tk.Label(

            self.login_frame,

            text="Username",
            bg="#F5F7FA",
            fg="#1F2937"

        )

        username_label.pack()


        self.username_entry = tk.Entry(

            self.login_frame,

            width=30

        )

        self.username_entry.pack(
            pady=10
        )

        connect_button = tk.Button(
            self.login_frame,
            command=self.connect_to_server,
            text="Connect",
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            relief="flat",
            width=15
        )

        connect_button.pack(
            pady=20
        )

    def create_chat_frame(self):

        self.chat_frame = tk.Frame(
            self.window

        )
        title = tk.Label(
            self.chat_frame,
            text="ConnectChat",
            font=("Arial",20,"bold"),
            bg="#F5F7FA",
            fg="#2563EB"
        )

        title.pack(
            pady=10
        )
        # صندوق عرض الرسائل
        self.chat_box = tk.Text(
            self.chat_frame,
            bg="white",
            fg="#1F2937",
            font=("Arial",11),
            relief="solid",
            bd=1
        )
        self.users_list = tk.Listbox(
            self.chat_frame,
            width=20,
            height=20
        )

        self.users_list.pack(
            side=tk.RIGHT,
            padx=10
        )

        self.chat_box.pack(pady=10)

        # مربع كتابة الرسالة
        self.message_entry = tk.Entry(
            self.chat_frame,
            width=45,
            font=("Arial",11),
            bd=1
        )
        self.message_entry.bind(
            "<Return>",
            self.send_message_enter
        )
        self.message_entry.pack(side=tk.LEFT, padx=10)

        # زر الإرسال
        self.send_button = tk.Button(
            self.chat_frame,
            text="Send",
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            relief="flat",
            width=10,
            command=self.send_message
        )

        self.send_button.pack(side=tk.LEFT)
    def connect_to_server(self):
        username = self.username_entry.get()

        if username:

            # إرسال اسم المستخدم للسيرفر
            self.client.send_username(username)
            receive_thread = threading.Thread(
                target=self.client.receive_messages
            )

            receive_thread.start()

            # إخفاء صفحة تسجيل الدخول
            self.login_frame.pack_forget()


            # إظهار صفحة المحادثة
            self.chat_frame.pack(
                expand=True
            )

    def send_message(self):

        message = self.message_entry.get()

        if message:

            # إرسال الرسالة للسيرفر
            self.client.send_message(message)


            # عرض رسالتك عندك
            self.chat_box.insert(
                tk.END,
                "\tYou: " + message + "\n"
            )


            # تنظيف مربع الكتابة
            self.message_entry.delete(
                0,
                tk.END
            )

    def display_message(self, message):

        if message.startswith("USERS:"):

            users = message.replace(
                "USERS:",
                ""
            )

            self.users_list.delete(
                0,
                tk.END
            )


            for user in users.split(","):

                self.users_list.insert(
                    tk.END,
                    user
                )

        else:

            self.chat_box.insert(
                tk.END,
                message + "\n"
            )
    def start(self):

        self.window.mainloop()
    def send_message_enter(self, event):

        self.send_message()