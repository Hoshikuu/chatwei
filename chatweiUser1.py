import tkinter as tk
from tkinter import scrolledtext, font

from weicore.coder import encodeb64
from weicore.cweiFormater import formater

from datetime import datetime
from requests import post

from time import sleep
from json import loads

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat")
        self.root.geometry("600x500")  # Aumentamos el ancho para acomodar el menú
        self.root.configure(bg="#1e1e1e")  # Fondo oscuro

        # Fuente moderna
        self.font = ("Segoe UI", 10)
        self.bold_font = ("Segoe UI", 10, "bold")

        # Lista de chats disponibles (puede ser dinámica)
        self.chats = ["Chat 1", "Chat 2", "Chat 3"]  # Ejemplo inicial
        self.current_chat = None  # Chat seleccionado actualmente

        # Frame principal que contendrá el chat y el menú
        self.main_frame = tk.Frame(root, bg="#1e1e1e")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para el menú a la izquierda
        self.menu_frame = tk.Frame(self.main_frame, bg="#252526", width=150)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        # Añadir elementos al menú
        self.menu_label = tk.Label(self.menu_frame, text="Chats", font=self.bold_font, bg="#252526", fg="#ffffff")
        self.menu_label.pack(pady=10)

        # Botones dinámicos para los chats
        self.chat_buttons = []
        self.update_chat_buttons()

        # Frame para los mensajes
        self.message_frame = tk.Frame(self.main_frame, bg="#1e1e1e")
        self.message_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.message_frame)

        # Área de mensajes con scrollbar
        self.message_area = scrolledtext.ScrolledText(
            self.message_frame, wrap=tk.WORD, yscrollcommand=self.scrollbar.set,
            bg="#1e1e1e", font=self.font, padx=10, pady=10, state=tk.DISABLED, bd=0, highlightthickness=0
        )
        self.message_area.pack(fill=tk.BOTH, expand=True)

        # Configurar etiquetas para la alineación y estilo de las burbujas
        self.message_area.tag_configure("left", justify=tk.LEFT, lmargin1=10, lmargin2=10, rmargin=50, spacing3=5,
                                       background="#333333", relief=tk.FLAT, borderwidth=0, wrap=tk.WORD,
                                       font=self.font, foreground="#ffffff")
        self.message_area.tag_configure("right", justify=tk.RIGHT, lmargin1=50, lmargin2=10, rmargin=10, spacing3=5,
                                        background="#0078d7", relief=tk.FLAT, borderwidth=0, wrap=tk.WORD,
                                        font=self.font, foreground="#ffffff")
        self.message_area.tag_configure("sender", font=self.bold_font, foreground="#cccccc")

        # Frame para la entrada de texto y botones
        self.input_frame = tk.Frame(root, bg="#252526", padx=10, pady=10)
        self.input_frame.pack(fill=tk.X)

        # Campo de entrada de texto
        self.entry = tk.Entry(self.input_frame, width=30, font=self.font, relief=tk.FLAT, bg="#333333", fg="#ffffff",
                              insertbackground="#ffffff", bd=0, highlightthickness=0)
        self.entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.send_message)

        # Botón para enviar mensaje
        self.send_button = tk.Button(
            self.input_frame, text="➤", font=self.font, bg="#0078d7", fg="white", relief=tk.FLAT,
            command=self.send_message, bd=0, activebackground="#005bb5"
        )
        self.send_button.pack(side=tk.LEFT, padx=5)

        # Alineación por defecto
        self.alignment = "left"

        self.no_history = True
        self.history()
        # while self.no_history:
        #     sleep(1)

        self.update_message()

    def set_alignment(self, alignment):
        self.alignment = alignment

    def send_message(self, event=None):
        if self.current_chat is None:
            print("Selecciona un chat primero")
            return

        message = self.entry.get()
        if message:
            # Cambia los usuarios
            data = {
                "data": encodeb64(formater(myUser, otherUser, datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f"), message))
            }
            post(APIurl + "send", json=data)

            self.set_alignment("left")
            self.display_message(message, self.alignment)
            self.entry.delete(0, tk.END)

    def display_message(self, message, alignment):
        self.message_area.config(state=tk.NORMAL)
        if alignment == "left":
            self.message_area.insert(tk.END, "Tú\n", "sender")
            self.message_area.insert(tk.END, f"{message}\n\n", "left")
        else:
            self.message_area.insert(tk.END, "Otro\n", "sender")
            self.message_area.insert(tk.END, f"{message}\n\n", "right")
        self.message_area.config(state=tk.DISABLED)
        self.message_area.yview(tk.END)  # Desplazar al final

    def update_message(self):
        if self.current_chat is None:
            self.root.after(500, self.update_message)
            return

        data = {
            "user": myUser
        }

        response = post(APIurl + "data", json=data)
        
        content = response.text

        if content != "false":
            self.display_message(content.replace('"', ''), "right")

        self.root.after(500, self.update_message)

    def history(self):
        if self.current_chat is None:
            return

        data = {
            "user": myUser
        }

        response = post(APIurl + "history", json=data)
        
        content = loads(response.text)

        for message in content:
            if message[1] == myUser:
                self.display_message(message[3], "left")
            else:
                self.display_message(message[3], "right")

        self.no_history = False

    def update_chat_buttons(self):
        # Limpiar botones existentes
        for button in self.chat_buttons:
            button.destroy()
        self.chat_buttons.clear()

        # Crear nuevos botones para cada chat
        for chat in self.chats:
            button = tk.Button(
                self.menu_frame, text=chat, font=self.font, bg="#0078d7", fg="white", relief=tk.FLAT,
                command=lambda c=chat: self.select_chat(c)
            )
            button.pack(pady=5, padx=10, fill=tk.X)
            self.chat_buttons.append(button)

    def select_chat(self, chat_name):
        self.current_chat = chat_name
        print(f"Chat seleccionado: {chat_name}")
        # Limpiar el área de mensajes
        self.message_area.config(state=tk.NORMAL)
        self.message_area.delete(1.0, tk.END)
        self.message_area.config(state=tk.DISABLED)
        # Cargar el historial del chat seleccionado
        self.history()

    def add_chat(self, chat_name):
        if chat_name not in self.chats:
            self.chats.append(chat_name)
            self.update_chat_buttons()

if __name__ == "__main__":

    myUser = "user1"
    otherUser = "user2"
    APIurl = "http://127.0.0.1:8000/"
    # APIurl = "http://chatwei.ddns.net:19280/"

    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()