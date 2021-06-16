import os

def titre_general():
    print ()
    print ()
    print ( "               ********************************************")
    print ( "               *    CONSTRUCTION DES CARRES APPOLINIENS   *")
    print ( "               * Par M.-L. Tran Cong - d'apres R. Coquard *")
    print ( "               ********************************************")
    print ()
    print ()
    print ()

# ----------------------------------------------------
# Fonctions de mise en route du programme
# ----------------------------------------------------
   
def initialisation_carres(mode,n): # Retourne un carré initialisé selon le mode choisi, et un carré rempli de 0
    tb_mag=[[0 for i in range(n)]for j in range(n)]
    
    if mode==1: # De gauche à droite et de haut en bas
        tb_init=[[n*j+i+1 for i in range(n)]for j in range(n)]
        
    elif mode==2:
        # Par cadrant, de gauche à droite et de haut en bas
        # remplissage de gauche à droite et de haut en bas au sein de chaque quadrant
        tb_init=[[nn**2*(j>=nn)+nn*j+(i<nn)+i+(nn**2-nn+1)*((i+1)//(nn+1))\
                  for i in range(n)]for j in range(n)]
        
    elif mode==3: # Tous les nombres impairs, puis les pairs
        tb_init=[[2*i+1+2*n*j+(j>=nn)-n**2*(j>=nn) for i in range(n)]for j in range(n)]
        
    elif mode==4: # Lignes pairs/impairs alternées
        tb_init=[[(2*i+1+n*j)*(j%2==0)+(2*(i+1)+n*(j-1))*(j%2) for i in range(n)]for j in range(n)]

        
    return tb_init,tb_mag

def choix_dimension(): # Retourne la dimension choisie (de la forme 4k+2)
    nb_valide = False
    while not nb_valide :
        try:
            n = int(input("Veuillez choisir la dimension du carré : "))
            if n % 4 == 2 :
                nb_valide = True
            else :
                print ( "Désolé ! Vous n'avez pas entré un nombre valide. Veuillez recommencer...")
        except ValueError:
            print ("Désolé ! Ce n'est pas un nombre. Essayez encore...")
    return n

# ----------------------------------------------------
# Fonction centrale de calcul
# ----------------------------------------------------
def calcul(mode,n):
    nn = n//2 # nn = cote du quadrant
    
    for no_qd in range(4): # no_qd = numero du quadrant (de 1 a 4)
        for l in range(nn): # l = numero de ligne (au sein du quadrant)
            for c in range(nn): # c = numero de colonne (au sein du quadrant)
                i = l + nn*(no_qd>1) # i = numero de ligne "global" (= par rapport au tableau entier)
                j = c + nn*(no_qd % 2) # j = numero de colonne "global" (= par rapport au tableau entier)

                # val_defaut contient la valeur de la case avant déplacement (d'après ce que i'en ai compris). On l'appelera "valeur par défaut" de la case
                # On commence par calculer la valeur par défaut de la case courante
                if mode == 1:
                    val_defaut = normal(j,i,n)
                elif mode == 2:
                    val_defaut = normal_quadr(c,l,no_qd,nn,val_defaut)
                elif mode == 3:
                    val_defaut = ip_puis_pa(j,i,n,nn,val_defaut)
                elif mode == 4:
                    val_defaut = ip_pa_1li(j,i,n,nn,val_defaut)
                elif mode == 5:
                    val_defaut = normal_1s2(j,i,n,nn,val_defaut)
                elif mode == 6:
                    val_defaut = pairs_impairs_en_colonnes_sym(j,i,n,nn,val_defaut)
                else:
                    val_defaut = normal_1s2_avec_symetrie_centrale_par_paires(j,i,n,nn,val_defaut)                    
                
                if j == i or j+i == n-1:   # Les diagonales restent en place
                    car_mag[i][j] = val_defaut
                else: 
                    # est_marquee appartient à {0,1}. est_marquee = 1 ssi la case est dans un "triangle isocèle"
                    est_marquee = (j == nn-1 or j == nn) and (i == 0 or i == n-1) # La case est au sommet ou au pied des deux colonnes centrales
                    est_marquee |= ((i == nn-1 or i == nn) and (j == 0 or  j == n-1)) # La case est à l'extrémité gauche ou droite des deux lignes centrales 
                    est_marquee |= (j == i - 1 or j + i == n-2 or j+i == n or j == i+1) # La case est sur une sur ou une sous diagonale

                    if no_qd== 0:
                        quadr0(c,l,j,i,n,nn,car_mag,val_defaut)
                    elif no_qd == 1:
                        quadr1(c,l,j,i,n,nn,car_mag,val_defaut,est_marquee)
                    elif no_qd == 2:
                        quadr2(c,l,j,i,n,nn,car_mag,val_defaut,est_marquee)
                    else:
                        quadr3(c,l,j,i,n,nn,car_mag,val_defaut,est_marquee)
    return car_mag

# ----------------------------------------------------
# Fonctions d'affichage
# ----------------------------------------------------

def affichage_stockage(car_init,car_mag,mode,n): # Détermine comment afficher le carré : dans un fichier ou dans la console
    print ()
    if n > 34:
        print ()
        print ( "Dimension trop grande : création d'un fichier")
        ecriture_dans_fichier(car_mag,mode,n)            
    else:
        affichage(car_mag,car_init,n)
        print ()
    print ()

    # Decommenter la ligne suivante pour faire le test magie
    #teste_magie(car_mag,n)
    return

def affichage(car_mag,car_init,n):
    print ()
    print ( "#############################################")
    print ( "           Carré d'ordre ",n)
    print ( "#############################################")
    print ()
    for i in range(n):
        for j in range(n):
            # Pour voir le carré initial, décommenter la ligne 2 et commenter la ligne 1
            print ('{0:>{1}d}'.format(car_mag[i][j],len(str(n**2))),end=" ") # On utilise format pour créer un espace de la taille du chiffre le plus grand
            #print ('{0:>{1}d}'.format(car_init[i][j],len(str(n**2))),end=" ")
        print()     

def ecriture_dans_fichier(car_mag,mode,n): # Génère dans le répertoire courant un fichier txt contenant le carre
    rep = os.getcwd() # Repertoire courant
    nom = "carre_" + str(n) + ".txt"      
    chemin_nom = rep + chr(92) + nom # chr(92) est un backslash
    fichier = open(nom,'w')
    lgmax = 1 + len(str(n**2))
    blanc = " "
    for i in range(n):
        enreg = "" # Variable où on construit la chaîne de caractères
        for j in range(n):
            nb = str(car_mag[i][j])
            lg = len(nb)
            enreg += (blanc*(lgmax-lg)) + nb # On ajuste le nb d'espaces pour avoir un rendu aligné           
        fichier.write(enreg+"\n")
    fichier.close()
    print ( "Vous trouverez votre fichier ici :",chemin_nom)
    return
           
def teste_magie(car_mag,n): # Aide à vérifier si un carré est magique : affiche la somme de chaque ligne chaque colonne et chaque diagonale
    print ( "Test des lignes")
    for j in range(n):
        print(sum(car_mag[j]),end=" ")

    print ( "\n\nTest des colonnes")
    for j in range(n):
        print(sum(list(zip(*car_mag))[j]),end=" ")

    print ( "\n\nTest des diagonales")
    tot1 = 0
    tot2 = 0
    for j in range(n):
        tot1 = tot1 + car_mag[j][j]
        tot2 = tot2 + car_mag[j][n-j-1]
    print (tot1,tot2)
    print ()

# -----------------------------------------------------------
# Fonctions d'application des symétries dans chaque quadrant
# (Ce sont les fonctions effectives de transformation)
# -----------------------------------------------------------
def quadr0(c,l,j,i,n,nn,car_mag,val_defaut):
    # Note : est_marquee n'intervient pas dans ce quadrant
    if ((c - l) > n/4.0 and c > l) or ((l - c)< n/4.0 and c < l): # (c > l inutile)
        # k premières sous-diagonales et k dernières sur-diagonales
        # cases "bleues" : la case est envoyée sur sa symétrique verticale
        car_mag[i][n-1-j] = val_defaut
    else:
        # k premières sur-diagonales et k dernières sous-diagonales
        # cases "rouges" : la case est envoyée sur sa symétrique horizontale
        car_mag[n-i-1][j]= val_defaut
    return car_mag

def quadr1(c,l,j,i,n,nn,car_mag,val_defaut,est_marquee):
    if (c + l < nn-1 and c + l > n/4.0-1)or c + l > 3*n/4.0-1:
        # k premières sur-diagonales et k-dernières sous-diagonales
        # cases "orange" : sym horizontale
        car_mag[n - i-1][j] = val_defaut
    elif est_marquee == 0 and (c + l < n/4.0-1 or (c + l > nn-1 and c + l< 3*n/4.0-1)):
        # k dernières sur-diagonales et k premières sous-diagonales SANS LES CASES MARQUEES
        # cases "bleu ciel" : sym verticale
        car_mag[i][n-j-1] = val_defaut
    else:
        # Coin supérieur gauche et 1ere sous-diagonale (cases marquées du "triangle pointant vers le haut")
        # cases "vert clair" : sym centrale
        car_mag[n-i-1][n-j-1] = val_defaut
    return car_mag

def quadr2(c,l,j,i,n,nn,car_mag,val_defaut,est_marquee):
    if (c + l> n/4.0 -1 and c + l < nn-1) or c + l> 3*n/4.0-1:
        # k premières sur-diagonales et k-dernières sous-diagonales
        # cases "roses" : sym verticale
        car_mag[i][n-j-1] = val_defaut
    elif est_marquee == 0 and (c + l < n/4.0-1 or (c + l >nn-1 and c + l < 3*n/4.0-1)):
        # k dernières sur-diagonales et k premières sous-diagonales SANS LES CASES MARQUEES
        # cases "jaunes" : sym horizontale
        car_mag[n -i- 1][j] = val_defaut
    else:
        # Coin supérieur gauche et sous-diagonale (cases marquées du "triangle pointant vers le haut")
        # cases "noires" : sym centrale
        car_mag[n-i-1][n-j-1] = val_defaut
    return car_mag

def quadr3(c,l,j,i,n,nn,car_mag,val_defaut,est_marquee):
    if est_marquee == 1:
        # Toutes les cases marquées ie :
        # Coin supérieur droit et coin inférieur gauche, sur-diagonale et sous-diagonale
        # cases "vert foncé" : sym centrale
        car_mag[n-i-1][n-j-1] = val_defaut
    elif (c<l and l-c > n/4.0) or (c > l and c-l < n/4.0):
        # k dernières sous-diagonales et k premières sur-diagonales SANS LES CASES MARQUEES
        # cases "violettes" : sym verticale
        car_mag[i][n-j-1] = val_defaut
    else:
        # k premières sous-diagonales et k dernières sur-diagonales SANS LES CASES MARQUEES
        # cases "marron" : sym horizontale
        car_mag[n-i-1][j]= val_defaut
    return car_mag

# ------------------------------------------------------
# Fonctions de calcul de la valeur par defaut de la case
# ------------------------------------------------------
def normal(j,i,n):
    val_defaut = n*i + j + 1
    return val_defaut

def normal_quadr(c,l,no_qd,nn,val_defaut):
    val_defaut = nn**2*no_qd + nn*l + c + 1
    return val_defaut

def ip_puis_pa(j,i,n,nn,val_defaut):
    val_defaut = (2*j+1+i*2*n)*(i<nn)+(i>=nn)*(2+2*j+(i-nn)*2*n)
    return val_defaut

def ip_pa_1li(j,i,n,nn,val_defaut):
    if i %2 == 0:
        val_defaut = 2 * j+ 1 + 2*n*(i/2)*(i>0)
    else:
        val_defaut = 2*(j+1)+ 2*n*(i/2)
    return val_defaut

def normal_1s2(j,i,n,nn,val_defaut):
    val_defaut = 1+j/2+2*nn**2*(j%2)+nn*i          
    return val_defaut

def pairs_impairs_en_colonnes_sym(j,i,n,nn,val_defaut):
    if j == 0 or j == n-1:
        val_defaut=normal(j,i,n,nn,val_defaut)
    else:
        dp = (((j+1 - 2*(j>nn-1))/2)% 2 == 1)
        if dp == 1:
            val_defaut = n*i + n - j
        else:
            val_defaut=normal(j,i,n,nn,val_defaut)
    return val_defaut

def normal_1s2_avec_symetrie_centrale_par_paires(j,i,n,nn,val_defaut):
    val_defaut=j/2+1+nn**2*(j%2==1)+nn*i+nn**2*(i>nn-1)
    return val_defaut

# ------------------------------------------------------
# CORPS DU PROGRAMME (= main)
# ------------------------------------------------------
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
            # car_init est rempli selon le mode choisi
            # car_mag est un tableau de 0
            
            car_mag = calcul(mode,n) # On remplit car_mag
            affichage_stockage(car_init,car_mag,mode,n)
            print ()
            input('                ...Pour continuer, appuyer sur ENTREE ... ')
            print ()
print ()
print ()
print ( "                       Au revoir !")
