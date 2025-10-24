from flask import Flask, render_template_string, request, jsonify
import database as db
import random
import os

app = Flask(__name__)
db.init_db()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Ruleta Casino</title>
    <style>
        body { 
            font-family: 'Arial', sans-serif; 
            text-align: center; 
            margin: 20px; 
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            color: white;
            min-height: 100vh;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        
        h1 {
            color: #ffd700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            margin-bottom: 30px;
        }
        
        .panel-usuario {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
        }
        
        input, select {
            padding: 8px;
            margin: 5px;
            border: none;
            border-radius: 5px;
            background: rgba(255,255,255,0.9);
        }
        
        .ruleta { 
            width: 350px; 
            height: 350px; 
            border: 5px solid #ffd700; 
            border-radius: 50%; 
            margin: 20px auto;
            position: relative;
            background: #0a5c0a;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(255,215,0,0.5);
        }
        
        .numero {
            position: absolute;
            width: 35px;
            height: 35px;
            line-height: 35px;
            text-align: center;
            color: white;
            font-weight: bold;
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            transform-origin: center;
        }
        
        .boton-apuesta { 
            margin: 5px; 
            padding: 12px 20px; 
            background: #007bff; 
            color: white; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .boton-apuesta:hover {
            background: #0056b3;
            transform: scale(1.05);
        }
        
        .boton-rojo {
            background: #dc3545;
        }
        
        .boton-rojo:hover {
            background: #c82333;
        }
        
        .boton-negro {
            background: #212529;
        }
        
        .boton-negro:hover {
            background: #000;
        }
        
        #resultado { 
            margin-top: 20px; 
            font-size: 1.3em; 
            font-weight: bold;
            padding: 15px;
            border-radius: 10px;
            background: rgba(255,255,255,0.1);
        }
        
        .ganador {
            color: #7fff00;
            animation: pulse 0.5s infinite;
        }
        
        .perdedor {
            color: #ff4444;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .info-saldo {
            font-size: 1.2em;
            color: #ffd700;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎰 Ruleta Casino 🎰</h1>
        
        <div class="panel-usuario">
            <div>
                <label>👤 Usuario: </label>
                <input type="text" id="usuario" placeholder="Ingresa tu nombre">
                <button class="boton-apuesta" onclick="cargarUsuario()">Cargar Usuario</button>
            </div>
            <div id="info-usuario" class="info-saldo"></div>
        </div>
        
        <div class="ruleta" id="ruleta"></div>
        
        <div class="panel-usuario">
            <div>
                <label>💰 Apuesta: $</label>
                <input type="number" id="monto" min="1" value="10" style="width: 80px;">
                
                <label>🎯 Tipo: </label>
                <select id="tipo-apuesta">
                    <option value="color">Rojo/Negro</option>
                    <option value="numero">Número específico</option>
                </select>
            </div>
            
            <div id="opciones-apuesta" style="margin-top: 15px;">
                <button class="boton-apuesta boton-rojo" onclick="apostar('rojo')">🔴 ROJO (x2)</button>
                <button class="boton-apuesta boton-negro" onclick="apostar('negro')">⚫ NEGRO (x2)</button>
            </div>
            
            <div id="opciones-numero" style="display:none; margin-top: 15px;">
                <input type="number" id="numero-apuesta" min="0" max="36" placeholder="0-36" style="width: 80px;">
                <button class="boton-apuesta" onclick="apostarNumero()">🎯 Apostar Número (x36)</button>
            </div>
        </div>
        
        <div id="resultado"></div>
    </div>

    <script>
        let usuarioActual = null;
        
        function cargarUsuario() {
            const usuario = document.getElementById('usuario').value;
            if (!usuario) {
                alert('Por favor ingresa un nombre de usuario');
                return;
            }
            
            fetch('/usuario/' + usuario)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        document.getElementById('info-usuario').innerHTML = 
                            `<span style="color: #ff4444;">${data.error}</span>`;
                        usuarioActual = null;
                    } else {
                        document.getElementById('info-usuario').innerHTML = 
                            `👤 Usuario: <strong>${data.nombre}</strong> | 💰 Saldo: <strong>$${data.saldo}</strong>`;
                        usuarioActual = data.nombre;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error al cargar usuario');
                });
        }

        function apostar(tipo) {
            if (!usuarioActual) {
                alert('Primero carga un usuario');
                return;
            }
            
            const monto = parseInt(document.getElementById('monto').value);
            if (!monto || monto <= 0) {
                alert('Ingresa un monto válido');
                return;
            }
            
            fetch('/apostar', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    usuario: usuarioActual,
                    tipo: tipo,
                    monto: monto
                })
            }).then(r => r.json()).then(data => {
                mostrarResultado(data);
            }).catch(error => {
                console.error('Error:', error);
                alert('Error al realizar apuesta');
            });
        }

        function apostarNumero() {
            if (!usuarioActual) {
                alert('Primero carga un usuario');
                return;
            }
            
            const monto = parseInt(document.getElementById('monto').value);
            const numero = parseInt(document.getElementById('numero-apuesta').value);
            
            if (!monto || monto <= 0) {
                alert('Ingresa un monto válido');
                return;
            }
            
            if (numero < 0 || numero > 36 || isNaN(numero)) {
                alert('Ingresa un número válido entre 0 y 36');
                return;
            }
            
            fetch('/apostar', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    usuario: usuarioActual,
                    tipo: 'numero',
                    valor: numero,
                    monto: monto
                })
            }).then(r => r.json()).then(data => {
                mostrarResultado(data);
            }).catch(error => {
                console.error('Error:', error);
                alert('Error al realizar apuesta');
            });
        }

        function mostrarResultado(data) {
            const resultadoDiv = document.getElementById('resultado');
            
            if (data.error) {
                resultadoDiv.innerHTML = `<div class="perdedor">❌ ${data.error}</div>`;
                return;
            }
            
            const esGanador = data.resultado.includes('¡Ganaste!');
            resultadoDiv.innerHTML = `
                <div class="${esGanador ? 'ganador' : 'perdedor'}">
                    ${esGanador ? '🎉' : '😢'} ${data.resultado}<br>
                    💰 Nuevo saldo: $${data.nuevo_saldo}
                </div>
            `;
            
            // Actualizar información del usuario
            cargarUsuario();
        }

        document.getElementById('tipo-apuesta').addEventListener('change', function() {
            const tipo = this.value;
            document.getElementById('opciones-apuesta').style.display = 
                tipo === 'color' ? 'block' : 'none';
            document.getElementById('opciones-numero').style.display = 
                tipo === 'numero' ? 'block' : 'none';
        });

        // Dibujar ruleta
        function dibujarRuleta() {
            const ruleta = document.getElementById('ruleta');
            ruleta.innerHTML = '';
            
            const numeros = [0,32,15,19,4,21,2,25,17,34,6,27,13,36,11,30,8,23,10,5,24,16,33,1,20,14,31,9,22,18,29,7,28,12,35,3,26];
            const totalNumeros = numeros.length;
            
            for (let i = 0; i < totalNumeros; i++) {
                const angulo = (i / totalNumeros) * 2 * Math.PI;
                const radio = 160;
                const x = 175 + radio * Math.cos(angulo);
                const y = 175 + radio * Math.sin(angulo);
                
                const div = document.createElement('div');
                div.className = 'numero';
                div.textContent = numeros[i];
                div.style.left = (x - 17.5) + 'px';
                div.style.top = (y - 17.5) + 'px';
                
                // Colores de la ruleta europea
                if (numeros[i] === 0) {
                    div.style.backgroundColor = 'green';
                } else if ([1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36].includes(numeros[i])) {
                    div.style.backgroundColor = '#dc3545'; // Rojo
                } else {
                    div.style.backgroundColor = '#212529'; // Negro
                }
                
                ruleta.appendChild(div);
            }
        }

        // Inicializar ruleta al cargar la página
        window.onload = dibujarRuleta;
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/usuario/<nombre>')
def obtener_usuario(nombre):
    usuario = db.get_usuario(nombre)
    if usuario:
        return jsonify({'nombre': usuario[1], 'saldo': usuario[2]})
    return jsonify({'error': 'Usuario no encontrado'}), 404

