import tkinter as tk
from tkinter import ttk
import time
import threading
import requests
import json
from datetime import datetime

from weicore.coder import encodeb64
from weicore.cweiKey import *
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
        chat_app = ChatApp(chat_root, username)
        
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
    def __init__(self, root, user):
        self.root = root
        self.root.title("chatwei")
        self.root.geometry(f"900x600+{(root.winfo_screenwidth() - 1300) // 2}+{(root.winfo_screenheight() - 700) // 2}")
        self.root.minsize(900, 600)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Colores para el modo oscuro
        self.bg_dark = "#1E1E1E"
        self.bg_sidebar = "#252526"
        self.bg_chat = "#2D2D30"
        self.text_color = "#FFFFFF"
        self.accent_color = "#007ACC"
        self.message_sent_bg = "#007ACC"
        self.message_received_bg = "#3E3E42"
        self.input_bg = "#3E3E42"
        
        # Configuración del tema
        self.root.configure(bg=self.bg_dark)
        
        # Crear el estilo personalizado para la barra de desplazamiento
        self.create_scrollbar_style()
        
        # Crear los marcos principales
        self.create_main_frames()
        
        # Crear los elementos de la interfaz
        self.create_sidebar()
        self.create_chat_area()
        self.create_input_area()
        
        
        
        self.other_user = ""
        self.user = user

        # Datos de ejemplo
        with open(chatsFile, "r", encoding="utf-8") as file:
            self.chats = json.load(file)
        
        # Añadir chats de ejemplo
        for chat in self.chats:
            self.add_chat_button(chat["id"], chat["user"], chat["name"], chat["last_message"], chat["time"])
        
        # Chat actual
        self.current_chat = ""
        
        self.update_message()
        
    def create_scrollbar_style(self):
        # Estilo para los widgets
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background=self.bg_dark)
        self.style.configure('Sidebar.TFrame', background=self.bg_sidebar)
        self.style.configure('Chat.TFrame', background=self.bg_chat)
        self.style.configure('TButton', background=self.accent_color, foreground=self.text_color)
        self.style.map('TButton', background=[('active', '#0086E3')])
        
        # Estilo minimalista para la barra de desplazamiento
        self.style.configure("Minimal.Vertical.TScrollbar", 
                          gripcount=0, 
                          background="#3E3E42", 
                          darkcolor="#3E3E42", 
                          lightcolor="#3E3E42",
                          troughcolor=self.bg_chat, 
                          bordercolor=self.bg_chat, 
                          arrowcolor=self.bg_chat,
                          arrowsize=0)
        
    def create_main_frames(self):
        # Crear marco principal que contiene todo
        self.main_frame = ttk.Frame(self.root, style='TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear marco izquierdo (sidebar para los chats)
        self.sidebar_frame = ttk.Frame(self.main_frame, style='Sidebar.TFrame', width=250)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        self.sidebar_frame.pack_propagate(False)  # Mantener el tamaño fijo
        
        # Crear marco derecho (área del chat)
        self.right_frame = ttk.Frame(self.main_frame, style='TFrame')
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
    def create_sidebar(self):
        # Título de la barra lateral
        self.sidebar_title = tk.Label(self.sidebar_frame, text="Chats", font=("Helvetica", 14, "bold"),
                                    bg=self.bg_sidebar, fg=self.text_color)
        self.sidebar_title.pack(pady=10, fill=tk.X)
        
        # Separador
        ttk.Separator(self.sidebar_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=5)
        
        # Marco con scrollbar para la lista de chats
        self.chats_container = tk.Frame(self.sidebar_frame, bg=self.bg_sidebar)
        self.chats_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas y scrollbar para la lista de chats
        self.chats_canvas = tk.Canvas(self.chats_container, bg=self.bg_sidebar, highlightthickness=0)
        self.sidebar_scrollbar = ttk.Scrollbar(self.chats_container, orient=tk.VERTICAL, 
                                              command=self.chats_canvas.yview,
                                              style="Minimal.Vertical.TScrollbar")
        self.chats_canvas.configure(yscrollcommand=self.sidebar_scrollbar.set)
        
        # Colocar el scrollbar (oculto hasta que sea necesario)
        self.sidebar_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chats_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame dentro del canvas para contener los botones de chat
        self.chats_frame = tk.Frame(self.chats_canvas, bg=self.bg_sidebar)
        self.chats_canvas.create_window((0, 0), window=self.chats_frame, anchor="nw", tags="self.chats_frame")
        
        self.chats_frame.bind("<Configure>", lambda e: self.chats_canvas.configure(scrollregion=self.chats_canvas.bbox("all")))
        self.chats_canvas.bind("<Configure>", lambda e: self.chats_canvas.itemconfig("self.chats_frame", width=e.width))
        
        # Configurar scrolling con la rueda del ratón
        self.chats_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        
    def on_mousewheel(self, event):
        # Determinar qué canvas debe recibir el evento de desplazamiento
        widget_under_cursor = event.widget.winfo_containing(event.x_root, event.y_root)
        
        # Si el cursor está sobre o dentro del área de chats
        if self.is_widget_in_chats_area(widget_under_cursor):
            self.chats_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        # Si el cursor está sobre o dentro del área de mensajes
        elif self.is_widget_in_messages_area(widget_under_cursor):
            self.chat_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def is_widget_in_chats_area(self, widget):
        # Comprueba si el widget está dentro del área de chats
        parent = widget
        while parent is not None:
            if parent == self.chats_frame or parent == self.chats_canvas:
                return True
            try:
                parent = parent.master
            except:
                break
        return False
    
    def is_widget_in_messages_area(self, widget):
        # Comprueba si el widget está dentro del área de mensajes
        parent = widget
        while parent is not None:
            if parent == self.messages_frame or parent == self.chat_canvas:
                return True
            try:
                parent = parent.master
            except:
                break
        return False
        
    def create_chat_area(self):
        # Título del chat actual
        self.chat_title_frame = tk.Frame(self.right_frame, bg=self.bg_dark)
        self.chat_title_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.chat_title = tk.Label(self.chat_title_frame, text="", font=("Helvetica", 12, "bold"),
                                bg=self.bg_dark, fg=self.text_color)
        self.chat_title.pack(side=tk.LEFT, padx=10)
        
        # Área de mensajes
        self.chat_frame = tk.Frame(self.right_frame, bg=self.bg_chat)
        self.chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Crear canvas y scrollbar para el área de mensajes
        self.chat_canvas = tk.Canvas(self.chat_frame, bg=self.bg_chat, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.chat_frame, orient=tk.VERTICAL, 
                                       command=self.chat_canvas.yview,
                                       style="Minimal.Vertical.TScrollbar")
        self.chat_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame dentro del canvas para contener los mensajes
        self.messages_frame = tk.Frame(self.chat_canvas, bg=self.bg_chat)
        self.chat_canvas_window = self.chat_canvas.create_window((0, 0), window=self.messages_frame, anchor="nw", tags="self.messages_frame")
        
        # Configurar el tamaño del frame de mensajes y la región de desplazamiento
        self.messages_frame.bind("<Configure>", self.on_frame_configure)
        self.chat_canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Asegurar que se vea el último mensaje
        self.root.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)
        
    def on_frame_configure(self, event):
        # Actualizar la región de desplazamiento del canvas cuando el frame cambia de tamaño
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        
    def on_canvas_configure(self, event):
        # Ajustar el ancho del frame de mensajes al ancho del canvas
        canvas_width = event.width
        self.chat_canvas.itemconfig(self.chat_canvas_window, width=canvas_width)

    def create_input_area(self):
        # Área de entrada de mensajes
        self.input_frame = tk.Frame(self.right_frame, bg=self.bg_dark)
        self.input_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.message_entry = tk.Text(self.input_frame, wrap=tk.WORD, height=2, 
                                    bg=self.input_bg, fg=self.text_color,
                                    insertbackground=self.text_color,
                                    font=("Helvetica", 10))
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Botón de enviar
        self.send_button = tk.Button(self.input_frame, text="Enviar", font=("Helvetica", 10),
                                    bg=self.accent_color, fg=self.text_color,
                                    activebackground="#0086E3", activeforeground=self.text_color,
                                    relief=tk.FLAT, command=self.send_message_on_return)
        self.send_button.pack(side=tk.RIGHT, padx=5)
        
        # Vincular la tecla Enter para enviar el mensaje
        self.message_entry.bind("<Return>", self.send_message_on_return)
        
    def send_message_on_return(self, event = None):
        # Enviar mensaje con Enter, pero permitir Shift+Enter para nueva línea
        if event == None:
            self.send_message()
            return "break"  # Evitar el salto de línea predeterminado
        if not event.state & 0x1: # Shift no está presionado
            self.send_message()
            return "break"  # Evitar el salto de línea predeterminado
    
    def send_message(self):
        message = self.message_entry.get("1.0", tk.END).strip()
        if message:
            self.add_message(message, "Tú", True, datetime.now().strftime("%Y-%m-%d-%H-%M"))
            message = encriptA(message, 16, self.key)
            data = {
                "chatid": self.current_chat,
                "id": sha512(message),
                "sender": self.user,
                "receiver": self.other_user,
                "message": message,
                "time": datetime.now().strftime("%Y-%m-%d-%H-%M"),
                "fase": "1"
            }
            requests.post(APIurl + "swap", json=data)

            self.message_entry.delete("1.0", tk.END)
            # Asegurar que el scroll baje completamente para mostrar el mensaje más reciente
            self.root.update_idletasks()  # Actualizar la interfaz para que se creen los widgets
            self.chat_canvas.yview_moveto(1.0)  # Mover al final

    def add_message(self, text, sender, is_sent, current_time):
        # Crear el marco del mensaje
        message_frame = tk.Frame(self.messages_frame, bg=self.bg_chat)
        message_frame.pack(fill=tk.X, pady=5, padx=10)
        
        # Alineación según si es enviado o recibido
        align = tk.RIGHT if is_sent else tk.LEFT
        
        # Crear un marco para el mensaje con esquinas redondeadas
        bubble_bg = self.message_sent_bg if is_sent else self.message_received_bg
        
        # Utilizamos un Frame con relief para dar un efecto de bordes suavizados
        bubble_frame = tk.Frame(message_frame, 
                               bg=bubble_bg,
                               padx=10, pady=5,
                               borderwidth=1,
                               relief=tk.GROOVE)  # GROOVE da un efecto ligeramente redondeado
        bubble_frame.pack(side=align, anchor=tk.NE if is_sent else tk.NW)
        
        # Texto del mensaje
        message_text = tk.Label(bubble_frame, text=text, wraplength=350, justify=tk.LEFT,
                               bg=bubble_bg, fg=self.text_color, font=("Helvetica", 10))
        message_text.pack(fill=tk.X)
        
        # Hora del mensaje
        # current_time = datetime.now().strftime("%H:%M")
        time_label = tk.Label(bubble_frame, text=current_time, font=("Helvetica", 7),
                             bg=bubble_bg, fg=self.text_color)
        time_label.pack(side=tk.RIGHT, padx=(5, 0), pady=(2, 0))
        
        # Desplazar hacia abajo para mostrar el nuevo mensaje
        self.root.update_idletasks()  # Asegurar que la interfaz se actualice
        self.chat_canvas.yview_moveto(1.0)  # Scroll al final
    
    def add_chat_button(self, id, other_user, name, last_message, time):
        # Crear el marco para el botón de chat
        chat_button_frame = tk.Frame(self.chats_frame, bg=self.bg_sidebar, cursor="hand2")
        chat_button_frame.pack(fill=tk.X, pady=2)
        
        # Asegurar que todo el frame actúe como un botón
        chat_button_frame.bind("<Button-1>", lambda e, n=name: self.select_chat(id, other_user, name))
        
        # Añadir avatar (un círculo con la primera letra del nombre)
        avatar_frame = tk.Frame(chat_button_frame, bg=self.accent_color, width=40, height=40)
        avatar_frame.pack(side=tk.LEFT, padx=(5, 10), pady=5)
        avatar_frame.pack_propagate(False)
        
        avatar_label = tk.Label(avatar_frame, text=name[0], font=("Helvetica", 16, "bold"),
                               bg=self.accent_color, fg=self.text_color)
        avatar_label.place(relx=0.5, rely=0.5, anchor="center")
        # Hacer que el label también responda a los clicks
        avatar_label.bind("<Button-1>", lambda e, n=name: self.select_chat(id, other_user, name))
        
        # Añadir información del chat
        chat_info_frame = tk.Frame(chat_button_frame, bg=self.bg_sidebar)
        chat_info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)
        
        name_label = tk.Label(chat_info_frame, text=name, font=("Helvetica", 10, "bold"),
                             bg=self.bg_sidebar, fg=self.text_color, anchor="w")
        name_label.pack(fill=tk.X)
        # Hacer que el label de nombre también responda a los clicks
        name_label.bind("<Button-1>", lambda e, n=name: self.select_chat(id, other_user, name))
        
        message_label = tk.Label(chat_info_frame, text=last_message, font=("Helvetica", 8),
                                bg=self.bg_sidebar, fg="#BBBBBB", anchor="w")
        message_label.pack(fill=tk.X)
        # Hacer que el label de mensaje también responda a los clicks
        message_label.bind("<Button-1>", lambda e, n=name: self.select_chat(id, other_user, name))
        
        # Añadir la hora del último mensaje
        time_label = tk.Label(chat_button_frame, text=time, font=("Helvetica", 8),
                             bg=self.bg_sidebar, fg="#BBBBBB")
        time_label.pack(side=tk.RIGHT, padx=5)
        # Hacer que el label de hora también responda a los clicks
        time_label.bind("<Button-1>", lambda e, n=name: self.select_chat(id, other_user, name))
    
    def update_message(self):
        if self.current_chat == "":
            self.root.after(500, self.update_message)
            return
        
        data = {
            "chatid": self.current_chat,
            "receiver": self.user
        }

        response = requests.post(APIurl + "getswap", json=data)
        if response.text == "[]":
            self.root.after(500, self.update_message)
            return 
        
        content = json.loads(response.text)[0]
        if content[5] == "1":
            data = {
                "chatid": self.current_chat,
                "id": content[0],
                "sender": self.user,
                "receiver": self.other_user,
                "message": encriptB(content[3], 16, self.key),
                "time": datetime.now().strftime("%Y-%m-%d-%H-%M"),
                "fase": "2"
            }
            requests.post(APIurl + "swap", json=data)
        if content[5] == "2":
            data = {
                "chatid": self.current_chat,
                "id": content[0],
                "sender": self.user,
                "receiver": self.other_user,
                "message": decriptA(content[3], 16, self.key),
                "time": datetime.now().strftime("%Y-%m-%d-%H-%M"),
                "fase": "3"
            }
            requests.post(APIurl + "swap", json=data)
        if content[5] == "3":
            message = decriptB(content[3], 16, self.key)
            self.add_message(message, self.other_user, False, datetime.now().strftime("%Y-%m-%d-%H-%M"))

        
        self.root.after(500, self.update_message)

    def chat_history(self):
        data = {
            "user": self.user,
            "other_user": self.other_user
        }

        response = requests.post(APIurl + "history", json=data)
        
        content = json.loads(response.text)

        for message in content:
            if message[1] == self.user:
                self.add_message(message[3], message[1], True, message[4])
            else:
                self.add_message(message[3], message[1], False, message[4])

        self.no_history = False

    def select_chat(self, id, other_user, name):
        self.current_chat = id
        self.chat_title.config(text=name)
        self.other_user = other_user
        self.key = "gulag"
        self.clear_messages()
        # self.chat_history()
        # Aquí normalmente cargarías los mensajes del chat seleccionado
        # Por simplicidad, no implementamos esa funcionalidad en este ejemplo

    def clear_messages(self):
        """
        Elimina todos los mensajes mostrados actualmente en el área de chat.
        """
        # Destruir todos los widgets hijos en el frame de mensajes
        for widget in self.messages_frame.winfo_children():
            widget.destroy()
        
        # Actualizar el canvas después de eliminar los mensajes
        self.root.update_idletasks()
        
        # Reiniciar la región de desplazamiento del canvas
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        
        # Opcional: Mostrar un mensaje indicando que la conversación está vacía
        # empty_frame = tk.Frame(self.messages_frame, bg=self.bg_chat)
        # empty_frame.pack(fill=tk.X, expand=True, pady=20)
        
        # empty_label = tk.Label(empty_frame, 
        #                     text="No hay mensajes en esta conversación",
        #                     font=("Helvetica", 10, "italic"),
        #                     fg="#888888", 
        #                     bg=self.bg_chat)
        # empty_label.pack(pady=30)
        
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
    APIurl = "http://127.0.0.1:8000/"
    chatsFile = "chatsA.json"
    
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()