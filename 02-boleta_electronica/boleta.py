SUBTOTAL = 0
IGV = 0.18


def mostrar_menu_principal():
    print("\nHOLA BIENVENIDOS, UN GUSTO EN ATENDERLOS :D")
    print("|" + "=" * 29 + "|")
    print("|" + " " * 7 + "RESTAURANTE S.A" + " " * 7 + "|")
    print("|" + " " * 13 + "MENÚ" + " " * 12 + "|")
    print("|" + "=" * 29 + "|")
    print("|" + " " + "A" + " " + "|" + "DESAYUNO" + " " * 17 + "|")
    print("|" + " " + "B" + " " + "|" + "ALMUERZO" + " " * 17 + "|")
    print("|" + " " + "C" + " " + "|" + "CENA" + " " * 21 + "|")
    print("|" + " " + "D" + " " + "|" + "=" * 9 + " " + "SALIR" + " " + "=" * 9 + "|")
    print("|" + "=" * 29 + "|")

def mostrar_menu(tipo):
    print("\n" + "=" * 30)
    print(f"       MENÚ DE {tipo.upper()}")
    print("=" * 30)

    if tipo == "Desayuno":
        print("1. Café              - S/4.50")
        print("2. Chocolate         - S/5.00")
        print("3. Jugo de Fresas    - S/9.00")
        print("4. Jugo de Papaya    - S/8.00")
        print("5. Pan con Pollo     - S/7.00")
        print("6. Pan con Jamón     - S/7.00")
        print("7. Pan con Tortilla  - S/7.00")
        print("8. Salir")
    elif tipo == "Almuerzo":
        print("1. Café              - S/4.50")
        print("2. Chocolate         - S/5.00")
        print("3. Jugo de Fresas    - S/9.00")
        print("4. Jugo de Papaya    - S/8.00")
        print("5. Pan con Pollo     - S/7.00")
        print("6. Pan con Jamón     - S/7.00")
        print("7. Pan con Tortilla  - S/7.00")
        print("8. Salir")
    elif tipo == "Cena":
        print("1. Pizza Exprés      - S/9.00")
        print("2. Ensalada Campera  - S/7.50")
        print("3. Gazpacho          - S/6.00")
        print("4. Caldo de Gallina  - S/6.00")
        print("5. Pollo al Horno    - S/5.50")
        print("6. Menestrón         - S/4.00")
        print("7. Salir")
    
    print("=" * 30)

while True:
    mostrar_menu_principal()
    res = input("Seleccione su tipo de comida por favor: ").upper()

    if res == "A":
        while True:
            mostrar_menu("Desayuno")
            selec = input("Elija su producto: ")
            if selec == "1":
                SUBTOTAL += 4.50
            elif selec == "2":
                SUBTOTAL += 5.00
            elif selec == "3":
                SUBTOTAL += 9.00
            elif selec == "4":
                SUBTOTAL += 8.00
            elif selec == "5":
                SUBTOTAL += 7.00
            elif selec == "6":
                SUBTOTAL += 7.00
            elif selec == "7":
                SUBTOTAL += 7.00
            elif selec == "8":
                break  # Salir del menú de desayuno
            else:
                print("Opción inválida. Error")

    elif res == "B":
        while True:
            mostrar_menu("Almuerzo")
            selec = input("Elija su producto: ")
            if selec == "1":
                SUBTOTAL += 4.50
            elif selec == "2":
                SUBTOTAL += 5.00
            elif selec == "3":
                SUBTOTAL += 9.00
            elif selec == "4":
                SUBTOTAL += 8.00
            elif selec == "5":
                SUBTOTAL += 7.00
            elif selec == "6":
                SUBTOTAL += 7.00
            elif selec == "7":
                SUBTOTAL += 7.00
            elif selec == "8":
                break  # Salir del menú de desayuno
            else:
                print("Opción inválida. Error")

    elif res == "C":
        while True:
            mostrar_menu("Cena")
            selec = input("Elija su producto: ")
            if selec == "1":
                SUBTOTAL += 9.00
            elif selec == "2":
                SUBTOTAL += 7.50
            elif selec == "3":
                SUBTOTAL += 6.00
            elif selec == "4":
                SUBTOTAL += 6.00
            elif selec == "5":
                SUBTOTAL += 5.50
            elif selec == "6":
                SUBTOTAL += 4.00
            elif selec == "7":
                break  # Salir del menú de cena
            else:
                print("Opción inválida. Error")

    elif res == "D":  
        SUBTOTAL1 = SUBTOTAL * IGV
        TOTAL = SUBTOTAL + SUBTOTAL1
        print("|" + "=" * 29 + "|")
        print(f"Subtotal: S/{SUBTOTAL:.2f}")
        print(f"IGV (18%): S/{SUBTOTAL1:.2f}")
        print(f"Total a pagar: S/{TOTAL:.2f}")
        print("¡Gracias por su compra! :)")
        print("|" + "=" * 29 + "|")
        break
    else:
        print("Opción no válida. Error")