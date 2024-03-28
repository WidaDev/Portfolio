#Par Timothé Kalinka et Héloïs d'Argent

import random
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk

class Carte():
    """Une carte est compossé de:
        -une figure
        -une couleur
        -une valeur
        -une position
        -une taille"""
    
    def __init__(self,val, coul, w=60, x=0, y=0):
        """Constructeur de la classe carte"""
        self.__valeur=val
        self.__couleur=coul
        if not(self.__couleur=='atout'):
            match val:
                case 11:
                    self.__figure="valet"
                case 12:
                    self.__figure="cavalier"
                case 13:
                    self.__figure="dame"
                case 14:
                    self.__figure="roi"
                case _:
                    self.__figure=str(val)
        elif val == 0:
            self.__figure='excuse'
        else:
            self.__figure=str(val)

        # Paramètres géométriques
        self.__x = x
        self.__y = y
        self.__w=w
        self.__h=int(w*(9/5))

        self.__bg_base=Image.open(f"carte/{self.printcarte()}.png")
        self.__bg=self.__bg_base.resize((self.__w,self.__h))
        
        self.__bgg=self.__bg.convert('L')
        draw = ImageDraw.Draw(self.__bgg)
        draw.line([(0, 0), (self.__w, self.__h)], fill="black", width=4)
        draw.line([(self.__w, 0), (0,self.__h)], fill="black", width=4)

        self.__Gr_bg=self.__bg_base.resize((self.__w+5,self.__h+8))
        self.__bg = ImageTk.PhotoImage(self.__bg)
        self.__bgg = ImageTk.PhotoImage(self.__bgg)
        self.__Gr_bg = ImageTk.PhotoImage(self.__Gr_bg)
        self.up=False

        self.dedans=False
                
        # Point cliqué
        self.dx = self.dy = None

        self.__affiche=False

    def Getsize(self): 
        """retourne la taille d'une carte"""
        return self.__w,self.__h
    
    def GetValeur(self):
        """retourne la valeur d'une carte"""
        return self.__valeur
    
    def GetCouleur(self):
        """retourne la couleur d'une carte"""
        return self.__couleur
        
    def GetFigure(self):
        """retourne la figure d'une carte"""
        return self.__figure
    
    def GetPosition(self):
        """retourne la position de la carte"""
        return self.__x,self.__y
    
    def __SetFigure(self,val):
        """Muttateur de figure"""
        if not(self.__couleur=='atout'):
            match val:
                case 11:
                    self.__figure="valet"
                case 12:
                    self.__figure="cavalier"
                case 13:
                    self.__figure="dame"
                case 14:
                    self.__figure="roi"
                case _:
                    self.__figure=str(val)
        elif val == 0:
            self.__figure='excuse'
        else:
            self.__figure=str(val)
    
    def SetValeur(self,val):
        """Retourne Vrai si la valeur de la carte à changer
        par val
        Retourne Faux sinon (val n'appartient pas à [2;14])
        """
        if 0<=val<=22:
            self.__valeur=val
            self.__SetFigure(val)
            return True
        else:
            return False
        
    def SetCouleur(self,coul):
        """Retourne Vrai si la couleur de la carte à changer
        par val
        Retourne Faux sinon (valeur non comprise dans le domaine)
        """
        first_couleur=["carreau","coeur","pique","trefle","atout"]
        if coul in first_couleur:
            self.__couleur=coul
            return True
        else:
            return False

    def SetPosition(self,x,y):
        """Muttateur de la position"""
        self.__x = x
        self.__y = y
        if self.__affiche:
            self.cacher()
            self.afficher()

    def Setsize(self,w):
        """Muttateur de la taille d'une carte"""
        self.__w=w
        self.__h=int(w*(28/15))
        self.__bg=self.__bg_base.resize((self.__w,self.__h))
        self.__bgg=self.__bg.convert('L')
        self.__Gr_bg=self.__bg_base.resize((self.__w+5,self.__h+8))

        if self.__affiche:
            self.cacher()
            self.afficher()

    def printcarte(self):
        """affiche la carte sélectionné"""
        if self.GetFigure()!="excuse":
            return(self.GetFigure()+"_de_"+self.GetCouleur())
        else: return("excuse")
    
    def printprintcarte(self,event=None):
        """print la carte selectionner"""
        print(self.printcarte())

    def afficher(self,jouable=True,up=False,dp=False):
        """affiche une carte"""
        self.cacher()
        if dp:
            self.label1 = tk.Label(image = self.__bg)
            self.label1.bind('<Button-1>', self.printprintcarte)

        elif jouable:
            if up:          
                self.label1 = tk.Label(image = self.__Gr_bg)

            else:
                self.label1 = tk.Label(image = self.__bg)
            
            self.label1.bind('<Button-1>', self.selection)

        else:
            self.label1 = tk.Label(image = self.__bgg)
            self.label1.bind('<Button-1>', self.printprintcarte)

        self.label1.place(x=self.__x, y=self.__y)                
            
    def selection(self, event=None):
        """permet de sélection et deselectionner des cartes"""
        print(self.printcarte())
        if pli.ja.sele["nb_choose"]<pli.ja.sele["nb_max"] and not(self.up):
            pli.ja.sele["nb_choose"]+=1
            pli.ja.sele[self]=not(pli.ja.sele[self])
            self.up=not(self.up)                
            self.afficher(up=self.up)

        elif self.up:
            pli.ja.sele["nb_choose"]-=1
            pli.ja.sele[self]=not(pli.ja.sele[self])
            self.up=not(self.up)                
            self.afficher(up=self.up)
        
    def cacher(self):
        """cache une carte"""
        if "label1" in self.__dict__:
            self.label1.destroy()

    def est_dedans(self, x, y):
        """ Renvoie True si le point (x,y) est à l'intérieur de l'objet
        """
        return (self.__x < x < self.__x + self.__w 
            and self.__y < y < self.__y + self.___h)
    
