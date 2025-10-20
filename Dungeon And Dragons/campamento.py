# campamento.py
# usamos la funcion limpiar pantalla
import os
from items import crear_items_disponibles, usar_item

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def campamento(equipo, inventario, oro, mazmorra_actual, costo_guardado):
    while True:
        limpiar_pantalla()
        #muestra el oro del jugador y el nivel de mazmorra. Tambien muestra las distintas opciones que puede tomar el jugador
        print(f"=== Campamento (Oro: {oro}, Mazmorra: {mazmorra_actual}) ===")
        print("1. Ver stats de héroes")
        print("2. Comprar ítems")
        print("3. Vender almas de monstruo")
        print("4. Equipar ítems")
        print("5. Guardar partida")
        print("6. Continuar aventura")
        opcion = input("Elige una opción (1-6): ")

        if opcion == "1":
            limpiar_pantalla()
            #muestra las estadisticas de los heroes seleccionados
            print("Stats de héroes:")
            for heroe in equipo:
                equipped = ", ".join(item.nombre for item in heroe.equipped_items) or "Ninguno"
                print(f"{heroe.nombre}: Vida {heroe.vida_actual}/{heroe.vida_max}, Ataque {heroe.get_ataque()}, Defensa {heroe.get_defensa()}, Equipado: {equipped}")
            print("\nPresiona Enter para volver al campamento.")
            input()

        elif opcion == "2":
            limpiar_pantalla()
            #muestra una seccion para comprar items
            items_disponibles = crear_items_disponibles()
            print("Ítems disponibles para comprar:")
            for i, item in enumerate(items_disponibles, 1):
                print(f"{i}. {item.nombre} ({item.precio} oro)")
            try:
                item_idx = int(input(f"Elige ítem (1-{len(items_disponibles)}): ")) - 1
                item = items_disponibles[item_idx]
                if oro >= item.precio:
                    inventario.append(item)
                    oro -= item.precio
                    limpiar_pantalla()
                    print(f"Compraste {item.nombre}. Oro restante: {oro}")
                    print("Presiona Enter para volver al campamento.")
                    input()
                else:
                    limpiar_pantalla()
                    print("No tienes suficiente oro.")
                    #en el caso de que el usuario no tenga suficiente oro
                    print("Presiona Enter para volver al campamento.")
                    input()
            except (ValueError, IndexError):
                limpiar_pantalla()
                print("Entrada inválida.")
                print("Presiona Enter para volver al campamento.")
                input()

        elif opcion == "3":
            limpiar_pantalla()
            #permite vender el alma de mounstro obtenidas tras el combate
            print("Almas en inventario:")
            almas = [item for item in inventario if "Alma de Monstruo" in item.nombre]
            if not almas:
                print("No tienes almas para vender.")
                print("Presiona Enter para volver al campamento.")
                input()
            else:
                for i, alma in enumerate(almas, 1):
                    print(f"{i}. {alma.nombre}")
                print(f"{len(almas)+1}. Vender todas")
                try:
                    opcion_vender = int(input(f"Elige opción (1-{len(almas)+1}): "))
                    if opcion_vender == len(almas) + 1:
                        for alma in almas:
                            oro += 50 if alma.nombre == "Alma de Monstruo I" else 100 if alma.nombre == "Alma de Monstruo II" else 200
                            inventario.remove(alma)
                        limpiar_pantalla()
                        print(f"Vendiste todas las almas. Oro actual: {oro}")
                        print("Presiona Enter para volver al campamento.")
                        input()
                    else:
                        alma = almas[opcion_vender - 1]
                        oro += 50 if alma.nombre == "Alma de Monstruo I" else 100 if alma.nombre == "Alma de Monstruo II" else 200
                        inventario.remove(alma)
                        limpiar_pantalla()
                        print(f"Vendiste {alma.nombre}. Oro actual: {oro}")
                        print("Presiona Enter para volver al campamento.")
                        input()
                except (ValueError, IndexError):
                    limpiar_pantalla()
                    print("Entrada inválida.")
                    print("Presiona Enter para volver al campamento.")
                    input()

        elif opcion == "4":
            limpiar_pantalla()
            #perimte equipar los objetos comprados al heroe
            print("Héroes:")
            for i, heroe in enumerate(equipo, 1):
                print(f"{i}. {heroe.nombre}")
            try:
                heroe_idx = int(input(f"Elige héroe (1-{len(equipo)}): ")) - 1
                heroe = equipo[heroe_idx]
                limpiar_pantalla()
                print(f"Equipar ítems para {heroe.nombre}:")
                print("Ítems en inventario:")
                for i, item in enumerate(inventario, 1):
                    print(f"{i}. {item.nombre}")
                item_idx = int(input(f"Elige ítem (1-{len(inventario)}): ")) - 1
                usar_item(inventario[item_idx], heroe)
                limpiar_pantalla()
                print(f"{heroe.nombre} equipa/usó {inventario[item_idx].nombre}.")
                if inventario[item_idx].tipo in ["arma", "armadura", "pocion_vida", "pocion_fuerza", "pocion_especial"]:
                    inventario.pop(item_idx)
                print("Presiona Enter para volver al campamento.")
                input()
            except (ValueError, IndexError):
                limpiar_pantalla()
                print("Entrada inválida.")
                print("Presiona Enter para volver al campamento.")
                input()

        elif opcion == "5":
            limpiar_pantalla()
            #permite guardar la partida a costo de oro, aumentando el doble por cada partida guardada
            if oro >= costo_guardado:
                oro -= costo_guardado
                from guardado import guardar_partida
                guardar_partida(equipo, inventario, oro, mazmorra_actual)
                print(f"Partida guardada. Costo: {costo_guardado} oro. Oro restante: {oro}")
                costo_guardado *= 2
                print("Presiona Enter para volver al campamento.")
                input()
            else:
                print(f"No tienes suficiente oro. Costo de guardado: {costo_guardado}")
                print("Presiona Enter para volver al campamento.")
                input()

        elif opcion == "6":
            limpiar_pantalla()
            #permite continuar con la siguiente mazmorra
            return oro, costo_guardado
        else:
            limpiar_pantalla()
            print("Opción inválida.")
            print("Presiona Enter para volver al campamento.")
            input()

