import psutil
import time
from influxdb import InfluxDBClient

# Configuración de conexión
client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('boar_telemetry')

print("B.O.A.R. Telemetry System: ONLINE")

try:
    while True:
        # 1. Obtener datos del sistema
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        temp = 0
        
        # Intentar leer temperatura del Rock Pi
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                temp = int(f.read()) / 1000
        except:
            temp = 0

        # 2. Estructurar el paquete de datos
        data = [
            {
                "measurement": "vital_signs",
                "fields": {
                    "cpu_usage": cpu,
                    "ram_usage": ram,
                    "temperature": temp
                }
            }
        ]

        # 3. Enviar a InfluxDB
        client.write_points(data)
        print(f"Enviado: CPU: {cpu}% | RAM: {ram}% | Temp: {temp}°C")
        
except KeyboardInterrupt:
    print("Telemetry Stopped.")