class JeuDeCarte:
    """un Jeu de Carte composée d'un nb de carte et d'un paquet"""

    def __init__ (self,Nb,w):
        """constructeur"""

        self.__NbCartes=Nb
        self.__Paquet=[]
        firstValue=1
        for i in range(22):
            self.__Paquet.append(Carte(i,"atout",w=w))
        for carteparcoul in range((self.__NbCartes-22)//4):
            for coul in ["carreau","coeur","pique","trefle"]:
                self.__Paquet.append(Carte(firstValue+carteparcoul,coul,w=w))

    def GetNbCartes(self):
        """retourne la valeur de NbCartes"""
        return self.__NbCartes
    
    def GetPaquet(self):
        """retourne la valeur de Paquet"""
        return self.__Paquet
    
    def SetPaquet(self,paquet):
        self.__Paquet=paquet
    
    def mellange(self):
        """mélange le paquet"""
        random.shuffle(self.__Paquet)

    def printpaquet(self):
        """affiche le paquet"""
        for card in self.__Paquet:
            card.printprintcarte(card)
             
    def ajouteCarte(self,card):
        """ajoute une carte au paquet"""
        self.__Paquet.append(card)
    
    def couper(self):
        """coupe le jeu"""
        i=random.randint(3,75)
        paquet1,paquet2=self.__Paquet[0:i],self.__Paquet[i:-1]
        self.__Paquet=paquet2+paquet1

    def restart(self):
        """permet de remetre le paquet et les cartes en position de base"""
        for carte in self.__Paquet:
            carte.cacher()
            carte.up=False

class Joueur:
    """un joueur posède, une main, une équipe(qui ne sera connu que par le programe), un nombre de point"""
    def __init__(self):
        self.main = []
        self.attaquant =False
        self.points = 0
        self.nom = ''
        self.num = 0
        self.triee=False
        self.nboutler=0
        self.score=0
    
    def naming(self, num):
        """nommes le joueur"""
        self.nom = listeJoueurs[num]
        self.num = num

    def endGame(self):
        """affiche les point du joueur en fin de manche"""
        return f"{self.nom} possède {self.points} points."
    
    def selection(self,ply,nb_carte,h):
        """permet de choisir des cartes"""
        global pli
        pli=ply
        self.sele={"nb_choose":0,"nb_max":nb_carte}
        for carte in self.main:
            self.sele[carte]= False
        self.afficheAsk(h)

    def afficheAsk(self,h):
        """permet d'afficher le button pour passer au joueur suivant"""
        self.TextNext = canvas.create_text(215, 290, text=f"C'est à {self.nom} de jouer.", fill="White", font=('Times', 14))
        self.BoutonNext = tk.Button(text="Continuer", command= lambda : self.afficheTrue(h))
        self.BoutonNext.place(x=323, y=278)
    
    def afficheTrue(self,h):
        canvas.delete(self.TextNext)
        self.BoutonNext.destroy()
        self.affiche_main(h)
    
    def valider(self):
        """permet de valider une selection de carte"""
        if self.sele["nb_choose"]==self.sele["nb_max"]:
            i=0
            while i<len(self.main):
                if self.sele[self.main[i]]:
                    self.main[i].cacher()
                    if self.main[i].GetValeur()==0 and len(self.main)!=0 and self.attaquant:
                        self.nboutler+=1
                        self.score+=4
                    pli.ajoutecarte(self.main[i],self)
                    del(self.main[i])
                    i-=1
                i+=1
            bt.destroy()
            pli.affiche_plie()
            self.cacher_main()
            pli.jeu(pli.i_j)

    def cacher_main(self):
        """éfface la main de l'écrant"""
        for i in self.main:
            i.cacher()

    def affiche_main(self,h,jouer=True):
        """affiche la main du joueur"""
        if not jouer:
            for i in range(len(self.main)):
                w,hcarte=self.main[i].Getsize()
                self.main[i].SetPosition(15+(w+10)*(i%8),h//2+(hcarte+15)*(i//8))
                self.main[i].afficher(dp=True)
        elif pli.Getcouleur()=='chien' or pli.Getcouleur() is None:
            for i in range(len(self.main)):
                w,hcarte=self.main[i].Getsize()
                self.main[i].SetPosition(15+(w+10)*(i%8),h//2+(hcarte+15)*(i//8))
                self.main[i].afficher(jouable=True)
       
        else:
            #cjr: carte jouable règle...
            cjr1,cjr2=False,False
            if pli.Getcouleur()=='atout':
                i=0
                while i<len(self.main) and not cjr1:
                    w,hcarte=self.main[i].Getsize()
                    if (pli.Getbestcarte().GetValeur()<self.main[i].GetValeur()
                        and self.main[i].GetCouleur()=='atout' and not self.main[i].GetValeur()==0):
                        cjr1=True
                    elif  not cjr2 and self.main[i].GetCouleur()=='atout' and not self.main[i].GetValeur()==0:
                        cjr2=True
                    i+=1
                for i in range(len(self.main)):
                    self.main[i].SetPosition(15+(w+10)*(i%8),h//2+(hcarte+15)*(i//8))
                    if cjr1:
                        if self.main[i].GetValeur()==0:
                            self.main[i].afficher(jouable=True)
                        elif (pli.Getbestcarte().GetValeur()<self.main[i].GetValeur() 
                        and self.main[i].GetCouleur()=='atout'):
                            self.main[i].afficher(jouable=True)
                        else:
                            self.main[i].afficher(jouable=False)
                    elif cjr2:
                        if self.main[i].GetValeur()==0:
                            self.main[i].afficher(jouable=True)
                        elif self.main[i].GetCouleur()=='atout':
                            self.main[i].afficher(jouable=True)
                        else:
                            self.main[i].afficher(jouable=False)
                    else:
                        self.main[i].afficher(jouable=True)
            else:
                i=0
                while i<len(self.main) and not cjr1:
                    w,hcarte=self.main[i].Getsize()
                    if self.main[i].GetCouleur()==pli.Getcouleur():
                        cjr1=True
                    elif  not cjr2 and self.main[i].GetCouleur()=='atout' and not self.main[i].GetValeur()==0:
                        cjr2=True
                    i+=1
                for i in range(len(self.main)):
                    self.main[i].SetPosition(15+(w+10)*(i%8),h//2+(hcarte+15)*(i//8))
                    if cjr1:
                        if self.main[i].GetValeur()==0:
                            self.main[i].afficher(jouable=True)
                        elif self.main[i].GetCouleur()==pli.Getcouleur():
                            self.main[i].afficher(jouable=True)
                        else:
                            self.main[i].afficher(jouable=False)
                    elif cjr2:
                        if self.main[i].GetValeur()==0:
                            self.main[i].afficher(jouable=True)
                        elif self.main[i].GetCouleur()=='atout':
                            self.main[i].afficher(jouable=True)
                        else:
                            self.main[i].afficher(jouable=False)
                    else:
                        self.main[i].afficher(jouable=True)

class plie:
    """un plie à une couleur, une liste de carte, un vainqueur, un nombre de carte attendue"""

    def __init__ (self,list_joueur,h,partie):
        """constructeur"""

        self.__liste_carte=[]
        self.list_joueur=list_joueur
        self.__cut=False
        self.__coul=None
        self.__partie=partie
        self.h=h

    def Getlistecarte(self):
        """guetteur renvoie la liste des cartes"""
        return self.__liste_carte
    
    def Getlistjoueur(self):
        """guetteur renvoie le nombre de carte"""
        return self.list_joueur
    
    def Getcouleur(self):
        """getteur retourne la couleur du plie"""
        return self.__coul
    
    def Getvainqueur(self):
        """guetteur renvoie le gagnant présumé du plie"""
        return self.__winner
    
    def Getbestcarte(self):
        """retourne la meilleur carte du plie"""
        return self.__bestcarte
    
    def Getcut(self):
        """renvoie si le plie à été coupé (un atout joué)"""
        return self.__cut

    def ajoutecarte(self,carte,joueur):
        """ajoute une carte aux plie"""
        self.__liste_carte.append(carte)
        if len(self.__liste_carte)==1:
            self.__winner=joueur
            self.__bestcarte=carte
            self.__coul=carte.GetCouleur()
            if self.Getcouleur()=="atout":
                self.__cut=True
        elif carte.GetCouleur()=="atout" and not carte.GetValeur==0 and not self.__cut:
            self.__cut=True
            self.__bestcarte=carte
            self.__winner=joueur
        elif (carte.GetCouleur()==self.__bestcarte.GetCouleur() 
              and carte.GetValeur()>self.__bestcarte.GetValeur()):
            self.__bestcarte=carte
            self.__winner=joueur

    def jeu(self,i_j):
        """permet de jouer un plie"""
        global bt

        if len(self.__liste_carte)<len(self.list_joueur):
            self.i_j=i_j
            self.valide=False
            self.ja=self.list_joueur[(i_j+len(self.__liste_carte))%(len(self.list_joueur))]
            self.ja.selection(self,1,self.h)
            bt=tk.Button(text="Valider",command=self.ja.valider, font=("Times", 13))
            bt.place(x=215,y=30)
        elif len(self.list_joueur[i_j].main)!=0:
            self.deplace_plie()         
            self.ajoute_point()
            pli=plie(self.Getlistjoueur(),self.h,self.__partie)
            i=0
            for j in range(len(self.list_joueur)):
                if self.list_joueur[j]==self.__winner:
                    i=j
            pli.jeu(i)
        else:
            self.deplace_plie()
            self.ajoute_point()
            self.__partie.end_game()

    def ajoute_point(self):
        """ajoute les point au joueur et remet les carte dans le paquet"""
        for i in self.__liste_carte:
            if self.__winner.attaquant:
                if (i.GetValeur()==21 or 
                    (i.GetValeur()==1 and i.GetCouleur()=="atout")
                    or (len(self.__winner.main)==0 and i.GetValeur()==0)):
                    self.__winner.score+=4.5
                    self.__winner.nboutler+=1
                elif i.GetFigure()=='roi':
                    self.__winner.score+=4.5
                elif i.GetFigure()=='dame':
                    self.__winner.score+=3.5
                elif i.GetFigure()=='cavalier':
                    self.__winner.score+=2.5
                elif i.GetFigure()=='roi':
                    self.__winner.score+=1.5
                else:
                    self.__winner.score+=0.5
            self.__partie.paquet.ajouteCarte(i)       
    
    def affiche_plie(self):
        """permet d'afficher le plie"""
        for i in range(len(self.__liste_carte)):
            w,hcarte=self.__liste_carte[i].Getsize()
            self.__liste_carte[i].SetPosition(135+(w+10)*(i%8),self.h//2-150+(hcarte+15)*(i//8))
            self.__liste_carte[i].afficher(dp=True)

    def deplace_plie(self):
        """permet de déplacer le plie"""
        for i in range(len(self.__liste_carte)):
            w,hcarte=self.__liste_carte[i].Getsize()
            self.__liste_carte[i].SetPosition(15+(w+10)*(i%3),15+(hcarte+15)*(i//3))
            self.__liste_carte[i].afficher(dp=True)

class Fenetre(tk.Tk):
    """la fennetre principale (la classe est une fenetre tk)"""
    def __init__(self,w):
        """construsteur"""
        super().__init__()
        global canvas

        self.title("Tarot")
        self.iconphoto(False, tk.PhotoImage(file="carte/1_de_atout.png"))
        #Création des valeurs correct pour la taille de fenêtre
        self.w=w
        self.h=int((63/50)*w)
        canvas=tk.Canvas(width=self.w, height=self.h)
        self.w=w
        self.h=int((63/50)*w)
        canvas.grid()
        
        #Création de fond d'écran
        self.wallpaper= (Image.open("FD.png"))
        self.wallpaper = self.wallpaper.resize((self.w, self.h))
        self.wallpaper = ImageTk.PhotoImage(self.wallpaper)
        canvas.create_image (0,0, image =self.wallpaper, anchor="nw")
        
        #creation de paquet de carte
        self.mon_jeu=JeuDeCarte(78,w=(self.w//10))

        # début de la partie
        Jeu = Partie(self.mon_jeu,self.h)

class Partie():
    """la classe partie est composé d'un nombre de joueur, d'une liste de joueur, d'un chien et d'un paquet de carte"""
    def __init__(self, paquet,h):
        self.nbJoueurs = len(listeJoueurs)
        self.creerPartie()
        self.chien = []
        self.paquet=paquet
        self.paquet.mellange()
        self.Distribution()
        self.height=h
        self.indiceChien = 0
        self.demandeChien()
        

    def creerPartie(self):
        """initialise la partie"""
        theJoueurs = []
        for i in range(self.nbJoueurs):
            currentJoueur = Joueur()
            currentJoueur.naming(i)
            theJoueurs.append(currentJoueur)
        self.listeJoueurs = theJoueurs

    def testeur(self):
        """vérifie qu'il n'y a pas d'erreur"""
        if self.nbJoueurs not in (3,4,5):
            print("Nombre de joueurs incorrect.")
            exit()

        if len(self.paquet.GetPaquet()) != 72:
            print("Nombre de carte annormal.")
            exit()
    
    def Distribution(self):
        """distribue les cartes à tout les joueurs"""
        if self.nbJoueurs == 3:
            cardToDistrib = 4
        else : cardToDistrib = 3

        #retire le chien avant la distribution
        for i in range(6):
            self.chien.append(self.paquet.GetPaquet().pop(random.randint(0, len(self.paquet.GetPaquet())-i-1)))

        while len(self.paquet.GetPaquet()) != 0:
            for joueur in self.listeJoueurs:
                for i in range(cardToDistrib):
                    joueur.main.append(self.paquet.GetPaquet()[i])
                self.paquet.SetPaquet(self.paquet.GetPaquet()[cardToDistrib:])
        
    def print_cartes(self):
        """afiche les carte d'un joueur dans la console"""
        for i in range(self.nbJoueurs):
            nom = self.listeJoueurs[i]
            print(f"Le joueurs {i}: {nom.nom}, possède :")
            for carte in range(len(nom.main)):
                print(nom.main[carte].printcarte())
            print("\n", "\n")

    def jouer(self):
        """comence la partie"""
        self.p=plie(self.listeJoueurs,self.height,self)
        self.p.jeu(self.indiceChien)
    
    def demandeChien(self):
        """commence les enchers pour le moment seul la prise à garde sans le chien est disponible"""
        self.Chientexte = canvas.create_text(250,45, font=("Times", 16), text=f"{listeJoueurs[self.indiceChien]}, voulez vous le chien ?", fill="White")
        self.listeJoueurs[self.indiceChien].affiche_main(self.height,jouer=False)
        self.boutonChienOui = tk.Button(text="Accepter", command=self.ChienOui,font=('Times', 14))
        self.boutonChienNon = tk.Button(text="Refuser", command=self.ChienNon, font=('Times', 14))
        self.boutonChienOui.place(x=100, y=265)
        self.boutonChienNon.place(x=350, y=265)
    
    def ChienNon(self):
        """s'active si le chien n'est pas voulue"""
        self.indiceChien+=1
        canvas.delete(self.Chientexte)
        self.boutonChienNon.destroy()
        self.boutonChienOui.destroy()
        if self.indiceChien == 4:
            self.indiceChien-=1
            self.ChienOui()
        else:
            self.demandeChien()
    
    def ChienOui(self):
        """s'active si le chien est voulue"""
        self.boutonChienNon.destroy()
        self.boutonChienOui.destroy()
        canvas.delete(self.Chientexte)
        print(listeJoueurs[self.indiceChien],"veut le chien.")
        self.listeJoueurs[self.indiceChien].attaquant=True
        self.attaquant=self.listeJoueurs[self.indiceChien]
        self.ajoute_chien()
        self.jouer()

    def end_game(self):
        """permet l'affichage des point en fin de manche"""
        self.paquet.restart()
        victoire=False
        if 56-(5*self.attaquant.nboutler+5*self.attaquant.nboutler//2)<self.attaquant.score:
            victoire=True
        for i in range(len(self.listeJoueurs)):
            self.listeJoueurs[i].points+=(2*int(self.listeJoueurs[i].attaquant)-1)*((2*int(victoire)-1)*25+(int(self.attaquant.score)-(56-(5*self.attaquant.nboutler+5*self.attaquant.nboutler//2))))
            canvas.create_text(250,self.height//2+i*50, font=("Times", 16), text=self.listeJoueurs[i].endGame(), fill="White")
        bt=tk.Button(text="Continuer",command=self.manche_suivante, font=("Times", 13))
        bt.place(x=450, y=320)

    def manche_suivante(self):
        """passe à la manche suivante"""
        self.paquet.cut()
        self.Distribution()
        self.indiceChien = 0
        self.demandeChien()
    
    def ajoute_chien(self):
        """gère les point du chien pour le prenneur"""
        for i in self.chien:
            if (i.GetValeur()==21 or 
                (i.GetValeur()==1 and i.GetCouleur()=="atout")
                or (len(self.attaquant.main)==0 and i.GetValeur()==0)):
                self.attaquant.score+=4.5
                self.attaquant.nboutler+=1
            elif i.GetFigure()=='roi':
                self.attaquant.score+=4.5
            elif i.GetFigure()=='dame':
                self.attaquant.score+=3.5
            elif i.GetFigure()=='cavalier':
                self.attaquant.score+=2.5
            elif i.GetFigure()=='roi':
                self.attaquant.score+=1.5
            else:
                self.attaquant.score+=0.5
            self.paquet.ajouteCarte(i)


class Main_menu:
    """menu principal"""
    def __init__(self):
        
        # Création du widget de fond
        self.canvas = tk.Canvas(width=700,height=450)
        self.canvas.config(highlightthickness=2)
        self.canvas.pack()
        # Création du texte "Titre"
        self.canvas.create_image(0,0, image=image_de_fond, anchor='w')
        self.canvas.create_text(370,100, text="Tarot", font=("DK Carte Blanche", 65, "underline"), state = "disabled", fill='White')


        # Création du bouton "Jouer"
        self.bouton_jouer = tk.Button(fenetre, text="Jouer", command=self.jouer, font=("Helvetica", 16), height=1, width=10)
        self.bouton_jouer.place(x=310,y=250)

        # Création du bouton "Quitter"
        self.bouton_quitter = tk.Button(fenetre, text="Quitter", command=fenetre.quit, font=("Helvetica", 16), height=1, width=10)
        self.bouton_quitter.place(x=310, y=300)

        # Boucle principale
        fenetre.mainloop()
    
    def jouer(self):
        """lance la sélection du nombre de joueur"""
        self.bouton_jouer.destroy()
        self.bouton_quitter.destroy()
        Select = Selection(self.canvas)
        
class Selection:
    """selection du nombre de joueur"""
    def __init__(self, canvas):

        #Choix du nombre de joueur
        self.bouton3 = tk.Button(fenetre, text="3 Joueurs", command=self.threePlayers, font=("Helvetica", 16), height=1, width=10)
        self.bouton3.place(x=310,y=250)
        
        self.bouton4 = tk.Button(fenetre, text="4 Joueurs", command=self.fourPlayers, font=("Helvetica", 16), height=1, width=10)
        self.bouton4.place(x=310,y=300)
        
        self.bouton_quitter = tk.Button(fenetre, text="Quitter", command=fenetre.quit, font=("Helvetica", 16), height=1, width=6)
        self.bouton_quitter.place(x=600,y=400)
        self.canvas = canvas

    def threePlayers(self):
        """cas 3 joueurs"""
        self.bouton3.destroy()
        self.bouton4.destroy()
        self.bouton_quitter.destroy()
        self.zone_texte_1 = tk.Entry(fenetre, width=20, font=("Times", 12))
        self.zone_texte_1.place(x=280, y=200)

        self.zone_texte_2 = tk.Entry(fenetre, width=20, font=("Times", 12))
        self.zone_texte_2.place(x=280, y=240)

        self.zone_texte_3 = tk.Entry(fenetre, width=20, font=("Times", 12))
        self.zone_texte_3.place(x=280, y=280)

        # Bouton pour valider et ajouter le texte à la liste
        self.bouton_valider = tk.Button(fenetre, text="Valider", command=self.Validation3, font=('Times', 14))
        self.bouton_valider.place(x=450, y=320)

        #Bouton pour revenir à la fenêtre précédente
        self.bouton_annuler = tk.Button(fenetre, text="Annuler", command=self.annulation, font=('Times', 14))
        self.bouton_annuler.place(x=200, y=320)
        # Liste pour stocker les textes
        self.liste_texte = []

                    
    def fourPlayers(self):
        """cas 4 joueurs"""
        self.bouton3.destroy()
        self.bouton4.destroy()
        self.bouton_quitter.destroy()
        self.zone_texte_1 = tk.Entry(fenetre, width=20, font=("Times", 12))
        self.zone_texte_1.place(x=280, y=200)

        self.zone_texte_2 = tk.Entry(fenetre, width=20, font=("Times", 12))
        self.zone_texte_2.place(x=280, y=240)

        self.zone_texte_3 = tk.Entry(fenetre, width=20, font=("Times", 12))
        self.zone_texte_3.place(x=280, y=280)

        self.zone_texte_4 = tk.Entry(fenetre, width=20, font=("Times", 12))
        self.zone_texte_4.place(x=280, y=320)
        
        # Bouton pour valider et ajouter le texte à la liste
        self.bouton_valider = tk.Button(fenetre, text="Valider", command=self.Validation4, font=('Times', 14))
        self.bouton_valider.place(x=450, y=360)

        #Bouton pour revenir à la fenêtre précédente
        self.bouton_annuler = tk.Button(fenetre, text="Annuler", command=self.annulation, font=('Times', 14))
        self.bouton_annuler.place(x=200, y=360)
        # Liste pour stocker les textes
        self.liste_texte = []
        
    def Validation3(self):
        """validation 3 joueurs"""
        global listeJoueurs
        self.bouton_valider.destroy()
        texte_1 = self.zone_texte_1.get()
        texte_2 = self.zone_texte_2.get()
        texte_3 = self.zone_texte_3.get()
        if texte_1 =="" or texte_2 == "" or texte_3 =="":
            print("Merci de donner un nom aux Joueurs.")
            self.zone_texte_1.destroy()
            self.zone_texte_2.destroy()
            self.zone_texte_3.destroy()
            self.threePlayers()
            self.Add_temporary_text()
        else:
            # Ajouter les textes à la liste
            self.liste_texte.append(texte_1)
            self.liste_texte.append(texte_2)
            self.liste_texte.append(texte_3)
            fenetre.destroy()
            listeJoueurs = self.liste_texte
            game=Fenetre(500)

            game.mainloop()
        
    def Validation4(self):
        """cas 4 joueurs"""
        global listeJoueurs
        self.bouton_valider.destroy()
        texte_1 = self.zone_texte_1.get()
        texte_2 = self.zone_texte_2.get()
        texte_3 = self.zone_texte_3.get()
        texte_4 = self.zone_texte_4.get()
        if texte_1 =="" or texte_2 == "" or texte_3 =="":
            print("Merci de donner un nom aux Joueurs.")
            self.zone_texte_1.destroy()
            self.zone_texte_2.destroy()
            self.zone_texte_3.destroy()
            self.zone_texte_4.destroy()
            self.fourPlayers()
            self.Add_temporary_text()
        else:
            # Ajouter les textes à la liste
            self.liste_texte.append(texte_1)
            self.liste_texte.append(texte_2)
            self.liste_texte.append(texte_3)
            self.liste_texte.append(texte_4)
            fenetre.destroy()
            listeJoueurs = self.liste_texte
            game=Fenetre(500)

            game.mainloop()
            
    def Add_temporary_text(self):
        """affiche un message d'erreur si tout les joueur n'ont pas de nom"""
        self.Message = self.canvas.create_text(370, 170, font =('Times', 12, 'bold', "underline") ,
                                               text= "Merci de donner un nom aux joueurs.", fill='black')
        fenetre.after(4000, self.canvas.delete, self.Message)
    
    def annulation(self):
        """permet d'annuler"""
    # Parcourir tous les widgets enfants et détruire les boutons
        for widget in fenetre.winfo_children():
            if isinstance(widget, tk.Button) or isinstance(widget, tk.Entry):
                widget.destroy()
        self.__init__(self.canvas)

def main():
    global fenetre,image_de_fond
    # Création de la fenêtre principale
    fenetre = tk.Tk()
    fenetre.title("Tarot Multijoueurs")
    fenetre.geometry("700x450")
    # Chargement de l'image de fond
    image_de_fond = Image.open("FD.png")
    image_de_fond = ImageTk.PhotoImage(image_de_fond)
    Jeu = Main_menu()

if __name__=="__main__":
    main()