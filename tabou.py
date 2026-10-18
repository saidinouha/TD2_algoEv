
from collections import deque

capacite_D1 = 8
demandes = [4, 5, 8]

cout_D1 = [5, 3, 4]
cout_D2 = [6, 7, 2]


def cout_total(solution):
    cout = 0

    for j in range(3):
        quantite_D1 = solution[j]
        quantite_D2 = demandes[j] - quantite_D1

        cout += quantite_D1 * cout_D1[j]
        cout += quantite_D2 * cout_D2[j]

    return cout


def generer_voisins(solution):
    voisins = []

    for i in range(3):
        for j in range(3):
            if i == j:
                continue

            # D1 doit avoir au moins un conteneur
            # a retirer du magasin i
            # et le magasin j doit avoir une demande restante
            if solution[i] > 0 and solution[j] < demandes[j]:
                voisin = solution.copy()
                voisin[i] -= 1
                voisin[j] += 1

                voisins.append((voisin, (i, j)))

    return voisins


def recherche_taboue(solution_initiale, iterations=100, tenure=5):
    solution = solution_initiale.copy()
    meilleure_solution = solution.copy()

    liste_taboue = deque(maxlen=tenure)

    for iteration in range(iterations):
        voisins = generer_voisins(solution)

        meilleur_voisin = None
        meilleur_cout = float("inf")
        meilleur_mouvement = None

        for voisin, mouvement in voisins:
            cout = cout_total(voisin)

            mouvement_interdit = mouvement in liste_taboue
            aspiration = cout < cout_total(meilleure_solution)

            if mouvement_interdit and not aspiration:
                continue

            if cout < meilleur_cout:
                meilleur_cout = cout
                meilleur_voisin = voisin
                meilleur_mouvement = mouvement

        if meilleur_voisin is None:
            break

        solution = meilleur_voisin

        i, j = meilleur_mouvement
        liste_taboue.append((j, i))

        if cout_total(solution) < cout_total(meilleure_solution):
            meilleure_solution = solution.copy()

    return meilleure_solution


initiale = [2, 3, 3]

resultat = recherche_taboue(initiale)

print("Quantites livrees par D1 :", resultat)
print("Quantites livrees par D2 :",
      [demandes[j] - resultat[j] for j in range(3)])
print("Cout total :", cout_total(resultat))
