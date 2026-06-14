"""
Controlador de interfaz para la pantalla de Login.
Conecta LoginView con AuthController y decide qué panel abrir según el rol.
"""
import tkinter as tk
from app.controllers.auth_controller import AuthController
from app.controllers.ticket_controller import TicketController
from app.controllers.reporte_controller import ReporteController
from app.views.ticket_view import TicketView
from app.views.soporte_view import SoporteView
from app.views.reporte_view import ReporteView


class LoginController:
    """
    Controlador del flujo de autenticación.
    Recibe las credenciales de la vista y decide a qué panel redirigir.
    """

    def __init__(self, root, login_view):
        self.root = root
        self.login_view = login_view

        # Controladores de datos (lógica de negocio)
        self.auth_controller   = AuthController()
        self.ticket_controller = TicketController()
        self.reporte_controller = ReporteController(self.ticket_controller)

    def iniciar_sesion(self):
        """Valida credenciales y abre el panel correspondiente al rol."""
        username, password = self.login_view.obtener_credenciales()

        if not username or not password:
            self.login_view.mostrar_error("Por favor completa usuario y contraseña.")
            return

        usuario = self.auth_controller.iniciar_sesion(username, password)

        if not usuario:
            self.login_view.mostrar_error("Usuario o contraseña incorrectos.")
            return

        # Ocultar ventana de login y abrir el panel del rol correspondiente
        self.root.withdraw()

        if usuario.rol == "Empleado":
            self._abrir_panel_empleado(usuario)
        elif usuario.rol == "SoporteIT":
            self._abrir_panel_soporte(usuario)

    def _abrir_panel_empleado(self, usuario):
        """Abre la ventana del panel de Empleado."""
        from app.ui_controllers.ticket_ui_controller import TicketUIController

        ventana = tk.Toplevel(self.root)

        def logout():
            ventana.destroy()
            self.login_view.limpiar()
            self.root.deiconify()

        vista = TicketView(ventana, usuario.nombre, on_logout=logout)
        ctrl  = TicketUIController(vista, self.ticket_controller, usuario.username)
        vista.set_controller(ctrl)
        ctrl.cargar_mis_tickets()

        ventana.protocol("WM_DELETE_WINDOW", logout)

    def _abrir_panel_soporte(self, usuario):
        """Abre la ventana del panel de Soporte IT."""
        from app.ui_controllers.soporte_ui_controller import SoporteUIController

        ventana = tk.Toplevel(self.root)

        def logout():
            ventana.destroy()
            self.login_view.limpiar()
            self.root.deiconify()

        reporte_view = ReporteView()
        vista = SoporteView(ventana, usuario.nombre, on_logout=logout)
        ctrl  = SoporteUIController(vista, self.ticket_controller,
                                    self.reporte_controller, reporte_view, usuario)
        vista.set_controller(ctrl)
        ctrl.cargar_todos_tickets()

        ventana.protocol("WM_DELETE_WINDOW", logout)
