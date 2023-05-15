##INPORTAZIOAK
import xml.etree.ElementTree as ET
import os
import datetime
import json
import math
import pandas as pd
from tqdm import tqdm

#################### 1. FASETIK ERABILTZEN DIREN FUNTZIOAK ####################

#Fasearen irteera utziko den tokia prestatzen du. Irteera helbidea itzultzen du.
def sortuInguruneEgokia (karpetaIzena): 
    kont=0 #Karpetaren izena errepikatuta badago bereizteko zenbakia.
    while True: #Izen ezberdineko karpeta bat sortu arte
        try: #Saiatu
            if (kont == 0): #Lehen saiakera bada, eskatutako izenarekin saiatu 
                os.mkdir(karpetaIzena)
                azken_izena=karpetaIzena
            else: #Bestela
                os.mkdir(karpetaIzena+"_"+str(kont)) #Izen artifizial batekin saiatu
                azken_izena=karpetaIzena+"_"+str(kont)
            break
        except FileExistsError:
            kont+=1 
    return azken_izena

#Sarrera gisa sartzen zaion helbidean kokatzen diren fitxategien eta horko azpikarpeten fitxategien bide-izen guztiak itzultzen ditu. Sarreran, gainera, kontuan hartzea nahi den fitxategi mota ezarri behar zaio.
def eskuratu_fitxategi_guztiak (non_daude,mota):
    root_dir = non_daude #Script-a kokatuta dagoen karpeta hartzen da oinarritzat
    file_set = set() #Definitu izenak gordeko diren multzoa
    for dir_, _, files in os.walk(root_dir): #Sarrera karpetako karpeta bakoitza aztertu
        for file_name in files: #Haren fitxategiak aztertu 
            if (file_name.split(".")[1] == mota): #XML fitxategiak soilik hartu kontuan.  
                rel_dir = os.path.relpath(dir_, root_dir) 
                rel_file = os.path.join(rel_dir, file_name)
                file_set.add(rel_file) #Haien bide-izenak multzora gehitu.
    return(file_set)

#Bilatu nahi den meteoroaren izena eta meteoro guztiak dituen zerrenda sartu behar zaizkio.
#Uneko meteoroaren indizea eta meteoroak hiztegia eguneratuta itzuliko ditu. 
def eskuratuMeteoroIndizea (izena,meteoroak):
    if izena not in meteoroak: #Meteoroen hiztegian uneko meteoroaren izena ez bada ageri:
        meteoroak[izena]=len(meteoroak) #Indize bat esleitu
        indizea=len(meteoroak)+1 #Dataren informazioak lehen bi indizeak okupatuak ditu, hori kontutan hartu
    else:
        indizea=meteoroak[izena]+2 #Dataren informazioak lehen bi indizeak okupatuak ditu, hori kontutan hartu
    return indizea, meteoroak

#Data zehatz bati dagokion erregistroa, uneko meteoroari erregistroan dagokion indizea eta meteoroaren balioa sartu behar zaizkio.
#Erregistro eguneratua itzuliko du.
def gehitu_erregistroan (erregistroa,non,meteoroa):
    if (len(erregistroa) <= non): 
        for i in range(non-len(erregistroa)+1): #Meteoroari ez dagozkion espazioetan egin hau:
            erregistroa.append(None) #None ipini
    erregistroa[non]=meteoroa #Bestela, meteoroa ipini dagokion posizioan ???????????ETA len(erregistroa) > NON bada, beste balioak?
    return(erregistroa)

#Egun eta ordu zehatz bat, balioen datu-egitura eta meteoroen izenen zerrenda sartu behar zaizkio
#Egun eta ordu zehatz bati dagokion erregistroa, meteoroen zerrrenda, itzuliko du meteoroen zerrenda eguneratuarekin batera. Kontuan hartu meteoro batzuk hasieran (lehen egunetan) ez agertzea posible dela eta gero agertzea.
def eman_erregistroa (eguna,ordua,datuak,meteoroak):
    erregistroa = [list(eguna.attrib.values())[0],list(ordua.attrib.values())[0]] #Data informazioa ezarri erregistroko lehen bi datu gisa.
    for bakoitza in datuak: #Entitatearen informazio-espazio bakoitzeko egin:
        indizea, meteoroak = eskuratuMeteoroIndizea(bakoitza.tag,meteoroak) #Jakin zein meteoro edo aldagai mota den (izena)
        erregistroa = gehitu_erregistroan(erregistroa,indizea,bakoitza.text) #Erregistroa eguneratu
    return(erregistroa, meteoroak)

#Uneko fitxategiaren bide-izena sartuko zaio, sarrera karpetaren egitura adierazten duen pos aldagaiarekin batera (pos = 2 azpikarpeta bat, pos = 3 bi azpikarpeta)
#Fitxategia dagokion estazioaren kodea, neurketa bakoitzeko datuak dituen zerrenda eta meteoroen (aldagai meteorologikoen) izenen zerrenda itzuliko du. 
def eskuratuFitxategiarenErregistroak (fitxategia,pos):
    try: #XMLaren erro entitatea eskuratzeko saiakera
        erroa = ET.parse(fitxategia).getroot()
    except:
        return(None,None,None)
    meteoroak = { }
    estazioa=fitxategia.split("/")[pos] #Eskuratu estazioaren kodea
    erregistroak = [ ] #Haren erregistro edo entitateen datuak bilduko dituen zerrenda
    for haurra in erroa: #Erro entitatearen azpientitate bakoitzeko (OpenDatako datu-egitura jarraituz):
        for haurra2 in haurra: #Horren azpientitate bakoitzeko:
            for haurra3 in haurra2: #Berdina
                erregistroa, meteoroak=eman_erregistroa(haurra,haurra2,haurra3,meteoroak) #Eskuratu entitatearen informazioa
                erregistroak.append(erregistroa) #Gehitu hori zerrendan
    return(estazioa,erregistroak,meteoroak)

