

# B.O.A.R. (Building Operations and Autonomous Rescue) 🐗🚑

**B.O.A.R.** es un ecosistema robótico de rescate diseñado para la detección de víctimas y la estabilización de entornos en zonas de desastre. A diferencia de los sistemas convencionales, B.O.A.R. integra **Edge AI** y un sistema de control distribuido para operar de forma totalmente autónoma sin dependencia de la nube.

## 🧠 Arquitectura del Sistema

El funcionamiento se basa en una arquitectura **Master-Slave** (Maestro-Esclavo) que divide la carga de trabajo en dos niveles de procesamiento:

### 1. Nivel Superior: Inteligencia y Visión (Nodo Maestro)
* **Hardware:** Rock Pi 3C.
* **SO:** Debian 12 Bookworm (Optimizado para estabilidad).
* **Funciones:**
    * **Computer Vision:** Modelo de detección entrenado con +4,900 imágenes para identificación de objetivos.
    * **LLM (Large Language Model):** Toma de decisiones lógica basada en lo solicitado por el usuario.
    * **Telemetría:** Servidor MQTT para envío de datos en tiempo real.
    * **Acceso Remoto:** Gestión total del sistema vía SSH para diagnósticos de emergencia.

### 2. Nivel Inferior: Control y Actuación (Nodo Esclavo)
* **Hardware:** LEGO EV3.
* **Funciones:**
    * **Navegación:** Control de motores.
    * **Seguridad:** Gestión de sensores ultrasónicos para el protocolo de frenado activo (distancia de seguridad de 15 cm).
    * **Resiliencia:** Capacidad de mantener movimientos básicos incluso si el nodo maestro se encuentra en reinicio o carga pesada.

---

## 🚀 Sellpoints Técnicos

* **Edge Computing:** Procesamiento local completo. El robot no requiere conexión a internet para ejecutar sus modelos de IA o tomar decisiones de rescate.
* **Redundancia de Comunicación:** Sistema de monitoreo dual mediante telemetría MQTT y respaldo administrativo por SSH.
* **Detección de Alta Precisión:** Algoritmos de visión artificial con umbrales de confianza ajustados para minimizar falsos positivos en entornos complejos.
* **Chasis Resiliente:** Diseño de carcasa integrada para protección de componentes críticos contra polvo y condiciones adversas.

---

## 🛠️ Stack Tecnológico

* **Lenguajes:** Python (IA, lógica, control de motores y sensores)
* **Protocolos:** MQTT, SSH
* **IA:** TensorFlow Lite / Edge Impulse / Ollama 3.2
* **Monitoreo:** Dashboard de telemetría.

---

## 👥 Equipo (B.O.A.R. Industries)

* **Carlos Alberto Ortiz:** Programación e Interlocución Técnica.
* **Pedro Luis Mena:** Construcción y Diseño Mecánico.
* **Angie Sang:** Lead Research y Análisis de Datos.

---

## 📈 Roadmap

- [ ] Implementación de Navegación SLAM con LiDAR 3D.
- [ ] Desarrollo de comunicación para sistemas **Swarm** (Enjambre).
- [ ] Optimización de consumo energético para misiones de larga duración.

---

> **Nota:** Este proyecto ha sido desarrollado como parte de la participación en la **World Robot Olympiad (WRO)**, representando la innovación robótica desde la República Dominicana.
