# EHeguraldia
Euskal Herriko eguraldia jaisteko tresna. Kodea Wikipediako (https://eu.wikipedia.org/wiki/Wikiproiektu:Informatika#Eguraldia._Datu_meteorologikoak) proiektuaren parte da, kode honen egileak Xabier Irastorza eta Paula Ontalvilla dira.


## Nafarroako eguraldia jaisteko
Estazio manualak jaisteko *kode* karpetako ```mainAUT.py``` eta ```mainMAN.py``` fitxategiak daude bakoitzak estazio automatikoak eta manualak jaisten dituztelarik, hurrenez hurren. Horien emaitza **ESTAZAIO AUTOMATIKOAK** eta  **ESTAZAIO MANUALAK** karpetetan gordetzen dira _json_ formatuan.

#### **KONTUZ!!!**
Ancín intia estazio automatikoan kode aldatu behar da.  ``years = [str(i) for i in range(1880, 2022)]`` lerroan hurrengoa jarriz: ``years = [str(i) for i in range(2015, 2022)]``


## Gipuzkoa/Bizkaia/Arabakoa eguraldia jaisteko
**Ezarpena** karpeta ``WikiEguraldia.py`` fitxategiaren _path_ berdinean egon behar da bertan emaitzak gordeko baitira. 


## Wikipediara igotzeko pausuak
json guztiak .txt batean jarri bakoitza xxx eta yyy bidez bereiztua dagoela. [Pywikibot](https://www.mediawiki.org/wiki/Manual:Pywikibot/Installation) deskargatu eta ondoren terminalean:
```
python3 ~/pywikibot/pwb.py pagefromfile -file:name.txt -begin:xxx -end:yyy -notitle  -summary:"message" -force
```


