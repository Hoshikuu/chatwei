import tkinter as tk
from tkinter import ttk
import time
import threading
import requests

from weicore.coder import encodeb64
from weicore.cweiFormater import formater
from weicore.cipweiV2 import *

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatWei - Login")
        self.root.geometry(f"400x350+{(root.winfo_screenwidth() - 400) // 2}+{(root.winfo_screenheight() - 450) // 2}")
        self.root.resizable(False, False)
        
        # Configuración tema oscuro
        self.bg_color = "#1e1e1e"
        self.fg_color = "#e0e0e0"
        self.accent_color = "#3700B3"
        self.entry_bg = "#2d2d2d"
        self.button_color = "#6200EE"
        self.button_hover = "#7722FF"
        self.register_color = "#404040"  # Color más sutil para el botón de registro
        self.register_hover = "#505050"
        
        self.root.configure(bg=self.bg_color)
        
        # Frame principal
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        self.title_label = tk.Label(self.main_frame, text="ChatWei", 
                                   font=("Helvetica", 18, "bold"), 
                                   bg=self.bg_color, fg=self.fg_color)
        self.title_label.pack(pady=10)
        
        # Usuario
        self.username_label = tk.Label(self.main_frame, text="Usuario", 
                                     bg=self.bg_color, fg=self.fg_color,
                                     font=("Helvetica", 10))
        self.username_label.pack(anchor='w')
        
        self.username_entry = tk.Entry(self.main_frame, font=("Helvetica", 11),
                                     bg=self.entry_bg, fg=self.fg_color,
                                     insertbackground=self.fg_color,
                                     relief=tk.FLAT, bd=5)
        self.username_entry.pack(fill='x', pady=5)
        
        # Contraseña
        self.password_label = tk.Label(self.main_frame, text="Contraseña", 
                                     bg=self.bg_color, fg=self.fg_color,
                                     font=("Helvetica", 10))
        self.password_label.pack(anchor='w', pady=(10, 0))
        
        self.password_entry = tk.Entry(self.main_frame, show="•", font=("Helvetica", 11),
                                     bg=self.entry_bg, fg=self.fg_color,
                                     insertbackground=self.fg_color,
                                     relief=tk.FLAT, bd=5)
        self.password_entry.pack(fill='x', pady=5)
        
        # Botón de iniciar sesión
        self.login_button = tk.Button(self.main_frame, text="Iniciar Sesión", 
                                    command=self.login, 
                                    bg=self.button_color, fg=self.fg_color,
                                    font=("Helvetica", 11),
                                    activebackground=self.button_hover,
                                    activeforeground=self.fg_color,
                                    relief=tk.FLAT, bd=0,
                                    padx=10, pady=5,
                                    cursor="hand2")
        self.login_button.pack(pady=15)
        
        # Botón para crear nuevo usuario
        self.register_button = tk.Button(self.main_frame, text="Crear usuario nuevo", 
                                      command=self.open_register, 
                                      bg=self.register_color, fg=self.fg_color,
                                      font=("Helvetica", 10),
                                      activebackground=self.register_hover,
                                      activeforeground=self.fg_color,
                                      relief=tk.FLAT, bd=0,
                                      padx=8, pady=3,
                                      cursor="hand2")
        self.register_button.pack()
        
        # Estado
        self.status_label = tk.Label(self.main_frame, text="", fg="#ff5252", bg=self.bg_color)
        self.status_label.pack(pady=(10, 0))
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username and password:
            self.status_label.config(text="Conectando...", fg="#4fc3f7")
            self.root.update()
            
            data = {
                "user": username,
                "password": sha512(password)
            }
            
            response = requests.post(APIurl + "login", json=data).text
            if response == '"OK"':
                self.root.withdraw()
                self.open_main_windows(username)
            else:
                self.status_label.config(text="Error en la contraseña o usuario", fg="#ff5252")
        else:
            self.status_label.config(text="Completa todos los campos", fg="#ff5252")
    
    def open_register(self):
        # Abre la ventana de registro
        self.root.withdraw()
        register_window = tk.Toplevel(self.root)
        RegisterWindow(register_window, self)
    
    def open_main_windows(self, username):
        # Crear ventana para el chat
        chat_root = tk.Toplevel()
        chat_app = ChatApp(chat_root)
        
        # Crear ventana para el gestor de amigos
        friends_root = tk.Toplevel()
        friends_manager = FriendsManager(friends_root)
        
        # Vincular el gestor de amigos con el chat
        chat_app.set_friends_manager(friends_manager)
        friends_manager.set_chat_app(chat_app)

