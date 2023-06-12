# Projet ITC

"""
Explication brève du projet
"""


# modules

import sys

sys.setrecursionlimit(15000)

var = sys.argv
print(var)

file = var[1]


"""
general func
"""

def fusion_aux(l1,l2,l):
    if l1 == []:
        return(l+l2)
    if l2 == []:
        return(l+l1)
    else:
        if l1[0][1] > l2[0][1]:
            return( fusion_aux( l1.copy(), l2[1:].copy(), (l + [l2[0]]).copy() ) )
        else:
            return( fusion_aux( l1[1:].copy(), l2.copy(), (l + [l1[0]]).copy() ) )

def fusion(l1,l2):
    return( fusion_aux(l1,l2,[]) )


def couper(l):
    l1 = []
    l2 = []
    for i in range(len(l)):
        if i%2 == 0:
            l1.append(l[i])
        else:
            l2.append(l[i])
    return(l1.copy(),l2.copy())

def tri_fusion(l):
        l1, l2 = couper(l)
        if l1 == []:
            return l2.copy()
        if l2 == []:
            return l1.copy()
        else:
            return(fusion( tri_fusion( l1.copy() ).copy(), tri_fusion( l2.copy() ).copy() ))



"""
code
"""




def freq(file):
    with open(file, 'r') as my_file:
        file_content = my_file.read()
        file_content_split = file_content.split()

    #print(file_content)
    cont = []
    counter = {}
    count = 0
    for i in range(len(file_content_split)):
        if file_content_split[i] == "%%%%%":
            count += 1
        if ((count%2)==1):
            cont.append(file_content_split[i])
            if cont[-1] not in counter:
                counter[cont[-1]] = 1
            else:
                counter[cont[-1]] += 1
    cont.pop(0)


    #print(cont)
    #print(counter)
    return(cont,counter)

def sort_dict(d):
    liste = []
    for i in d:
        liste.append( (i,d[i]) )
    #print(liste)
    L = tri_fusion(liste)
    print(L)









sort_dict(freq(file)[1])
