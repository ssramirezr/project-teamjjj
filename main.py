global CACHE_FIRST
global CACHE_FOLLOW

def leer_gramatica() -> dict:
    n_noterminales = int(input())
    gramatica = {}
    for i in range(n_noterminales):
        entrada = input().split()
        gramatica[entrada[0]] = entrada[1:]
    return gramatica

def first(cadena: str, gramatica: dict, producciones_pasadas) -> set:
    if cadena[0] in producciones_pasadas:
        return set()
    
    if cadena[0] in CACHE_FIRST:
        return CACHE_FIRST[cadena[0]]

    producciones_pasadas.append(cadena[0])
    first_set = set()
    if cadena[0] in gramatica:
        for produccion in gramatica[cadena[0]]:
            for elemento in first(produccion[0], gramatica, producciones_pasadas):
                first_set.add(elemento)
    else:
        return cadena[0]
    
    CACHE_FIRST[cadena[0]] = first_set
    return first_set


for i in range(int(input())):    
    gramatica = leer_gramatica()
    CACHE_FIRST = {}
    CACHE_FOLLOW = {}
    for noterminal in gramatica.keys():
        print(f"First({noterminal}) = {first(noterminal, gramatica, [])}")