#Hilabete batean estazio batean jaso diren neurketa guztiak dituen zerrenda (erregistro moduan) eta meteoroen izenen zerrenda sartuko zaizkio.
#CSVa idazteko baliatuko den testua itzuliko du.  
def bihurtuCSV (estazioa_hila,meteoroak):
    testua="" #CSVa sortzeko erabiliko den testua
    goiburua="Data,Ordua," #Goiburukoan (lehen lerroa) lehenik eguna eta ordua egongo dira.  
    for i in meteoroak: #Aldagai meteorologiko bakoitzeko zutabe bat, ondoren. 
        goiburua=goiburua+i+","
    testua=goiburua+"\n" #Datuen errenkadak idazten hasteko lehen lerroari amaiera eman.
    for i in estazioa_hila: #Erregistro (neurketa aldi) bakoitzeko egin: 
        goiburua=""
        for j in i: #Aldagai bakoitzaren informazioa idatzi
            goiburua=goiburua+str(j)+","
        testua=testua+goiburua+"\n" #Errenkada bukatu
    return(testua)

#CSV fitxategiak sortzeko funtzioa, CSVan ipini behar den testua eta fitxategi berriaren bide-izena sartu behar zaizkio. Fitxategi hori kokatu beharko den posizioa adierazteko karpetak sartu dakizkioke.
def sortuCSV (testua,estazioaKarpeta,irteera_karpeta,izena):
    izen_osoa=irteera_karpeta+"/"
    if estazioaKarpeta is not None: 
        if (not os.path.isdir(irteera_karpeta+"/"+estazioaKarpeta)):
            os.mkdir(irteera_karpeta+"/"+estazioaKarpeta)
        izen_osoa=irteera_karpeta+"/"+estazioaKarpeta
    izen_osoa=izen_osoa+"/"+izena
    f = open(izen_osoa,"w") #Sortu.
    f.write(testua) #Idatzi.
    f.close() #Itxi.

#############################################################################
############## 2. FASETIK AURRERA ERABILTZEN DIREN FUNTZIOAK ################
#############################################################################

#Estazioen izenak eta kodeak erlazionatzen dituzten konfigurazio fitxategien bide-izenak jasotzen ditu sarrera bezala. 
#Erlazio horiek adierazten dituen Python-eko hiztegia itzultzen du. 
def lortuEstazioenIzenak (jsona,tsva):
    estHiztegia = { } #Erlazioak jasoko dituen hiztegia hasieratu. 
    with open(jsona) as json_fitxa: #Ireki lehen konfigurazio fitxategia
        data = json.load(json_fitxa)
    for i in data: #Fitxategi horretako entitate bakoitza jaso eta hiztegian ipini
        estHiztegia[i["Kode"]]=i["Izena"]
    df = pd.read_csv(tsva,sep="\t") #Bigarren konfigurazio fitxategia ireki
    for index, row in df.iterrows(): #Errenkadaz errenkada irakurri
        if row["Kodea"] not in list(estHiztegia.keys()): #Oraindik kode hori duen estazioa gehitu gabe badago:
            estHiztegia[row["Kodea"]]=row["Izena"] #Gehitu
    return(estHiztegia)

#Uneko fitxategiaren Pandas data-framea sartu behar zaio
#Fitxategi honek kontutan hartzen dituen aldagai meteorologikoen zerrenda eta lehen neurketaren data (urtea, hila eta eguna) itzuliko ditu. 
def aztertuFitxa (irakurketa):
    try:
        meteoroak = list(irakurketa.columns)[2:] #Eskuratu meteoroak goiburuetatik, lehen biak datari dagozkionez kendu
    except IndexError:
        meteoroak = [ ]
    urtea = irakurketa.iloc[1]['Data']
    data = urtea.split("-")
    dat = datetime.datetime(int(data[0]),int(data[1]),int(data[2]))
    return (meteoroak, dat)

#Datak ordenatuta dituen zerrenda, fitxategiak ordenatuta dituen zerrenda, zerrenda horietara gehitu nahi den fitxategiaren hasiera-data eta edukia sartuko zaizkio.
#Ordenatutako zerrendetara uneko fitxategiaren data eta edukia gehituko dira, ordena mantenduz. 
def eguneratuZerrendak (datak,fitxak,data,fitxa):
    pos=0 #Fitxategia kokatu behar den posizioa zehazten duen aldagaia
    for i in datak: #Ordenatutako zerrenda korritu
        if i > data: #Uneko data pasatzen duen lehen dataren posizioaren aurreko posizioarekin gelditu 
            break
        pos+=1
    datak.insert(pos,data) #Txertatu hor uneko data
    fitxak.insert(pos,fitxa) #Txertatu hor uneko fixtategiaren edukia
    return(datak,fitxak)

