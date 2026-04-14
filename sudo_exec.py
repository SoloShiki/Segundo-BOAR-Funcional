import llm
import subprocess

# Configuramos el modelo y el template
model = llm.get_model("ollama/llama3") # Asegúrate que este sea el nombre que viste en 'llm models'

def execute_protocol(command):
    prompt = f"Si la siguiente orden pide ejecutar un test, responde ÚNICAMENTE con el código python necesario. Orden: {command}"
    
    # Obtenemos la respuesta de la IA usando tu template de Boar
    response = model.prompt(prompt, system="Eres el sistema de ejecución de Boar Industries. Si el usuario pide un test, genera el código.")
    code = response.text().strip()
    
    # Limpiamos bloques de código si la IA los pone (```python ... ```)
    if "```" in code:
        code = code.split("```")[1].replace("python", "").strip()

    print(f"\n[BOAR PROTOCOL] Ejecutando código generado:\n{code}\n")
    
    # Ejecución real (¡Cuidado! Esto es una prueba)
    with open("temp_boar_test.py", "w") as f:
        f.write(code)
    
    subprocess.run(["python3", "temp_boar_test.py"])

if __name__ == "__main__":
    cmd = input("Boar Industries > Ingrese orden de comando: ")
    if "ejecutar test" in cmd.lower():
        execute_protocol(cmd)
    else:
        print("Orden no reconocida por el protocolo de ejecución.")
