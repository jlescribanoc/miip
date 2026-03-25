#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor web con Flask
"""

from flask import Flask, request, jsonify, render_template_string
import socket
import platform

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Informacion del Servidor</title>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #333; border-bottom: 3px solid #0078d4; padding-bottom: 10px; }
        .info { margin: 15px 0; padding: 10px; background: #f9f9f9; border-left: 4px solid #0078d4; }
        .label { font-weight: bold; color: #0078d4; }
        .value { font-family: monospace; font-size: 1.1em; margin-top: 5px; }
        .footer { margin-top: 20px; font-size: 0.8em; color: #666; text-align: center; }
        .refresh-btn {
            background: #0078d4;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 15px;
        }
        .refresh-btn:hover {
            background: #005a9e;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>Informacion del Servidor</h1>
        <div class="info">
            <div class="label">Nombre del equipo:</div>
            <div class="value">{{ hostname }}</div>
        </div>
        <div class="info">
            <div class="label">IP Local:</div>
            <div class="value">{{ local_ip }}</div>
        </div>
        <div class="info">
            <div class="label">Sistema Operativo:</div>
            <div class="value">{{ os_info }}</div>
        </div>
        <div class="info">
            <div class="label">Tu IP (visitante):</div>
            <div class="value">{{ visitor_ip }}</div>
        </div>
        <button class="refresh-btn" onclick="location.reload()">Actualizar</button>
        <div class="footer">
            Servidor Python Flask | <a href="/api/info">API JSON</a>
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
    print(f"Acceso local:    http://localhost:5000")
    print(f"Acceso red local: http://{local_ip}:5000")
    print(f"API JSON:        http://{local_ip}:5000/api/info")
    print("=" * 60)
    print("Presiona CTRL+C para detener el servidor")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=8888, debug=False)