def eguneratuZerrendakEzegonkorki (meteoroOrdena,unekoMeteoroak,datak,fitxak,data,fitxa):
    berriak_denentzat = list(set(unekoMeteoroak) - set(meteoroOrdena))
    berriak_unekoarentzat = list(set(meteoroOrdena) - set(unekoMeteoroak))
    for i in fitxak:
        for j in berriak_denentzat:
            i[j]=["None"]*len(i.index)
    meteoroOrdena.extend(berriak_denentzat)
    for j in berriak_unekoarentzat:
        fitxa[j]=["None"]*len(fitxa.index)
    ordena_egokia=fitxak[0].columns
    fitxa = fitxa[ordena_egokia]
    pos=0 #Fitxategia kokatu behar den posizioa zehazten duen aldagaia
    for i in datak: #Ordenatutako zerrenda korritu
        if i > data: #Uneko data pasatzen duen lehen dataren posizioaren aurreko posizioarekin gelditu 
            break
        pos+=1
    datak.insert(pos,data) #Txertatu hor uneko data
    fitxak.insert(pos,fitxa) #Txertatu hor uneko fixtategiaren edukia
    return(datak,fitxak,meteoroOrdena)

#Itzuli nahi diren meteoroen hiztegia eta meteoro itzuliak dituen hiztegia sartuko zaizkio. Huts-egiteen erregistroa ere sartu beharko zaio.
#Goiburu itzulia itzuliko du, huts-egiteen erregistroarekin batera.
def itzuliMeteoroak (meteoroak,itzuliak,hutsak):
    itzulita = ""
    for i in meteoroak: #Meteoro bakoitzeko egin:
        euskaraz="" #Euskarazko bertsioaren hasieraketa
        bai=0
        for j in itzuliak: #Itzulpena duten meteoro bakoitzeko egin:
            if j in i: #Itzulpena baldin badu meteoroak:
                euskaraz=itzuliak[j] #Euskaraz ezar daiteke
                bai=1 #Hala adierazi
        if ("_a_" in i): #_a_-k gaztelaniazko datu-basetan posizioa adierazten du beti
            zatiak=i.split("_a_") #Posizioa eskuratu 
            euskaraz=euskaraz+"_"+zatiak[1]+"-ra" #Euskaraz ipini
        if (bai == 0): #Ezin izan bada itzulpena egin:
            if (i != "Data" and i != "Ordua" and i not in hutsak): #Data edo Ordua ez bada uneko meteoroa (hauek jada itzulita daudelako ez dira itzuli):
                hutsak.append(i) #Jakinarazi
            euskaraz=i #Euskararatutako meteoroa
        itzulita=itzulita+euskaraz+"," #Itzulpena egin
    return(itzulita+"\n",hutsak)

#CSV fitxa bati goiburukoa kentzeko funtzioa
def eskuratuKenMet (testua):
    kont=0
    while (testua[kont] != "\n"): #Lehen lerro bukaera topatzean bukatu begizta
        kont+=1
    return(kont+1) #Itzuli bigarren lerroaren lehen karakterearen posizioa

#Estazio baten CSVa (urte guztietako neurketekin) sortuko du.
#Data ordenatuak dituen zerrenda, fitxategien eduki ordenatu duen zerrenda, CSV berria kokatu behar den karpetaren bide-izena, ezarri nahi zaion izena eta kontuan hartzen dituen meteoroak sartu behar zaizkio.
#CSVa sortuko du.
def sortuEstazioarenCSVa (datak,fitxak,karpeta,estazioa,meteoroak):
    testu_bihurtuta=fitxak[0].to_csv(index=False)
    csv="Data,Ordua,"+meteoroak+testu_bihurtuta[eskuratuKenMet(testu_bihurtuta):len(testu_bihurtuta)-1] #Lehen CSVaren edukiarekin hasieratu testua bilduko duen aldagaia.
    for i in range(1,len(datak)):
        testu_bihurtuta=fitxak[i].to_csv(index=False)
        csv=csv+"\n"+testu_bihurtuta[eskuratuKenMet(testu_bihurtuta):len(testu_bihurtuta)-1]
    f = open(karpeta+"/"+estazioa+".csv","w")
    f.write(csv)
    f.close()
    return([],[])

#############################################################################
############## 3. FASETIK AURRERA ERABILTZEN DIREN FUNTZIOAK ################
#############################################################################
#Tenperatura nerketa 100 eta 150 cm artean da fidagarria, hori betetzen den edo ez itzultzen du.
def tenperaturaNeurketaOnargarriaDa (uneko_zutabea):
    if "Aire.Tenp" in uneko_zutabea:
        zatia = uneko_zutabea.split("_")[1]
        distantzia = int(zatia.split("c")[0])
        if distantzia >= 100 and distantzia <= 150:
            return True
    return False
