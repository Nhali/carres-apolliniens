#-*- coding: utf-8 -*-

# Pour un fonctionnement en mode console (DOS), remplacer # -*- coding: utf-8 -*-
# par # -*-coding:cp437-*-

from os import getcwd

def titre_general():
    print ()
    print ()
    print ( "               *********************************************")
    print ( "               *   CARRES DE DIMENSIONS IMPAIREMENT PAIRE  *")
    print ( "               *         Modèle du Carré du Soleil         *")
    print ( "               *********************************************")
    print ()
    print ()
    print ()
   
def initialisation_carres(mode,n):
    tb_mag=[[0 for j in range(n)]for i in range(n)]
    if mode==1:
        tb_init=[[n*i+j+1 for j in range(n)]for i in range(n)]
    elif mode==2:
        tb_init=[[nn**2*(i>=nn)+nn*i+(j<nn)+j+(nn**2-nn+1)*((j+1)//(nn+1))\
                  for j in range(n)]for i in range(n)]
    elif mode==3:
        tb_init=[[2*j+1+2*n*i+(i>=nn)-n**2*(i>=nn) for j in range(n)]for i in range(n)]
    elif mode==4:
        tb_init=[[(2*j+1+n*i)*(i%2==0)+(2*(j+1)+n*(i-1))*(i%2) for j in range(n)]for i in range(n)]

        
    return tb_init,tb_mag

def choix_dimension():
    while True:
        try:
            n = int(input("Veuillez choisir la dimension du carré : "))
            if n % 2 == 0 and n % 4 != 0:
                if (n//2) % 2 == 1:
                    break
            print ( "Désolé ! Vous n'avez pas entré un nombre valide. Veuillez recommencer...")
        except ValueError:
            print ( "Désolé ! Ce n'est pas un nombre. Essayez encore...")
    return n

# Procédure centrale de calcul
def calcul(mode,n):
    nn,tnb=n//2,0
    print(type(nn))
    for no_qd in range(4):
        for l in range(nn):
            for c in range(nn):
                j = l + nn*(no_qd>1)
                i = c + nn*(no_qd % 2)
                if mode == 1:
                    tnb=normal(i,j,n,nn,tnb)
                elif mode == 2:
                    tnb=normal_quadr(c,l,no_qd,nn,tnb)
                elif mode == 3:
                    tnb=ip_puis_pa(i,j,n,nn,tnb)
                elif mode == 4:
                    tnb=ip_pa_1li(i,j,n,nn,tnb)
                elif mode == 5:
                    tnb=normal_1s2(i,j,n,nn,tnb)
                elif mode == 6:
                    tnb=pairs_impairs_en_colonnes_sym(i,j,n,nn,tnb)
                else:
                    tnb=normal_1s2_avec_symetrie_centrale_par_paires(i,j,n,nn,tnb)                    
                
                if i == j or i+j == n-1:   # Les diagonales restent en place
                    car_mag[j][i] = tnb
                else:           # initialisation du drapeau d'appartenance à une forme
                    tem = (i == nn-1 or i == nn) and (j == 0 or j == n-1)
                    tem = tem + ((j == nn-1 or j == nn) and (i == 0 or  i == n-1))
                    tem = tem + (i == j - 1 or i + j == n-2 or i+j == n or i == j+1)
                    if no_qd== 0:
                        quadr1(c,l,i,j,n,nn,car_mag,tnb,tem)
                    elif no_qd == 1:
                        quadr2(c,l,i,j,n,nn,car_mag,tnb,tem)
                    elif no_qd == 2:
                        quadr3(c,l,i,j,n,nn,car_mag,tnb,tem)
                    else:
                        quadr4(c,l,i,j,n,nn,car_mag,tnb,tem)
    return car_mag

def affichage_stockage(car_init,car_mag,mode,n):
    print ()
    if n > 34:
        print ()
        print ( "Dimension trop grande : création d'un fichier")
        ecriture_dans_fichier(car_mag,mode,n)            
    else:
        affichage(car_mag,car_init,n)
        print ()
    print ()
    #teste_magie(car_mag,n)
    return

# Pour voir le carré initial, remplacer après le print (car_mag[j][i] par car_init[j][i]
def affichage(car_mag,car_init,n):
    print ()
    print ( "#############################################")
    print ( "           Carré d'ordre ",n)
    print ( "#############################################")
    print ()
    for j in range(n):
        for i in range(n):
           if n == 6:
               print ( "%2i" % car_mag[j][i],end=" ")
           elif n < 34:
               print ( "%3i" % car_mag[j][i],end=" ")
        print ()
        if n > 10:
            print ()       

def ecriture_dans_fichier(car_mag,mode,n):
    rep = getcwd()
    nom = "Impapairs_" + str(n)+".txt"      
    chemin_nom=rep+chr(92)+nom
    fichier = open(nom,'w')
    lgmax = 1 + len(str(n**2))
    blanc ="                   "
    for j in range(n):
        enreg=""
        for i in range(n):
            nb = str(car_mag[j][i])
            lg = len(nb)
            enreg += blanc[0:lgmax-lg]+nb            
        fichier.write(chaine+"\n")
    fichier.close()
    print ( "Vous trouverez votre fichier ici",chemin_nom)
    return
           
def teste_magie(car_mag,n):
    print ( "Test des lignes")
    for i in range(n):
        print(sum(car_mag[i]),end=" ")

    print ( "\n\nTest des colonnes")
    for i in range(n):
        print(sum(list(zip(*car_mag))[i]),end=" ")

    print ( "\n\nTest des diagonales")
    tot1 = 0
    tot2 = 0
    for i in range(n):
        tot1 = tot1 + car_mag[i][i]
        tot2 = tot2 + car_mag[i][n-i-1]
    print (tot1,tot2)
    print ()

# Application des symétries dans chaque quadrant
def quadr1(c,l,i,j,n,nn,car_mag,tnb,tem):
    if ((c - l) > n/4.0 and c > l) or ((l - c)< n/4.0 and c < l):
        car_mag[j][n-1-i] = tnb
    else:
        car_mag[n-j-1][i]= tnb
    return car_mag

def quadr2(c,l,i,j,n,nn,car_mag,tnb,tem):
    if (c + l < nn-1 and c + l > n/4.0-1)or c + l > 3*n/4.0-1:
        car_mag[n - j-1][i] = tnb
    elif tem == 0 and (c + l < n/4.0-1 or (c + l > nn-1 and c + l< 3*n/4.0-1)):
        car_mag[j][n-i-1] = tnb
    else:
        car_mag[n-j-1][n-i-1] = tnb
    return car_mag

def quadr3(c,l,i,j,n,nn,car_mag,tnb,tem):
    if (c + l> n/4.0 -1 and c + l < nn-1) or c + l> 3*n/4.0-1:
        car_mag[j][n-i-1] = tnb
    elif tem == 0 and (c + l < n/4.0-1 or (c + l >nn-1 and c + l < 3*n/4.0-1)):
        car_mag[n -j- 1][i] = tnb
    else:
        car_mag[n-j-1][n-i-1] = tnb
    return car_mag

def quadr4(c,l,i,j,n,nn,car_mag,tnb,tem):
    if tem == 1:
        car_mag[n-j-1][n-i-1] = tnb
    elif (c<l and l-c > n/4.0) or (c > l and c-l < n/4.0):
        car_mag[j][n-i-1] = tnb
    else:
        car_mag[n-j-1][i]= tnb
    return car_mag

# Méthodes de calcul (dans l'ordre)
def normal(i,j,n,nn,tnb):
    tnb = n*j + i + 1
    return tnb

def normal_quadr(c,l,no_qd,nn,tnb):
    tnb = nn**2*no_qd + nn*l + c + 1
    return tnb

def ip_puis_pa(i,j,n,nn,tnb):
    tnb = (2*i+1+j*2*n)*(j<nn)+(j>=nn)*(2+2*i+(j-nn)*2*n)
    return tnb

def ip_pa_1li(i,j,n,nn,tnb):
    if j %2 == 0:
        tnb = 2 * i+ 1 + 2*n*(j/2)*(j>0)
    else:
        tnb = 2*(i+1)+ 2*n*(j/2)
    return tnb

def normal_1s2(i,j,n,nn,tnb):
    tnb = 1+i/2+2*nn**2*(i%2)+nn*j          
    return tnb

def pairs_impairs_en_colonnes_sym(i,j,n,nn,tnb):
    if i == 0 or i == n-1:
        tnb=normal(i,j,n,nn,tnb)
    else:
        dp = (((i+1 - 2*(i>nn-1))/2)% 2 == 1)
        if dp == 1:
            tnb = n*j + n - i
        else:
            tnb=normal(i,j,n,nn,tnb)
    return tnb

def normal_1s2_avec_symetrie_centrale_par_paires(i,j,n,nn,tnb):
    tnb=i/2+1+nn**2*(i%2==1)+nn*j+nn**2*(j>nn-1)
    return tnb

mode=10
while mode!= 0:

    titre_general()
    print ()
    print ( " 1. Dans l'ordre normal par ligne du carré")
    print ( " 2. Dans l'ordre normal par ligne de quadrant")
    print ( " 3. Tous les nombres impairs, puis les pairs")
    print ( " 4. Avec lignes de nombres impairs et pairs alternées")
    print ( " 5. Ordre normal en sautant une case à chaque fois dans le carré")
    print ( " 6. Par 2 colonnes à la fois avec symétrie dans chaque quadrant")
    print ( " 7. Ordre normal en sautant une case et par paires symétriques de somme n²")
    print ( "                   0. Sortie du programme")
    print ()
    try:
        mode = int(input("     Votre choix : "))
    except ValueError:
        print ( "Désolé ! Ce n'est pas un nombre. Essayez encore...")
        print ()
        print ()
    else:
        if mode > 7:
            print ( "Désolé ! Vous n'avez pas entré un nombre valide. Veuillez recommencer...")
            print ()
            print ()
        elif mode >0:
            n=choix_dimension()
            car_init,car_mag=initialisation_carres(mode,n)
            car_mag=calcul(mode,n)
            affichage_stockage(car_init,car_mag,mode,n)
            print ()
            input('                ...Pour continuer, appuyer sur ENTREE ... ')
            print ()
print ()
print ()
print ( "                       Au revoir !")

