import tkinter as tk
from tkinter import ttk, messagebox

class ChatMinimalista:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat")
        self.root.geometry("500x400")
        
        # Configurar tema oscuro
        self.configurar_tema_oscuro()
        
        # Cargar datos
        self.cargar_datos()
        
        # Crear la interfaz
        self.crear_interfaz()
    
    def configurar_tema_oscuro(self):
        # Colores para el tema oscuro
        self.bg_color = "#1E1E1E"  # Fondo principal
        self.fg_color = "#FFFFFF"  # Color de texto
        self.accent_color = "#0078D7"  # Color de acento
        self.second_bg = "#252526"  # Segundo color de fondo
        self.highlight = "#3E3E42"  # Color de resaltado
        
        self.root.configure(bg=self.bg_color)
        
        # Estilo para los widgets
        self.style = ttk.Style()
        self.style.theme_use("default")
        
        # Configurar estilo para Treeview
        self.style.configure("Treeview", 
                             background=self.second_bg, 
                             foreground=self.fg_color, 
                             fieldbackground=self.second_bg)
        
        self.style.map("Treeview", 
                       background=[('selected', self.accent_color)])
        
        # Configurar estilo para botones
        self.style.configure("TButton", 
                             background=self.accent_color, 
                             foreground=self.fg_color)
    
    def cargar_datos(self):
        # Datos de ejemplo
        self.amigos = [
            {"nombre": "Ana", "estado": "online"},
            {"nombre": "Carlos", "estado": "offline"},
            {"nombre": "Elena", "estado": "online"}
        ]
        
        self.solicitudes = [
            {"nombre": "Roberto"},
            {"nombre": "Laura"}
        ]
    
    def crear_interfaz(self):
        # Panel principal
        self.panel_principal = tk.PanedWindow(self.root, bg=self.bg_color, 
                                              sashwidth=1, sashrelief="solid")
        self.panel_principal.pack(fill="both", expand=True)
        
        # Panel izquierdo (Amigos)
        self.frame_amigos = tk.Frame(self.panel_principal, bg=self.bg_color)
        self.panel_principal.add(self.frame_amigos, width=300)
        
        # Título de amigos con estilo minimalista
        tk.Label(self.frame_amigos, text="AMIGOS", font=("Arial", 10), 
                 bg=self.bg_color, fg=self.fg_color).pack(anchor="w", padx=10, pady=(10, 5))
        
        # Lista de amigos
        self.frame_lista_amigos = tk.Frame(self.frame_amigos, bg=self.second_bg)
        self.frame_lista_amigos.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.lista_amigos = ttk.Treeview(self.frame_lista_amigos, show="tree", 
                                          selectmode="browse", height=12)
        self.lista_amigos.heading("#0", text="")
        self.lista_amigos.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(self.frame_lista_amigos, orient="vertical", 
                                   command=self.lista_amigos.yview)
        scrollbar.pack(side="right", fill="y")
        self.lista_amigos.configure(yscroll=scrollbar.set)
        
        # Panel derecho (Solicitudes)
        self.frame_solicitudes = tk.Frame(self.panel_principal, bg=self.bg_color)
        self.panel_principal.add(self.frame_solicitudes)
        
        # Título de solicitudes
        tk.Label(self.frame_solicitudes, text="SOLICITUDES", font=("Arial", 10), 
                 bg=self.bg_color, fg=self.fg_color).pack(anchor="w", padx=10, pady=(10, 5))
        
        # Lista de solicitudes
        self.frame_lista_solicitudes = tk.Frame(self.frame_solicitudes, bg=self.second_bg)
        self.frame_lista_solicitudes.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.lista_solicitudes = ttk.Treeview(self.frame_lista_solicitudes, show="tree", 
                                              selectmode="browse", height=6)
        self.lista_solicitudes.heading("#0", text="")
        self.lista_solicitudes.pack(side="left", fill="both", expand=True)
        
        scrollbar_solicitudes = ttk.Scrollbar(self.frame_lista_solicitudes, orient="vertical", 
                                              command=self.lista_solicitudes.yview)
        scrollbar_solicitudes.pack(side="right", fill="y")
        self.lista_solicitudes.configure(yscroll=scrollbar_solicitudes.set)
        
        # Barra inferior con botones
        self.frame_botones = tk.Frame(self.root, bg=self.highlight, height=40)
        self.frame_botones.pack(fill="x", side="bottom")
        
        # Botones minimalistas con iconos simbólicos
        self.btn_mensaje = tk.Button(self.frame_botones, text="💬", font=("Arial", 12), 
                                    bg=self.highlight, fg=self.fg_color, bd=0, 
                                    activebackground=self.accent_color, width=3,
                                    command=self.enviar_mensaje)
        self.btn_mensaje.pack(side="left", padx=10, pady=5)
        
        self.btn_agregar = tk.Button(self.frame_botones, text="➕", font=("Arial", 12), 
                                    bg=self.highlight, fg=self.fg_color, bd=0, 
                                    activebackground=self.accent_color, width=3,
                                    command=self.mostrar_agregar)
        self.btn_agregar.pack(side="left", padx=10, pady=5)
        
        self.btn_aceptar = tk.Button(self.frame_botones, text="✓", font=("Arial", 12), 
                                   bg=self.highlight, fg="#4CAF50", bd=0, 
                                   activebackground=self.accent_color, width=3,
                                   command=self.aceptar_solicitud)
        self.btn_aceptar.pack(side="right", padx=10, pady=5)
        
        self.btn_rechazar = tk.Button(self.frame_botones, text="✗", font=("Arial", 12), 
                                    bg=self.highlight, fg="#F44336", bd=0, 
                                    activebackground=self.accent_color, width=3,
                                    command=self.rechazar_solicitud)
        self.btn_rechazar.pack(side="right", padx=10, pady=5)
        
        # Actualizar listas
        self.actualizar_listas()
    
    def actualizar_listas(self):
        # Limpiar listas
        for item in self.lista_amigos.get_children():
            self.lista_amigos.delete(item)
        
        for item in self.lista_solicitudes.get_children():
            self.lista_solicitudes.delete(item)
        
        # Llenar lista de amigos
        for amigo in self.amigos:
            tag = amigo["estado"]
            self.lista_amigos.insert("", "end", text=amigo["nombre"], tags=(tag,))
        
        # Configurar colores según estado
        self.lista_amigos.tag_configure("online", foreground="#4CAF50")
        self.lista_amigos.tag_configure("offline", foreground="#9E9E9E")
        
        # Llenar lista de solicitudes
        for solicitud in self.solicitudes:
            self.lista_solicitudes.insert("", "end", text=solicitud["nombre"])
    
    def enviar_mensaje(self):
        seleccion = self.lista_amigos.selection()
        if not seleccion:
            return
        
        amigo = self.lista_amigos.item(seleccion[0])["text"]
        messagebox.showinfo("Chat", f"Iniciando chat con {amigo}")
    
    def mostrar_agregar(self):
        # Ventana emergente minimalista
        self.ventana_agregar = tk.Toplevel(self.root)
        self.ventana_agregar.title("Agregar")
        self.ventana_agregar.geometry("250x100")
        self.ventana_agregar.resizable(False, False)
        self.ventana_agregar.configure(bg=self.bg_color)
        self.ventana_agregar.transient(self.root)
        self.ventana_agregar.grab_set()
        
        # Marco para el contenido
        frame = tk.Frame(self.ventana_agregar, bg=self.bg_color, padx=15, pady=15)
        frame.pack(fill="both", expand=True)
        
        # Campo de entrada
        tk.Label(frame, text="Usuario:", bg=self.bg_color, fg=self.fg_color).pack(anchor="w")
        
        self.entrada_usuario = tk.Entry(frame, bg=self.second_bg, fg=self.fg_color,
                                       insertbackground=self.fg_color, bd=0)
        self.entrada_usuario.pack(fill="x", pady=5)
        self.entrada_usuario.focus_set()
        
        # Botón de enviar
        tk.Button(frame, text="Enviar", bg=self.accent_color, fg=self.fg_color,
                 bd=0, padx=10, command=self.enviar_solicitud).pack(anchor="e")
    
    def enviar_solicitud(self):
        usuario = self.entrada_usuario.get().strip()
        if not usuario:
            return
        
        # Aquí iría el código para enviar la solicitud
        self.ventana_agregar.destroy()
    
    def aceptar_solicitud(self):
        seleccion = self.lista_solicitudes.selection()
        if not seleccion:
            return
        
        usuario = self.lista_solicitudes.item(seleccion[0])["text"]
        
        # Buscar y eliminar la solicitud
        for solicitud in self.solicitudes[:]:
            if solicitud["nombre"] == usuario:
                self.solicitudes.remove(solicitud)
                break
        
        # Añadir a amigos
        self.amigos.append({"nombre": usuario, "estado": "online"})
        
        # Actualizar listas
        self.actualizar_listas()
    
    def rechazar_solicitud(self):
        seleccion = self.lista_solicitudes.selection()
        if not seleccion:
            return
        
        usuario = self.lista_solicitudes.item(seleccion[0])["text"]
        
        # Buscar y eliminar la solicitud
        for solicitud in self.solicitudes[:]:
            if solicitud["nombre"] == usuario:
                self.solicitudes.remove(solicitud)
                break
        
        # Actualizar lista
        self.actualizar_listas()

# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatMinimalista(root)
    root.mainloop()