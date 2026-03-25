# Informacion del Servidor - Flask App

Aplicación web en Flask que muestra información del servidor y la IP del visitante.

## Endpoints

- `/` — Página principal con información del servidor
- `/api/info` — API REST en formato JSON

## Despliegue en Render

1. Sube este repositorio a GitHub.
2. En [render.com](https://render.com), crea un nuevo **Web Service** conectado al repositorio.
3. Render detectará automáticamente el archivo `render.yaml`.
4. En la configuración del servicio, agrega el dominio personalizado `miip.ts24h.net`.

## Ejecución local

```bash
pip install -r requirements.txt
python app.py
```
