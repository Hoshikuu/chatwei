import tkinter as tk
from requests import post
from datetime import datetime

from weicore.coder import encodeb64
from weicore.cweiFormater import formater

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CHATWEI")
        self.root.geometry("600x400")
        
        # Etiqueta para mostrar el resultado
        self.message = tk.Label(root, text="", font=("Arial", 12))
        self.message.pack(pady=20)

        self.message_camp = tk.Entry(root, text="", font=("Arial", 12))
        self.message_camp.pack(pady=20)
        
        self.send_button = tk.Button(root, text="SEND", font=("Arial", 12), command=self.send_message)
        self.send_button.pack(pady=20)
        
        # Iniciar la primera actualización
        self.update_label()

    def update_label(self):
        try:
            data = {
                "user": "user2"
            }

            response = post("http://127.0.0.1:8000/data", json=data)
            response.raise_for_status()  # Lanza error si hay un error HTTP
            
            content = response.text

            if content == "false":
                raise Exception
            
            # Actualiza el Label
            self.result_label.config(text=content)
            
        except Exception as e:
            pass
        self.root.after(1000, self.update_label)
    
    def send_message(self):
        try:
            message = self.message_camp.get()
            mes = encodeb64(formater("user1", "user2", datetime.now().strftime("%Y-%m-%d-%H-%M-%S"), message))

            data = {
                "data": mes
            }

            response = post("http://127.0.0.1:8000/send", json=data)
            response.raise_for_status()  # Lanza error si hay un error HTTP
            
            content = response.text
            
            # Actualiza el Label
            self.result_label.config(text=content)
            
        except Exception as e:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()