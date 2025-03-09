import tkinter as tk
from tkinter import scrolledtext, font

from weicore.coder import encodeb64
from weicore.cweiFormater import formater

from datetime import datetime
from requests import post

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat")
        self.root.geometry("400x500")
        self.root.configure(bg="#1e1e1e")  # Fondo oscuro

        # Fuente moderna
        self.font = ("Segoe UI", 10)
        self.bold_font = ("Segoe UI", 10, "bold")

        # Frame para los mensajes
        self.message_frame = tk.Frame(root, bg="#1e1e1e")
        self.message_frame.pack(fill=tk.BOTH, expand=True)

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

        self.update_message()

    def set_alignment(self, alignment):
        self.alignment = alignment

    def send_message(self, event=None):
        message = self.entry.get()
        if message:
            # Cambia los usuarios
            data = {
                "data": encodeb64(formater("user1", "user2", datetime.now().strftime("%Y-%m-%d-%H-%M-%S"), message))
            }
            post("http://127.0.0.1:8000/send", json=data)

            self.set_alignment("left")
            self.display_message(message, self.alignment)
            self.entry.delete(0, tk.END)

            # response = post("http://127.0.0.1:8000/send", json=data)
            # response.raise_for_status()  # Lanza error si hay un error HTTP
            
            # content = response.text

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
        data = {
            "user": "user1"
        }

        response = post("http://127.0.0.1:8000/data", json=data)
        
        content = response.text

        if content != "false":
            self.set_alignment("right")
            self.display_message(content.replace('"', ''), self.alignment)

        self.root.after(1000, self.update_message)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()