import tkinter as tk
import requests
from base64 import b64encode, b64decode
from functions.cweiFormater import formater

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Solicitudes GET en tiempo real")
        self.root.geometry("600x400")
        
        # Etiqueta para mostrar el resultado
        self.result_label = tk.Entry(root, text="", font=("Arial", 12))
        self.result_label.pack(pady=20)
        
        self.send_button = tk.Button(root, text="SEND", font=("Arial", 12), command=self.update_label)
        self.send_button.pack(pady=20)
    
    def encode_base64(self, text):
        encoded_bytes = b64encode(text.encode('utf-8'))
        return encoded_bytes.decode('utf-8')

    def update_label(self):
        try:
            message = self.result_label.get()
            mes = self.encode_base64(formater("user1", "user2", "2025-03-06-00-16-32", message))

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