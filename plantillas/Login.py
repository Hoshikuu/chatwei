import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat App - Inicio de Sesión")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Configuración visual
        self.root.configure(bg="#f0f0f0")
        
        # Frame principal
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        self.title_label = tk.Label(self.main_frame, text="Iniciar Sesión", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        self.title_label.pack(pady=10)
        
        # Usuario
        self.username_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.username_frame.pack(fill='x', pady=10)
        
        self.username_label = tk.Label(self.username_frame, text="Usuario:", bg="#f0f0f0", font=("Helvetica", 12))
        self.username_label.pack(anchor='w')
        
        self.username_entry = tk.Entry(self.username_frame, font=("Helvetica", 12))
        self.username_entry.pack(fill='x', pady=5)
        
        # Contraseña
        self.password_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.password_frame.pack(fill='x', pady=10)
        
        self.password_label = tk.Label(self.password_frame, text="Contraseña:", bg="#f0f0f0", font=("Helvetica", 12))
        self.password_label.pack(anchor='w')
        
        self.password_entry = tk.Entry(self.password_frame, show="•", font=("Helvetica", 12))
        self.password_entry.pack(fill='x', pady=5)
        
        # Botón de iniciar sesión
        self.login_button = tk.Button(self.main_frame, text="Iniciar Sesión", command=self.login, 
                                     bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"),
                                     activebackground="#45a049", relief=tk.RAISED, bd=0,
                                     padx=20, pady=5)
        self.login_button.pack(pady=20)
        
        # Estado
        self.status_label = tk.Label(self.main_frame, text="", fg="red", bg="#f0f0f0")
        self.status_label.pack()
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Aquí deberías implementar la verificación de credenciales con tu base de datos
        # Por ahora, simularemos una autenticación simple
        if username and password:  # Validación simple
            self.status_label.config(text="Iniciando sesión...", fg="blue")
            self.root.update()
            
            # Simulamos verificación
            time.sleep(1)
            
            # Si la autenticación es exitosa
            self.root.withdraw()  # Ocultamos la ventana de login
            
            # Iniciamos la ventana principal de chat y el gestor de amigos
            self.open_main_windows(username)
        else:
            self.status_label.config(text="Usuario y contraseña son requeridos", fg="red")
    
    def open_main_windows(self, username):
        # Crear una nueva ventana para el chat
        chat_root = tk.Toplevel()
        
        # Iniciar las clases de chat y gestor de amigos
        chat_app = ChatWindow(chat_root, username)
        
        # Crear ventana para el gestor de amigos
        friends_root = tk.Toplevel()
        friends_manager = FriendsManager(friends_root, username, chat_app)
        
        # Vincular el gestor de amigos con el chat
        chat_app.set_friends_manager(friends_manager)


class ChatWindow:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.friends_manager = None
        
        self.root.title(f"Chat - {username}")
        self.root.geometry("600x500")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Frame principal con dos paneles
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill='both')
        
        # Panel de mensajes (70% del ancho)
        self.messages_frame = tk.Frame(self.main_frame, bg="white")
        self.messages_frame.pack(side=tk.LEFT, fill='both', expand=True)
        
        # Área de mensajes
        self.message_area = tk.Text(self.messages_frame, state='disabled', wrap=tk.WORD,
                                   font=("Helvetica", 11), bd=0, bg="#f9f9f9")
        self.message_area.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Scrollbar para el área de mensajes
        scrollbar = tk.Scrollbar(self.message_area)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        self.message_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.message_area.yview)
        
        # Frame para la entrada de texto y botón
        self.input_frame = tk.Frame(self.messages_frame)
        self.input_frame.pack(fill='x', padx=10, pady=10)
        
        # Entrada de texto
        self.message_entry = tk.Entry(self.input_frame, font=("Helvetica", 11))
        self.message_entry.pack(side=tk.LEFT, fill='x', expand=True, padx=(0, 5))
        self.message_entry.bind("<Return>", lambda event: self.send_message())
        
        # Botón de enviar
        self.send_button = tk.Button(self.input_frame, text="Enviar", command=self.send_message,
                                    bg="#4CAF50", fg="white")
        self.send_button.pack(side=tk.RIGHT)
        
        # Actualizar el área de mensajes con mensaje de bienvenida
        self.update_message_area(f"Bienvenido {username}! Selecciona un amigo para chatear.")

    def set_friends_manager(self, friends_manager):
        self.friends_manager = friends_manager
    
    def update_message_area(self, message):
        self.message_area.config(state='normal')
        self.message_area.insert(tk.END, message + "\n")
        self.message_area.see(tk.END)
        self.message_area.config(state='disabled')
    
    def send_message(self):
        message = self.message_entry.get().strip()
        if message:
            # Aquí implementarías el envío del mensaje al destinatario seleccionado
            self.update_message_area(f"Tú: {message}")
            self.message_entry.delete(0, tk.END)
    
    def on_closing(self):
        # Cerrar también la ventana de amigos si está abierta
        if self.friends_manager:
            self.friends_manager.root.destroy()
        self.root.destroy()


