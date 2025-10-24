#!/bin/bash

# Colores para el menú
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Función para mostrar el banner
mostrar_banner() {
    clear
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════╗"
    echo "║           🎰 GESTIÓN RULETA CASINO 🎰       ║"
    echo "║                                              ║"
    echo "║           Sistema de Administración         ║"
    echo "╚══════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Función para pausa
pausa() {
    echo -e "\n${YELLOW}Presiona Enter para continuar...${NC}"
    read
}

# Función principal del menú
menu_principal() {
    while true; do
        mostrar_banner
        
        echo -e "${GREEN}=== MENÚ PRINCIPAL ===${NC}"
        echo -e "${BLUE}1.${NC} 👤 Crear usuario"
        echo -e "${BLUE}2.${NC} 💰 Consultar saldo"
        echo -e "${BLUE}3.${NC} 📈 Acreditar saldo"
        echo -e "${BLUE}4.${NC} 📋 Listar usuarios"
        echo -e "${BLUE}5.${NC} 🚪 Salir"
        echo -e "${GREEN}=======================${NC}"
        
        read -p "Seleccione una opción [1-5]: " opcion

        case $opcion in
            1)
                echo -e "\n${CYAN}--- CREAR NUEVO USUARIO ---${NC}"
                read -p "Nombre del nuevo usuario: " nombre
                read -p "Saldo inicial: $" saldo
                
                # Validar saldo
                if ! [[ "$saldo" =~ ^[0-9]+(\.[0-9]+)?$ ]] || (( $(echo "$saldo <= 0" | bc -l) )); then
                    echo -e "${RED}❌ Error: El saldo debe ser un número mayor a 0${NC}"
                else
                    python manage.py crear "$nombre" "$saldo"
                fi
                pausa
                ;;
            2)
                echo -e "\n${CYAN}--- CONSULTAR SALDO ---${NC}"
                read -p "Nombre del usuario: " nombre
                python manage.py saldo "$nombre"
                pausa
                ;;
            3)
                echo -e "\n${CYAN}--- ACREDITAR SALDO ---${NC}"
                read -p "Nombre del usuario: " nombre
                read -p "Monto a acreditar: $" monto
                
                # Validar monto
                if ! [[ "$monto" =~ ^[0-9]+(\.[0-9]+)?$ ]] || (( $(echo "$monto <= 0" | bc -l) )); then
                    echo -e "${RED}❌ Error: El monto debe ser un número mayor a 0${NC}"
                else
                    python manage.py acreditar "$nombre" "$monto"
                fi
                pausa
                ;;
            4)
                echo -e "\n${CYAN}--- LISTA DE USUARIOS ---${NC}"
                python manage.py listar
                pausa
                ;;
            5)
                echo -e "\n${GREEN}🎲 ¡Gracias por usar el sistema! 🎲${NC}"
                echo -e "${YELLOW}¡Que la suerte esté siempre de tu lado!${NC}\n"
                exit 0
                ;;
            *)
                echo -e "${RED}❌ Opción no válida. Por favor, seleccione 1-5.${NC}"
                pausa
                ;;
        esac
    done
}

# Verificar si Python está instalado
if ! command -v python &> /dev/null; then
    echo -e "${RED}❌ Error: Python no está instalado o no está en el PATH${NC}"
    exit 1
fi

# Verificar si el script manage.py existe
if [ ! -f "manage.py" ]; then
    echo -e "${RED}❌ Error: No se encuentra el archivo manage.py${NC}"
    echo "Asegúrate de estar en el directorio management/"
    exit 1
fi

# Ejecutar menú principal
menu_principal
