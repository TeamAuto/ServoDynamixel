""" Auteur: Luca Freund
    Date:   23.02.2023

    Ce code permet de communiquer avec les servos dynamixel

    Auteur: Diego Lamas
    Date:   01.10.2024

    Modif V7:
    ajout de gestion de couple en cycle avec plusieurs modes
"""

"""
    pour une utilisation "normale" modifier les valeurs de :
        "Plc.Connection" (ID de votre automate) ligne 40
        "NomServoList" (Nom défini pour chaques servo) a la ligne 47 (si néescésaire)
"""

import pyads
import time
from Pyads import *
from dynamixel_sdk import *
from U2D2 import *

#Declaration de variable utiles
DoneInfo = False
MoveInit = False
DoneHoming = False
AttendRun = False
HomingPosition0 = False
Move = 0
CodeErreur = 0
Erreur = 0
iCompteurTest = 0 #Permet de mesurer le temps de cycle
Compteur = 0

plc = Plc()
Servo = Dxl()

plc.Connection("192.168.0.30.1.1") # ID de l'automate (le meme que dans twincat)
Etat_PLC = plc.EtatActuelle()
MachineState, ADSErreur = Etat_PLC

if ADSErreur != 0 or MachineState != 5:
    print("Erreur")

NomServoList = ["ServoA", "ServoB", "ServoC", "ServoD", "ServoE", "ServoF", "ServoG", "ServoH", "ServoI", "ServoJ", "ServoK", "ServoL", "ServoM", "ServoN", "ServoO", "ServoP", "ServoQ", "ServoR", "ServoS", "ServoT"] # � modifier en fonction du nom que vous souhaitez donner a vos Servo, d�clarer chaque servo avec les memes nom dans le POU ServoDynamixel (ne pas mettre de chiffres dans les nom)
ListValeurNom = plc.CreationVariableList("ServoDynamixel", NomServoList)
Nom_ID, Nom_ModeRotation, Nom_PosMin, Nom_PosMax, Nom_PosInit, Nom_MoveInit, Nom_HomingONOFF, Nom_HomingBasHaut, Nom_CapteurHoming, Nom_VitesseHoming, Nom_ForceHoming, Nom_PositionApresHoming, Nom_ForceMax, Nom_ForceMaxAntihoraire, Nom_ForceDepassee, Nom_MarcheArriere, Nom_MoveRun, Nom_Prioritaire, Nom_PositionOrdre, Nom_Vitesse, Nom_Force, Nom_PositionReel, Nom_Position0, Nom_HomingDone, Nom_Etat, Nom_CodeErreur, Nom_Movement, Nom_EnCycle, Nom_PositionActuelle = ListValeurNom


Val_PosInit = [0 for i in range((len(Nom_ID)))]
Val_PosInitStock =  [0 for i in range((len(Nom_ID)))]
Val_Move = [0 for i in range((len(Nom_ID)))]
Val_Force = [0 for i in range((len(Nom_ID)))]
Val_MoveRun = [0 for i in range((len(Nom_ID)))]
Val_HomingBasHaut = [0 for i in range((len(Nom_ID)))]
Val_VitesseHoming = [0 for i in range((len(Nom_ID)))]
Val_ForceHoming = [0 for i in range((len(Nom_ID)))]
Val_PositionApresHoming = [0 for i in range((len(Nom_ID)))]
Val_ForceMax = [0 for i in range((len(Nom_ID)))]
Val_ForceMaxAntihoraire = [0 for i in range((len(Nom_ID)))]
Val_ForceDepassee = [0 for i in range((len(Nom_ID)))]
Val_MarcheArriere = [0 for i in range((len(Nom_ID)))]
Val_PositionOrdre = [0 for i in range((len(Nom_ID)))]
Val_PositionReel = [0 for i in range((len(Nom_ID)))]
Val_PositionActuelle = [0 for i in range((len(Nom_ID)))]
Val_PositionHomingMin = [0 for i in range((len(Nom_ID)))]
Val_PositionOrdrePrecedent = [0 for i in range((len(Nom_ID)))]
Val_PositionOrdrePrecedent_2 = [0 for i in range((len(Nom_ID)))]
Val_VitessePrecedent = [0 for i in range((len(Nom_ID)))]
Val_CodeErreur = [0 for i in range((len(Nom_ID)))]
Val_Prioritaire = [False for i in range((len(Nom_ID)))]
Val_MoveRun = [False for i in range((len(Nom_ID)))]
Val_HomingDone = [False for i in range((len(Nom_ID)))]
Val_CapteurHoming = [False for i in range((len(Nom_ID)))]
Val_MovePrecedent = [False for i in range((len(Nom_ID)))]
Val_NbCycle = [0 for i in range((len(Nom_ID)))]
ListFusionSend = [0 for i in range((len(Nom_ID)))]
ListFusionSendList = [0 for i in range((len(Nom_ID)))]