#Datu-baseko zein zutabe hartuko diren kontuan zehazten du (tenperatura eta prezipitazio zutabeak).
def erabakiKontuanHartzekoZutabeak (zutabeGuztiak):
    minDistPrez=math.inf
    minDistTenp=math.inf
    kontuanHartu = [None]*2
    tenpEgina=False
    distEzeg=False
    for i in zutabeGuztiak:
        zatia = i.split("_")
        try:
            zatia=zatia[1]
            distantzia = int(zatia.split("c")[0])
        except: #Index Error or Value Error
            continue
        if ("Prezip" in i and distantzia < minDistPrez): #Lehenetsi distantzia txikienera daudenak
            minDistPrez=distantzia
            kontuanHartu[0]=i
        elif ("Aire.Tenp" in i and not tenpEgina):
            if (distantzia >= 100 and distantzia <= 150): #Lehenetsi distantzia txikienera dauden sentsoreak
                kontuanHartu[1]=i
                minDistTenp=-100
                tenpEgina=True
            elif distantzia < minDistTenp:
                minDistTenp=distantzia
                kontuanHartu[1]=i
                distEzeg=True
    return kontuanHartu, distEzeg

#Egunkako datuak kalkulatzeko funtzioa, egun bakoitzeko batez bestekoez osatutako Data Frame bat itzultzen du.
def kalkulatuEgunekoDatuak (lehen_neurketa,azken_neurketa,df,zutabeak):
    errenkada = { }
    itzuli=[None]*4
    for i in range(lehen_neurketa,azken_neurketa+1): #10 minuturoko datuak aztertu
        for j in zutabeak:
            if j is None:
                continue
            try: 
                balioa=df.iloc[i][j]
            except:
                continue
            if balioa is not None and str(balioa) != "None":
                balioa=float(balioa)
                if "Prezip" in j:
                    if j in errenkada.keys():
                        errenkada[j]+=balioa
                    else:
                        errenkada[j]=balioa
                else:
                    if j in errenkada.keys(): #Data frame berriko errenkada bakoitzak prezipitazio maximoa, minimoa, batez bestekoa eta prezipitazioak izango ditu.
                        errenkada[j][0]+=balioa 
                        errenkada[j][1]+=1
                        if balioa > errenkada[j][2]:
                            errenkada[j][2]=balioa
                        elif balioa < errenkada[j][3]:
                            errenkada[j][3]=balioa
                    else:
                        errenkada[j]=[0]*4 #Hasieratu errenkada berria
                        errenkada[j][0]=balioa
                        errenkada[j][1]=1
                        errenkada[j][2]=balioa
                        errenkada[j][3]=balioa
    for k in errenkada: 
        if "Prezip" in k:
            itzuli[2]=round(errenkada[k],2)
        else:
            itzuli[0]=errenkada[k][2]
            itzuli[1]=errenkada[k][3]
            itzuli[3]=round(errenkada[k][0]/errenkada[k][1],2) #Prezipitazioen batez bestekoa kalkulatu
    return itzuli
#Hirugarren faseko funtzio nagusia
def hirugarrenFasea (i,kontuanHartutakoZutabeak,irteera_karpeta3):
    df = pd.read_csv(i)
    izena=i.split("/")[-1]
    egun_df = pd.DataFrame(columns=kontuanHartutakoZutabeak)
    zutabeak, distEzeg=erabakiKontuanHartzekoZutabeak(df.columns)
    for j in range(0,len(df),144):
        errenkada = kalkulatuEgunekoDatuak(j,j+143,df,zutabeak)
        errenkada.insert(0,str(df.iloc[j]["Data"]))
        egun_df.loc[len(egun_df)]=errenkada
    if distEzeg:
        distantzia_ezegokiak.append((i,zutabeak[1]))
    testua = egun_df.to_csv("."+irteera_karpeta3+"/"+izena,index=False)
    return distantzia_ezegokiak

#############################################################################
############## 4. FASETIK AURRERA ERABILTZEN DIREN FUNTZIOAK ################
#############################################################################

#Data Frame bat emanda honek bere baitan duen azken data itzultzen du.
def lortuAzkenData (df):
    azkena=0
    for index, row in df.iterrows():
        if str(row["PrezipitazioMetatua"]) != "nan" or str(row["TenperaturaMaximoa"]) != "nan" or str(row["TenperaturaMinimoa"]) != "nan" or str(row["BatezBestekoTenperatura"]) != "nan":
            azkena=index
    return(azkena)

#Orain arteko hilabetekako datuak, uneko hilabeteari dagokion zerrenda eta uneko hilabetean egin diren neurketen kontagailua sartuta, hilabetekako datuen datu-egitura eguneratuko du.
def eguneratuDatuak(datuak,unekoa,kontagailuak):
    if (kontagailuak[0] == 0): #Ez bada neurketarik egin:
        unekoa[2]='null' #Hala adierazi
        unekoa[1]='null'
    else: #Bestela
        unekoa[2]=round(unekoa[2]/kontagailuak[0],4) #Batez besteko tenperatura maximoa kalkulatu
    if (kontagailuak[1] == 0): #Tenperatura minimoa behin ere ez bada neurtu hilabete honetan
        unekoa[3]='null' #Ezin da minimoen batez bestekoa eta minimo absolutua kalkulatu.
        unekoa[4]='null'
    else:
        unekoa[3]=round(unekoa[3]/kontagailuak[1],4) #Eguneratu minimoen batez bestekoa
    if (kontagailuak[2] == 0): #Prezipitazioen inguruko daturik ez bada hil honetan
        unekoa[5]='null' #Ezin da prezipitazio metatua kalkulatu
        unekoa[6]='null' #Ezta ere euria egindako egun kopurua
    else:
        unekoa[5]=round(unekoa[5],4) #Bestela, kalkulatu
    datuak.append(unekoa)
    return(datuak)

