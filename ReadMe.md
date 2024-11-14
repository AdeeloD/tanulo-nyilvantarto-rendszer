# Hersics Előd 

# Neptun:YNZT92

# Gazdaságinformatikus szak

## Tanuló Nyilvántartó Rendszer

### Projekt leírása

Ez a projekt egy Tanuló nyilvántartó rendszer, amely lehetővé teszi egy adatbázisban lévő tanulók adatainak kezelését egy grafikus felhasználói felületen keresztül. A program segítségével új tanulókat lehet hozzáadni az adatbázishoz, meglévő tanulók adatait lekérdezni, módosítani és törölni. A grafikus felületet a tkinter könyvtár segítségével valósítottam meg, és a PostgreSQL adatbázishoz való kapcsolódást a psycopg2 könyvtár biztosítja.

### Szükséges könyvtárak és telepítésük

A program működéséhez szükséges csomagok telepítése:

    pip install psycopg2-binary python-dotenv

Fájlok

    HE_Modul.py: Az adatbázis-kezelő osztályt (HEOsztaly) tartalmazza.
    main.py: A GUI-t megvalósító fájl, amely a HEOsztaly osztályt használja a műveletek végrehajtásához.

Konfiguráció

Létre kell hozni .env fájlt a következő tartalommal, hogy az adatbázis-kapcsolat megfelelően működjön:

    DB_HOST=<adatbázis_cím>
    DB_NAME=<adatbázis_név>
    DB_USER=<adatbázis_felhasználó>
    DB_PASSWORD=<adatbázis_jelszó>

### Modulok és osztályok

#### HE_Modul.py

Ez a fájl tartalmazza a HEOsztaly osztályt, amely az adatbázis-kezelésért felelős. Az osztály az adatbáziskapcsolat megnyitásáért és lezárásáért, valamint az alapvető CRUD műveletek (Create, Read, Update, Delete) végrehajtásáért felel.
Osztály: HEOsztaly

    __init__(self): Az adatbázis-kapcsolatot inicializálja a .env fájlban megadott adatok alapján. Ha a kapcsolat sikeres, egy üzenetet jelenít meg.

    is_valid_neptun_code(neptun_kod): Egy statikus metódus, amely ellenőrzi, hogy a Neptun kód formátuma helyes-e (6 karakter, betűk és számok).

    uj_tanulo_hozzaadasa_HE(self, nev, neptun_kod, email, nemzetiseg, osztondijas, szuletesi_datum, megjegyzes): Új tanulót ad az adatbázishoz. Ellenőrzi a Neptun kód formátumát, és ha helyes, elvégzi az SQL beszúrást.

    tanulok_lekerdezese_HE(self): Visszaadja az adatbázisban lévő összes tanuló adatait.

    tanulo_torlese_HE(self, neptun_kod): Egy tanuló törlése a megadott Neptun kód alapján.

    tanulo_modositasa_HE(self, neptun_kod, nev, email, nemzetiseg, osztondijas, szuletesi_datum, megjegyzes): Egy tanuló adatainak módosítása a megadott Neptun kód alapján.

    __del__(self): Az osztály törlésekor bezárja az adatbázis kapcsolatot.

#### main.py

Ez a fájl tartalmazza az alkalmazás grafikus felhasználói felületét, amelyen keresztül a felhasználó végrehajthatja a CRUD műveleteket.
Osztály: App

    __init__(self, root): Inicializálja a GUI-t, beállítja a főképernyő méretét, létrehozza az adatbázis objektumot, és meghatározza a beviteli mezőket, gombokat és a táblázatot.

    tanulo_hozzaadasa_HE(self): Összegyűjti a felhasználói adatokat, ellenőrzi a születési dátum formátumát, majd hozzáadja az adatokat az adatbázishoz.

    tanulok_listaja_HE(self): Lekéri és megjeleníti az adatbázisban lévő összes tanuló adatait a táblázatban.

    tanulo_torlese_HE(self): Kiválasztott tanuló törlése a táblázatból és az adatbázisból.

    tanulo_szerkesztese_HE(self): Kiválasztott tanuló adatainak szerkesztése. A beviteli mezőket a kiválasztott tanuló adataival tölti ki, és a módosítások mentéséhez szükséges gombot megjeleníti.

    tanulo_modositasa_HE(self): Elmenti a módosított adatokat az adatbázisba.

### Használat

A main.py fájl elindítása:

    python main.py

Az alkalmazás grafikus felületén az alábbi műveletek érhetők el:

Tanuló Hozzáadása: Új tanuló hozzáadása az adatbázishoz.

Tanulók Listája: Az összes tanuló megtekintése az adatbázisban.

Tanuló Törlése: Kiválasztott tanuló törlése.

Szerkesztés: A kiválasztott tanuló adatainak szerkesztése.

### Kódlogika

A kód alapvetően két fő komponensből áll:

Adatbázis-kezelő modul (HE_Modul.py): Ez az osztály végzi az adatbázissal kapcsolatos műveleteket.
Grafikus felület (main.py): A felhasználói interfészt és az adatbeviteli/lekérdezési logikát tartalmazza, amely a HEOsztaly objektum segítségével végzi el a kéréseket.

### Hibakezelés

Adatbázis-hibák: Az adatbázis kapcsolódási és műveleti hibák try-except blokkokkal kezelve vannak. Hibák esetén a tranzakció visszavonódik, és hibaüzenet jelenik meg.
Input ellenőrzés: A Neptun kód és a születési dátum formátuma ellenőrzésre kerül.