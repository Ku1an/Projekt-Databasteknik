# Projekt-Databasteknik

**Dependenceis** - Flask, mysql-connector-python


## Fil Beskrivning

**projekt.sql** - Alla tabeller,funktioner och triggers för schemat

**data.sql** - All nodvändig data för schemat samt programmet

**dump.sql** - SQL dumpen av allt

**main.py** - Själva programmet (EXE)

**modules.py** - moduler som main.py använder

static och templates är flask mapar med html som css filer, även bilder.


## Guide till användning

Steg 1 : Ladda ner nodvändiga bibliotek i din virtuella miljö  *(i denna miljö finns alla filer)* .

Steg 2 : Sätt upp databasen, kör  *projekt.sql*  först och sen  *data.sql*.

Steg 3 : Nu är det klart. Kör **_python main.py_**

Steg 4 : Nu är hemsidan uppe. I en developer mijö bör adressen vara **http://127.0.0.1:5000/**