#Egunkako datuak dituen Data Frame-a emanda, hilabetekako datuak dituen zerrenda itzuliko du.
def eskuratuHilabetekakoDatuak (fitxa):
    datuak = [ ] #Hilabetekako datuen zerrenda hasieratu
    aurHila=-1 #Aurreko hilabetearen zenbakia
    hasi=False #Lehen exekuzioa den edo ez
    azkena=lortuAzkenData(fitxa) #Azkenenko data lortu
    for index, row in fitxa.iterrows(): #Egun bakoitzari neurketa bat dagokio, bakoitzeko egin:
        hila=row["Data"].split("-")[1] #Eskuratu hilabetea
        if (hila != aurHila): #Ikusi ea aldatu den azken neurketarekiko
            if hasi: #Lehen iterazioa ez bada:
                datuak=eguneratuDatuak(datuak,unekoa,kontagailuak) #Kalkulatu hilabetekako datuak
            unekoa=[0]*(len(fitxa.columns)+2) #Uneko hilabeteko datuak dituen zerrenda
            unekoa[1]=-300 #Tenperatura maximoa
            unekoa[4]=100000000 #Tenperatura minimoa
            unekoa[0]=row["Data"].split("-")[0] + "-" +row["Data"].split("-")[1] #Data
            kontagailuak=[0]*(len(fitxa.columns)-1) #Aldagai bakoitza zenbat egunetan neurtu den jasotzen duen zerrenda
            unekoa[6]=0 #Euri egunak
            if index+26 >= azkena: #Exekuzio infinitua saihesteko
                break
        if str(row["TenperaturaMaximoa"]) != "nan": #Tenperatura maximoa kalkulatu bada uneko egunean:
                hasi=True #Egin daitekeen hurrengo aldian hilabetekako datuak kalkulatu
                if (row["TenperaturaMaximoa"] > unekoa[1]): #Tenperatura maximo absolutua gorde
                    unekoa[1]=row["TenperaturaMaximoa"]
                unekoa[2]=unekoa[2]+row["TenperaturaMaximoa"] #Tenperatura maximoen batez bestekorako
                kontagailuak[0]+=1 #Neurketa egin izanaren berri eman
        if str(row["TenperaturaMinimoa"]) != "nan": #Berdina baina tenperatura minimoarekin
                hasi=True
                if (row["TenperaturaMinimoa"] < unekoa[4]):
                    unekoa[4]=row["TenperaturaMinimoa"]
                unekoa[3]=unekoa[3]+row["TenperaturaMinimoa"]
                kontagailuak[1]+=1
        if str(row["PrezipitazioMetatua"]) != "nan": #Berdina prezipitazioekin
                hasi=True
                unekoa[5]=unekoa[5]+row["PrezipitazioMetatua"]
                kontagailuak[2]+=1
                if (row["PrezipitazioMetatua"] > 0): #Euri egun bat gehiago
                    unekoa[6]+=1
        aurHila=hila
    if hasi and unekoa[1]!=-300: #Azken hilabetearen datuak ere gorde, behin begiztatik aterata
        datuak=eguneratuDatuak(datuak,unekoa,kontagailuak)
    return(datuak)

#############################################################################
########################## BESTELAKO FUNTZIOAK ##############################
#############################################################################

#Programak exekuzioan zehar izandako hutsegiteak inprimatuko ditu, motaren arabera bereizita
def inprimatu_hutsak (xml_hutsak,fitxategi_hutsak,itzulpen_hutsak,meteoro_falta,meteoro_ezberdinak,estazio_ezezagunak,elkartutako_estazioak,kode_ezegokiak,bateratze_gehiegi,bateratzerik_ez,distantzia_ezegokiak):
    testua="*************************HUTSEGITEAK***************************"
    testua=testua+"\n\nXML fitxategiak deskodetzean izandako hutsegiteak:\n"
    for i in xml_hutsak:
        testua=testua+str(i)+"\n"
    testua=testua+"\n\nEdukirik ez duten fitxategiak:\n"
    for i in fitxategi_hutsak:
        testua=testua+str(i)+"\n"
    testua=testua+"\n\nEuskararatu ezin izan diren aldagai izenak:\n"
    for i in itzulpen_hutsak:
        testua=testua+str(i)+"\n"
    testua=testua+"\n\nAldagai meteorologikorik ez duten fitxategiak:\n"
    for i in meteoro_falta:
        testua=testua+str(i)+"\n"
    testua=testua+"\n\nDenboran zehar aldagai meteorologiko desberdinak erabili dituzten estazioak:\n"
    for i in meteoro_ezberdinak:
        testua=testua+str(i)+"\n"
    testua=testua+"\n\nEzezagunak diren estazioak:\n"
    for i in estazio_ezezagunak:
        testua=testua+str(i)+"\n"
    testua=testua+"\n\nElkarketak egin zaizkien estazioak:\n"
    for i in elkartutako_estazioak:
        testua=testua+str(i)+"\n"
    testua=testua+"\n\nEzohiko kodeak edo desegokiak dituzten estazioak:\n"
    for i in kode_ezegokiak:
        testua=testua+str(i)+"\n"
    testua=testua+"\n\nBi baino fitxategi gehiago elkartzea eskatzen zuten estazioak:\n"
    for i in bateratze_gehiegi:
        testua=testua+str(i)+"\n"
    testua=testua+"\n\nElkarketarik eskatzen ez dituzten estazioak:\n"
    for i in bateratzerik_ez:
        testua=testua+str(i)+"\n"
    testua=testua+"\n\nEstazio hauetan tenperaturaren neurketa egiteko sentsorea ez dago distantzia fidagarrian:\n"
    for i in distantzia_ezegokiak:
        testua=testua+str(i)+"\n"
    return testua

