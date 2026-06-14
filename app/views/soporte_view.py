"""
Vista de Soporte IT — panel de gestión de tickets para técnicos.
Permite ver todos los tickets, asignarse uno y resolverlo.
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
NARANJA      = "#e67e22"


class SoporteView:
    """
    Ventana del panel de Técnico de Soporte IT.
    Muestra la consola global de tickets y permite gestionarlos.
    """

    def __init__(self, root, nombre_usuario, on_logout):
        self.root = root
        self.nombre_usuario = nombre_usuario
        self.on_logout = on_logout
        self.controller = None

        self.root.title(f"Help Desk — Panel de Soporte IT ({nombre_usuario})")
        self.root.geometry("1000x600")
        self.root.configure(bg=AZUL_OSCURO)
        self.root.resizable(True, True)

        self._construir_interfaz()

    def set_controller(self, controller):
        self.controller = controller

    # ── Construcción ──────────────────────────────────────────────────────

    def _construir_interfaz(self):
        """Construye la interfaz del panel de soporte."""
        # ── Barra superior ──
        topbar = tk.Frame(self.root, bg=AZUL_MEDIO, height=52)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        tk.Label(topbar, text="🎧 Mesa de Ayuda", font=("Segoe UI", 13, "bold"),
                 bg=AZUL_MEDIO, fg=BLANCO).pack(side="left", padx=20, pady=12)

        tk.Label(topbar, text=f"🔧 {self.nombre_usuario}  |  Soporte IT",
                 font=("Segoe UI", 10), bg=AZUL_MEDIO, fg=AMARILLO).pack(side="left", padx=8)

        tk.Button(topbar, text="Cerrar sesión", font=("Segoe UI", 9),
                  bg=ROJO, fg=BLANCO, relief="flat", cursor="hand2",
                  activebackground="#c0392b", command=self.on_logout).pack(side="right", padx=20, pady=12)

        # ── Barra de acciones ──
        acciones = tk.Frame(self.root, bg=AZUL_OSCURO)
        acciones.pack(fill="x", padx=16, pady=(12, 0))

        tk.Label(acciones, text="Consola global de tickets",
                 font=("Segoe UI", 13, "bold"), bg=AZUL_OSCURO, fg=BLANCO).pack(side="left")

        # Botones de acción
        for texto, cmd, color in [
            ("↻ Actualizar",   self._on_actualizar,  AZUL_OSCURO),
            ("Asignarme",      self._on_asignar,      AZUL_ACENTO),
            ("Resolver",       self._on_resolver,     VERDE),
            ("Ver reporte 📊", self._on_reporte,      NARANJA),
        ]:
            tk.Button(acciones, text=texto, font=("Segoe UI", 9, "bold"),
                      bg=color, fg=BLANCO, relief="flat", cursor="hand2",
                      activebackground=AZUL_MEDIO,
                      command=cmd).pack(side="right", padx=4, ipadx=10, ipady=4)

        # ── Tabla global ──
        frame_tabla = tk.Frame(self.root, bg=AZUL_MEDIO)
        frame_tabla.pack(fill="both", expand=True, padx=16, pady=12)

        cols = ("ID", "Creador", "Categoría", "Prioridad", "Estado", "Técnico", "Fecha")
        self.tabla = ttk.Treeview(frame_tabla, columns=cols, show="headings")

        anchos = {"ID": 40, "Creador": 110, "Categoría": 110,
                  "Prioridad": 80, "Estado": 100, "Técnico": 120, "Fecha": 145}
        for col in cols:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=anchos.get(col, 100),
                              anchor="center" if col in ("ID", "Prioridad", "Estado") else "w")

        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll_y.set)

        self.tabla.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        scroll_y.pack(side="left", fill="y", pady=8, padx=(0, 8))

        # Tags de color por estado
        self.tabla.tag_configure("Abierto",     foreground=ROJO)
        self.tabla.tag_configure("En Progreso", foreground=AMARILLO)
        self.tabla.tag_configure("Resuelto",    foreground=VERDE)

        # Doble clic abre detalles
        self.tabla.bind("<Double-1>", self._on_doble_clic)

        # ── Barra de estado inferior ──
        self.lbl_estado = tk.Label(self.root, text="Selecciona un ticket para gestionarlo.",
                                   font=("Segoe UI", 9), bg=AZUL_OSCURO, fg=GRIS_TEXTO)
        self.lbl_estado.pack(pady=(0, 8))

    # ── Eventos ───────────────────────────────────────────────────────────

    def _on_actualizar(self):
        if self.controller:
            self.controller.cargar_todos_tickets()

    def _on_asignar(self):
        if self.controller:
            self.controller.asignar_ticket()

    def _on_resolver(self):
        if self.controller:
            self.controller.resolver_ticket()

    def _on_reporte(self):
        if self.controller:
            self.controller.generar_reporte()

    def _on_doble_clic(self, event):
        """Abre ventana de detalles al hacer doble clic en un ticket."""
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion[0], "values")
        id_ticket = str(valores[0])
        ticket = next((t for t in self._tickets if str(t.id_ticket) == id_ticket), None)
        if ticket:
            self._mostrar_detalle(ticket)

    def _mostrar_detalle(self, ticket):
        """Ventana emergente con todos los detalles del ticket."""
        ventana = tk.Toplevel(self.root)
        ventana.title(f"Ticket #{ticket.id_ticket} — Detalles")
        ventana.geometry("480x520")
        ventana.configure(bg=AZUL_OSCURO)
        ventana.resizable(False, True)
        ventana.grab_set()

        color_estado = {
            "Abierto": ROJO,
            "En Progreso": AMARILLO,
            "Resuelto": VERDE
        }.get(ticket.estado, BLANCO)

        tk.Label(ventana, text=f"Ticket #{ticket.id_ticket}",
                 font=("Segoe UI", 15, "bold"), bg=AZUL_OSCURO, fg=BLANCO).pack(pady=(20, 4))
        tk.Label(ventana, text=ticket.estado, font=("Segoe UI", 10, "bold"),
                 bg=AZUL_OSCURO, fg=color_estado).pack(pady=(0, 16))

        panel = tk.Frame(ventana, bg=AZUL_MEDIO)
        panel.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        campos = [
            ("Creador",    ticket.creador),
            ("Categoría",  ticket.categoria),
            ("Prioridad",  ticket.prioridad),
            ("Fecha",      ticket.fecha_creacion),
            ("Técnico",    ticket.tecnico_asignado or "Sin asignar"),
        ]
        for etiqueta, valor in campos:
            fila = tk.Frame(panel, bg=AZUL_MEDIO)
            fila.pack(fill="x", padx=16, pady=3)
            tk.Label(fila, text=f"{etiqueta}:", font=("Segoe UI", 9, "bold"),
                     bg=AZUL_MEDIO, fg=GRIS_TEXTO, width=10, anchor="w").pack(side="left")
            tk.Label(fila, text=valor, font=("Segoe UI", 9),
                     bg=AZUL_MEDIO, fg=BLANCO, anchor="w").pack(side="left")

        tk.Label(panel, text="Descripción:", font=("Segoe UI", 9, "bold"),
                 bg=AZUL_MEDIO, fg=GRIS_TEXTO, anchor="w").pack(fill="x", padx=16, pady=(8, 2))
        txt_desc = tk.Text(panel, height=3, font=("Segoe UI", 9),
                           bg=AZUL_OSCURO, fg=BLANCO, relief="flat", bd=6, wrap="word")
        txt_desc.insert("1.0", ticket.descripcion)
        txt_desc.config(state="disabled")
        txt_desc.pack(fill="x", padx=16, pady=(0, 8))

        if ticket.resolucion:
            tk.Label(panel, text="Resolución:", font=("Segoe UI", 9, "bold"),
                     bg=AZUL_MEDIO, fg=VERDE, anchor="w").pack(fill="x", padx=16, pady=(4, 2))
            txt_res = tk.Text(panel, height=3, font=("Segoe UI", 9),
                              bg=AZUL_OSCURO, fg=VERDE, relief="flat", bd=6, wrap="word")
            txt_res.insert("1.0", ticket.resolucion)
            txt_res.config(state="disabled")
            txt_res.pack(fill="x", padx=16, pady=(0, 8))

        tk.Button(ventana, text="Cerrar", font=("Segoe UI", 9),
                  bg=AZUL_ACENTO, fg=BLANCO, relief="flat", cursor="hand2",
                  command=ventana.destroy).pack(pady=(0, 16), ipadx=20, ipady=4)

    # ── Métodos públicos ──────────────────────────────────────────────────

    def obtener_ticket_seleccionado_id(self):
        """Retorna el ID del ticket seleccionado en la tabla, o None."""
        seleccion = self.tabla.selection()
        if not seleccion:
            return None
        valores = self.tabla.item(seleccion[0], "values")
        return str(valores[0]) if valores else None

    def pedir_solucion(self):
        """Abre un diálogo para que el técnico ingrese la solución."""
        return simpledialog.askstring(
            "Resolución del ticket",
            "Describe la solución aplicada:",
            parent=self.root
        )

    def mostrar_tickets(self, tickets):
        """Rellena la tabla con todos los tickets del sistema."""
        self._tickets = tickets  # Guardamos para consultar en doble clic
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for t in tickets:
            tecnico = t.tecnico_asignado or "—"
            self.tabla.insert("", tk.END,
                values=(t.id_ticket, t.creador, t.categoria,
                        t.prioridad, t.estado, tecnico, t.fecha_creacion),
                tags=(t.estado,))

    def mostrar_mensaje(self, mensaje, exito=True):
        """Actualiza la barra inferior con el resultado de una acción."""
        color = VERDE if exito else ROJO
        self.lbl_estado.config(text=mensaje, fg=color)

    def mostrar_info(self, titulo, mensaje):
        messagebox.showinfo(titulo, mensaje, parent=self.root)

    def mostrar_error(self, mensaje):
        messagebox.showerror("Error", mensaje, parent=self.root)

    def mostrar_advertencia(self, mensaje):
        messagebox.showwarning("Atención", mensaje, parent=self.root)
