import tkinter as tk
import requests
from base64 import b64encode
from functions.cweiFormater import formater
from datetime import datetime

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Solicitudes GET en tiempo real")
        self.root.geometry("600x400")
        
        # Etiqueta para mostrar el resultado
        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.pack(pady=20)

        self.message_camp = tk.Entry(root, text="", font=("Arial", 12))
        self.message_camp.pack(pady=20)
        
        self.send_button = tk.Button(root, text="SEND", font=("Arial", 12), command=self.send_message)
        self.send_button.pack(pady=20)
        
        # Iniciar la primera actualización
        self.update_label()
    
    def encode_base64(self, text):
        encoded_bytes = b64encode(text.encode('utf-8'))
        return encoded_bytes.decode('utf-8')

    def update_label(self):
        try:
            data = {
                "user": "user2"
            }

            response = requests.post("http://127.0.0.1:8000/data", json=data)
            response.raise_for_status()  # Lanza error si hay un error HTTP
            
            content = response.text

            if content == "false":
                raise requests.exceptions.RequestException
            
            # Actualiza el Label
            self.result_label.config(text=content)
            
        except requests.exceptions.RequestException as e:
            pass
        self.root.after(1000, self.update_label)
    
    def send_message(self):
        try:
            message = self.message_camp.get()
            mes = self.encode_base64(formater("user1", "user2", datetime.now().strftime("%Y-%m-%d-%H-%M-%S"), message))

            data = {
                "data": mes
            }

            response = requests.post("http://127.0.0.1:8000/send", json=data)
            response.raise_for_status()  # Lanza error si hay un error HTTP
            
            content = response.text
            
            # Actualiza el Label
            self.result_label.config(text=content)
            
        except requests.exceptions.RequestException as e:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()