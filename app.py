#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor web con Flask - Diseño responsive para móviles
"""

from flask import Flask, request, jsonify, render_template_string
import socket
import platform

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informacion del Servidor</title>
    <style>
        *, *::before, *::after {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: Arial, sans-serif;
            background: #f0f4f8;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 16px;
        }

        .container {
            width: 100%;
            max-width: 600px;
        }

        .card {
            background: #ffffff;
            border-radius: 14px;
            padding: 24px 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.10);
        }

        h1 {
            color: #1a1a2e;
            font-size: clamp(1.2rem, 5vw, 1.6rem);
            border-bottom: 3px solid #0078d4;
            padding-bottom: 12px;
            margin-bottom: 20px;
        }

        .info-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 12px;
        }

        .info {
            background: #f4f8ff;
            border-left: 4px solid #0078d4;
            border-radius: 8px;
            padding: 12px 14px;
        }

        .label {
            font-weight: bold;
            color: #0078d4;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 4px;
        }

        .value {
            font-family: 'Courier New', monospace;
            font-size: clamp(0.85rem, 3.5vw, 1rem);
            color: #1a1a2e;
            word-break: break-all;
        }

        .actions {
            margin-top: 20px;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        .btn {
            flex: 1 1 140px;
            background: #0078d4;
            color: white;
            border: none;
            padding: 12px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: bold;
            text-align: center;
            text-decoration: none;
            transition: background 0.2s ease;
            display: inline-block;
        }

        .btn:hover, .btn:active {
            background: #005a9e;
        }

        .btn-outline {
            background: transparent;
            border: 2px solid #0078d4;
            color: #0078d4;
        }

        .btn-outline:hover, .btn-outline:active {
            background: #0078d4;
            color: white;
        }

        .footer {
            margin-top: 18px;
            font-size: 0.75rem;
            color: #888;
            text-align: center;
        }

        @media (min-width: 480px) {
            .info-grid {
                grid-template-columns: 1fr 1fr;
            }
        }

        @media (min-width: 600px) {
            .card {
                padding: 32px 28px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>Informacion del Servidor</h1>

            <div class="info-grid">
                <div class="info">
                    <div class="label">Nombre del equipo</div>
                    <div class="value">{{ hostname }}</div>
                </div>
                <div class="info">
                    <div class="label">IP Local</div>
                    <div class="value">{{ local_ip }}</div>
                </div>
                <div class="info">
                    <div class="label">Sistema Operativo</div>
                    <div class="value">{{ os_info }}</div>
                </div>
                <div class="info">
                    <div class="label">Tu IP (visitante)</div>
                    <div class="value">{{ visitor_ip }}</div>
                </div>
            </div>

            <div class="actions">
                <button class="btn" onclick="location.reload()">&#x21BB; Actualizar</button>
                <a class="btn btn-outline" href="/api/info">{ } Ver API JSON</a>
            </div>

            <div class="footer">Servidor Python Flask</div>
        </div>
    </div>
</body>
</html>
"""

def get_local_ip():
    """Obtiene la IP local real del servidor"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return socket.gethostbyname(socket.gethostname())

@app.route('/')
def index():
    """Pagina principal con informacion"""
    hostname = socket.gethostname()
    local_ip = get_local_ip()
    visitor_ip = request.remote_addr
    os_info = f"{platform.system()} {platform.release()}"

    return render_template_string(HTML_TEMPLATE,
                                   hostname=hostname,
                                   local_ip=local_ip,
                                   os_info=os_info,
                                   visitor_ip=visitor_ip)

@app.route('/api/info')
def api_info():
    """API REST que devuelve informacion en formato JSON"""
    hostname = socket.gethostname()
    local_ip = get_local_ip()
    visitor_ip = request.remote_addr

    return jsonify({
        'servidor': {
            'nombre': hostname,
            'ip_local': local_ip,
            'sistema_operativo': platform.system(),
            'version_so': platform.release(),
            'arquitectura': platform.machine()
        },
        'visitante': {
            'ip': visitor_ip,
            'user_agent': request.headers.get('User-Agent')
        }
    })

if __name__ == '__main__':
    local_ip = get_local_ip()
    print("=" * 60)
    print("Servidor Flask iniciado")
    print("=" * 60)
    print(f"Acceso local:     http://localhost:8888")
    print(f"Acceso red local: http://{local_ip}:8888")
    print(f"API JSON:         http://{local_ip}:8888/api/info")
    print("=" * 60)
    print("Presiona CTRL+C para detener el servidor")
    print("=" * 60)

    app.run(host='0.0.0.0', port=8888, debug=False)