@app.route('/apostar', methods=['POST'])
def apostar():
    data = request.json
    usuario = db.get_usuario(data['usuario'])
    
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    saldo_actual = usuario[2]
    monto = data['monto']
    
    if monto > saldo_actual:
        return jsonify({'error': 'Saldo insuficiente'}), 400
    
    # Generar número ganador
    numero_ganador = random.randint(0, 36)
    
    # Determinar color ganador (ruleta europea)
    rojos = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
    color_ganador = 'rojo' if numero_ganador in rojos else 'negro'
    
    # Calcular resultado
    if data['tipo'] == 'numero':
        if data['valor'] == numero_ganador:
            nuevo_saldo = saldo_actual + (monto * 35)  # Paga 35:1
            resultado = f"¡Ganaste! Número {numero_ganador} - ¡Felicidades!"
        else:
            nuevo_saldo = saldo_actual - monto
            resultado = f"Perdiste. Número ganador: {numero_ganador}"
            
    else:  # Apuesta a color
        if data['tipo'] == color_ganador:
            nuevo_saldo = saldo_actual + monto  # Paga 1:1
            resultado = f"¡Ganaste! Número {numero_ganador} ({color_ganador})"
        else:
            nuevo_saldo = saldo_actual - monto
            resultado = f"Perdiste. Número ganador: {numero_ganador} ({color_ganador})"
    
    # Actualizar saldo en base de datos
    db.actualizar_saldo(data['usuario'], nuevo_saldo)
    
    return jsonify({
        'resultado': resultado,
        'nuevo_saldo': nuevo_saldo,
        'numero_ganador': numero_ganador
    })

if __name__ == '__main__':
    print("🎰 Servidor de Ruleta iniciando...")
    print("🌐 Accede en: http://localhost:5678")
    print("⏹️  Presiona Ctrl+C para detener el servidor")
    app.run(host='0.0.0.0', port=5678, debug=False)
