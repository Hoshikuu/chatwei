import tkinter as tk
from tkinter import ttk
from datetime import datetime
import requests
import json

from weicore.coder import encodeb64
from weicore.cweiFormater import formater
from weicore.cipweiV2 import *

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("chatwei")
        self.root.geometry("900x600")
        self.root.minsize(900, 600)
        
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
        
        self.otherUser = ""
        self.update_message()

        # Datos de ejemplo
        self.chats = [
            {"name": "user2", "last_message": "", "time": ""},
            {"name": "user1", "last_message": "", "time": ""},
        ]
        
        # Añadir chats de ejemplo
        for chat in self.chats:
            self.add_chat_button(chat["name"], chat["last_message"], chat["time"])
        
        # Chat actual
        self.current_chat = "Hola"
        
    def get_last_message(self, otherUser):
        response = requests.post(APIurl + "last", json={"user": myUser, "otherUser": otherUser})
        if response.text == "":
            return ""

        content = json.loads(response.text)
        return "'" + content[3] + "'"

    def get_last_time(self, otherUser):
        response = requests.post(APIurl + "last", json={"user": myUser, "otherUser": otherUser})
        if response.text == "":
            return ""

        content = json.loads(response.text)
        return "'" + content[4] + "'"
    
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
                                    relief=tk.FLAT, command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=5)
        
        # Vincular la tecla Enter para enviar el mensaje
        self.message_entry.bind("<Return>", self.send_message_on_return)
        
    def send_message_on_return(self, event):
        # Enviar mensaje con Enter, pero permitir Shift+Enter para nueva línea
        if not event.state & 0x1: # Shift no está presionado
            self.send_message()
            return "break"  # Evitar el salto de línea predeterminado
    
    def send_message(self):
        message = self.message_entry.get("1.0", tk.END).strip()
        if message:
            self.add_message(message, "Tú", True, datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f"))

            data = {
                "data": encodeb64(formater(myUser, self.otherUser, datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f"), message))
            }
            requests.post(APIurl + "send", json=data)

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
    
    def add_chat_button(self, name, last_message, time):
        # Crear el marco para el botón de chat
        chat_button_frame = tk.Frame(self.chats_frame, bg=self.bg_sidebar, cursor="hand2")
        chat_button_frame.pack(fill=tk.X, pady=2)
        
        # Asegurar que todo el frame actúe como un botón
        chat_button_frame.bind("<Button-1>", lambda e, n=name: self.select_chat(n))
        
        # Añadir avatar (un círculo con la primera letra del nombre)
        avatar_frame = tk.Frame(chat_button_frame, bg=self.accent_color, width=40, height=40)
        avatar_frame.pack(side=tk.LEFT, padx=(5, 10), pady=5)
        avatar_frame.pack_propagate(False)
        
        avatar_label = tk.Label(avatar_frame, text=name[0], font=("Helvetica", 16, "bold"),
                               bg=self.accent_color, fg=self.text_color)
        avatar_label.place(relx=0.5, rely=0.5, anchor="center")
        # Hacer que el label también responda a los clicks
        avatar_label.bind("<Button-1>", lambda e, n=name: self.select_chat(n))
        
        # Añadir información del chat
        chat_info_frame = tk.Frame(chat_button_frame, bg=self.bg_sidebar)
        chat_info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)
        
        name_label = tk.Label(chat_info_frame, text=name, font=("Helvetica", 10, "bold"),
                             bg=self.bg_sidebar, fg=self.text_color, anchor="w")
        name_label.pack(fill=tk.X)
        # Hacer que el label de nombre también responda a los clicks
        name_label.bind("<Button-1>", lambda e, n=name: self.select_chat(n))
        
        message_label = tk.Label(chat_info_frame, text=last_message, font=("Helvetica", 8),
                                bg=self.bg_sidebar, fg="#BBBBBB", anchor="w")
        message_label.pack(fill=tk.X)
        # Hacer que el label de mensaje también responda a los clicks
        message_label.bind("<Button-1>", lambda e, n=name: self.select_chat(n))
        
        # Añadir la hora del último mensaje
        time_label = tk.Label(chat_button_frame, text=time, font=("Helvetica", 8),
                             bg=self.bg_sidebar, fg="#BBBBBB")
        time_label.pack(side=tk.RIGHT, padx=5)
        # Hacer que el label de hora también responda a los clicks
        time_label.bind("<Button-1>", lambda e, n=name: self.select_chat(n))
    
    def update_message(self):
        if self.otherUser != "" and self.otherUser != myUser:
            data = {
                "user": myUser,
                "otherUser": self.otherUser
            }

            response = requests.post(APIurl + "data", json=data)
            
            content = json.loads(response.text)
            
            if content != False:
                self.add_message(content[3], self.otherUser, False, content[4])

        self.root.after(500, self.update_message)

    def chat_history(self):
        data = {
            "user": myUser,
            "otherUser": self.otherUser
        }

        response = requests.post(APIurl + "history", json=data)
        
        content = json.loads(response.text)

        for message in content:
            if message[1] == myUser:
                self.add_message(message[3], message[1], True, message[4])
            else:
                self.add_message(message[3], message[1], False, message[4])

        self.no_history = False

    def select_chat(self, name):
        self.current_chat = name
        self.chat_title.config(text=name)
        self.otherUser = name
        self.clear_messages()
        self.chat_history()
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

if __name__ == "__main__":
    myUser = "user2"
    APIurl = "http://127.0.0.1:8000/"
    # APIurl = "http://chatwei.ddns.net:19280/"

    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()