#############################################################################
########################## PROGRAMAREN HASIERA ##############################
#############################################################################

####   HUTSEGITEEN ERREGISTROAK  ####
xml_hutsak = [ ] #XMLak deskodetzean izandako akatsak biltzeko zerrenda
itzulpen_hutsak = [ ] #Euskararatzeetan izandako akatsak biltzeko zerrenda
meteoro_falta = [ ] #Aldagai meteorologikorik topatu ez zaizkien fitxategiak
meteoro_ezberdinak = [ ] #Aldagai meteorologikoak bat ez datozkien fitxategiak
estazio_ezezagunak = [ ]
elkartutako_estazioak = [ ]
kode_ezegokiak = [ ]
bateratze_gehiegi = [ ]
bateratzerik_ez = [ ]
fitxategi_hutsak = [ ]
distantzia_ezegokiak = [ ]


####   INGURUNE ALDAGAIAK ####
sarrera_karpeta="" #SARTU DATUAK DAUDEN KARPETAREN BIDE IZENA
irteera_karpeta1="./Lehen_Irteera" #SARTU LEHEN IRTEERA (XML -> CSV) GORDEKO DEN KARPETA
irteera_karpeta2="./Bigarren_Irteera" #SARTU BIGARREN IRTEERA (Estazio bakoitzeko CSV bat) GORDEKO DEN KARPETA
irteera_karpeta3="./Hirugarren_Irteera" #Sartu HIRUGARREN IRTEERA (Egunkako batez bestekoak) GORDEKO DEN KARPETA
irteera_karpeta4="./Laugarren_Irteera" #SARTU LAUGARREN IRTEERA (Hilabetekako batez bestekoak) GORDEKO DEN KARPETA
jsona="./ezarpenak/estazioak.json" #Estazioen izenak biltzen dien JSONaren kokapena.
tsva="./ezarpenak/estazioakHedatua.tsv" #Estazioen izen gehiago biltzen dituen TSVaren kokapena.
itzulpenak="./ezarpenak/euskarazkoAldagaiIzenak.json" #Euskarazko aldagai izenak dituen fitxategiaren kokapena.
tabGoiburua="./ezarpenak/tabGoiburua.json" #TAB fitxategiak sortzeko goiburua duen fitxategiaren kokapena
loga="./ezarpenak/hutsegiteak.txt" #LOG fitxategia gordetzea nahi den tokia.
kontuanHartutakoZutabeak=["Data","TenperaturaMaximoa","TenperaturaMinimoa","PrezipitazioMetatua","BatezBestekoTenperatura"] #Estazio bakoitzetik erauziko diren zutabeak. 

#1. FASEA: XMLtik CSVra pasatzea. Open Datako XML fitxategiak CSV bihurtzen dira. 
fitxategiak=eskuratu_fitxategi_guztiak(sarrera_karpeta,"xml") #Fitxategien izenak eskuratzen dira. 
irteera_karpeta1 = sortuInguruneEgokia(irteera_karpeta1)
print("XMLak deskodetzen...")
for kont, i in tqdm(enumerate(fitxategiak),mininterval=10):
    helbidea=i.split("/")
    if (len(helbidea) == 2):
        pos=2
        estazioaKarpeta=helbidea[0]
    elif (len(helbidea) == 3):
        pos=3
        estazioaKarpeta=helbidea[1]
    else:
        pos=1
    estazioa, erregistroak,meteoroak = eskuratuFitxategiarenErregistroak(sarrera_karpeta+"/"+i,pos) #Neurketa bakoitzeko datuak eskuratu eta zerrenda batean itzuli
    if (estazioa == None): #Akatsen bat gertatu bada XMLa deskodetzean:
        xml_hutsak.append(i) #Haren berri eman
        continue
    testua = bihurtuCSV(erregistroak,meteoroak) #Eskuratu CSVan ipini daitekeen testua
    sortuCSV(testua,estazioaKarpeta,irteera_karpeta1,str(estazioa+"_"+str(kont)+".csv")) #Sortu fitxategia
print("Eginda.")

#2. FASEA: CSV anitzetatik (OpenData-ren formatuan) estazio bakoitzarentzat CSV bakar bat sortzen du.
print("Estazio bakoitzari CSV bat sortzen...")
irteera_karpeta2 = sortuInguruneEgokia(irteera_karpeta2)
with open(itzulpenak) as itzul:
    meteoItzuliak = json.load(itzul) #Aldagai meteorologiko itzulien hiztegia kargatu
