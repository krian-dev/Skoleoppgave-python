# Programmeringslogg selvstednig oppgave

## 1.02.2023 på skole
Dette her var første time, det var da jeg skulle finne ut hva jeg skulle lage og hvordan jeg skulle det. Jeg kom fram til at jeg skulle lage noe som gikk over internett og at det skulle være et quiz spill. Jeg sjekket med metoder jeg kunne utnytte for å kunne **"hoste"** og **"reade"** en server output, jeg kom fram til at jeg kunne bruke et allerede lagt up framework kalt ***Django Framework*** eller at jeg kan bruke python sin innebyggde socket funksjon. 

## 1.02.2023 hjemme
Her jobbet jeg litt hjemme også lastet jeg ned en eksperimentell versjon av ***Django Framework*** på en annen PC og testet rundt med dette da jeg fikk et script til å kjørers på en lokal nettside. Dette gjorde jeg ved
```shell
test@hjemmelaptop:~$ django-admin startproject mysite
```
Dette lagde dette her under i filbanen jeg spesifiserte. Dette her er ***"root directory"*** som funker som en kontainer, ingenting jeg gjør utenom denne filbanen har noen betydning og den kan ikke hente filer utenfor siden den ikke vet om det.

```file
mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```


***manage.py*** er et kommandlinje verktøy som lar deg handle og endre på prosjektet på flere måter. Du kan lese detaljene på <a href ="https://docs.djangoproject.com/en/4.1/ref/django-admin/"> django-admin and manage.py </a>

