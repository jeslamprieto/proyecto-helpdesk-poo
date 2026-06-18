# Proceso de desarrollo — Help Desk

## 1. Idea inicial

La idea surgió de una necesidad real en cualquier organización: tener un sistema centralizado donde los empleados puedan reportar problemas técnicos y el equipo de soporte pueda gestionarlos de forma ordenada. Se eligió una aplicación de mesa de ayuda porque es un software útil, fácil de entender y permite aplicar todos los conceptos vistos en el curso de POO.

---

## 2. Análisis del problema

**¿Quién usaría el software?**
- **Empleados** de una organización que necesitan reportar incidencias técnicas como problemas de red, software dañado, equipos con fallas, entre otros.
- **Técnicos de Soporte IT** que reciben, gestionan y resuelven esas incidencias.

**¿Para qué lo usarían?**
- Los empleados para crear tickets de soporte y hacer seguimiento a sus solicitudes.
- Los técnicos para ver todos los tickets, asignárselos y registrar la solución aplicada.

---

## 3. Diseño de la solución

**Clases principales:**

- `Ticket` — representa una incidencia con atributos como categoría, prioridad, estado y resolución.
- `Usuario` — clase base con encapsulamiento de contraseña. De ella heredan `Empleado` y `SoporteIT`.
- `ArticuloConocimiento` — representa soluciones reutilizables en una base de conocimiento.
- `AuthController` — maneja la autenticación y persistencia de usuarios en JSON.
- `TicketController` — gestiona la creación, listado y persistencia de tickets en JSON.
- `ReporteController` — genera gráficos estadísticos con matplotlib.

**Arquitectura MVC aplicada:**

- **Modelo** (`app/models/`): lógica de negocio y entidades del sistema. No interactúa con la interfaz.
- **Vista** (`app/views/`): ventanas gráficas construidas con tkinter. Solo muestra datos y captura eventos del usuario.
- **Controlador** (`app/controllers/`): gestiona la persistencia y lógica principal.
- **Controlador de interfaz** (`app/ui_controllers/`): conecta las vistas con los controladores de datos, siguiendo el principio de separación de responsabilidades.

**Flujo general:**
1. El usuario abre la app y se muestra la ventana de login.
2. Según el rol, se redirige al panel de Empleado o al panel de Soporte IT.
3. El empleado puede crear tickets y ver los suyos.
4. El técnico puede ver todos los tickets, asignárselos y resolverlos.
5. Los datos se guardan automáticamente en archivos JSON.

---

## 4. Implementación

El desarrollo se dividió en tres etapas:

**Etapa 1 — Modelos y controladores (consola)**
Se construyeron las clases del modelo (`Ticket`, `Usuario`, `Empleado`, `SoporteIT`) aplicando encapsulamiento, herencia y polimorfismo. Se implementaron los controladores de autenticación, tickets y reportes con persistencia en JSON.

**Etapa 2 — Vistas en consola con Rich**
Se crearon las vistas iniciales usando la librería Rich para mostrar menús y tablas en la terminal, permitiendo probar el flujo completo del sistema.

**Etapa 3 — Migración a interfaz gráfica con tkinter**
Se reemplazaron todas las vistas de consola por ventanas gráficas con tkinter. Se agregó la carpeta `app/ui_controllers/` para conectar las nuevas vistas con la lógica existente sin modificar los modelos ni los controladores originales.

---

## 5. Pruebas

Se utilizó pytest para escribir 7 pruebas automatizadas ubicadas en `tests/test_helpdesk.py`:

- `test_crear_ticket_valido` — verifica que un ticket se crea con los datos correctos.
- `test_asignar_tecnico_cambia_estado` — verifica que al asignar un técnico el estado cambia a "En Progreso".
- `test_resolver_ticket_valido` — verifica que al resolver un ticket el estado cambia a "Resuelto".
- `test_verificar_password_correcto` — verifica que la autenticación funciona con contraseña correcta.
- `test_verificar_password_incorrecto` — verifica que retorna False con contraseña incorrecta.
- `test_prioridad_invalida_lanza_error` — verifica que una prioridad inválida lanza `ValueError`.
- `test_resolver_sin_solucion_lanza_error` — verifica que resolver sin solución lanza `ValueError`.

Resultado: **7/7 pruebas exitosas**.

---

## 6. Dificultades encontradas

- **Migración de consola a tkinter**: adaptar el flujo de menús secuenciales a una interfaz gráfica con eventos requirió reorganizar la arquitectura y agregar la capa de controladores de interfaz.
- **Integración de matplotlib con tkinter**: para mostrar el gráfico dentro de la app (no como imagen externa) se usó `FigureCanvasTkAgg`, que permite incrustar figuras de matplotlib directamente en ventanas tkinter.
- **Gestión del flujo de login**: manejar el ciclo de login → panel → logout → login nuevamente requirió controlar correctamente la visibilidad de las ventanas con `withdraw()` y `deiconify()`.

---

## 7. Mejoras futuras

- Agregar registro de nuevos usuarios desde la interfaz.
- Implementar búsqueda y filtrado de tickets por estado, prioridad o categoría.
- Integrar la base de conocimiento para sugerir soluciones automáticas al técnico.
- Exportar reportes en PDF o Excel.
- Agregar notificaciones cuando un ticket cambia de estado.
- Implementar un sistema de prioridad automática basado en palabras clave de la descripción usando IA.
