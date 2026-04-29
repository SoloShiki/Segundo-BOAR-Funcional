import cv2
import os
import sys
from edge_impulse_linux.image import ImageImpulseRunner

# --- CONFIGURACIÓN ---
# Usamos la ruta absoluta para evitar el FileNotFoundError en el entorno de la Rock Pi
MODEL_PATH = "/home/rock/BOARWRO/Robos/modelfile.eim"
THRESHOLD = 0.75
DETECTION_LIMIT = 5
VIDEO_DEVICE_ID = 0  # Cambia a 1 si usas una cámara externa y no detecta la 0

def main():
    counter = 0
    
    # Verificar si el archivo existe antes de iniciar
    if not os.path.exists(MODEL_PATH):
        print(f"Error: No se encuentra el archivo en {MODEL_PATH}")
        print("Asegúrate de haberle dado permisos con: chmod +x modelfile.eim")
        return

    print("Iniciando B.O.A.R. Vision System...")

    # El bloque 'with' asegura que el runner se cierre correctamente al terminar
    with ImageImpulseRunner(MODEL_PATH) as runner:
        try:
            # Inicializar el modelo
            model_info = runner.init()
            print(f"Modelo cargado exitosamente: {model_info['project']['name']}")
            print(f"Buscando detecciones con un umbral de {THRESHOLD}...")

            # El runner gestiona la cámara internamente pasando solo el ID
            for res, img in runner.classifier(VIDEO_DEVICE_ID):
                
                if "bounding_boxes" in res["result"]:
                    detections_in_frame = False
                    
                    for bbox in res["result"]["bounding_boxes"]:
                        if bbox["value"] >= THRESHOLD:
                            counter += 1
                            detections_in_frame = True
                            print(f"[{counter}/{DETECTION_LIMIT}] Objeto: {bbox['label']} | Confianza: {bbox['value']:.2f}")
                            
                            # Si alcanzamos el límite, salimos del bucle de bboxes
                            if counter >= DETECTION_LIMIT:
                                break
                    
                # Condición de salida del generador del clasificador
                if counter >= DETECTION_LIMIT:
                    print("\nSe ha alcanzado el límite de 5 detecciones. Finalizando programa...")
                    break

        except Exception as e:
            print(f"Error durante la ejecución: {e}")
        
        finally:
            # Aunque el 'with' lo maneja, forzamos el stop por seguridad en hardware embebido
            if runner:
                runner.stop()
                print("Runner detenido correctamente.")

if __name__ == "__main__":
    main()
