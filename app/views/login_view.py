"""
Vista de Login — ventana de inicio de sesión del sistema Help Desk.
Construida con tkinter. No contiene lógica de negocio.
"""
import tkinter as tk
from tkinter import messagebox


# ── Paleta de colores del sistema ──────────────────────────────────────────
AZUL_OSCURO  = "#1a2332"   # Fondo principal
AZUL_MEDIO   = "#243447"   # Fondo de paneles
AZUL_ACENTO  = "#2d6cdf"   # Botones y resaltados
BLANCO       = "#f0f4ff"   # Texto principal
GRIS_TEXTO   = "#8fa3bf"   # Texto secundario
ROJO_ERROR   = "#e74c3c"   # Errores


class LoginView:
    """
    Ventana de autenticación del sistema.
    Muestra un formulario de usuario y contraseña.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Help Desk — Iniciar Sesión")
        self.root.geometry("420x520")
        self.root.resizable(False, False)
        self.root.configure(bg=AZUL_OSCURO)

        # Referencia al controlador (se inyecta después)
        self.controller = None

        self._construir_interfaz()

    def set_controller(self, controller):
        """Inyecta el controlador una vez que todos los componentes están listos."""
        self.controller = controller

    # ── Construcción de la interfaz ────────────────────────────────────────

    def _construir_interfaz(self):
        """Construye todos los widgets de la pantalla de login."""
        # Contenedor central con padding
        frame = tk.Frame(self.root, bg=AZUL_MEDIO, bd=0)
        frame.place(relx=0.5, rely=0.5, anchor="center", width=340, height=420)

        # Logo / ícono texto
        tk.Label(frame, text="🎧", font=("Segoe UI", 42),
                 bg=AZUL_MEDIO, fg=AZUL_ACENTO).pack(pady=(32, 4))

        tk.Label(frame, text="Mesa de Ayuda", font=("Segoe UI", 18, "bold"),
                 bg=AZUL_MEDIO, fg=BLANCO).pack()

        tk.Label(frame, text="Ingresa tus credenciales para continuar",
                 font=("Segoe UI", 9), bg=AZUL_MEDIO, fg=GRIS_TEXTO).pack(pady=(2, 24))

        # Campo usuario
        tk.Label(frame, text="Usuario", font=("Segoe UI", 10, "bold"),
                 bg=AZUL_MEDIO, fg=GRIS_TEXTO, anchor="w").pack(fill="x", padx=32)

        self.entry_usuario = tk.Entry(frame, font=("Segoe UI", 11),
                                      bg=AZUL_OSCURO, fg=BLANCO,
                                      insertbackground=BLANCO,
                                      relief="flat", bd=8)
        self.entry_usuario.pack(fill="x", padx=32, pady=(2, 14))

        # Campo contraseña
        tk.Label(frame, text="Contraseña", font=("Segoe UI", 10, "bold"),
                 bg=AZUL_MEDIO, fg=GRIS_TEXTO, anchor="w").pack(fill="x", padx=32)

        self.entry_password = tk.Entry(frame, font=("Segoe UI", 11),
                                       bg=AZUL_OSCURO, fg=BLANCO,
                                       insertbackground=BLANCO,
                                       relief="flat", bd=8, show="●")
        self.entry_password.pack(fill="x", padx=32, pady=(2, 24))

        # Botón ingresar
        self.btn_ingresar = tk.Button(
            frame, text="Ingresar", font=("Segoe UI", 11, "bold"),
            bg=AZUL_ACENTO, fg=BLANCO, relief="flat", cursor="hand2",
            activebackground="#1a4fa8", activeforeground=BLANCO,
            command=self._on_ingresar
        )
        self.btn_ingresar.pack(fill="x", padx=32, ipady=8)

        # Atajo: Enter también inicia sesión
        self.root.bind("<Return>", lambda e: self._on_ingresar())

    # ── Eventos ───────────────────────────────────────────────────────────

    def _on_ingresar(self):
        """Delega la acción de login al controlador."""
        if self.controller:
            self.controller.iniciar_sesion()

    # ── Métodos públicos usados por el controlador ────────────────────────

    def obtener_credenciales(self):
        """Retorna (username, password) ingresados por el usuario."""
        return self.entry_usuario.get().strip(), self.entry_password.get()

    def mostrar_error(self, mensaje):
        """Muestra una ventana emergente de error."""
        messagebox.showerror("Error de acceso", mensaje, parent=self.root)
        self.entry_password.delete(0, tk.END)

    def limpiar(self):
        """Limpia los campos del formulario."""
        self.entry_usuario.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
