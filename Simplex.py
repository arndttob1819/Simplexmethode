import copy
"""
Zielfunktion ZF: bis zu neun Variablen, Koeffizienten angeben und max/min
Restriktionen Ri: bis zu neun Gleichungen, jeweils Koeffizienten angeben in der Form: X >= A * x1 + B * x2 + ...
Nichtnegativität ist gefordert.
"""

def ZF(mode, X, Koeff):
    """
    mode == 0 für minimieren
    mode == 1 für maximieren
    """
    ZF = [mode]+[X]+[Koeff[i] for i in range(len(Koeff))]
    return ZF

def RS(Rechnung, X, Koeff):
    """
    Rechnung == 0 für gleichheit
    Rechnung == 1 für größer gleich
    Rechnung == -1 für kleiner gleich
    """
    RS = [Rechnung]+[X]+[Koeff[i] for i in range(len(Koeff))]
    return RS

def Tabelle(ZF = [0, 0], R1 = [0,0], R2 = [0,0], R3 = [0,0], R4 = [0,0], R5 = [0,0], R6 = [0,0], R7 = [0,0], R8 = [0,0], R9 = [0,0]):
    Tab = [[] for i in range(12)]
    Tab[0] = ZF
    Tab[1] = R1
    Tab[2] = R2
    Tab[3] = R3
    Tab[4] = R4
    Tab[5] = R5
    Tab[6] = R6
    Tab[7] = R7
    Tab[8] = R8
    Tab[9] = R9
    Tab[10] = ["x"+str(i) for i in range(1,10)]
    Tab[11] = ["u"+str(i) for i in range(1,10)]
    if ZF[0] == 0:
        NewTab = copy.deepcopy(Tab)
        for n in range(1,10):
            for m in range(n-1, len(Tab[n])):
                if Tab[m] == [0,0]:
                    pass
                else:
                    if len(Tab[n])-1>m:
                        NewTab[m][n], NewTab[n-1][m+1] = Tab[n-1][m+1], Tab[m][n]
                    else:
                        try:
                            NewTab[n-1].append(Tab[m][n])
                            NewTab[m][n] = 0
                        except IndexError:
                            pass
        for i in range(1,10):
            if checkZero(NewTab[i][1:]):
                NewTab[i] = [0,0]
        Tab = copy.deepcopy(NewTab)
    for i in range(2,len(Tab[0])):
        Tab[0][i] = -1*Tab[0][i]
    return Tab

def checkZero(liste):
    for i in liste:
        if i !=0:
            return False
    return True

def showTabelle(Tab):
    print("")
    """
    Erstellen der Kopfzeile
    """
    Kopfzeile = "            "
    for i in range(len(Tab[-2])):
        Kopfzeile += "            " + Tab[-2][i]
    print(Kopfzeile)
    """
    Erstellen der Zielfunktionszeile
    """
    Zeile = ""
    for i in range(1, len(Tab[0])):
        Zeile +=auffuellen(14-len(str(round(Tab[0][i],2))))+str(round(Tab[0][i],2))
    print(Zeile)
    """
    Erstellen der Rechenzeilen
    """    
    for i in range(1,10):
        if Tab[i] == [0, 0]:
            pass
        else:
            Zeile = Tab[-1][i-1]
            for j in range(1, len(Tab[i])):
                if j == 1:
                    Zeile +=auffuellen(12-len(str(round(Tab[i][j],2))))+str(round(Tab[i][j],2))
                else:
                    Zeile +=auffuellen(14-len(str(round(Tab[i][j],2))))+str(round(Tab[i][j],2))
            print(Zeile)
    print("")
    return

def auffuellen(n):
    zeile = ""
    for i in range(n):
        zeile += " "
    return zeile

def pivotspalte(Tab):
    """
    Wählen der Pivotspalte
    """
    spalte = []
    for i in range(len(Tab[0])-2):
        if Tab[0][2+i]<0:
            spalte.append([Tab[0][2+i], 2+i])
    if spalte != []:
        PS = maximum(spalte)
        return PS
  
def pivotzeile(Tab, PS):
    """
    Wählen der Pivotzeile
    """
    zeile = []
    for i in range(1, 10):
        if Tab[i] == [0,0]:
            pass
        else:
            try:
                
                zeile.append([(Tab[i][1]/Tab[i][PS]),i])
                #print([(Tab[i][1]/Tab[i][PS]),i])
            except ZeroDivisionError:
                pass
    if zeile != []:
        if minimum(zeile)==-1:
            return -1
        PZ = minimum(zeile)
        return PZ

def maximum(liste):
    zahl = 0
    for i in range(len(liste)):
        if liste[i][0]>=0:
            pass
        else:
            if zahl<abs(liste[i][0]):
                zahl = abs(liste[i][0])
                k = liste[i][1]
    return k

def minimum(liste):
    zahl = float("inf")
    k = -1
    for i in range(len(liste)):
        if liste[i][0]<=0:
            pass
        else:
            if zahl>liste[i][0]:
                zahl = abs(liste[i][0])
                k = liste[i][1]
    return k

def simplex(Tab, PZ, PS):
    if PZ == -1:
        return -1 
    Pivot = Tab[PZ][PS]
    print(PZ,PS,Pivot)
    NewTab = copy.deepcopy(Tab)
    for i in range(0,10):
        if NewTab[i] == [0,0]:
            pass
        else:
            for j in range(1, len(NewTab[i])):
                
                if i == PZ and j == PS:
                    #print("Pivotelement")
                    NewTab[i][j] = 1/Pivot
                elif i == PZ:
                    #print("Pivotzeile")
                    NewTab[i][j] = Tab[i][j]/Pivot
                elif j == PS:
                    #print("Pivotspalte")
                    NewTab[i][j] = -1*Tab[i][j]/Pivot
                else:
                    #print("Kreuzregel")
                    #print(Tab[i][j], " - ",Tab[i][PS], " * ",Tab[PZ][j], " / ", Pivot, " = ",  Tab[i][j] - ((Tab[i][PS]*Tab[PZ][j])/Pivot))
                    NewTab[i][j] = Tab[i][j] - ((Tab[i][PS]*Tab[PZ][j])/Pivot)
                    
    temp = NewTab[-2][PS-2]
    NewTab[-2][PS-2] = NewTab[-1][PZ-1]
    NewTab[-1][PZ-1] = temp
    return NewTab        

def iteration(Tab):
    showTabelle(Tab)
    while 1:
        k = 0
        for i in range(1,len(Tab[0])):
            if k == 0:
                if Tab[0][i]<0:
                    PS = pivotspalte(Tab)
                    PZ = pivotzeile(Tab, PS)
                    Tab = simplex(Tab, PZ, PS)
                    if Tab == -1:
                        return
                    showTabelle(Tab)
                    k = 1
        if k == 0:
            return Tab
                
            
       
        
################# Test
ZF = ZF(1, 0, [2,0,-3, 5])
R1 = RS(-1, 1, [0,-1,3,0])
R2 = RS(-1, 5, [2,1,0,-2])
R3 = RS(-1, 2, [3,0,-3,1])
Tab = Tabelle(ZF, R1, R2, R3)

iteration(Tab)
#hello world
