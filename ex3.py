
import random
import math
from collections import deque

random.seed(42)

couts = {
    (1, 2): 14, (1, 3): 15, (1, 8): 17,
    (2, 3): 13, (2, 4): 14, (2, 5): 20, (2, 8): 21,
    (3, 4): 11, (3, 5): 21, (3, 6): 17,
    (3, 7): 9,  (3, 8): 9,
    (4, 5): 11, (4, 6): 10, (4, 7): 8, (4, 8): 20,
    (5, 6): 15, (5, 7): 18,
    (6, 7): 9,
    (7, 8): 13
}

# Rendre la matrice symetrique
for (i, j), valeur in list(couts.items()):
    couts[(j, i)] = valeur


def cout_circuit(circuit):# Calcul du cout d'un circuit

    total = 0

    for i in range(len(circuit) - 1):
        depart = circuit[i]
        arrivee = circuit[i + 1]

        # Une liaison absente rend le circuit invalide
        if (depart, arrivee) not in couts:
            return float("inf")

        total += couts[(depart, arrivee)]

    return total


def generer_voisins(circuit):
    voisins = []

    for i in range(1, len(circuit) - 2):
        for j in range(i + 1, len(circuit) - 1):
            voisin = circuit.copy()

            voisin[i], voisin[j] = voisin[j], voisin[i]

            if cout_circuit(voisin) != float("inf"):
                mouvement = tuple(sorted(
                    (circuit[i], circuit[j])
                ))

                voisins.append((voisin, mouvement))

    return voisins  # La ville 1 reste au debut et a la fin




def recherche_taboue(circuit_initial, iterations=100, tenure=5):
    courant = circuit_initial.copy()
    meilleur = courant.copy()

    liste_taboue = deque(maxlen=tenure)

    print("\n  recherche tabou")
    print("Solution initiale :", courant)
    print("Cout initial :", cout_circuit(courant))

    for iteration in range(1, iterations + 1):
        voisins = generer_voisins(courant)

        meilleur_voisin = None
        meilleur_mouvement = None
        meilleur_cout = float("inf")

        for voisin, mouvement in voisins:
            cout = cout_circuit(voisin)

            aspiration = cout < cout_circuit(meilleur)

            if mouvement in liste_taboue and not aspiration:
                continue

            if cout < meilleur_cout:
                meilleur_cout = cout
                meilleur_voisin = voisin
                meilleur_mouvement = mouvement

        if meilleur_voisin is None:
            print("Aucun voisin admissible.")
            break

        # Acc le meilleur voisin admissible
        courant = meilleur_voisin
        liste_taboue.append(meilleur_mouvement)

        if cout_circuit(courant) < cout_circuit(meilleur):
            meilleur = courant.copy()

        print(
            f"Iteration {iteration}: "
            f"circuit = {courant}, "
            f"cout = {cout_circuit(courant)}"
        )

    print("\nMeilleur circuit :", meilleur)
    print("Cout minimal trouve :", cout_circuit(meilleur))

    return meilleur


#recuit simule

def recuit_simule(circuit_initial, T=20, alpha=0.8, iterations=5):
    courant = circuit_initial.copy()
    meilleur = courant.copy()

    print("\n recui simule")
    print("Solution initiale :", courant)
    print("Cout initial :", cout_circuit(courant))

    for iteration in range(1, iterations + 1):
        voisins = generer_voisins(courant)

        if not voisins:
            print("Aucun voisin valide")
            break

        voisin, _ = random.choice(voisins)

        cout_courant = cout_circuit(courant)
        cout_voisin = cout_circuit(voisin)

        delta = cout_voisin - cout_courant

        # Accepter une amelioration ou, parfois, une degradation selon la temperature
        if delta < 0:
            accepter = True
        else:
            probabilite = math.exp(-delta / T)
            accepter = random.random() < probabilite

        if accepter:
            courant = voisin

        if cout_circuit(courant) < cout_circuit(meilleur):
            meilleur = courant.copy()

        print(
            f"Iteration {iteration}: "
            f"T = {T:.2f}, "
            f"voisin = {voisin}, "
            f"cout voisin = {cout_voisin}, "
            f"accepte = {accepter}, "
            f"cout courant = {cout_circuit(courant)}"
        )

        # Diminution empirique de la temperature
        T *= alpha

    print("\nMeilleur circuit :", meilleur)
    print("Cout minimal trouve :", cout_circuit(meilleur))

    return meilleur


# Execution

initial = [1, 2, 3, 4, 5, 6, 7, 8, 1]

recherche_taboue(initial, iterations=100, tenure=5)

recuit_simule(
    initial,
    T=20,
    alpha=0.8,
    iterations=5
)
