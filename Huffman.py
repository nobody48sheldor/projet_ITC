'''
import heapq
from heapq import heappop, heappush
'''


# Implémente le type arbre binaire en python
class Node:
    def __init__(self, caractere: str, frequence: int, gauche=None, droit=None) -> None:
        self.caractere = caractere
        self.frequence = frequence
        self.gauche = gauche
        self.droit = droit
    
    '''
    # Modifie la relation d'ordre pour que la file d'attente de priorité classe les noeuds en fonction de leurs fréquences
    def __lt__(self, autre):
        self.frequence < autre.frequence
    '''


# Renvoie un dictionnaire contenant les caractères du texte et leurs nombres d'apparitions associés
def obtenir_frequences(texte: str) -> dict:
    res = {}
    for c in texte:
        res[c] = res.get(c, 0) + 1
    return res


# freq est un dictionnaire de la forme lettre:nombre d'apparitions
def construire_arbre_huffman(freq: dict) -> Node:
    liste_temp = [Node(c, f) for c, f in freq.items()]  # créer l'arbre de Huffman associé

    while len(liste_temp) != 1:
        # on récupère les deux noeuds de fréquence la plus basse
        liste_temp = sorted(liste_temp, reverse=True, key=lambda n: n.frequence)
        gauche = liste_temp.pop()
        droit = liste_temp.pop()

        # et on les combine en un nouveau noeud interne
        total = gauche.frequence + droit.frequence
        liste_temp.append(Node(None, total, gauche, droit))
    
    return liste_temp[0]

'''
# freq est un dictionnaire de la forme lettre:nombre d'apparitions
def construire_arbre_huffman(freq: dict) -> Node:
    liste_temp = [Node(c, f) for c, f in freq.items()]  # créer l'arbre de Huffman associé
    heapq.heapify(liste_temp)

    while len(liste_temp) != 1:
        # on récupère les deux noeuds de fréquence la plus basse
        gauche = heappop(liste_temp)
        droit = heappop(liste_temp)

        # on les combine en un nouveau noeud interne
        total = gauche.frequence + droit.frequence
        heappush(liste_temp, Node(None, total, gauche, droit))
    
    return liste_temp[0]
'''


# Assigne les codes de huffman à chaque caractère de l'arbre de huffman
def assigner_codes(arbre: Node) -> dict:
    codes = {}
    def aux(arbre: Node, acc: str):
        if arbre is None:
            return

        # Si le noeud est une feuille, on renvoie le code associé
        if arbre.gauche is None and arbre.droit is None:
            codes[arbre.caractere] = acc if len(acc) > 0 else "1"
        
        # Sinon, noeud gauche -> 0 et noeud droit -> 1
        aux(arbre.gauche, acc + "0")
        aux(arbre.droit, acc + "1")
    aux(arbre, '')
    return codes


# Encode un texte suivant l'algorithme de Huffman.
# Pour rendre le programme lisible, la classe string est utilisée pour stocker la chaîne codée.
def encoder(texte):
    freq = obtenir_frequences(texte)
    arbre = construire_arbre_huffman(freq)
    codes = assigner_codes(arbre)
    #print("Les codes de huffman sont", codes)
    res = ""
    for c in texte:
        res += codes.get(c)
    return res, arbre


def aux(arbre, indice, s):
    if arbre is None:
        return indice, None
 
    # a trouvé un neud feuille, i.e. un caractère
    if arbre.gauche is None and arbre.droit is None:
        return indice, arbre.caractere
 
    indice += 1
    arbre = arbre.gauche if s[indice] == '0' else arbre.droit
    return aux(arbre, indice, s)


def decoder(texte_encodee, arbre):
    texte_decodee = ""

    # pour éviter les cas pathologiques tels que "fff", "gggggg" etc.
    if arbre.gauche is None and arbre.droite is None:
        return arbre.frequences*arbre.caractere
    else:
        indice = -1
        while indice < len(texte_encodee) - 1:
            i, c = aux(arbre, indice, texte_encodee)
            indice = i
            texte_decodee += c
    return texte_decodee


texte = "Never gonna give you up, never gonna let you doooown"
texte_encodee, arbre = encoder(texte)
texte_decodee = decoder(texte_encodee, arbre)
print(f"Chaîne initial : {texte}\nLongeur : {len(texte)}*8={len(texte)*8}")
print(f"Chaîne encodée : {texte_encodee}\nLongueur : {len(texte_encodee)}")
print(f"Chaîne décodéé : {texte_decodee}")
print("Gain en longueur :", len(texte)*8 - len(texte_encodee))



#print(encoder("Huffman coding is a data compression algorithm."))