estDatuak = lortuEstazioenIzenak(jsona,tsva) #Estazioen kodeak izenekin erlazionatzen dituen Python-eko hiztegia eskuratu
os.chdir("./"+irteera_karpeta1+"/") #Mugitu uneko estazioaren karpetara
karpetak = [x[0] for x in os.walk(".")] #Lehen faseko irteeran sortu diren karpeta guztiak eskuratu
for i in tqdm(karpetak,mininterval=10): #Karpeta (estazio) bakoitzeko egin:
    datak = [ ] #Data ordenatuak dituen zerrenda
    fitxak = [ ] #Fitxategien edukia dataren arabera ordenatuta duen zerrenda
    meteoroak = [ ] #Hasieratu meteoroak, estazio bakoitzak desberdinak har baititzake kontuan
    if (i == "."): #Puntu karpeta guraso karpeta da
        continue  #Ez egin ezer hor
    fitxategiak=eskuratu_fitxategi_guztiak(i,"csv") #Eskuratu karpetaren fitxategi guztiak
    estazioa=i.split("/")[1] #Estazioaren kodea karpetaren izenaren berdina izango da
    lehena=True
    ezegonkorra=False
    for j in fitxategiak: #Karpetako fitxategi bakoitzeko egin:
        izena=i+"/"+j[2:] 
        irakur = pd.read_csv(izena) #Irakurri CSV gisa
        irakur = irakur.loc[:, ~irakur.columns.str.contains('^Unnamed')] #Ezabatu zutabe hutsak
        try:
            met, dat = aztertuFitxa(irakur) #Eskuratu fitxak kontuan hartzen dituen aldagai meteorologikoak eta hasiera data
        except IndexError:
            fitxategi_hutsak.append(j)
            continue
        if len(met) == 0: #Ez badu aldagai meteorologikorik kontuan hartzen:
            meteoro_falta.append(izena)
            continue
        if not ezegonkorra and (set(met) == set(meteoroak) or lehena): #Ziurtatu estazioaren neurketa guztietan aldagai meteorologiko berdinak hartu direla kontuan (bestela kaosa)
            datak, fitxak = eguneratuZerrendak(datak,fitxak,dat,irakur) #Data orden egokian kokatu uneko fitxategia
            meteoroak=met
        else:
            datak, fitxak, meteoroak = eguneratuZerrendakEzegonkorki(meteoroak,met,datak,fitxak,dat,irakur) #Data orden egokian kokatu uneko fitxategia
            if i not in meteoro_ezberdinak:
                meteoro_ezberdinak.append(i)
            ezegonkorra=True
        lehena=False 
    meteoroak, itzulpen_hutsak=itzuliMeteoroak(meteoroak,meteoItzuliak,itzulpen_hutsak) #Aldagai meteorologikoak euskaratu
    try: #Saiatu
        izena=estDatuak[estazioa] #Uneko estazioari dagokion izena eskuratzen
    except KeyError: #Ezin bada
        izena=estazioa #Kodea erabili izen bezala
    except FileExistsError: #Jada estazioari dagokion fitxategi bat baldin badago (aurreko exekuzio batekoa)
        kont=2 #Izen berri bat asmatzeko kontagailua
        while True: #Izen berri bat topatu arte
            izena=estDatuak[estazioa]+str(kont) #Izen berria
            if not os.path.isfile(irteera_karpeta2+izena): #Jada aurkitu bada:
               break #Bukatu begizta
            else:
                kont+=1 
    sortuEstazioarenCSVa (datak,fitxak,"../"+irteera_karpeta2,estazioa+"_"+izena,meteoroak) #Sortu estazioari dagokion CSVa
os.chdir("../") #Itzuli guraso fitxategira 
print("Eginda.")

#3. FASEA: 10 minutukako neurketa egunkako neurketa bihurtzea
print("Egunkako datuak sortzen...")
irteera_karpeta3 = sortuInguruneEgokia(irteera_karpeta3)
fitxategiak=eskuratu_fitxategi_guztiak(irteera_karpeta2,"csv") #Fitxategien izenak eskuratzen dira.
fitxak2=eskuratu_fitxategi_guztiak("./Hirugarren_Irteera","csv") #Fitxategien izenak eskuratzen dira.
os.chdir("./"+irteera_karpeta2+"/")
for i in tqdm(fitxategiak,mininterval=10):
    if i in fitxak2:
        continue
    distantzia_ezegokiak.extend(hirugarrenFasea(i,kontuanHartutakoZutabeak,irteera_karpeta3))
os.chdir("../") #Itzuli guraso fitxategira 
print("Eginda.")

#4. FASEA: Egunkako neurketak hilabetekako neurketa bihurtzea
print("Hilabetekako datuak sortzen...")
irteera_karpeta4 = sortuInguruneEgokia(irteera_karpeta4)
fitxak=eskuratu_fitxategi_guztiak(irteera_karpeta3,"csv") #Fitxategien izenak eskuratzen dira.
estDatuak = lortuEstazioenIzenak(jsona,tsva) #Estazioen izenak dituen hiztegia lortu.
with open(tabGoiburua) as f:
    text=json.load(f)
