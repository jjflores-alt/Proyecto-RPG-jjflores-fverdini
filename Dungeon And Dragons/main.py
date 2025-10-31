# main.py

import os
from personajes import crear_heroes
from enemigos import generar_enemigos
from combate import combate
from campamento import campamento
from guardado import cargar_partida
from items import Item

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    limpiar_pantalla()
    print("""
    === Dungeon and Dragons ===
    1. Jugar partida nueva
    2. Cargar partida
    3. Tutorial
    4. Créditos
    5. Salir
    """)
    return input("Elige una opción (1-5): ")

def main():
    while True:
        opcion = mostrar_menu()
        if opcion == "1":
            print("""
            === Dungeon and Drangons ===
            En la antigua tierra de Leiva, la paz se ha roto.
            Desde las montañas del norte, el temible Vharzum, el Dragón Carmesi, ha despertado de su letargo, extendiendo fuego y destryccion sobre el reino.

            La criatura se oculta en lo mas profundo de la Mazmorra de las Cenizas, un laberinto de cuatro niveles construido por una civilizacion olvidada, donde la magia y la corrupcion se entrelazan.

            Tres aventureros, movidos por el deber, la ambicion o la redencion, se adentran en sus oscuras profundidades. Allí deberán enfrentar horrores antiguos, superar pruebas dificiles y desafiar su propio destino.

            Porque esta no es solo la lucha contra un dragon cualquiera...
            Esta es una batalla por el destino mismo de Leiva.
            """)
            print("Presiona Enter para continuar.")
            input()
            
            heroes_disponibles = crear_heroes()
            equipo = []
            while len(equipo) < 3:
                limpiar_pantalla()
                print(f"\nElige héroe {len(equipo)+1}/3:")
                print("Héroes disponibles:")
                for contador, heroe in enumerate(heroes_disponibles, 1):
                    print(f"{contador}. {heroe.nombre} (Vida: {heroe.vida_max}, Ataque: {heroe.get_ataque()}, Defensa: {heroe.get_defensa()})")
                try:
                    idx = int(input(f"Elige héroe (1-{len(heroes_disponibles)}): ")) - 1
                    if idx < 0 or idx >= len(heroes_disponibles):
                        print("Índice inválido. Presiona Enter para continuar.")
                        input()
                        continue
                    nombre_personalizado = input(f"Nombre para {heroes_disponibles[idx].nombre} (Enter para mantener): ")
                    heroe = heroes_disponibles.pop(idx)
                    heroe.nombre = nombre_personalizado if nombre_personalizado else heroe.nombre
                    equipo.append(heroe)
                    limpiar_pantalla()
                    print(f"{heroe.nombre} añadido al equipo.")
                    print("Presiona Enter para continuar.")
                    input()
                except ValueError:
                    print("Entrada inválida. Presiona Enter para continuar.")
                    input()
            inventario = []
            oro = 100
            mazmorra_actual = 1
            costo_guardado = 10

            # Flujo de mazmorras
            while mazmorra_actual <= 4 and any(heroes.esta_vivo() for heroes in equipo):
                limpiar_pantalla()
                print(f"\nEntrando en la Mazmorra {mazmorra_actual}")
                enemigos = generar_enemigos(mazmorra_actual)
                victoria, oro_ganado, almas = combate(equipo, enemigos, inventario)
                oro += oro_ganado
                inventario.extend([Item(alma, "alma", 0, 0) for alma in almas if alma])
                if not victoria:
                    limpiar_pantalla()
                    print("""
                    GAME OVER
                    En la antigua tierra de Leiva, la esperanza se extinguío.
                    El rugido de Vharzum, el Dragón Carmesí, resonó por ultima vez sobre los campos ardientes, marcando el fin de toda resistencia.

                    Los tres aventureros que descendieron a la Mazmorra de las Cenizas jamás regresaron.
                    Sus cuerpos quedaron perdidos entre los escombros de una civilizacion maldita, y con ellos se desvaneció la ultima chispa de valor del reino.

                    Las aldeas fueron consumidas por el fuego, las montañas se agrietaron, y el cielo se tornó rojo como la sangre misma.
                    Leiva cayó en el olvido, convertida en un desierto de cenizas donde solo el eco del Dragó aún respira.

                    Porque cuando los héroes caen, no solo mueren los hombres...
                    Mueren también las leyendas
                    """)
                    print("Presiona Enter para volver al menú.")
                    input()
                    break
                if mazmorra_actual < 4:
                    limpiar_pantalla()
                    print("¿Ir al campamento? (s/n)")
                    if input().lower() == "s":
                        oro, costo_guardado = campamento(equipo, inventario, oro, mazmorra_actual, costo_guardado)
                mazmorra_actual += 1
            if mazmorra_actual > 4:
                limpiar_pantalla()
                print("""
                En la antigua tierra de Leiva, la oscuridad fue finalmente vencida.
                Tras descender a las profundidades de la Mazmorra de Cenizas, los tres aventureros enfrentaron horrores inimaginables y superaron cada nivel con valor y determinacion.

                En el corazón del abismo aguardaba Vharzum, el Dragon Carmesí, envuelto en llamas y furia. Con su caída, el reino de Leiva renació.
                Los campos volvieron a florecer, las campanas resonaron en cada aldea, y la paz regresó al pueblo.

                Las hazañas de los héroes se convirtieron el leyenda...
                aunque los sabios murmuran que, bajo las ruinas,
                el mal nunca desaparece del todo.

                Porque incluso en tiempos de luz,
                la oscuridad siempre aguarda su momento para volver.
                """)
                print("Presiona Enter para volver al menú.")
                input()

        elif opcion == "2":
            partida = cargar_partida()
            if partida:
                equipo, inventario, oro, mazmorra_actual = partida
                costo_guardado = 10 * (2 ** max(0, mazmorra_actual - 1))
                while mazmorra_actual <= 4 and any(heroes.esta_vivo() for heroes in equipo):
                    limpiar_pantalla()
                    print(f"\nEntrando en la Mazmorra {mazmorra_actual}")
                    enemigos = generar_enemigos(mazmorra_actual)
                    victoria, oro_ganado, almas = combate(equipo, enemigos, inventario)
                    oro += oro_ganado
                    inventario.extend([Item(alma, "alma", 0, 0) for alma in almas if alma])
                    if not victoria:
                        limpiar_pantalla()
                        print("""
                        GAME OVER
                        En la antigua tierra de Leiva, la esperanza se extinguío.
                        El rugido de Vharzum, el Dragón Carmesí, resonó por ultima vez sobre los campos ardientes, marcando el fin de toda resistencia.
                        
                        Los tres aventureros que descendieron a la Mazmorra de las Cenizas jamás regresaron.
                        Sus cuerpos quedaron perdidos entre los escombros de una civilizacion maldita, y con ellos se desvaneció la ultima chispa de valor del reino.
                        
                        Las aldeas fueron consumidas por el fuego, las montañas se agrietaron, y el cielo se tornó rojo como la sangre misma.
                        Leiva cayó en el olvido, convertida en un desierto de cenizas donde solo el eco del Dragó aún respira.
                        
                        Porque cuando los héroes caen, no solo mueren los hombres...
                        Mueren también las leyendas
                        """)
                        
                        print("Presiona Enter para volver al menú.")
                        input()
                        break
                    if mazmorra_actual < 4:
                        limpiar_pantalla()
                        print("¿Ir al campamento? (s/n)")
                        if input().lower() == "s":
                            oro, costo_guardado = campamento(equipo, inventario, oro, mazmorra_actual, costo_guardado)
                    mazmorra_actual += 1
                if mazmorra_actual > 4:
                    limpiar_pantalla()
                    print("""
                En la antigua tierra de Leiva, la oscuridad fue finalmente vencida.
                Tras descender a las profundidades de la Mazmorra de Cenizas, los tres aventureros enfrentaron horrores inimaginables y superaron cada nivel con valor y determinacion.

                En el corazón del abismo aguardaba Vharzum, el Dragon Carmesí, envuelto en llamas y furia. Con su caída, el reino de Leiva renació.
                Los campos volvieron a florecer, las campanas resonaron en cada aldea, y la paz regresó al pueblo.

                Las hazañas de los héroes se convirtieron el leyenda...
                aunque los sabios murmuran que, bajo las ruinas,
                el mal nunca desaparece del todo.

                Porque incluso en tiempos de luz,
                la oscuridad siempre aguarda su momento para volver.
                """)
                    print("Presiona Enter para volver al menú.")
                    input()

        elif opcion == "3":
            limpiar_pantalla()
            with open("tutorial.txt", "r") as file:
                print(file.read())
            print("Presiona Enter para volver al menú.")
            input()

        elif opcion == "4":
            limpiar_pantalla()
            with open("creditos.txt", "r") as file:
                print(file.read())
            print("Presiona Enter para volver al menú.")
            input()

        elif opcion == "5":
            limpiar_pantalla()
            print("¡Gracias por jugar!")
            break
        else:
            limpiar_pantalla()
            print("Opción inválida. Presiona Enter para continuar.")
            input()

if __name__ == "__main__":

    main()

