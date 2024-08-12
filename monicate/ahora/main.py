import sys
import gi
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk4agg import FigureCanvasGTK4Agg as FigureCanvas

from enfermedad import Enfermedad
from comunidad import Comunidad
from simulador import Simulador

gi.require_version('Gtk', '4.0')
from gi.repository import Gio, GObject, Gtk

def on_quit_action(self, _action):
    quit()

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Inicializar las clases del simulador
        self.enfermedad = Enfermedad(infeccion_probable=0.19, recuperacion_probable=0.03)
        self.comunidad = Comunidad(num_ciudadanos=2000, enfermedad=self.enfermedad, num_infectados=10)
        self.simulador = Simulador()
        self.simulador.set_comunidad(self.comunidad)
        self.resultados = []

        # Box principal
        self.main_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 6)
        self.set_child(self.main_box)

        # Menu
        header_bar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=header_bar)
        self.set_title("Simulador de Enfermedades")

        # Listado del menu
        menu = Gio.Menu.new()

        # Create a popover
        self.popover = Gtk.PopoverMenu()
        self.popover.set_menu_model(menu)

        # Crea un menu
        self.menu_popover = Gtk.MenuButton()
        self.menu_popover.set_popover(self.popover)
        self.menu_popover.set_icon_name("open-menu-symbolic")

        # Agrega headerbar el menu popover
        header_bar.pack_end(self.menu_popover)

        # Add an about dialog
        about_menu = Gio.SimpleAction.new("about", None)
        about_menu.connect("activate", self.show_about_dialog)
        self.add_action(about_menu)
        menu.append("Acerca de", "win.about")

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", on_quit_action)
        self.add_action(action)
        menu.append("Salir", "win.quit")

        # Botón de Iniciar Simulación
        boton_iniciar = Gtk.Button(label="Iniciar Simulación")
        boton_iniciar.connect("clicked", self.ejecutar_simulacion)
        header_bar.pack_start(boton_iniciar)

        # Dropdown
        actions = ["Mostrar Gráfico de Líneas", "Mostrar Gráfico de Barras"]
        actions_model = Gtk.StringList()
        for action in actions:
            actions_model.append(action)
        self.actions_dropdown = Gtk.DropDown(model=actions_model)
        self.actions_dropdown.connect("notify::selected", self.actualizar_graficos)
        self.main_box.append(self.actions_dropdown)

        self.info_label = Gtk.Label(label="")
        self.main_box.append(self.info_label)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.main_box.append(self.canvas)

    def show_about_dialog(self, action, param):
        self.about = Gtk.AboutDialog()
        self.about.set_transient_for(self)
        self.about.set_modal(self)

        self.about.set_authors(["Tu Nombre"])
        self.about.set_copyright("Copyright 2024 Tu Nombre")
        self.about.set_license_type(Gtk.License.GPL_3_0)
        self.about.set_website("http://example.com")
        self.about.set_website_label("Mi Sitio Web")
        self.about.set_version("1.0")
        self.about.set_logo_icon_name("org.example.example")
        self.about.set_visible(True)

    def ejecutar_simulacion(self, widget):
        self.resultados = []
        for dia in range(50):
            self.simulador.run(pasos=1)
            self.resultados.append(
                (dia + 1, len(self.simulador.susceptibles), len(self.simulador.infectados), len(self.simulador.recuperados))
            )
            print(f"Dia {dia + 1}: Susceptibles: {len(self.simulador.susceptibles)}, Infectados: {len(self.simulador.infectados)}, Recuperados: {len(self.simulador.recuperados)}")
        self.info_label.set_text("Simulación completada. Datos actualizados.")
        self.actualizar_graficos()

    def actualizar_graficos(self, *args):
        if not self.resultados or not all(len(lista) > 0 for lista in zip(*self.resultados)):
            self.info_label.set_text("No hay datos de simulación para mostrar.")
            return

        selected_index = self.actions_dropdown.get_selected()
        if selected_index == -1:
            self.info_label.set_text("Por favor, seleccione una acción.")
            return

        if selected_index == 0:
            self.mostrar_grafico_lineas()
        elif selected_index == 1:
            self.mostrar_grafico_barras()

    def mostrar_grafico_lineas(self):
        if not self.resultados:
            self.info_label.set_text("No hay datos de simulación para mostrar.")
            return

        self.figure.clear()
        dias, susceptibles, infectados, recuperados = zip(*self.resultados)

        ax = self.figure.add_subplot(1, 1, 1)
        ax.plot(dias, susceptibles, label='Susceptibles', color='tab:blue')
        ax.plot(dias, infectados, label='Infectados', color='tab:orange')
        ax.plot(dias, recuperados, label='Recuperados', color='tab:green')

        ax.set_xlabel('Días')
        ax.set_ylabel('Número de personas')
        ax.set_title('Evolución de la enfermedad')
        ax.legend()

        self.canvas.draw()

    def mostrar_grafico_barras(self):
        if not self.resultados:
            self.info_label.set_text("No hay datos de simulación para mostrar.")
            return

        self.figure.clear()
        dias, susceptibles, infectados, recuperados = zip(*self.resultados)

        x = np.arange(len(dias))
        width = 0.25

        ax = self.figure.add_subplot(1, 1, 1)
        rects1 = ax.bar(x - width, susceptibles, width, label='Susceptibles', color='tab:blue')
        rects2 = ax.bar(x, infectados, width, label='Infectados', color='tab:orange')
        rects3 = ax.bar(x + width, recuperados, width, label='Recuperados', color='tab:green')

        ax.set_xlabel('Días')
        ax.set_ylabel('Número de personas')
        ax.set_title('Evolución de la enfermedad')
        ax.set_xticks(x)
        ax.set_xticklabels(dias)
        ax.legend()

        self.canvas.draw()

class MyApp(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def do_activate(self):
        active_window = self.props.active_window
        if active_window:
            active_window.present()
        else:
            self.win = MainWindow(application=self)
            self.win.present()

app = MyApp()
app.run(sys.argv)
