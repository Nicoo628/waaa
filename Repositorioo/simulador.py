class Simulador:
    def __init__(self):
        self.comunidad = None  # Inicializar la comunidad como None

    def set_comunidad(self, comunidad):
        self.comunidad = comunidad  # Establecer la comunidad

    def run(self, pasos):
        print("Iniciando simulación...")
        for dia in range(1, pasos + 1):
            self.comunidad.simular_dia()  # Simular el día para la comunidad
            susceptibles = self.comunidad.contar_estado("Susceptible")
            infectados = self.comunidad.contar_estado("Infectado")
            recuperados = self.comunidad.contar_estado("Recuperado")
            total_contagios = infectados + recuperados  # Total de contagios (infectados + recuperados)
            print(f"Día {dia}: Susceptibles: {susceptibles}, Infectados: {infectados}, Recuperados: {recuperados}, Total Contagios: {total_contagios}")