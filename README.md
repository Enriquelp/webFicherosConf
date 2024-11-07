# Visualización de Modelos de Características para Kubernetes y Docker

Este proyecto es una página web que funciona como interfaz para la visualización de dos modelos de características (Feature Models, FM): uno de **manifiestos de Kubernetes** y otro de **Docker**. Los modelos se presentan en forma de árbol, donde cada nodo representa una característica y puede desplegarse para explorar más a fondo la estructura del modelo.

## Características

- **Visualización en forma de árbol**: La interfaz muestra los modelos de características en un árbol interactivo, lo que permite navegar entre las diferentes propiedades y configuraciones de cada nodo.
- **Desplegables informativos**: Cada nodo tiene un pequeño desplegable que muestra información adicional sobre su configuración.
- **Carga de archivos JSON**: La página permite subir un archivo de configuración en formato JSON con los valores de las características del modelo, lo cual facilita la personalización y modificación de los modelos.
- **Generación de manifiestos de Kubernetes**: A partir de la configuración en el archivo JSON, se puede generar un manifiesto de Kubernetes en formato YAML, listo para ser utilizado en la creación y despliegue de objetos en un entorno Kubernetes.
- **Comprobación de la validez del manifiesto**: Es posible comprobar la validez del manifiesto sin la necesidad de tener que desplegarlos en un cluster de Kubernetes.

## Instalación

Sigue estos pasos para configurar y ejecutar el proyecto localmente.

1. **Clonar el repositorio**

   ```
   git clone https://github.com/Enriquelp/webFicherosConf.git
   cd webFicherosConf

   ```
2. **Crear el entorno virtual**

   Asegúrate de tener Python instalado. Luego, crea y activa un entorno virtual:

   ```
   python -m venv venv
   .\venv\Scripts\activate # activar entorno virtual en Windows
   source venv/bin/activate # activar entorno virtual en Linux
   ```
3. **Instalar las dependencias**
  
   Con el entorno virtual activado, instala las dependencias con el archivo "requirements.txt"

   ```
   pip install -r requirements.txt
   ```
4. **Ejecutar la aplicacion**
   ```
   python app.py
   ```
   La aplicación estará disponible en http://localhost:5000.