Val_EnCycle = plc.Lit_Variable_List_Bool(Nom_EnCycle)

while Val_EnCycle[0]:
    Val_ID = plc.Lit_Variable_List_Int(Nom_ID)

    Val_EnCycle = plc.Lit_Variable_List_Bool(Nom_EnCycle)
    Val_Etat = plc.Lit_Variable_List_Int(Nom_Etat)

    if Val_Etat[0] == 0:
    #Etat Init
        print("Etat Init")
    if Val_Etat[0] == 10:
    #Etat PreSetup
        print("Etat PreSetup")

        CodeErreur = [10 for i in range((len(Nom_ID)))] #Reset l'erreur
        Val_Nom_CodeErreur = plc.FusionNomValeur(Nom_CodeErreur, CodeErreur)
        plc.Ecrit_Variable_List(Val_Nom_CodeErreur)

        Erreur, Val_PositionReel = Servo.LirePostionList(Val_ID)
        Val_Nom_PositionReel = plc.FusionNomValeur(Nom_PositionReel, Val_PositionReel)
        plc.Ecrit_Variable_List(Val_Nom_PositionReel)
        Val_Etat = [20 for i in range((len(Nom_ID)))]
        Val_Nom_Etat = plc.FusionNomValeur(Nom_Etat, Val_Etat)
        plc.Ecrit_Variable_List(Val_Nom_Etat)

    if Val_Etat[0] == 20:
    #Etat Setup
        print("Etat Setup")
        Val_ModeRotation = plc.Lit_Variable_List_Int(Nom_ModeRotation)
        Val_PosMin = plc.Lit_Variable_List_Int(Nom_PosMin)
        Val_PosMax = plc.Lit_Variable_List_Int(Nom_PosMax)
        for i in range(len(Val_ID)):
            Erreur = Servo.TorqueOFF(Val_ID[i])
        for i in range(len(Val_ID)):
            Erreur = Servo.ModeRot(Val_ID[i], Val_ModeRotation[i])
            Erreur = Servo.PositionMin(Val_ID[i], Val_PosMin[i])
            Erreur = Servo.PositionMax(Val_ID[i], Val_PosMax[i])
            Erreur = Servo.TorqueON(Val_ID[i])

        Val_Etat = [30 for i in range((len(Nom_ID)))]
        Val_Nom_Etat = plc.FusionNomValeur(Nom_Etat, Val_Etat)
        plc.Ecrit_Variable_List(Val_Nom_Etat)

    if Val_Etat[0] == 30:
    #Position Init
        print("Position Init")
        if DoneInfo == False:
            Val_Vitesse = plc.Lit_Variable_List_Int(Nom_Vitesse)

            for i in range(len(Val_ID)):
                Val_PosInit[i] = plc.Lit_Variable(Nom_PosInit[i])
                Val_PosInitStock[i] = Val_PositionReel[i] + Val_PosInit[i]
                print(Val_PosInit[i])
                Erreur = Servo.EcrireVitesse(Val_ID[i], Val_Vitesse[i])
                Erreur = Servo.StockPosition(Val_ID[i], Val_PosInitStock[i])
            DoneInfo = True
        elif DoneInfo == True:
            Val_MoveInit = plc.Lit_Variable(Nom_MoveInit[0])
            print(Val_MoveInit)
            if Val_MoveInit == True:
                Erreur = Servo.MoveSyncro()
                time.sleep(0.1)
                while not MoveInit:
                    for i in range(len(Val_ID)):
                        Erreur, Val_Move[i] = Servo.EnMouvement(Val_ID[i])
                        print(Val_Move[i])
                        Erreur, Val_PositionReel[i] = Servo.LirePosition(Val_ID[i])
                        Erreur, Val_Force[i] = Servo.ForceActuelle(Val_ID[i])
                        plc.Ecrit_Variable(Nom_Movement[i], Val_Move[i])
                        plc.Ecrit_Variable(Nom_PositionReel[i], Val_PositionReel[i])
                        plc.Ecrit_Variable(Nom_Force[i], Val_Force[i])
                    print(Val_Move)
                    if all(val == 0 for val in Val_Move):
                        print("je suis la")
                        MoveInit = True
                        Val_Etat = [35 for i in range((len(Nom_ID)))]
                        Val_Nom_Etat = plc.FusionNomValeur(Nom_Etat, Val_Etat)
                        plc.Ecrit_Variable_List(Val_Nom_Etat)

    if Val_Etat[0] == 35:
    #Homing
        Val_MoveRun[0] = plc.Lit_Variable(Nom_MoveRun[0])
        print("Homing")
        print(Val_MoveRun[0])
        print(AttendRun)
        if AttendRun == True and Val_MoveRun[0] == True:
            time.sleep(0.5)
            Val_Etat = [40 for i in range((len(Nom_ID)))]
            Val_Nom_Etat = plc.FusionNomValeur(Nom_Etat, Val_Etat)
            plc.Ecrit_Variable_List(Val_Nom_Etat)
        elif not AttendRun:
            for i in range(len(Val_ID)):
                Val_HomingONOFF = plc.Lit_Variable(Nom_HomingONOFF[i])
                if i == len(Val_ID) -1:
                    print("Fin Homing")
                    AttendRun = True
                if Val_HomingONOFF == True:
                    Val_HomingBasHaut[i] = plc.Lit_Variable(Nom_HomingBasHaut[i])
                    Val_VitesseHoming[i] = plc.Lit_Variable(Nom_VitesseHoming[i])
                    Val_ForceHoming[i] = plc.Lit_Variable(Nom_ForceHoming[i])
                    Val_PositionApresHoming[i] = plc.Lit_Variable(Nom_PositionApresHoming[i])

                    Erreur, Val_PositionReel[i] = Servo.LirePosition(Val_ID[i])
                    Erreur = Servo.EcrireVitesse(Val_ID[i], Val_VitesseHoming[i])
                    print(Val_PositionReel[i])

                    if Val_HomingBasHaut[i] == 10 or Val_HomingBasHaut[i] == 15:
                        Val_PositionOrdre[i] = Val_PositionReel[i] + 100000
                    elif Val_HomingBasHaut[i] == 20 or Val_HomingBasHaut[i] == 25:
                        Val_PositionOrdre[i] = Val_PositionReel[i] - 100000

                    Erreur = Servo.PositionGoal(Val_ID[i], Val_PositionOrdre[i])

                    while not Val_HomingDone[i]:
                        if Val_HomingBasHaut[i] == 10:
                            Erreur, Val_Force[i] = Servo.ForceActuelle(Val_ID[i])
                            print(Val_Force[i])
                            print(Val_ForceHoming[i])
                            if Val_Force[i] > Val_ForceHoming[i] and not Val_Force[i] > 60000:
                                HomingPosition0 = True
                                print("je suis 10")

                        elif Val_HomingBasHaut[i] == 15:
                            Val_CapteurHoming[i] = plc.Lit_Variable(Nom_CapteurHoming[i])
                            if Val_CapteurHoming[i] == True:
                                HomingPosition0 = True

                        elif Val_HomingBasHaut[i] == 20:
                            Erreur, Val_Force[i] = Servo.ForceActuelle(Val_ID[i])
                            if Val_Force[i] < Val_ForceHoming[i] and not Val_Force[i] < -60000:
                                HomingPosition0 = True
                                print("je suis 20")

                        elif Val_HomingBasHaut[i] == 25:
                            Val_CapteurHoming[i] = plc.Lit_Variable(Nom_CapteurHoming[i])
                            if Val_CapteurHoming[i] == True:
                                HomingPosition0 = True

                        while not Val_HomingDone[i] and HomingPosition0:
                            print("Move Init")
                            Erreur, Val_PositionReel[i] = Servo.LirePosition(Val_ID[i])
                            Val_PositionOrdre[i] = Val_PositionReel[i]
                            Val_PositionHomingMin[i] = Val_PositionReel[i]
                            Erreur = Servo.PositionGoal(Val_ID[i], Val_PositionOrdre[i])
                            if Val_HomingBasHaut[i] == 10 or Val_HomingBasHaut[i] == 15:
                                Val_PositionApresHoming[i] = Val_PositionApresHoming[i] *-1
                            Val_PositionOrdre[i] = Val_PositionReel[i] + Val_PositionApresHoming[i]
                            Erreur = Servo.EcrireVitesse(Val_ID[i], Val_Vitesse[i])
                            Erreur = Servo.PositionGoal(Val_ID[i], Val_PositionOrdre[i])
                            HomingPosition0 = False
                            Val_HomingDone[i] = True
                            plc.Ecrit_Variable(Nom_Position0[i], Val_PositionHomingMin[i])
                            plc.Ecrit_Variable(Nom_HomingDone[i], Val_HomingDone[i])

    if Val_Etat[0] == 40:
    #Mode Run
        Nom_List_to_Read = Nom_Prioritaire + Nom_Vitesse + Nom_PositionOrdre + Nom_ForceMax + Nom_ForceMaxAntihoraire + Nom_ForceDepassee + Nom_Force
        Val_Read = plc.Lit_Variable_List_Int(Nom_List_to_Read)

        Val_Prioritaire = Val_Read[0:len(Nom_ID)]
        Val_Vitesse = Val_Read[len(Nom_ID):(len(Nom_ID)*2)]
        Val_PositionOrdre = Val_Read[(len(Nom_ID)*2):(len(Nom_ID)*3)]
        Val_ForceMax = Val_Read[(len(Nom_ID)*3):(len(Nom_ID)*4)]
        Val_ForceMaxAntihoraire = Val_Read[(len(Nom_ID)*4):(len(Nom_ID)*5)]
        Val_ForceDepassee = Val_Read[(len(Nom_ID)*5):(len(Nom_ID)*6)]
        Val_Force = Val_Read[(len(Nom_ID)*6):(len(Nom_ID)*7)]

        PosArret = [0 for i in range(len(Nom_ID))]
        CoupleDepasse = [False for i in range(len(Nom_ID))]

        #On connait les info importantes on fait quelques chose en fonction des datas qu'�n recoit
        for i in range(len(Val_ID)):
            if abs(Val_PositionOrdre[i] - Val_PositionActuelle[i])>50 or Val_PositionOrdre[i] != Val_PositionOrdrePrecedent[i] or Val_PositionOrdre[i] != Val_PositionOrdrePrecedent_2[i] or Val_Move[i] == True or Val_MovePrecedent[i] == True or Val_Prioritaire[i] == 1:
                if Val_Vitesse[i] != Val_VitessePrecedent[i]:
                    Erreur = Servo.EcrireVitesse(Val_ID[i], Val_Vitesse[i])

                Erreur = Servo.PositionGoal(Val_ID[i], Val_PositionOrdre[i] + Val_PositionHomingMin[i])

                Erreur, Val_PositionReel[i] = Servo.LirePosition(Val_ID[i])
                Erreur, Val_Move[i] = Servo.EnMouvement(Val_ID[i])
                Erreur, Val_Force[i] = Servo.ForceActuelle(Val_ID[i])

                Val_PositionOrdrePrecedent_2[i] = Val_PositionOrdrePrecedent[i]
                Val_PositionOrdrePrecedent[i] = Val_PositionOrdre[i]
                Val_VitessePrecedent[i] != Val_Vitesse[i]
                Val_PositionActuelle[i] = Val_PositionReel[i] - Val_PositionHomingMin[i]

                print(f"Servo {Val_ID[i]} position actuelle {Val_PositionActuelle[i]} position ordre {Val_PositionOrdre[i]} différence {abs(Val_PositionOrdre[i] - Val_PositionActuelle[i])} force {Val_Force[i]}")

                if ((((Val_ForceMaxAntihoraire[i] == 0 and abs(Val_Force[i]) > abs (Val_ForceMax[i])) or (Val_ForceMaxAntihoraire[i] != 0 and ((Val_Force[i] < 0 and abs(Val_Force[i]) > abs(Val_ForceMaxAntihoraire[i])) or (Val_Force[i] > 0 and abs (Val_Force[i]) > abs(Val_ForceMax[i]))))) and Val_NbCycle[i] >= 4) or ((Val_ForceMaxAntihoraire[i] == 0 and abs(Val_Force[i]) > abs (Val_ForceMax[i] +200)) or (Val_ForceMaxAntihoraire[i] != 0 and ((Val_Force[i] < 0 and abs(Val_Force[i]) > abs(Val_ForceMaxAntihoraire[i] +200)) or (Val_Force[i] > 0 and abs (Val_Force[i]) > abs(Val_ForceMax[i] +200))))) or (abs(Val_Force[i]) > 990)) and Val_ForceMax[i] != 0 and Val_ForceDepassee[i] != 0:
                    print("couple dépassé")
                    print(f"Servo {Val_ID[i]} Force {Val_Force[i]} / force max : {Val_ForceMax[i]} ou {Val_ForceMaxAntihoraire[i]} ForceDepassee {Val_ForceDepassee[i]}")
                    Val_NbCycle[i] = 0
                    CoupleDepasse[i] = True
                    Val_Etat = [70 for i in range((len(Nom_ID)))]
                    Val_Nom_Etat = plc.FusionNomValeur(Nom_Etat, Val_Etat)
                    plc.Ecrit_Variable_List(Val_Nom_Etat)
                    for i in range(len(Val_ID)):
                        Erreur, Val_PositionReel[i] = Servo.LirePosition(Val_ID[i])
                        Erreur = Servo.PositionGoal(Val_ID[i], Val_PositionReel[i])
                        PosArret[i] = Val_PositionReel[i]
                    break

                Val_NbCycle[i] = Val_NbCycle[i] +1
            else :
                Val_NbCycle[i] = 0

            Val_MovePrecedent[i] = Val_Move[i]


        for i in range(len(Val_ID)):
            ListNomSend = Nom_Movement + Nom_PositionReel + Nom_Force + Nom_PositionActuelle
            ListValeurSend = Val_Move + Val_PositionReel + Val_Force + Val_PositionActuelle

        ListFusionSend = plc.FusionNomValeur(ListNomSend, ListValeurSend)
        plc.Ecrit_Variable_List(ListFusionSend)

    if Val_Etat[0] == 50:
    #Mode Stop/Erreur
        print("Stop/Erreur")
        if Erreur == True:
            CodeErreur = [10 for i in range((len(Nom_ID)))]
            Val_Nom_CodeErreur = plc.FusionNomValeur(Nom_CodeErreur, CodeErreur)
            plc.Ecrit_Variable_List(Val_Nom_CodeErreur)
        while Val_Etat[0] == 50 :
            Val_Etat = plc.Lit_Variable_List_Int(Nom_Etat)

    if Val_Etat[0] == 60:
    #Mode Fin Match
        print("Fin du Match")
        Servo.TorqueOFF(100)
        Servo.FermeturePort()

    if Val_Etat[0] == 70:
    #Couple dépassé
        for i in range(len(Val_ID)):
                Val_ForceDepassee[i] = plc.Lit_Variable(Nom_ForceDepassee[i])
                Val_MarcheArriere[i] = plc.Lit_Variable(Nom_MarcheArriere[i])
                Erreur, Val_PositionReel[i] = Servo.LirePosition(Val_ID[i])

                if CoupleDepasse[i]:
                    if Val_ForceDepassee[i] == 1:
                       print(f"Servo {Val_ID[i]} arrêté")
                       Val_Etat = [50 for i in range(len(Nom_ID))]
                       Val_Nom_Etat = plc.FusionNomValeur(Nom_Etat, Val_Etat)
                       plc.Ecrit_Variable_List(Val_Nom_Etat)

                    elif Val_ForceDepassee[i] == 2 or Val_ForceDepassee[i] == 3:
                       Val_PositionOrdre[i] = PosArret[i] - Val_MarcheArriere[i]
                       Erreur = Servo.PositionGoal(Val_ID[i], Val_PositionOrdre[i])
                       if Val_PositionReel[i] < Val_PositionOrdre[i] +20 and Val_PositionReel[i] > Val_PositionOrdre[i] -20 :
                            print(f"Servo {Val_ID[i]} Retour")
                            if Val_ForceDepassee[i] == 2:
                                Val_Etat = [40 for i in range(len(Nom_ID))]
                                Val_Nom_Etat = plc.FusionNomValeur(Nom_Etat, Val_Etat)
                                plc.Ecrit_Variable_List(Val_Nom_Etat)
                            elif Val_ForceDepassee[i] == 3:
                                Val_Etat = [50 for i in range(len(Nom_ID))]
                                Val_Nom_Etat = plc.FusionNomValeur(Nom_Etat, Val_Etat)
                                plc.Ecrit_Variable_List(Val_Nom_Etat)

                    elif Val_ForceDepassee[i] == 4 or Val_ForceDepassee[i] == 5:
                        for U in range(20):
                            if Compteur == 0:
                                Erreur = Servo.EcrireVitesse(Val_ID[i], 0)

                            Val_PositionOrdre[i] = PosArret[i] -100
                            Erreur = Servo.PositionGoal(Val_ID[i], Val_PositionOrdre[i])
                            time.sleep(0.03)
                            Val_PositionOrdre[i] = PosArret[i]
                            Erreur = Servo.PositionGoal(Val_ID[i], Val_PositionOrdre[i])
                            time.sleep(0.03)
                            Compteur += 1

                            if Compteur >= 20:
                                if Val_ForceDepassee[i] == 4:
                                    Val_Etat = [40 for i in range(len(Nom_ID))]
                                    Val_Nom_Etat = plc.FusionNomValeur(Nom_Etat, Val_Etat)
                                    plc.Ecrit_Variable_List(Val_Nom_Etat)
                                elif Val_ForceDepassee[i] == 5:
                                    Val_Etat = [50 for i in range(len(Nom_ID))]
                                    Val_Nom_Etat = plc.FusionNomValeur(Nom_Etat, Val_Etat)
                                    plc.Ecrit_Variable_List(Val_Nom_Etat)
                                Erreur = Servo.EcrireVitesse(Val_ID[i], Val_Vitesse[i])
                                Compteur = 0
                                break
    iCompteurTest = iCompteurTest +1
    #print (f"cycle : {iCompteurTest}")
else:
    print("c�est rater")
