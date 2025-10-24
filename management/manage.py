#!/usr/bin/env python3

import sys
import os
import sqlite3

# Agregar el directorio padre al path para importar database
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ruleta_server'))

from database import crear_usuario, get_usuario, actualizar_saldo, listar_usuarios

def mostrar_ayuda():
    print(""")
🎰 Sistema de Gestión - Ruleta Casino

Comandos disponibles:
  crear <nombre> <saldo>    - Crear nuevo usuario
  saldo <nombre>            - Consultar saldo de usuario
  acreditar <nombre> <monto> - Añadir saldo a usuario
  listar                    - Listar todos los usuarios
  ayuda                     - Mostrar esta ayuda

Ejemplos:
  python manage.py crear juan 500
  python manage.py saldo juan
  python manage.py acreditar juan 100
  python manage.py listar
""")

def main():
    if len(sys.argv) < 2:
        mostrar_ayuda()
        return

    comando = sys.argv[1]

    if comando == "crear":
        if len(sys.argv) != 4:
            print("❌ Error: Uso - python manage.py crear [nombre] [saldo_inicial]")
            return
        
        nombre = sys.argv[2]
        try:
            saldo = float(sys.argv[3])
            if saldo <= 0:
                print("❌ Error: El saldo debe ser mayor a 0")
                return
        except ValueError:
            print("❌ Error: El saldo debe ser un número válido")
            return
        
        if crear_usuario(nombre, saldo):
            print(f"✅ Usuario '{nombre}' creado con saldo inicial ${saldo:.2f}")
        else:
            print(f"❌ Error: El usuario '{nombre}' ya existe")

    elif comando == "saldo":
        if len(sys.argv) != 3:
            print("❌ Error: Uso - python manage.py saldo [nombre]")
            return
        
        nombre = sys.argv[2]
        usuario = get_usuario(nombre)
        if usuario:
            print(f"💰 Saldo de '{nombre}': ${usuario[2]:.2f}")
        else:
            print(f"❌ Error: Usuario '{nombre}' no encontrado")

    elif comando == "acreditar":
        if len(sys.argv) != 4:
            print("❌ Error: Uso - python manage.py acreditar [nombre] [monto]")
            return
        
        nombre = sys.argv[2]
        try:
            monto = float(sys.argv[3])
            if monto <= 0:
                print("❌ Error: El monto debe ser mayor a 0")
                return
        except ValueError:
            print("❌ Error: El monto debe ser un número válido")
            return
        
        usuario = get_usuario(nombre)
        if usuario:
            nuevo_saldo = usuario[2] + monto
            actualizar_saldo(nombre, nuevo_saldo)
            print(f"✅ Se acreditó ${monto:.2f} a '{nombre}'")
            print(f"💰 Nuevo saldo: ${nuevo_saldo:.2f}")
        else:
            print(f"❌ Error: Usuario '{nombre}' no encontrado")

    elif comando == "listar":
        usuarios = listar_usuarios()
        if not usuarios:
            print("📭 No hay usuarios registrados")
            return
        
        print("\n📋 Lista de Usuarios:")
        print("-" * 40)
        for i, (nombre, saldo) in enumerate(usuarios, 1):
            print(f"{i:2d}. {nombre:<15} ${saldo:>10.2f}")
        print("-" * 40)
        print(f"Total: {len(usuarios)} usuarios")

    elif comando in ["ayuda", "help", "--help", "-h"]:
        mostrar_ayuda()

    else:
        print(f"❌ Error: Comando '{comando}' no reconocido")
        mostrar_ayuda()

if __name__ == "__main__":
    main()
