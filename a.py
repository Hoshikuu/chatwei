import tkinter as tk
from tkinter import ttk
import json
import os
import random

class FriendManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Administrador de Amigos")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        # Color scheme - Dark mode
        self.bg_color = "#1e1e1e"
        self.secondary_bg = "#2d2d2d"
        self.accent_color = "#007acc"
        self.text_color = "#ffffff"
        self.highlight_color = "#3a3a3a"
        
        self.root.configure(bg=self.bg_color)
        
        # Variables
        self.input_text = tk.StringVar()
        self.friends_list = []
        self.current_view = "main"  # main, requests
        
        # Custom styling for dark theme
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('TEntry', fieldbackground=self.secondary_bg, foreground=self.text_color)
        self.style.map('TEntry', fieldbackground=[('focus', self.secondary_bg)])
        
        # Load friends data
        self.load_friends()
        
        # Create frames
        self.create_main_frame()
        self.create_requests_frame()
        
        # Show main view by default
        self.show_main_view()

    def load_friends(self):
        try:
            if os.path.exists("chats.json"):
                with open("chats.json", "r") as f:
                    self.friends_list = json.load(f)
            else:
                # Demo data
                self.friends_list = [
                    {"id": "ebe5328aa981889cc6b2d6129dc073589c7f48c50674401576ec423461885001daf3b5a352cc8d2faf26f1c040be7486aa732300d20ea460f4fdd60ef26a79c9", 
                     "user": "user2", "name": "user2", "last_message": "", "time": ""},
                    {"id": "abc123", "user": "alice", "name": "alice", "last_message": "", "time": ""},
                    {"id": "def456", "user": "bob", "name": "bob", "last_message": "", "time": ""}
                ]
        except Exception as e:
            print(f"Error loading friends: {e}")
            self.friends_list = []

    def create_main_frame(self):
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        
        # Top input area
        input_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.entry = ttk.Entry(input_frame, textvariable=self.input_text, font=("Helvetica", 12))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        send_button = tk.Button(input_frame, text="Enviar", bg=self.accent_color, fg=self.text_color, 
                                command=self.send_message, relief=tk.FLAT, padx=10)
        send_button.pack(side=tk.RIGHT)
        
        # Friends list area
        list_frame = tk.Frame(self.main_frame, bg=self.secondary_bg)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.friends_canvas = tk.Canvas(list_frame, bg=self.secondary_bg, highlightthickness=0)
        self.friends_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.friends_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.friends_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.friends_container = tk.Frame(self.friends_canvas, bg=self.secondary_bg)
        self.friends_canvas_window = self.friends_canvas.create_window((0, 0), window=self.friends_container, anchor=tk.NW)
        
        self.friends_container.bind("<Configure>", lambda e: self.friends_canvas.configure(
            scrollregion=self.friends_canvas.bbox("all")))
        
        # Toolbar
        toolbar_frame = tk.Frame(self.main_frame, bg=self.bg_color, height=50)
        toolbar_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)
        
        requests_button = tk.Button(toolbar_frame, text="Solicitudes", bg=self.accent_color, fg=self.text_color,
                                  command=self.show_requests_view, relief=tk.FLAT, padx=10)
        requests_button.pack(side=tk.LEFT, padx=5)
        
    def create_requests_frame(self):
        self.requests_frame = tk.Frame(self.root, bg=self.bg_color)
        
        # Header
        header_frame = tk.Frame(self.requests_frame, bg=self.bg_color)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        back_button = tk.Button(header_frame, text="← Atrás", bg=self.accent_color, fg=self.text_color,
                               command=self.show_main_view, relief=tk.FLAT, padx=10)
        back_button.pack(side=tk.LEFT)
        
        label = tk.Label(header_frame, text="Solicitudes de amistad", bg=self.bg_color, fg=self.text_color, font=("Helvetica", 12, "bold"))
        label.pack(side=tk.LEFT, padx=10)
        
        # Requests list area
        list_frame = tk.Frame(self.requests_frame, bg=self.secondary_bg)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Demo requests
        for i in range(3):
            request_frame = tk.Frame(list_frame, bg=self.secondary_bg, padx=5, pady=5, relief=tk.FLAT, bd=1)
            request_frame.pack(fill=tk.X, pady=2)
            
            # Avatar - using a simple colored label instead of PIL
            avatar_label = self.create_simple_avatar(request_frame, f"req{i}")
            avatar_label.pack(side=tk.LEFT, padx=5)
            
            # Username
            username_label = tk.Label(request_frame, text=f"request_user{i}", bg=self.secondary_bg, fg=self.text_color, font=("Helvetica", 11))
            username_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True, anchor=tk.W)
            
            # Buttons
            buttons_frame = tk.Frame(request_frame, bg=self.secondary_bg)
            buttons_frame.pack(side=tk.RIGHT)
            
            accept_button = tk.Button(buttons_frame, text="✓", bg="#2ecc71", fg=self.text_color, 
                                     relief=tk.FLAT, width=2, command=lambda i=i: self.accept_request(i))
            accept_button.pack(side=tk.LEFT, padx=2)
            
            reject_button = tk.Button(buttons_frame, text="✗", bg="#e74c3c", fg=self.text_color, 
                                     relief=tk.FLAT, width=2, command=lambda i=i: self.reject_request(i))
            reject_button.pack(side=tk.LEFT, padx=2)

    def show_main_view(self):
        self.current_view = "main"
        self.requests_frame.pack_forget()
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Clear previous friends list
        for widget in self.friends_container.winfo_children():
            widget.destroy()
        
        # Populate friends list
        for friend in self.friends_list:
            friend_frame = tk.Frame(self.friends_container, bg=self.secondary_bg, padx=5, pady=8, relief=tk.FLAT, bd=1)
            friend_frame.pack(fill=tk.X, pady=1)
            
            # Avatar - simple colored label
            avatar_label = self.create_simple_avatar(friend_frame, friend["user"])
            avatar_label.pack(side=tk.LEFT, padx=5)
            
            # Username
            username_label = tk.Label(friend_frame, text=friend["user"], bg=self.secondary_bg, fg=self.text_color, font=("Helvetica", 11))
            username_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True, anchor=tk.W)
            
            # Chat button
            chat_button = tk.Button(friend_frame, text="Chat", bg=self.accent_color, fg=self.text_color, 
                                   relief=tk.FLAT, padx=10, command=lambda u=friend["user"]: self.open_chat(u))
            chat_button.pack(side=tk.RIGHT, padx=5)

    def show_requests_view(self):
        self.current_view = "requests"
        self.main_frame.pack_forget()
        self.requests_frame.pack(fill=tk.BOTH, expand=True)

    def open_chat(self, username):
        print(f"Abriendo chat con: {username}")
        # Aquí iría el código para comunicarse con la aplicación de chat separada

    def send_message(self):
        text = self.input_text.get()
        if text:
            print(f"Texto enviado: {text}")
            self.input_text.set("")

    def accept_request(self, index):
        print(f"Solicitud aceptada: {index}")
        self.show_main_view()

    def reject_request(self, index):
        print(f"Solicitud rechazada: {index}")

    def create_simple_avatar(self, parent, username):
        # Generate a consistent color based on username
        random.seed(username)
        r = random.randint(30, 200)
        g = random.randint(30, 200)
        b = random.randint(30, 200)
        color = f"#{r:02x}{g:02x}{b:02x}"
        
        # First letter of username
        letter = username[0].upper()
        
        # Create a frame with fixed size to simulate a circle
        size = 32
        avatar_frame = tk.Frame(parent, width=size, height=size, bg=color)
        avatar_frame.pack_propagate(False)  # Prevent frame from shrinking to fit content
        
        # Add label with letter
        letter_label = tk.Label(avatar_frame, text=letter, fg="white", bg=color, font=("Helvetica", 14, "bold"))
        letter_label.place(relx=0.5, rely=0.5, anchor="center")  # Center the letter
        
        return avatar_frame

if __name__ == "__main__":
    root = tk.Tk()
    app = FriendManager(root)
    root.mainloop()