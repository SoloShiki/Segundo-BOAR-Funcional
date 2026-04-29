#!/usr/bin/env python3
import socket
import time
from ev3dev2.motor import MoveTank, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_3

# --- CONFIGURACIÓN DE HARDWARE ---
motores_traccion = MoveTank(OUTPUT_B, OUTPUT_A)
motor_mediano = MediumMotor(OUTPUT_C)
sensor = UltrasonicSensor(INPUT_3)

# --- PARÁMETROS ---
DISTANCIA_CRITICA = 15.0
VELOCIDAD_CRUCERO = 20

# --- CONFIGURACIÓN DE RED ---
UDP_IP = "0.0.0.0"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(False) 
sock.bind((UDP_IP, UDP_PORT))

print("BOAR-OS: Sistema con Actuador C listo (v3.5 compatible)")

movimiento_activo = False

try:
    while True:
        # 1. MONITOREO DEL SENSOR
        distancia_actual = sensor.distance_centimeters
        
        if movimiento_activo and distancia_actual <= DISTANCIA_CRITICA:
            motores_traccion.off(brake=True)
            movimiento_activo = False
            # Usamos .format() en lugar de f-strings para compatibilidad
            print("Obstaculo a {0:.1f}cm. Activando Motor C...".format(distancia_actual))
            
            # Motor C: 10% velocidad, 1.5 seg
            motor_mediano.on_for_seconds(speed=10, seconds=1.5, brake=True)
            print("Accion de Motor C completada.")

        # 2. ESCUCHA DE COMANDOS UDP
        try:
            data, addr = sock.recvfrom(1024)
            comando = data.decode().strip()
            
            if comando == "AVANZAR":
                if distancia_actual > DISTANCIA_CRITICA:
                    motores_traccion.on(VELOCIDAD_CRUCERO, VELOCIDAD_CRUCERO)
                    movimiento_activo = True
                else:
                    print("Bloqueado: Camino obstruido")

            elif comando == "PARAR":
                motores_traccion.off(brake=True)
                movimiento_activo = False

            elif comando == "LEER":
                respuesta = str(distancia_actual)
                sock.sendto(respuesta.encode(), addr)

        except BlockingIOError:
            pass

except KeyboardInterrupt:
    motores_traccion.off(brake=False)
    motor_mediano.off(brake=False)
    print("\nSistema detenido.")
finally:
    sock.close()
