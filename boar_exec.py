import llm
import subprocess
import os
import re

# Cargamos el modelo 3B (El cerebro de BOAR Industries)
MODELO = "ollama/llama3.2:3b"
try:
    model = llm.get_model(MODELO)
except:
    model = llm.get_model("llama3.2:3b")

# --- SYSTEM PROMPT INTEGRAL Y DEFINITIVO ---
SYSTEM_PROMPT = """Eres el Operador de Inteligencia Central de BOAR Industries, ejecutándote sobre BoarOS. Tu propósito es asistir al equipo (Carlos, Pedro y Angie) en la operación del robot B.O.A.R. (Building Operations & Autonomous Rescue).

### IDENTIDAD Y FILOSOFÍA
- Misión: INTERVENCIÓN ESTRUCTURAL ACTIVA. No eres un espectador; eres una herramienta que sostiene y estabiliza.
- Prioridad: Las "72 Horas Doradas" y la seguridad estructural.

### ARQUITECTURA TÉCNICA DE B.O.A.R.
1. Rock Pi (Visión/IA): Detección de víctimas con Edge Impulse.
2. EV3 (Navegación): Gestión de motores y sensores de proximidad.
3. Arduino (Actuación): Control del actuador lineal para soporte de escombros.

### PROTOCOLO DE EJECUCIÓN (ESTRICTO)
Cuando el equipo solicite una acción técnica o diagnóstico, identifica el script necesario y responde SIEMPRE con este formato:
[[RUN_SCRIPT: nombre_del_archivo.py]]

REGLAS DE RESPUESTA:
- Sé breve y técnico. No des explicaciones innecesarias.
- NO generes bloques de código Python.
- Aplica la TRIPLE VERIFICACIÓN: 1. Firma de IA, 2. Validación de Distancia, 3. Estabilidad Temporal.

### LISTA DE SCRIPTS AUTORIZADOS
- system.py (Reporte de sensores y hardware)
- test_actuador.py (Prueba de extensión del pistón)
- scan_entorno.py (Mapeo LiDAR de escombros)
- reset_boar.py (Reinicio de módulos)
"""

def ejecutar_protocolo_boar(archivo):
    # Limpieza de seguridad para el nombre del archivo
    archivo = archivo.strip().replace("[", "").replace("]", "").replace("`", "").replace(":", "").replace("RUN_SCRIPT", "").strip()
    
    ruta_completa = os.path.join(os.getcwd(), archivo)
    
    print("\n" + "—"*45)
    if os.path.exists(ruta_completa):
        print(f"[BOAR-OS] Iniciando ejecución: {archivo}")
        try:
            # Ejecución en el entorno local de Debian/WSL
            process = subprocess.run(["python3", ruta_completa], capture_output=True, text=True)
            if process.stdout:
                print(f"[SALIDA B.O.A.R.]:\n{process.stdout}")
            if process.stderr:
                print(f"[DEBUG/ERROR]:\n{process.stderr}")
        except Exception as e:
            print(f"[FALLO CRÍTICO]: {e}")
    else:
        print(f"[ALERTA] Archivo '{archivo}' no encontrado en el directorio activo.")
        print(f"Directorio: {os.getcwd()}")
    print("—"*45 + "\n")

def loop_agente():
    print(f"=== BOAR Industries IA v1.5 | Modelo: {MODELO} ===")
    print(f"BoarOS: Online | Listo para órdenes de Carlos, Pedro y Angie.")
    history = []

    while True:
        try:
            prompt_usuario = input("\nBOAR-HQ > ")
            if prompt_usuario.lower() in ["exit", "salir", "shutdown"]:
                print("Desconectando Núcleo de BOAR Industries...")
                break

            # Consulta al modelo con el System Prompt reforzado
            response = model.prompt(prompt_usuario, system=SYSTEM_PROMPT)
            output = response.text()

            # REGEX DE ALTA PRECISIÓN: Detecta la orden sin importar el formato de corchetes
            match = re.search(r"RUN_SCRIPT:\s*([\w\d\._-]+\.py)", output, re.IGNORECASE)
            
            if match:
                nombre_archivo = match.group(1)
                # Limpiamos el texto para mostrar solo la confirmación técnica
                clean_output = re.sub(r"\[\[.*?\]\]|\[.*?\]", "", output).strip()
                
                if clean_output:
                    print(f"\nAI: {clean_output}")
                else:
                    print(f"\nAI: Iniciando protocolo técnico solicitado...")
                
                ejecutar_protocolo_boar(nombre_archivo)
            else:
                # Si no hay comando, respuesta normal (limpia de posibles alucinaciones de código)
                print(f"\nAI: {output.split('```')[0].strip()}")

            history.append(f"U: {prompt_usuario} | AI: {output}")

        except Exception as e:
            print(f"Error en el ciclo de ejecución: {e}")

if __name__ == "__main__":
    loop_agente()
