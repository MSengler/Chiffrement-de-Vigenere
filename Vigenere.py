#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from ui_fenetre import Ui_Fenetre


m="om"
alphabet=[ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k','l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
cle=[]

# Exemple de texte à chiffrer
texte="lesfacteurspremiersdunombredecaractresentredeuxdbutsdesquencesfigurentdansletableauexxilapparatdansletableauquetouteslespriodessontdivisiblespartoutsecaleparfaitementsurunmotclefdelettresuneautremthodepourtrouverlalongueurdelaclefutiliselindicedeconcidenceunefoislalongueurdelacleftrouveonpeutdcouperletexteenautantdesoustextesdanslecasprsentchacundentreeuxtantobtenuparunmmechiffredecsaretpeuttredcryptparanalysedefrquenceschaquetextektantlasuitedeslettresquisontlapositionkmodulolacomparaisonentrelesdistributionsdeslettresdanschacundessoustextesonpeututiliserunindicedeconcidencedfinientredeuxdistributionspermetdedcouvrirlesdcalagesentreleslettresdumotclefetfacilitelarsolution"

def enlevecaractere(a):#enlève les majuscules, espaces, accents, caractères autres que des lettres
    i=len(a)-1
    b=a.lower()
    while i>=0:
        if ord(b[i])==224:
            b=b[0:i]+chr(97)+b[i+1:]
        if ord(b[i])==231:
            b=b[0:i]+chr(99)+b[i+1:]
        if 232<=ord(b[i])<=234:
            b=b[0:i]+chr(101)+b[i+1:]
        if ord(b[i])==244 or ord(b[i])==246:
            b=b[0:i]+chr(111)+b[i+1:]
        if ord(b[i])==249 or ord(a[i])==251:
            b=b[0:i]+chr(117)+b[i+1:]
        elif ord(b[i])>123 or 97>ord(b[i]):
            b=b[0:i]+b[i+1:]
        i=i-1
    return b

def divise2(a,k):
    l=['' for i in range(k)]
    n=len(a)
    for j in range(k):
        for i in range(j,n,k):
            l[j]=l[j]+a[i]
    return l

def indicedeconcidence(c):
    n=len(c)
    l=[0 for i in range(25)]
    for j in range (25):
         for k in range (n):
            if c[k]==alphabet[j]:
                l[j]=l[j]+1
    Ic=0
    n=len(c)
    if n!=0 and n!=1:
        for i in range (25):
            Ic=Ic+l[i]*(l[i]-1)/(n**2-n)
        return Ic
    else:
        return 0

def valeurplusproche(x,l):
    n=len(l)
    d=0
    p=l[0]
    for i in range(1,n):
        m=abs(x-p)
        b=abs(x-l[i])
        if m>b:
            p=l[i]
            d=i
    return d

def diviseur(n):
    l=[]
    for i in range(1,n):
        p=n%i
        if p==0:
            l.append(i)
    return l

def longueurcle(c): #on a choisit de limiter à une longueur de clé de 11
    n=len(c)
    l=[]
    for j in range(1,12):
        l2=divise2(c,j)
        ic=0
        for k in range (len(l2)):
            ic=ic+indicedeconcidence(l2[k])/len(l2)
        l.append(ic)
    d=valeurplusproche(0.0778,l)+1
    div=diviseur(d)
    for i in range(len(div)):
        if abs(l[div[i]-1]-l[d-1])<0.005:
            d=div[i]
            break
    return d

def max(f):
    max=0
    for i in range(len(f)):
        if f[i]>f[max]:
            max=i
    return max

def decalagerelatif2(c):#la lettre e est la lettre la plus fréquente en français
    f1=[0 for i in range(25)]
    n1=len(c)
    for j in range (25):
        for k in range (n1):
            if c[k]==alphabet[j]:
                f1[j]=f1[j]+1
    cle.append(max(f1)-4)
    return [c,-max(f1)+4]

def decale2(a,dr):
    for k in range (len(a)):
        d=ord(a[k])+dr
        if d>=123:
            d=97+(d-123)
        if d<=96:
            d=123+(d-97)
        a=a[0:k]+chr(d)+a[k+1:]
    return a

def replace2(l):
    a=[''for i in range(26)]
    n=len(l)
    for j in range(26):
        for m in range(len(l[n-1][1])):
            for i in range(n):
                a[j]=a[j][:]+l[i][j][m]
        b=''
        for p in range (n-1,-1,-1):
            k=len(l[p-1][1])
            i=0
            c=''
            while k<len(l[i][1]):
                c=c[:]+l[i][j][k]
                i=i+1
            b=c[:]+b[:]
        a[j]=a[j][:]+b[:]
    return a

def replace(l):
    a=''
    n=len(l)
    for j in range(len(l[n-1])):
        for i in range(n):
            a=a[:]+l[i][j]
    b=''
    for j in range (n-1,-1,-1):
        k=len(l[j-1])
        i=0
        c=''
        while k<len(l[i]):
            c=c[:]+l[i][k]
            i=i+1
        b=c[:]+b[:]
    a=a[:]+b[:]
    return a

def remettrecaractere(a,b):
    for i in range(len(a)):
        if 64<ord(a[i])<91:
            b=b[0:i]+b[i:]
        if 230<ord(a[i])<235 or ord(a[i])==224 or ord(a[i])==249 or ord(a[i])==251 :
            b=b[0:i]+b[i:]
        elif ord(a[i])>123 or 90<ord(a[i])<96 or ord(a[i])<65:
            b=b[0:i]+a[i]+b[i:]
    return b



class Main(QMainWindow, Ui_Fenetre):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.textecode=""
        self.textedecode=""
        #self.pushButton_Decodage.setEnabled(False)



    def codeVigenere(self,a,m):
        a=enlevecaractere(a)
        m=((len(a)//len(m))+1)*m
        for i in range (0,len(a)):
            if ord(a[i])>123 or 97>ord(a[i]):
                d=ord(a[i])
            else:
                d=ord(a[i])+ord(m[i])-97
                if d>=123:
                    d=97+(d-123)
            a=a[0:i]+chr(d)+a[i+1:]
        return a


    def decode(self,j):
        c=enlevecaractere(j)
        d=longueurcle(c)
        l=divise2(c,d)
        b=[]
        for i in range(len(l)):
            b.append(decalagerelatif2(l[i]))
            l[i]=decale2(b[i][0],b[i][1])
        cle=''
        lettre=[ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k','l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        for i in range(len(b)):
            bi=abs(b[i][1])
            cle=cle+lettre[bi]
        return [replace(l),cle]


    def codage(self):
        a,b= self.lineEditcode.text() , self.lineEditcle.text()
        #self.textecode=self.codeVigenere(a,b)
        self.textecode=remettrecaractere(a,self.codeVigenere(a,b))
        #self.pushButton_Decodage.setEnabled(True)
        self.lineEditcode.setText(self.textecode)
        print(self.textecode)


    def decodage(self):
        b= self.lineEditdecode.text()
        self.textedecode=self.decode(b)
        self.lineEditdecode.setText(remettrecaractere(self.textecode,self.textedecode[0]))
        self.lineEditcle.setText(self.textedecode[1])
        print(self.textedecode)

    def effacer(self):
        self.lineEditcode.setText("")
        self.lineEditdecode.setText("")
        self.lineEditcle.setText("")


app = QApplication(sys.argv)

main = Main()
main.show()

app.exec()
