"""
Controlador de interfaz para el panel de Soporte IT.
Conecta SoporteView con TicketController, ReporteController y ReporteView.
"""

class SoporteUIController:
    """
    Orquesta las acciones del técnico de soporte:
    ver todos los tickets, asignarse uno, resolverlo y generar reportes.
    """

    def __init__(self, vista, ticket_controller, reporte_controller, reporte_view, usuario):
        self.vista               = vista
        self.ticket_controller   = ticket_controller
        self.reporte_controller  = reporte_controller
        self.reporte_view        = reporte_view
        self.usuario             = usuario   # Objeto SoporteIT (modelo)

    def cargar_todos_tickets(self):
        """Carga y muestra todos los tickets del sistema."""
        todos = self.ticket_controller.listar_todos_los_tickets()
        self.vista.mostrar_tickets(todos)
        self.vista.mostrar_mensaje(f"{len(todos)} ticket(s) en el sistema.", exito=True)

    def asignar_ticket(self):
        """Asigna el ticket seleccionado al técnico actual."""
        id_ticket = self.vista.obtener_ticket_seleccionado_id()

        if not id_ticket:
            self.vista.mostrar_advertencia("Selecciona un ticket de la tabla primero.")
            return

        ticket = next(
            (t for t in self.ticket_controller.listar_todos_los_tickets()
             if str(t.id_ticket) == id_ticket), None
        )

        if not ticket:
            self.vista.mostrar_error(f"No se encontró el ticket #{id_ticket}.")
            return

        mensaje, exito = self.usuario.asignar_ticket(ticket)

        if exito:
            self.ticket_controller.guardar_tickets()
            self.cargar_todos_tickets()

        self.vista.mostrar_mensaje(mensaje, exito)

    def resolver_ticket(self):
        """Resuelve el ticket seleccionado con la solución ingresada."""
        id_ticket = self.vista.obtener_ticket_seleccionado_id()

        if not id_ticket:
            self.vista.mostrar_advertencia("Selecciona un ticket de la tabla primero.")
            return

        ticket = next(
            (t for t in self.ticket_controller.listar_todos_los_tickets()
             if str(t.id_ticket) == id_ticket), None
        )

        if not ticket:
            self.vista.mostrar_error(f"No se encontró el ticket #{id_ticket}.")
            return

        solucion = self.vista.pedir_solucion()

        if not solucion or not solucion.strip():
            self.vista.mostrar_advertencia("Debes escribir una solución para cerrar el ticket.")
            return

        mensaje, exito = self.usuario.resolver_ticket(ticket, solucion)

        if exito:
            self.ticket_controller.guardar_tickets()
            self.cargar_todos_tickets()

        self.vista.mostrar_mensaje(mensaje, exito)

    def generar_reporte(self):
        """Muestra el gráfico de estados en una ventana emergente."""
        tickets = self.ticket_controller.listar_todos_los_tickets()
        self.reporte_view.mostrar_grafico(self.vista.root, tickets)
