import paho.mqtt.client as mqtt
import socket
import time
import os
import sys
from edge_impulse_linux.image import ImageImpulseRunner

# --- CONFIGURACIÓN ---
IP_EV3 = "169.254.62.76"
PORT_UDP = 5005
MQTT_BROKER = "localhost"
MODEL_PATH = "/home/rock/BOARWRO/Robos/modelfile.eim"
ETIQUETA_OBJETIVO = "persona"
THRESHOLD_IA = 0.75
UMBRAL_FRENADO = 16.0  # Un poco más de 15 para margen de error

# --- TOPICS MQTT ---
TOPIC_STATUS = "boar/status"
TOPIC_DIST = "boar/telemetry/distance"
TOPIC_IA = "boar/telemetry/ia"
TOPIC_EV3 = "boar/telemetry/ev3"

# --- CONFIGURACIÓN DE RED ---
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
try:
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_start()
    client.publish(TOPIC_STATUS, "SISTEMA INICIADO")
except Exception as e:
    print(f"[!] Error MQTT (¿Está mosquitto corriendo?): {e}")

sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_udp.settimeout(1.0)  # Aumentado a 1s para evitar el error 999

def enviar_ev3(cmd):
    """Envía un comando al EV3 y registra en MQTT"""
    try:
        sock_udp.sendto(cmd.encode(), (IP_EV3, PORT_UDP))
        client.publish(TOPIC_EV3, f"CMD_SENT: {cmd}")
    except Exception as e:
        print(f"[!] Error de red al enviar: {e}")

def obtener_distancia():
    """Solicita la distancia al EV3. Retorna 999 si falla."""
    try:
        enviar_ev3("LEER")
        data, _ = sock_udp.recvfrom(1024)
        dist = float(data.decode().strip())
        client.publish(TOPIC_DIST, dist)
        return dist
    except socket.timeout:
        return 999.0
    except Exception as e:
        return 999.0

# --- LÓGICA PRINCIPAL ---
def iniciar_mision():
    print("\n" + "="*50)
    print("      B.O.A.R. INDUSTRIES - OMNI PROTOCOL V2")
    print("="*50)

    # 1. FASE DE VISIÓN ARTIFICIAL
    print(f"[*] Escaneando área en busca de: '{ETIQUETA_OBJETIVO}'...")
    detecciones = 0
    
    with ImageImpulseRunner(MODEL_PATH) as runner:
        runner.init()
        client.publish(TOPIC_STATUS, "IA_ACTIVE")

        for res, img in runner.classifier(0): # ID 0 es la C270
            if "bounding_boxes" in res["result"]:
                found_in_frame = False
                for bbox in res["result"]["bounding_boxes"]:
                    if bbox["label"] == ETIQUETA_OBJETIVO and bbox["value"] >= THRESHOLD_IA:
                        detecciones += 1
                        found_in_frame = True
                        print(f"    [!] DETECTADO: {bbox['label']} ({detecciones}/5)")
                
                if found_in_frame:
                    client.publish(TOPIC_IA, f"DETECTED_{detecciones}")

            if detecciones >= 5:
                print("[OK] Objetivo confirmado. Iniciando aproximación.")
                client.publish(TOPIC_STATUS, "TARGET_CONFIRMED")
                break

    # 2. FASE DE NAVEGACIÓN Y RESCATE
    print("[*] Ordenando avance a motores A y B...")
    enviar_ev3("AVANZAR")

    try:
        while True:
            dist = obtener_distancia()
            
            if dist == 999.0:
                print("    [?] Reintentando conexión con EV3...", end='\r')
            else:
                print(f"    >>> DISTANCIA: {dist:.1f} cm    ", end='\r')

            # Lógica de frenado
            if dist <= UMBRAL_FRENADO:
                enviar_ev3("PARAR")
                print(f"\n[FRENADO] Distancia de seguridad: {dist}cm")
                client.publish(TOPIC_STATUS, "STOP_REACHED")
                
                # 3. ACCIÓN DEL ACTUADOR (MOTOR C)
                print("[*] Ejecutando Motor C (Bajar)...")
                enviar_ev3("MOTOR_C_DOWN")
                time.sleep(2.0) # Tiempo para que el EV3 complete su acción (1.5s + margen)
                
                print("[*] Ejecutando Motor C (Subir)...")
                enviar_ev3("MOTOR_C_UP")
                time.sleep(2.0)

                print("[ÉXITO] Misión de rescate completada.")
                client.publish(TOPIC_STATUS, "MISSION_COMPLETE")
                break
            
            time.sleep(0.1)

    except KeyboardInterrupt:
        enviar_ev3("PARAR")
        print("\n[!] Abortado por el usuario.")
    finally:
        client.loop_stop()

if __name__ == "__main__":
    if os.path.exists(MODEL_PATH):
        iniciar_mision()
    else:
        print(f"Error fatal: El modelo no existe en {MODEL_PATH}")
