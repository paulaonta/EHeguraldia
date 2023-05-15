# EHeguraldia
Euskal Herriko eguraldia jaisteko tresna. Kodea Wikipediako (https://eu.wikipedia.org/wiki/Wikiproiektu:Informatika#Eguraldia._Datu_meteorologikoak) proiektuaren parte da, kode honen egileak Xabier Irastorza eta Paula Ontalvilla dira.


## Nafarroako eguraldia jaisteko
Estazio manualak jaisteko *kode* karpetako 



## Wikipediara igotzeko pausuak
json guztiak .txt batean jarri bakoitza xxx eta yyy bidez bereiztua dagoela. [Pywikibot](https://www.mediawiki.org/wiki/Manual:Pywikibot/Installation) deskargatu eta ondoren terminalean:
```
python3 ~/pywikibot/pwb.py pagefromfile -file:name.txt -begin:xxx -end:yyy -notitle  -summary:"message" -force
```


