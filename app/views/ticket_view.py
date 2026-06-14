"""
Vista de Tickets — pantalla principal para el rol Empleado.
Permite crear tickets y consultar los propios. Solo muestra datos, no procesa lógica.
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


AZUL_OSCURO  = "#1a2332"
AZUL_MEDIO   = "#243447"
AZUL_ACENTO  = "#2d6cdf"
BLANCO       = "#f0f4ff"
GRIS_TEXTO   = "#8fa3bf"
VERDE        = "#2ecc71"
AMARILLO     = "#f39c12"
ROJO         = "#e74c3c"


class TicketView:
    """
    Ventana del panel de Empleado.
    Muestra la tabla de tickets propios y el formulario para crear nuevos.
    """

    def __init__(self, root, nombre_usuario, on_logout):
        self.root = root
        self.nombre_usuario = nombre_usuario
        self.on_logout = on_logout      # Callback para cerrar sesión
        self.controller = None

        self.root.title(f"Help Desk — Panel de Empleado ({nombre_usuario})")
        self.root.geometry("860x560")
        self.root.configure(bg=AZUL_OSCURO)
        self.root.resizable(True, True)

        self._construir_interfaz()

    def set_controller(self, controller):
        self.controller = controller

    # ── Construcción ──────────────────────────────────────────────────────

    def _construir_interfaz(self):
        """Construye la interfaz completa del panel de empleado."""
        # ── Barra superior ──
        topbar = tk.Frame(self.root, bg=AZUL_MEDIO, height=52)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        tk.Label(topbar, text="🎧 Mesa de Ayuda", font=("Segoe UI", 13, "bold"),
                 bg=AZUL_MEDIO, fg=BLANCO).pack(side="left", padx=20, pady=12)

        tk.Label(topbar, text=f"👤 {self.nombre_usuario}  |  Empleado",
                 font=("Segoe UI", 10), bg=AZUL_MEDIO, fg=GRIS_TEXTO).pack(side="left", padx=8)

        tk.Button(topbar, text="Cerrar sesión", font=("Segoe UI", 9),
                  bg=ROJO, fg=BLANCO, relief="flat", cursor="hand2",
                  activebackground="#c0392b", command=self.on_logout).pack(side="right", padx=20, pady=12)

        # ── Cuerpo dividido en dos columnas ──
        cuerpo = tk.Frame(self.root, bg=AZUL_OSCURO)
        cuerpo.pack(fill="both", expand=True, padx=16, pady=12)

        # Columna izquierda: formulario nuevo ticket
        self._panel_formulario(cuerpo)

        # Columna derecha: tabla de mis tickets
        self._panel_tabla(cuerpo)

    def _panel_formulario(self, parent):
        """Panel izquierdo con el formulario para crear un ticket."""
        panel = tk.Frame(parent, bg=AZUL_MEDIO, width=280)
        panel.pack(side="left", fill="y", padx=(0, 12))
        panel.pack_propagate(False)

        tk.Label(panel, text="Nuevo ticket", font=("Segoe UI", 13, "bold"),
                 bg=AZUL_MEDIO, fg=BLANCO).pack(pady=(20, 16), padx=20, anchor="w")

        # Categoría
        tk.Label(panel, text="Categoría", font=("Segoe UI", 9, "bold"),
                 bg=AZUL_MEDIO, fg=GRIS_TEXTO).pack(anchor="w", padx=20)
        self.combo_categoria = ttk.Combobox(panel, state="readonly",
            values=["Redes", "Software", "Hardware", "Accesos", "Otro"])
        self.combo_categoria.set("Redes")
        self.combo_categoria.pack(fill="x", padx=20, pady=(2, 12))

        # Prioridad
        tk.Label(panel, text="Prioridad", font=("Segoe UI", 9, "bold"),
                 bg=AZUL_MEDIO, fg=GRIS_TEXTO).pack(anchor="w", padx=20)
        self.combo_prioridad = ttk.Combobox(panel, state="readonly",
            values=["Baja", "Media", "Alta"])
        self.combo_prioridad.set("Media")
        self.combo_prioridad.pack(fill="x", padx=20, pady=(2, 12))

        # Descripción
        tk.Label(panel, text="Descripción", font=("Segoe UI", 9, "bold"),
                 bg=AZUL_MEDIO, fg=GRIS_TEXTO).pack(anchor="w", padx=20)
        self.text_descripcion = tk.Text(panel, height=7, font=("Segoe UI", 10),
                                        bg=AZUL_OSCURO, fg=BLANCO,
                                        insertbackground=BLANCO, relief="flat", bd=6,
                                        wrap="word")
        self.text_descripcion.pack(fill="x", padx=20, pady=(2, 16))

        # Botón enviar
        tk.Button(panel, text="Enviar ticket", font=("Segoe UI", 10, "bold"),
                  bg=AZUL_ACENTO, fg=BLANCO, relief="flat", cursor="hand2",
                  activebackground="#1a4fa8",
                  command=self._on_crear_ticket).pack(fill="x", padx=20, ipady=8)

    def _panel_tabla(self, parent):
        """Panel derecho con la tabla de tickets del empleado."""
        panel = tk.Frame(parent, bg=AZUL_MEDIO)
        panel.pack(side="left", fill="both", expand=True)

        encabezado = tk.Frame(panel, bg=AZUL_MEDIO)
        encabezado.pack(fill="x", padx=16, pady=(16, 8))

        tk.Label(encabezado, text="Mis solicitudes", font=("Segoe UI", 13, "bold"),
                 bg=AZUL_MEDIO, fg=BLANCO).pack(side="left")

        tk.Button(encabezado, text="↻ Actualizar", font=("Segoe UI", 9),
                  bg=AZUL_OSCURO, fg=GRIS_TEXTO, relief="flat", cursor="hand2",
                  command=self._on_actualizar).pack(side="right")

        # Tabla con scrollbar
        cols = ("ID", "Categoría", "Prioridad", "Estado", "Fecha")
        self.tabla = ttk.Treeview(panel, columns=cols, show="headings", height=16)

        for col in cols:
            self.tabla.heading(col, text=col)
        self.tabla.column("ID", width=40, anchor="center")
        self.tabla.column("Categoría", width=110)
        self.tabla.column("Prioridad", width=80, anchor="center")
        self.tabla.column("Estado", width=110, anchor="center")
        self.tabla.column("Fecha", width=145)

        scroll = ttk.Scrollbar(panel, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.pack(side="left", fill="both", expand=True, padx=(16, 0), pady=(0, 16))
        scroll.pack(side="left", fill="y", pady=(0, 16), padx=(0, 8))

        # Tags de color por estado
        self.tabla.tag_configure("Abierto",     foreground=ROJO)
        self.tabla.tag_configure("En Progreso", foreground=AMARILLO)
        self.tabla.tag_configure("Resuelto",    foreground=VERDE)

        # Doble clic abre detalles del ticket
        self.tabla.bind("<Double-1>", self._on_doble_clic)

        # Hint debajo de la tabla
        tk.Label(panel, text="💡 Doble clic en un ticket para ver sus detalles",
                 font=("Segoe UI", 8), bg=AZUL_MEDIO, fg=GRIS_TEXTO).pack(pady=(0, 8))

    # ── Eventos ───────────────────────────────────────────────────────────

    def _on_crear_ticket(self):
        if self.controller:
            self.controller.crear_ticket()

    def _on_actualizar(self):
        if self.controller:
            self.controller.cargar_mis_tickets()

    def _on_doble_clic(self, event):
        """Abre ventana de detalles al hacer doble clic en un ticket."""
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion[0], "values")
        id_ticket = str(valores[0])

        # Buscar el ticket completo en la lista guardada
        ticket = next((t for t in self._tickets if str(t.id_ticket) == id_ticket), None)
        if ticket:
            self._mostrar_detalle(ticket)

    def _mostrar_detalle(self, ticket):
        """Abre una ventana emergente con todos los detalles del ticket."""
        ventana = tk.Toplevel(self.root)
        ventana.title(f"Ticket #{ticket.id_ticket} — Detalles")
        ventana.geometry("480x520")
        ventana.configure(bg=AZUL_OSCURO)
        ventana.resizable(False, True)
        ventana.grab_set()  # Bloquea la ventana padre mientras está abierta

        # Colores por estado
        color_estado = {
            "Abierto": ROJO,
            "En Progreso": AMARILLO,
            "Resuelto": VERDE
        }.get(ticket.estado, BLANCO)

        tk.Label(ventana, text=f"Ticket #{ticket.id_ticket}",
                 font=("Segoe UI", 15, "bold"), bg=AZUL_OSCURO, fg=BLANCO).pack(pady=(20, 4))

        tk.Label(ventana, text=ticket.estado, font=("Segoe UI", 10, "bold"),
                 bg=AZUL_OSCURO, fg=color_estado).pack(pady=(0, 16))

        # Panel de datos
        panel = tk.Frame(ventana, bg=AZUL_MEDIO)
        panel.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        campos = [
            ("Categoría",  ticket.categoria),
            ("Prioridad",  ticket.prioridad),
            ("Fecha",      ticket.fecha_creacion),
            ("Técnico",    ticket.tecnico_asignado or "Sin asignar"),
        ]

        for etiqueta, valor in campos:
            fila = tk.Frame(panel, bg=AZUL_MEDIO)
            fila.pack(fill="x", padx=16, pady=4)
            tk.Label(fila, text=f"{etiqueta}:", font=("Segoe UI", 9, "bold"),
                     bg=AZUL_MEDIO, fg=GRIS_TEXTO, width=10, anchor="w").pack(side="left")
            tk.Label(fila, text=valor, font=("Segoe UI", 9),
                     bg=AZUL_MEDIO, fg=BLANCO, anchor="w").pack(side="left")

        # Descripción
        tk.Label(panel, text="Descripción:", font=("Segoe UI", 9, "bold"),
                 bg=AZUL_MEDIO, fg=GRIS_TEXTO, anchor="w").pack(fill="x", padx=16, pady=(8, 2))
        txt_desc = tk.Text(panel, height=3, font=("Segoe UI", 9),
                           bg=AZUL_OSCURO, fg=BLANCO, relief="flat", bd=6,
                           wrap="word", state="normal")
        txt_desc.insert("1.0", ticket.descripcion)
        txt_desc.config(state="disabled")
        txt_desc.pack(fill="x", padx=16, pady=(0, 8))

        # Resolución (si existe)
        if ticket.resolucion:
            tk.Label(panel, text="Resolución:", font=("Segoe UI", 9, "bold"),
                     bg=AZUL_MEDIO, fg=VERDE, anchor="w").pack(fill="x", padx=16, pady=(4, 2))
            txt_res = tk.Text(panel, height=3, font=("Segoe UI", 9),
                              bg=AZUL_OSCURO, fg=VERDE, relief="flat", bd=6,
                              wrap="word", state="normal")
            txt_res.insert("1.0", ticket.resolucion)
            txt_res.config(state="disabled")
            txt_res.pack(fill="x", padx=16, pady=(0, 8))

        tk.Button(ventana, text="Cerrar", font=("Segoe UI", 9),
                  bg=AZUL_ACENTO, fg=BLANCO, relief="flat", cursor="hand2",
                  command=ventana.destroy).pack(pady=(0, 16), ipadx=20, ipady=4)

    # ── Métodos públicos ──────────────────────────────────────────────────

    def obtener_datos_formulario(self):
        """Retorna (categoria, descripcion, prioridad) del formulario."""
        return (
            self.combo_categoria.get(),
            self.text_descripcion.get("1.0", tk.END).strip(),
            self.combo_prioridad.get()
        )

    def limpiar_formulario(self):
        """Limpia el área de texto de descripción."""
        self.text_descripcion.delete("1.0", tk.END)
        self.combo_categoria.set("Redes")
        self.combo_prioridad.set("Media")

    def mostrar_tickets(self, tickets):
        """Rellena la tabla con la lista de tickets recibida."""
        self._tickets = tickets  # Guardamos para consultar en doble clic
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for t in tickets:
            self.tabla.insert("", tk.END,
                values=(t.id_ticket, t.categoria, t.prioridad, t.estado, t.fecha_creacion),
                tags=(t.estado,))

    def mostrar_exito(self, id_ticket):
        """Ventana emergente de confirmación de ticket creado."""
        messagebox.showinfo("Ticket creado",
                            f"✅ Tu ticket #{id_ticket} fue enviado.\nEl equipo de soporte lo atenderá pronto.",
                            parent=self.root)

    def mostrar_error(self, mensaje):
        messagebox.showerror("Error", mensaje, parent=self.root)

    def mostrar_advertencia(self, mensaje):
        messagebox.showwarning("Atención", mensaje, parent=self.root)
