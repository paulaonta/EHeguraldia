# EHeguraldia
Euskal Herriko eguraldia (momentuz Nafarroa) jaisteko tresna

## Wikipediara igotzeko pausuak
json guztiak .txt batean jarri bakoitza xxx eta yyy bidez bereiztua dagoela. [Pywikibot](https://www.mediawiki.org/wiki/Manual:Pywikibot/Installation) deskargatu eta ondoren terminalean:
```
python3 ~/pywikibot/pwb.py pagefromfile -file:name.txt -begin:xxx -end:yyy -notitle  -summary:"message" -force
```