Den indre ***mysite/*** mappen er den faktiske python pakken til prosjektet. Navnet på denne er python pakken du må bruke når du skal importere noe (e.g. ***mysite.urls***).

***mysite/__init__.py*** er en tom fil som forteller pyhton at denne filbanen skal behandles som en python pakke. Du kan lese mer på <a href ="https://docs.python.org/3/tutorial/modules.html#tut-packages"> denne tutorialen om python moduler </a>

***mysite/settings.py*** er URL deklarasjonen for prosjektet. Du kan lese me om URL-er på <a href ="https://docs.djangoproject.com/en/4.1/topics/http/urls/"> URL dispatcher siden til Django </a>

***mysite/asgi.py*** er inngangspunktet for ASGI-kompatible web servere som kan lese av ting til prosjektet. Les mer på <a href ="https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/"> ASGI browsers </a>

***mysite/wsgi.py*** er inngangspunktet for WSGI-kompatible web servere som kan lese av ting til prosjektet Les mer på <a href ="https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/"> WSGI browsers </a>

#### HER FORKLARTE JEG BARE VELDIG LETT MED BRUK AV EGEN ORD, HVIS DU VIL LESE DJANGO SINE EGENE FORKLARINGER PÅ DU SE PÅ
<a href ="https://docs.djangoproject.com/en/4.1/ref/django-admin/#django-admin-runserver"> Django-admin and runserver </a>

<br>

Etter dette kjørte jeg

```shell
test@hjemmelaptop:~$ python manage.py runserver
```

Da startet jeg serveren på ***"loopback-IP-en "127.0.0.1"***
Da fikk en gratulerer nettside av Django som kjører siden ***debug=0*** og ***runserver=1*** i debug filen. <br>
Bildet*1 i vedlagt fil.

Deretter kjørte jeg 
```shell
test@hjemmelaptop:~$ python manage.py startapp polls
```
<br> 
Dette lagde mappen kalt polls som er lagt opp slik.


```file
polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```

Deretter satt jeg veiws.py til 

```python
from django.http import HttpResponse


def index(request):
    return HttpResponse("Dette er en test")
```

Også lagde jeg en fil ***urls.py*** som jeg la i samme mappe, da så filbanen slik ut

```file
polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
    urls.py
```

Der skrev jeg dette slik at som peker veien som den skal finne ***views.py*** i.

```py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

Neste jeg gjorde var å peke URLconf på ***polls.url*** modulen. Så da la jeg til en import for ***django.urls.include*** og la til en ***include()*** i ***urlpatterns*** listen under ***mysite/urls.py***

```py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```
***include()*** er en funksjon som lar meg refere til andre URLconfigs. Når django møter en ***include()*** kutter den av hvilken del av URL-en som matcher opp til det punktet og sender restern av stringen til den inkluderte URLconfigen.

Når jeg da var ved **indexen** til veiwen testet jeg ved å kjøre 
```shell
test@hjemmelaptop:~$ python manage.py runserver
```

Når jeg da sjekket 127.0.0.1/polls
Fikk jeg "Hello, world. You're at the polls index". Noe som visste meg at det funka. 
***path()*** er en funksjon som kan ha 4 argumenter og trenger 2; **route** og **view**.
***route*** er en string som inneholder et URL mønster som når blir behandlet spørr Django ved den første mønsteret i **urlpatterns** and jobber seg neddover til den finner en som matcher.
***view*** når django finner et matchende mønster, ber den om den spesifiserte view funksjonen med en **"HttpRequest"** til det første argumententet eller verdien fra **route**.


## 8.02.2023 på skole
Jeg visste nå hvordan Django-Framework funket og hvordan python sine sockets funket og fant ut at til denne oppgaven var det mest egnet å bruke sockets slik at jeg slipper å skrive JavaScript til FrontEnd og hele spillet kan spilles i et shell rent back-end. Det jeg gjorde her var å skrive Kommando scriptet til spillet slik at jeg hadde et spill som funket lokalt. Jeg startet med å lage en ***"dictionary"*** med alle svarene som hadde en ***"token"*** som sa hvilket svar som var rett

```py
svar = {"Svaralternativ1  " : 0, 
        "Svaralternativ2  " : 1, 
        "Svaralternativ3  " : 0, 
        "Svaralternativ4  " : 0,
        }
```
Som du ser her sier den at ***"svaraleernativ2"*** er rett siden den har en token av 1.

Etter dette lagde jeg scriptet som skulle printe svaralterativene og nummerere de med en bokstav. Dette gjorde jeg ved å finne lengden av ***"dictionary-en"*** og printe svaralterativene sammen med en annen liste av alfabetet. 

```python
for i in range (len(svar)):
    print ("%s) %s" % (string.ascii_uppercase[i], list(svar.keys())[i]))
```

Deretter lagde jeg scriptet som finner ut hva du valgte og hvorfor "B = Svaralternativ2" f.eks.

```py
svaret_ditt = input("Hva tror du? ")

svaret_ditt = (string.ascii_uppercase.index(svaret_ditt))
svaret_ditt = list(svar.keys())[svaret_ditt]

```

Deretter må den jo finne ut om svaret ditt er riktig og for å gjøre det lagde jeg dette scriptet.

```py
if svar[svaret_ditt] == 1:
    print (" Bra jobba, du fikk rett")
    poeng = poeng + 1
else:
    print (" Du fikk feil")
print ("Du har",poeng, "poeng")
```
Da hadde jeg lokal koden til spillet som funket veldig greit (med et litt dumt teste spørsmål). Dette er det som er "main.py" i blant filene jeg sendte. 

## 8.02.2023 på skole
Denne gangen gjorde jeg nesten ingenting, grunnen til dette er at jeg hadde lagd alt dette her på Hjemmelaptopen som jeg ikke trudde at jeg kunne ta med på skolen, det jeg gjorde denne timen. Jeg leste også denne artikkelen/guiden <a href ="https://realpython.com/python-sockets/#application-client-and-server"> Python sockets client and server </a>.

## 15.02.2023 på skole
Denne timen gjorde jeg også lite, jeg lastet ned **Django-framework** på skole-pcen dette gjorde så jeg begynte og sette opp ting på nytt på denne helt til noen deler ble ødelagt og jeg måtte begynne på nytt hvor jeg tror at jeg bare innså at jeg måtte ta med Hjemme-pcen slik at jeg kunne lage ting der. 

## 15.02.2023 hjemme
Her jobbet jeg hjemme og øvde meg med Sockets, jeg har lagt til 3 filer som jeg alle skrev bare for å lære meg hvordan sockets funket. Dette var veldig grunnelegende. Bare slik at jeg vet hvordan en klient kommuniserer med en server. Jeg kan forklare de enkleste linjene her i testen jeg lagde selv ut i fra guiden her. 

```py
import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 1338 # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
```
Alt dette her bare setter opp en socket på **localhost** som er den "interne IP-en" til PCen din. Du kan koble deg til denne ved bruk av Telnet og spesifisere port så får du output i et konsoll vindu. 

```py
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            conn.sendall(b'What is your name? ')

            data = conn.recv(1024)
            data_wo_newline = data.decode("ascii").split("\n")[0].strip("\r")
```
Denne delen sier bare at den skal akseptere alt som prøver å koble seg til og at når noe kobler seg til skal den skrive at du koblet deg til på serveren og sende til alle tilkoblinger (som maks kan være 1 akkuratt nå siden jeg ikke tilatter multithreading) "What is your name?". den setter en variabel "data" som sier at den skal motta 1024 bytes per update og at den skal lage en nå linje i ascii som bare er en samling av tegn til en datamaskin. 

```py
            print("User: %r connected" % data_wo_newline)
            
            resp = "Welcome " + data_wo_newline + "! Welcome to my super awsm quiz master game of all times in this time!"
            conn.sendall(bytes(resp, "UTF-8"))
```
Denne siste delen sier at serveren skal skrive hvem som koblet seg til å svare med "Welcome "player"! Welcome to my super awsm quiz master game of all times in this time!" i UTF-8 som er et nyere sett med tegn og skrift til datamaskiner som jeg bare ville teste meg fram med. 

# 23.02.2023 Vinterferie!
<br />
<br />[Programmeringslogg.md](https://github.com/krian-dev/Skoleoppgave-python/files/10995050/Programmeringslogg.md)

## 30.02.2023 på skole
