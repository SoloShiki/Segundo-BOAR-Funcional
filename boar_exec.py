import requests
import json
import subprocess
import os
import re
import sys

# --- CONFIGURACIÓN DE RED Y RUTAS ---
PC_IP = "192.168.86.55"  # IP de tu servidor Ollama
OLLAMA_URL = f"http://{PC_IP}:11434/api/generate"
BASE_PATH = "/home/rock/BOARWRO/Robos"
MODELO = "llama3.2:3b"

# --- SYSTEM PROMPT: CEREBRO ESTRATÉGICO BOAROS ---
SYSTEM_PROMPT = """
[IDENTIDAD]
Eres BoarOS v2.6, la inteligencia artificial del robot B.O.A.R. (Autonomous Rescue Robot). 
Tu sede es Santiago de los Caballeros, República Dominicana.

[CONTEXTO SÍSMICO REAL - REPÚBLICA DOMINICANA]
- No confundir con Chile. En RD, el sismo relevante más reciente fue el 1 de febrero de 2023 (Mag 5.3, epicentro en Matanzas, Peravia).
- Santiago está ubicado sobre la Falla Septentrional, la más peligrosa del país.
- Conoces el terremoto de 1946 en Samaná (Mag 8.1), el más potente de nuestra historia.
- El objetivo de B.O.A.R. es actuar en las "Horas Doradas" tras un colapso estructural.

[EQUIPO]
- Carlos (Programador), Pedro (Constructor), Angie (Investigadora).

[PROTOCOLO DE RESPUESTA]
1. MODO INFORMATIVO: Si preguntan sobre el robot, componentes (Rock Pi 3C, LiDAR, Edge Impulse), sismología o prevención, responde con elocuencia y precisión técnica. NO ejecutes nada.
2. MODO ACCIÓN: SOLO si detectas una orden explícita de "iniciar misión", "arrancar", "comenzar rescate" o "ejecutar sistema", incluye la etiqueta: [[RUN_SCRIPT: system.py]].

[REGLA DE ORO]
Sé profesional, técnico y justifica siempre la necesidad del robot ante la vulnerabilidad sísmica de la isla.
"""

def consultar_cerebro_remoto(prompt):
    payload = {
        "model": MODELO,
        "prompt": f"System: {SYSTEM_PROMPT}\nUser: {prompt}",
        "stream": False
    }
    
    print("AI: Analizando...", end="", flush=True)
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        print("\r" + " " * 25 + "\r", end="") 
        
        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            return f"ERROR_SERVIDOR: Código {response.status_code}"
            
    except Exception as e:
        print("\r" + " " * 25 + "\r", end="")
        return f"ERROR_CONEXION: {e}"

def ejecutar_protocolo_boar(archivo):
    archivo = archivo.strip().lower()
    ruta_completa = os.path.join(BASE_PATH, archivo)
    
    print("\n" + "—"*55)
    if os.path.exists(ruta_completa):
        print(f"[BOAR-OS] DESPLEGANDO ACCIÓN FÍSICA: {archivo}")
        try:
            # Ejecución directa para ver logs de visión y sensores en tiempo real
            subprocess.run(["python3", ruta_completa])
        except Exception as e:
            print(f"[FALLO CRÍTICO DE HARDWARE]: {e}")
    else:
        print(f"[ALERTA] Archivo '{archivo}' no localizado en {BASE_PATH}")
    print("—"*55 + "\n")

def loop_agente():
    print(f"=====================================================")
    print(f"   BoarOS v2.6 | CENTRAL DE INTELIGENCIA Y RESCATE")
    print(f"=====================================================")
    print(f"Estado: ONLINE | Cerebro: {MODELO} | Cuerpo: Rock Pi 3C")
    print(f"Ubicación: Santiago, RD | Falla Activa: Septentrional")
    
    while True:
        try:
            prompt_usuario = input("\nBOAR-HQ > ")
            if not prompt_usuario.strip(): continue
            if prompt_usuario.lower() in ["exit", "salir", "quit"]: break

            output = consultar_cerebro_remoto(prompt_usuario)
            
            if "ERROR" in output:
                print(f"[!] {output}")
                continue

            # 1. Detectar si hay orden de ejecución
            match = re.search(r"RUN_SCRIPT[:\s]+([\w\d\._-]+\.py)", output, re.IGNORECASE)
            
            # 2. Limpiar la respuesta para que no se vea la etiqueta técnica en pantalla
            respuesta_voz = re.sub(r"\[\[RUN_SCRIPT:.*?\]\]", "", output).strip()
            
            if respuesta_voz:
                print(f"\nAI: {respuesta_voz}")

            # 3. Disparar ejecución física si corresponde
            if match:
                archivo_detectado = match.group(1).strip()
                print(f"\n[SISTEMA] >>> Autorización confirmada. Iniciando {archivo_detectado}...")
                ejecutar_protocolo_boar(archivo_detectado)

        except KeyboardInterrupt:
            print("\n[!] Apagando BoarOS por orden del operador...")
            break
        except Exception as e:
            print(f"\n[!] Error inesperado en el núcleo: {e}")

if __name__ == "__main__":
    loop_agente()
