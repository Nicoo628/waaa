import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib
from simulador import Simulador
from comunidad import Comunidad
from enfermedad import Enfermedad

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(title="Simulación Enfermedad. Proyecto final PA", application=app)
        self.set_default_size(800, 600)
        
        # Crear caja vertical principal
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_child(vbox)
        
        # Crear notebook para pestañas
        self.notebook = Gtk.Notebook()
        vbox.append(self.notebook)
        
        # Crear páginas del notebook
        self.create_results_page()
        self.create_citizens_page()
        
        # Inicializar simulación
        self.init_simulation()

    def create_results_page(self):
        """Crear la pestaña de resultados diarios"""
        self.page1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.notebook.append_page(self.page1, Gtk.Label(label="Resultados Diarios"))

        self.step_button_page1 = Gtk.Button(label="AVANZAR DIA")
        self.step_button_page1.connect("clicked", self.on_step_button_clicked)
        self.page1.append(self.step_button_page1)

        self.scrolled_window_resultados = Gtk.ScrolledWindow()
        self.scrolled_window_resultados.set_vexpand(True)
        self.scrolled_window_resultados.set_hexpand(True)
        self.textview_resultados = Gtk.TextView()
        self.textview_resultados.set_editable(False)
        self.textbuffer_resultados = self.textview_resultados.get_buffer()
        self.scrolled_window_resultados.set_child(self.textview_resultados)
        self.page1.append(self.scrolled_window_resultados)

    def create_citizens_page(self):
        """Crear la pestaña de atributos de los ciudadanos"""
        self.page2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.notebook.append_page(self.page2, Gtk.Label(label="Atributos Ciudadanos"))

        self.step_button_page2 = Gtk.Button(label="AVANZAR DIA")
        self.step_button_page2.connect("clicked", self.on_step_button_clicked)
        self.page2.append(self.step_button_page2)

        self.scrolled_window_ciudadanos = Gtk.ScrolledWindow()
        self.scrolled_window_ciudadanos.set_vexpand(True)
        self.scrolled_window_ciudadanos.set_hexpand(True)
        self.textview_ciudadanos = Gtk.TextView()
        self.textview_ciudadanos.set_editable(False)
        self.textbuffer_ciudadanos = self.textview_ciudadanos.get_buffer()
        self.scrolled_window_ciudadanos.set_child(self.textview_ciudadanos)
        self.page2.append(self.scrolled_window_ciudadanos)

    def init_simulation(self):
        """Inicializar los parámetros de la simulación"""
        covid = Enfermedad(infeccion_probable=0.3, promedio_pasos=18)
        talca = Comunidad(num_ciudadanos=2000, promedio_conexion_fisica=8, enfermedad=covid, num_infectados=10, probabilidad_conexion_fisica=0.8, archivo_nombres="nombres_apellidos.csv")
        self.simulador = Simulador()
        self.simulador.set_comunidad(comunidad=talca)
        self.dia_actual = 0

    def on_step_button_clicked(self, widget):
        """Manejar el evento de click en el botón de avanzar día"""
        self.dia_actual += 1
        self.simulador.comunidad.simular_dia()
        
        # Obtener conteo de estados
        susceptibles = self.simulador.comunidad.contar_estado("Susceptible")
        infectados = self.simulador.comunidad.contar_estado("Infectado")
        recuperados = self.simulador.comunidad.contar_estado("Recuperado")
        total_contagios = infectados + recuperados

        # Actualizar resultados diarios
        self.update_text_buffer(self.textbuffer_resultados, f"Día {self.dia_actual}: Susceptibles: {susceptibles}, Infectados: {infectados}, Recuperados: {recuperados}, Total Contagios: {total_contagios}\n", max_lines=20)

        # Actualizar detalles de ciudadanos
        texto_ciudadanos = "\n".join([f"{ciudadano.nombre} {ciudadano.apellido}, Estado: {ciudadano.estado}, Días Infectado: {ciudadano.dias_infectado}" for ciudadano in self.simulador.comunidad.ciudadanos[:50]])
        self.update_text_buffer(self.textbuffer_ciudadanos, texto_ciudadanos, max_lines=50)

    def update_text_buffer(self, textbuffer, new_text, max_lines):
        """Actualizar el buffer de texto, limitando la cantidad de líneas para evitar sobrecarga"""
        start_iter = textbuffer.get_start_iter()
        end_iter = textbuffer.get_end_iter()
        lines = textbuffer.get_text(start_iter, end_iter, True).split('\n')
        if len(lines) > max_lines:
            lines = lines[-max_lines:]
        textbuffer.set_text('\n'.join(lines))
        textbuffer.insert(textbuffer.get_end_iter(), new_text)

class AplicacionSimulacion(Gtk.Application):
    def __init__(self):
        super().__init__()

    def do_activate(self):
        ventana = MainWindow(self)
        ventana.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

app = AplicacionSimulacion()
app.run()
