def leer_gramatica() -> dict:
    n_noterminales = int(input())
    gramatica = {}
    for i in range(n_noterminales):
        entrada = input().split()
        gramatica[entrada[0]] = entrada[1:]
    return gramatica

# Función que calcula el conjunto FIRST de una cadena dada según una gramática.
def first(cadena: str, gramatica: dict, producciones_pasadas) -> set:
    # Utiliza una caché para evitar cálculos repetidos y mejorar el rendimiento.
    if cadena in CACHE_FIRST:
        return CACHE_FIRST[cadena]
    
    # Si la cadena está vacía, devuelve un conjunto vacío.
    if len(cadena) == 0:
        return set()

    # Evita ciclos en la gramática comprobando si la primera letra ya está en producciones_pasadas.
    # También verifica que la primera letra sea un símbolo no terminal (ASCII menor que 97).
    if cadena[0] in producciones_pasadas and ord(cadena[0]) < 97:
        return set()

    # Agrega la primera letra de la cadena a la lista de producciones pasadas.
    producciones_pasadas.append(cadena[0])
    first_set = set()
    
    # Si la primera letra de la cadena es un símbolo no terminal en la gramática:
    if cadena[0] in gramatica:
        # Itera sobre cada producción de este símbolo no terminal.
        for produccion in gramatica[cadena[0]]:
            # Calcula el conjunto FIRST del primer símbolo de la producción.
            first_produccion = first(produccion[0], gramatica, producciones_pasadas)
            
            # Si el conjunto FIRST contiene epsilon ("e"):
            if "e" in first_produccion:
                # Intenta encontrar el primer símbolo no epsilon en la producción.
                for i in range(1, len(produccion), 1):
                    # Remueve epsilon del conjunto FIRST actual.
                    first_produccion.remove("e")
                    # Añade los elementos del conjunto FIRST del siguiente símbolo de la producción.
                    for elemento in first(produccion[i], gramatica, producciones_pasadas):
                        first_produccion.add(elemento)
                    # Si no se encuentra epsilon en el conjunto FIRST actual, termina el bucle.
                    if "e" not in first_produccion:
                        break
            # Añade todos los elementos del conjunto FIRST de la producción al conjunto FIRST final.
            for elemento in first_produccion:
                first_set.add(elemento)
    else:
        # Si el símbolo no es un no terminal, devuelve el símbolo directamente.
        return cadena[0]
    
    # Devuelve el conjunto FIRST calculado.
    return first_set


# Función que calcula el conjunto FOLLOW de una cadena dada según una gramática.
def follow(cadena: str, gramatica: dict, producciones_pasadas) -> set:
    # Si la cadena está vacía, devuelve un conjunto vacío.
    if len(cadena) == 0:
        return set()
    
    # Si la cadena ya está en producciones_pasadas (para evitar ciclos):
    if cadena in producciones_pasadas:
        # Devuelve el conjunto FOLLOW desde la caché si está disponible.
        if cadena in CACHE_FOLLOW:
            return CACHE_FOLLOW[cadena]
        # Si no está en la caché, devuelve un conjunto vacío.
        return set()

    follow_set = set()
    # Marca la cadena como procesada agregándola a producciones_pasadas.
    producciones_pasadas.append(cadena)

    # Itera sobre cada símbolo no terminal y sus producciones en la gramática.
    for noterminal, producciones in gramatica.items():
        for produccion in producciones:
            # Si la cadena está en la producción:
            if cadena in produccion:
                indice = produccion.index(cadena)
                alfa, beta = produccion[:indice], produccion[indice+1:]
                # Calcula el conjunto FIRST de la cadena beta (lo que sigue después de la cadena en la producción).
                first_beta = first(beta, gramatica, [])
                # Si beta está vacío o contiene epsilon:
                if beta == "" or "e" in first_beta:
                    # Añade al conjunto FOLLOW de la cadena, los elementos del conjunto FOLLOW del no terminal.
                    for elemento in follow(noterminal, gramatica, producciones_pasadas):
                        follow_set.add(elemento)
                else:
                    # Si beta no está vacío ni contiene epsilon, añade los elementos del conjunto FIRST de beta.
                    for elemento in first_beta:
                        follow_set.add(elemento)

    # Manejo especial del símbolo inicial "S": Si la cadena es "S" y el conjunto FOLLOW está vacío, devuelve el valor en la caché.
    return CACHE_FOLLOW[cadena] if cadena == "S" and follow_set == set() else follow_set



for i in range(int(input())):    
    gramatica = leer_gramatica()
    CACHE_FOLLOW = {"S": {"$"}}
    CACHE_FIRST = {}

    for noterminal in gramatica.keys():
        CACHE_FIRST[noterminal] = first(noterminal, gramatica, [])
        print(f"First({noterminal}) = ", end="{")
        print(",".join(CACHE_FIRST[noterminal]), end="}\n") 
    
    for noterminal in gramatica.keys():
        CACHE_FOLLOW[noterminal] = follow(noterminal, gramatica, [])
        print(f"Follow({noterminal}) = ", end="{")
        print(",".join(CACHE_FOLLOW[noterminal]), end="}\n") 
