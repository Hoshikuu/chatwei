import tkinter as tk
from tkinter import scrolledtext, font

from weicore.coder import encodeb64
from weicore.cweiFormater import formater

from datetime import datetime
from requests import post

from time import sleep
from json import loads

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat")
        self.root.geometry("1280x720")
        self.bgColor = "#1e1e1e" # Configurar el color de fondo
        self.root.configure(bg=self.bgColor)

        # Frame que ocupa toda la interfaz
        self.mainFrame = tk.Frame(root, bg=self.bgColor)
        self.mainFrame.pack(fill=tk.BOTH, expand=True)

        # Frame donde apareceran los chats disponibles
        self.menuFrame = tk.Frame(self.mainFrame, bg="#252525")
        self.menuFrame.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        self.messageFrame = tk.Frame(self.mainFrame, bg=self.bgColor)
        self.messageFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.scrollBar = tk.Scrollbar(self.messageFrame)

        self.messageArea = scrolledtext.ScrolledText(self.messageFrame, wrap=tk.WORD, yscrollcommand=self.scrollBar.set, bg=self.bgColor, padx=10, pady=10, state=tk.DISABLED, bd=0, highlightthickness=0)
        self.messageArea.pack(fill=tk.BOTH, expand=True)

        self.inputFrame = tk.Frame(root, bg="#252526", padx=10, pady=20)
        self.inputFrame.pack(fill=tk.X)
        
        self.entry = tk.Text(self.inputFrame, wrap=tk.WORD, height=1, bg="#333333", fg="#ffffff", insertbackground="#ffffff", bd=0, highlightthickness=0)
        self.entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        self.entry.bind('<Shift-Return>', lambda event: self.entry.config(height=int(self.entry.index('end-1c').split('.')[0])))
        self.entry.bind("<Return>", self.sendMessage)

        

    def sendMessage(self, event):
        print("hola")




if __name__ == "__main__":

    myUser = "user1"
    otherUser = "user2"
    APIurl = "http://127.0.0.1:8000/"
    # APIurl = "http://chatwei.ddns.net:19280/"

    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()