os.chdir("./"+irteera_karpeta3+"/")
bateratzeko = { } 
for i in fitxak: #Fitxategi bakoitzeko egin:
    egina=False
    izena=i.split("/")[1].split(".")[0].split("_")[1] #Eskuratu estazioaren izena
    kodea=i.split("/")[1].split("_")[0] #Eskuratu estazioaren kodea
    try: #Saiatu
        begiratu=estDatuak[kodea] #Izen hori duen estazio bat bilatzen estazioen hiztegian
    except: #Ez badago
        estDatuak[kodea]=kodea #Kodea ipini izen gisa
        estazio_ezezagunak.append((i,izena)) #Estazio hori erregistratu gabe dago, aurrera egin
    if (kodea[0] == 'G'): #Estazioaren kodean G letra badago estazio zaharra da
        berria='C'+kodea[1:len(kodea)] #Estazio berriak kode bera izango du, baina C letrarekin hasita
        if berria in bateratzeko.keys(): #Saiatu topatzen estazio berriari dagozkion fitxategien sorta
            bateratzeko[berria].append(i) #Topatu bada gehitu uneko fitxategia
        else: #Bestela
            bateratzeko[kodea]=[i] #Sotu sorta berria eta gehitu uneko fitxategia
    elif (kodea[0] == 'C'): #Estazioa berria bada:
        berria='G'+kodea[1:len(kodea)] #Estazio zahar baliokide bat badu, haren kodea izango litzatekeena sortu
        if berria in bateratzeko.keys(): #Saiatu topatzen hari dagokion sarreraren bat
            bateratzeko[berria].append(i) #Baldin bada gehitu hor uneko fitxategia
        else:
            bateratzeko[kodea]=[i] #Bestela, sortu eta gehitu
    else:
        bateratzeko[kodea]=[i] #Aparteko kode bat badu estazioak, bere horretan gehitu fitxategia. 
for i in tqdm(bateratzeko.values(),mininterval=10): #Bateratzeak jasota dituen hiztegiko sarrera bakoitzeko egin:
    if len(i) == 2: #Estazio zaharra eta berria baldin baditu sarrerak:
        df1 = pd.read_csv(i[0],encoding = 'ISO-8859-1',low_memory=False) #Bakoitzaren fitxategia irakurri
        df2 = pd.read_csv(i[1],encoding = 'ISO-8859-1',low_memory=False)
        kodea1=i[0].split("/")[1].split("_")[0] #Bakoitzaren kodea eskuratu
        kodea2=i[1].split("/")[1].split("_")[0]
        if (kodea1[0] == 'G' and kodea2[0] == 'C'): #Fitxategi zaharra baldin badago lehenengo:
            izena=estDatuak[kodea2]+"_"+kodea2+"_"+kodea1 #Izen berria sortu
            df = df1.combine_first(df2) #Kateatu zaharretik hasita bi fitxategiak
            elkartutako_estazioak.append(i) 
        elif (kodea1[0] == 'C' and kodea2[0] == 'G'): #Fitxategi berria baldin badago lehenengo:
            izena=estDatuak[kodea1]+"_"+kodea1+"_"+kodea2
            df = df2.combine_first(df1) #Kateatu alderantzizko ordenean
            elkartutako_estazioak.append(i)
        else: #Kode egokiak ez badituzte estazioek:
            kode_ezegokiak.append(i)
            continue #Ez egin ezer
    elif len(i) > 2: #Bi bateratze baino gehiago baldin badaude:
        kodea1=i[0].split("/")[1].split("_")[0]
        kodea2=i[1].split("/")[1].split("_")[0]
        kodea3=i[2].split("/")[1].split("_")[0]
        bateratze_gehiegi.append((i,estDatuak[kodea1],estDatuak[kodea2],estDatuak[kodea3]))
        continue #Ezer ez egin
    else: #Ez badago bateratzerik:
        k=i[0].split("/")[1].split("_")[0]
        izena=estDatuak[k]+"_"+k
        df=pd.read_csv(i[0],encoding = 'ISO-8859-1',low_memory=False) #Irakurri modu arruntean fitxategi bakarra
        bateratzerik_ez.append(i)
    datuak=eskuratuHilabetekakoDatuak(df) #Hilabetekako datuak kalkulatu
    text["description"]["eu"]=izena + " estazio meteorologikoaren hilabetekako datuak" #TAB fitxategia sortzeko
    text['data'] = datuak #Datuak ipini TABean
    json_object = json.dumps(text, indent=4) #Sortu TAB fitxtegiaren edukia
    izena = izena.replace("_"," ") #Izena txukundu
    with open("."+irteera_karpeta4+"/"+izena+" estazio meteorologikoaren hilabetekako datuak.tab", "w") as outfile: #Sortu TAB fitxategia
        outfile.write(json_object)
os.chdir("../") #Itzuli guraso fitxategira
print("Eginda.")

l_testua=inprimatu_hutsak(xml_hutsak,fitxategi_hutsak,itzulpen_hutsak,meteoro_falta,meteoro_ezberdinak,estazio_ezezagunak,elkartutako_estazioak,kode_ezegokiak,bateratze_gehiegi,bateratzerik_ez,distantzia_ezegokiak)
with open (loga,"w") as f:
    f.write(l_testua)
