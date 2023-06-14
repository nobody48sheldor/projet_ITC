alphabet = [chr(i) for i in range(256)]

########################################
#### TRANSFORMEE DE BURROWS-WHEELER ####
########################################

def BWT(mot: str) -> str:
    """
    Prend en argument un mot quelconque
    Renvoie sa transformée de Burrows-Wheeler
    """
    n = len(mot)
    
    permutations = [mot[i:] + mot[:i] for i in range(n)] #Ensemble des permutations du mot
    permutations.sort() #Tri dans l'ordre lexiocgraphique des différentes permutations
    
    position = permutations.index(mot) #Position du mot d'origine
    
    mot_code = "" #Création de la transformée de B-W du mot
    for p in permutations:
        mot_code += p[-1]
    
    return position, mot_code


def BWT_trad(mot_code: tuple[int,str]) -> str:
    """
    Prend en argument une transformée de Burrows-Wheeler
    Renvoie le mot d'origine
    """
    position = mot_code[0] #Position du mot d'origine dans l'ensemble des translations
    mot = mot_code[1]
    n = len(mot) #Longueur du mot d'origine
    
    classement_lettres = [(i,mot[i]) for i in range(n)] #Ensemble des lettres et leur indice
    classement_lettres.sort(key = lambda x: x[1]) #Tri des tuples par ordre alphabétique
    
    parent = [None for _ in range(n)]
    for i in range(n):
        position_parent = classement_lettres[i][0]
        parent[position_parent] = i #Liste d'indice de la lettre précédente
    
    parcours = [position]
    for i in range(1,n):
        parcours.append(parent[parcours[i-1]]) #Création du parcours
    
    res = [mot[i] for i in parcours] #Création du mot sous forme de liste (à l'envers)
    res = res[::-1]
    
    return ''.join(res)



##################################
#### ALGORITHME MOVE-TO-FRONT ####
##################################


def MTF(mot: str) -> list[int]:
    """
    Prend en argument un mot
    Renvoie sa transformée Move-to-Front
    """
    alpha = alphabet.copy() #Copie de l'alphabet considéré

    mot_code = []
    
    for lettre in mot: #Application de la transformée MTF
        position = alpha.index(lettre) #Position de la lettre dans l'alphabet courant
        mot_code.append(position)
        
        alpha.pop(position) #Mise à jour de la position du caractère courant (lettre)
        alpha.insert(0, lettre)
    
    return mot_code


def MTF_trad(mot: list[int]) -> str:
    """
    Prend en argument une transformée Move-to-Front
    Renvoie le mot d'origine
    """
    alpha = alphabet.copy() #Copie de l'alphabet considéré

    mot_decode = ""

    for position in mot:
        lettre = alpha[position] #Recherche de la lettre correspondant à la position dans l'alphabet courant
        mot_decode += lettre
        
        alpha.pop(position) #Mise à jour de la position du caractère courant (lettre)
        alpha.insert(0,lettre)
        
    return mot_decode


def TTL(texte: str) -> list:
    liste = texte.split()
    return [int(i) for i in liste]


###########################
#### CODAGE DE HUFFMAN ####
###########################


'''import heapq
from heapq import heappop, heappush'''


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

'''# freq est un dictionnaire de la forme lettre:nombre d'apparitions
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
    
    return liste_temp[0]'''


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

def decoder2(texte_encodee, arbre):
    texte_decodee = ""

    # pour éviter les cas pathologiques tels que "fff", "gggggg" etc.
    if arbre.gauche is None and arbre.droite is None:
        return arbre.frequences*arbre.caractere
    else:
        indice = -1
        while indice < len(texte_encodee) - 1:
            i, c = aux(arbre, indice, texte_encodee)
            indice = i
            texte_decodee += str(c) + " "
    return texte_decodee



#############################
#### PROGRAMME PRINCIPAL ####
#############################


with open(r"C:\Users\Lucas\Desktop\ITC\texte.txt", 'r') as file:
    texte = file.read()

# Sans BW+MTF
texte_encodee, arbre = encoder(texte)
texte_decodee = decoder(texte_encodee, arbre)

# Avec BW+MTF
BW_texte = BWT(texte)
texte_encodee_BW_MTF, arbre = encoder(MTF(BW_texte[1]))
txt_MTF = decoder2(texte_encodee_BW_MTF, arbre)
liste_MTF = TTL(txt_MTF)
mot_BW = MTF_trad(liste_MTF)
texte_decodee_BW_MTF = BWT_trad((BW_texte[0], mot_BW))


print(f"Longeur initiale : {len(texte)}*8={len(texte)*8}")

# Sans BW & MTF
print("\n--- Sans Burrows-Wheeler & Move-to-front :( ---")
print("Chaîne correctement décodée ?", texte_decodee==texte)
print("Longueur après compression :", len(texte_encodee))
print("Gain en longueur :", len(texte)*8 - len(texte_encodee))

# Avec BW & MTF

print("\n--- Avec Burrows-Wheeler & Move-to-front :D ---")
print("Chaîne correctement décodée ?", texte_decodee_BW_MTF==texte)
print("Longueur après compression :", len(texte_encodee_BW_MTF))
print("Gain en longueur :", len(texte)*8 - len(texte_encodee_BW_MTF))
