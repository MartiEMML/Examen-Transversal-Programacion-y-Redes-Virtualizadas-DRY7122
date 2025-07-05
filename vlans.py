def tipo_vlan(numero_vlan):
    if 1 <= numero_vlan <= 1005:
        return "VLAN del rango normal"
    elif 1006 <= numero_vlan <= 4094:
        return "VLAN del rango extendido"
    else:
        return "Número de VLAN no válido"

def main():
    try:
        vlan = int(input("Ingresa el número de VLAN: "))
        resultado = tipo_vlan(vlan)
        print(resultado)
    except ValueError:
        print("Por favor ingresa un número válido.")

if __name__ == "__main__":
    main()