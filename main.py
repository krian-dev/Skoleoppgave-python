import django
import string
Spiller = input("Hva skal du hete?")

poeng = 0
print ("Kan meldinger føles?")


svar = {"Bare i bølger" : 0, 
        "Nei" : 1, 
        "Ja" : 0, 
        "Alltid hvis den ikke er i bølger" : 0,
        }
print(svar)

for i in range (len(svar)):
    #print ("%s) %s" % (string.ascii_uppercase[i], list(svar.keys())[i]))
    print(string.ascii_uppercase[i] + ") " + list(svar.keys())[i])



svaret_ditt = input("Hva tror du? ")

svaret_ditt = (string.ascii_uppercase.index(svaret_ditt))
svaret_ditt = list(svar.keys())[svaret_ditt]



if svar[svaret_ditt] == 1:
    print (" Bra jobba, du fikk rett")
    poeng = poeng + 1
else:
    print (" Du fikk feil")



