import tkinter as tk
import requests

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Solicitudes GET en tiempo real")
        self.root.geometry("600x400")
        
        # Etiqueta para mostrar el resultado
        self.result_label = tk.Label(root, text="Cargando...", font=("Arial", 12))
        self.result_label.pack(pady=20)
        
        # Iniciar la primera actualización
        self.update_label()
    
    def update_label(self):
        try:
            response = requests.get("http://127.0.0.1:8000/data")
            response.raise_for_status()  # Lanza error si hay un error HTTP
            
            content = response.text
            
            # Actualiza el Label
            self.result_label.config(text=content)
            
        except requests.exceptions.RequestException as e:
            pass
        self.root.after(1000, self.update_label)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()