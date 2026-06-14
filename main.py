"""
Punto de entrada del sistema Help Desk.
Inicializa la ventana principal y arranca el flujo de login.
"""
import tkinter as tk
from app.views.login_view import LoginView
from app.ui_controllers.login_ui_controller import LoginController


def main():
    root = tk.Tk()

    # Centrar ventana en pantalla
    root.eval('tk::PlaceWindow . center')

    # Crear vista y controlador del login
    login_view = LoginView(root)
    controller = LoginController(root, login_view)
    login_view.set_controller(controller)

    root.mainloop()


if __name__ == "__main__":
    main()