class FriendsManager:
    def __init__(self, root, username, chat_app):
        self.root = root
        self.username = username
        self.chat_app = chat_app
        
        self.root.title(f"Amigos - {username}")
        self.root.geometry("300x500")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Frame de búsqueda
        self.search_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.search_frame.pack(fill='x', padx=10, pady=10)
        
        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT, fill='x', expand=True, padx=(0, 5))
        
        self.search_button = tk.Button(self.search_frame, text="Buscar", bg="#4CAF50", fg="white")
        self.search_button.pack(side=tk.RIGHT)
        
        # Pestañas para amigos y solicitudes
        self.tab_control = ttk.Notebook(self.root)
        
        # Tab de amigos
        self.friends_tab = tk.Frame(self.tab_control)
        self.tab_control.add(self.friends_tab, text="Amigos")
        
        # Lista de amigos
        self.friends_listbox = tk.Listbox(self.friends_tab, font=("Helvetica", 11), bd=0,
                                        selectbackground="#4CAF50")
        self.friends_listbox.pack(expand=True, fill='both', padx=10, pady=10)
        self.friends_listbox.bind("<Double-1>", self.start_chat)
        
        # Scrollbar para la lista de amigos
        scrollbar = tk.Scrollbar(self.friends_listbox)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        self.friends_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.friends_listbox.yview)
        
        # Tab de solicitudes
        self.requests_tab = tk.Frame(self.tab_control)
        self.tab_control.add(self.requests_tab, text="Solicitudes")
        
        # Lista de solicitudes
        self.requests_listbox = tk.Listbox(self.requests_tab, font=("Helvetica", 11), bd=0,
                                         selectbackground="#4CAF50")
        self.requests_listbox.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Frame para botones de aceptar/rechazar
        self.request_buttons_frame = tk.Frame(self.requests_tab)
        self.request_buttons_frame.pack(fill='x', padx=10, pady=5)
        
        self.accept_button = tk.Button(self.request_buttons_frame, text="Aceptar", bg="#4CAF50", fg="white")
        self.accept_button.pack(side=tk.LEFT, padx=(0, 5), expand=True, fill='x')
        
        self.reject_button = tk.Button(self.request_buttons_frame, text="Rechazar", bg="#f44336", fg="white")
        self.reject_button.pack(side=tk.RIGHT, expand=True, fill='x')
        
        self.tab_control.pack(expand=True, fill='both')
        
        # Cargar amigos de ejemplo
        self.load_sample_friends()
    
    def load_sample_friends(self):
        # Esto es solo para demostración, deberías cargar amigos desde tu base de datos
        sample_friends = ["Ana", "Carlos", "Elena", "Miguel", "Sofía"]
        for friend in sample_friends:
            self.friends_listbox.insert(tk.END, friend)
    
    def start_chat(self, event):
        # Obtener el amigo seleccionado
        selection = self.friends_listbox.curselection()
        if selection:
            friend = self.friends_listbox.get(selection[0])
            # Actualizar el chat para mostrar que estamos chateando con este amigo
            self.chat_app.update_message_area(f"--- Iniciando chat con {friend} ---")
    
    def on_closing(self):
        # Cerrar también la ventana de chat si está abierta
        self.chat_app.root.destroy()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()