class RegisterWindow:
    def __init__(self, root, login_window):
        self.root = root
        self.login_window = login_window
        self.root.title("ChatWei - Registro")
        self.root.geometry(f"400x450+{(root.winfo_screenwidth() - 400) // 2}+{(root.winfo_screenheight() - 550) // 2}")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Usar los mismos colores que la ventana de login
        self.bg_color = self.login_window.bg_color
        self.fg_color = self.login_window.fg_color
        self.entry_bg = self.login_window.entry_bg
        self.button_color = self.login_window.button_color
        self.button_hover = self.login_window.button_hover
        
        self.root.configure(bg=self.bg_color)
        
        # Frame principal
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        self.title_label = tk.Label(self.main_frame, text="Crear usuario", 
                                   font=("Helvetica", 16, "bold"), 
                                   bg=self.bg_color, fg=self.fg_color)
        self.title_label.pack(pady=10)
        
        # Usuario
        self.username_label = tk.Label(self.main_frame, text="Usuario", 
                                     bg=self.bg_color, fg=self.fg_color,
                                     font=("Helvetica", 10))
        self.username_label.pack(anchor='w')
        
        self.username_entry = tk.Entry(self.main_frame, font=("Helvetica", 11),
                                     bg=self.entry_bg, fg=self.fg_color,
                                     insertbackground=self.fg_color,
                                     relief=tk.FLAT, bd=5)
        self.username_entry.pack(fill='x', pady=5)
        
        # email
        self.email_label = tk.Label(self.main_frame, text="Email", 
                                     bg=self.bg_color, fg=self.fg_color,
                                     font=("Helvetica", 10))
        self.email_label.pack(anchor='w')
        
        self.email_entry = tk.Entry(self.main_frame, font=("Helvetica", 11),
                                     bg=self.entry_bg, fg=self.fg_color,
                                     insertbackground=self.fg_color,
                                     relief=tk.FLAT, bd=5)
        self.email_entry.pack(fill='x', pady=5)
        
        # Contraseña
        self.password_label = tk.Label(self.main_frame, text="Contraseña", 
                                     bg=self.bg_color, fg=self.fg_color,
                                     font=("Helvetica", 10))
        self.password_label.pack(anchor='w', pady=(10, 0))
        
        self.password_entry = tk.Entry(self.main_frame, show="•", font=("Helvetica", 11),
                                     bg=self.entry_bg, fg=self.fg_color,
                                     insertbackground=self.fg_color,
                                     relief=tk.FLAT, bd=5)
        self.password_entry.pack(fill='x', pady=5)
        
        # Confirmar contraseña
        self.confirm_label = tk.Label(self.main_frame, text="Confirmar contraseña", 
                                    bg=self.bg_color, fg=self.fg_color,
                                    font=("Helvetica", 10))
        self.confirm_label.pack(anchor='w', pady=(10, 0))
        
        self.confirm_entry = tk.Entry(self.main_frame, show="•", font=("Helvetica", 11),
                                    bg=self.entry_bg, fg=self.fg_color,
                                    insertbackground=self.fg_color,
                                    relief=tk.FLAT, bd=5)
        self.confirm_entry.pack(fill='x', pady=5)
        
        # Botón de registrar
        self.register_button = tk.Button(self.main_frame, text="Registrar", 
                                       command=self.register, 
                                       bg=self.button_color, fg=self.fg_color,
                                       font=("Helvetica", 11),
                                       activebackground=self.button_hover,
                                       activeforeground=self.fg_color,
                                       relief=tk.FLAT, bd=0,
                                       padx=10, pady=5,
                                       cursor="hand2")
        self.register_button.pack(pady=15)
        
        # Estado
        self.status_label = tk.Label(self.main_frame, text="", fg="#ff5252", bg=self.bg_color)
        self.status_label.pack()
    
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()
        email = self.email_entry.get()
        
        if not username or not password or not confirm:
            self.status_label.config(text="Completa todos los campos", fg="#ff5252")
            return
            
        if password != confirm:
            self.status_label.config(text="Las contraseñas no coinciden", fg="#ff5252")
            return
            
        # Aquí implementarías la lógica para crear el usuario en tu sistema
        self.status_label.config(text="Creando usuario...", fg="#4fc3f7")
        self.root.update()
        
        data = {
            "user": username,
            "password": sha512(password),
            "email": email
        }
        
        # Simulamos proceso de registro
        response = requests.post(APIurl + "adduser", json=data).text
        
        if response == '"BAD"':
            self.status_label.config(text="Usuario o email existentes", fg="#ff5252")
            return
        
        # Una vez registrado exitosamente
        self.status_label.config(text="Usuario creado con éxito", fg="#66bb6a")
        self.root.update()
        time.sleep(1)
        
        # Cerrar ventana de registro y volver al login
        self.login_window.root.deiconify()
        self.root.destroy()
    
    def on_closing(self):
        self.login_window.root.deiconify()
        self.root.destroy()

class ChatApp:
    def __init__(self, root):
        # Implementación simplificada
        self.root = root
        self.root.title("ChatWei - Chat")
        self.root.geometry(f"900x600+{(root.winfo_screenwidth() - 1300) // 2}+{(root.winfo_screenheight() - 700) // 2}")
        self.root.configure(bg="#1e1e1e")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def set_friends_manager(self, friends_manager):
        self.friends_manager = friends_manager
        
    def on_closing(self):
        self.friends_manager.root.destroy()
        self.root.destroy()
        root.destroy()

class FriendsManager:
    def __init__(self, root):
        # Implementación simplificada
        self.root = root
        self.root.title("ChatWei - Contactos")
        self.root.geometry(f"400x600+{(root.winfo_screenwidth() + 500) // 2}+{(root.winfo_screenheight() - 700) // 2}")
        self.root.configure(bg="#1e1e1e")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def set_chat_app(self, chat_app):
        self.chat_app = chat_app
    
    def on_closing(self):
        self.chat_app.root.destroy()
        self.root.destroy()
        root.destroy()

if __name__ == "__main__":
    myUser = "user2"
    APIurl = "http://127.0.0.1:8000/"
    chatsFile = "chats.json"
    
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()