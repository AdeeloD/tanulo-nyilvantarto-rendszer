import psycopg2
from dotenv import load_dotenv
import os
import re


class HEOsztaly:
    def __init__(self):
        load_dotenv()
        try:

            self.conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD")
            )
            self.conn.autocommit = False
            self.cursor = self.conn.cursor()
            print("Sikeres adatbázis kapcsolat!")
        except psycopg2.Error as e:
            print(f"Adatbázis kapcsolódási hiba: {e}")

    @staticmethod
    def is_valid_neptun_code_HE(neptun_kod):
        return bool(re.match(r"^[A-Za-z0-9]{6}$", neptun_kod))

    def uj_tanulo_hozzaadasa_HE(self, nev, neptun_kod, email, nemzetiseg, osztondijas, szuletesi_datum, megjegyzes):
        if not self.is_valid_neptun_code_HE(neptun_kod):
            return "Érvénytelen Neptun kód formátum!"

        try:
            self.cursor.execute("""
                INSERT INTO tanulok (nev, neptun_kod, email, nemzetiseg, osztondijas, szuletesi_datum, megjegyzes)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (nev, neptun_kod, email, nemzetiseg, osztondijas, szuletesi_datum, megjegyzes))

            self.conn.commit()
            return "Tanuló sikeresen hozzáadva!"

        except psycopg2.Error as e:
            self.conn.rollback()
            return f"Hiba a hozzáadás során: {e}"

    def tanulok_lekerdezese_HE(self):
        try:
            self.cursor.execute(
                "SELECT nev, neptun_kod, email, nemzetiseg, osztondijas, szuletesi_datum, megjegyzes FROM tanulok")
            return self.cursor.fetchall()

        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Hiba a lekérdezés során: {e}")
            return []

    def tanulo_torlese_HE(self, neptun_kod):
        if not self.is_valid_neptun_code_HE(neptun_kod):
            return "Érvénytelen Neptun kód formátum!"

        try:
            self.cursor.execute("DELETE FROM tanulok WHERE neptun_kod = %s", (neptun_kod,))
            if self.cursor.rowcount == 0:
                return "Nem található tanuló a megadott Neptun kóddal."

            self.conn.commit()
            return "Tanuló sikeresen törölve!"
        except psycopg2.Error as e:
            self.conn.rollback()
            return f"Hiba a törlés során: {e}"

    def tanulo_modositasa_HE(self, neptun_kod, nev, email, nemzetiseg, osztondijas, szuletesi_datum, megjegyzes):
        if not self.is_valid_neptun_code_HE(neptun_kod):
            return "Érvénytelen Neptun kód formátum!"

        try:
            self.cursor.execute("""
                UPDATE tanulok 
                SET nev = %s, email = %s, nemzetiseg = %s, osztondijas = %s, szuletesi_datum = %s, megjegyzes = %s
                WHERE neptun_kod = %s
            """, (nev, email, nemzetiseg, osztondijas, szuletesi_datum, megjegyzes, neptun_kod))

            if self.cursor.rowcount == 0:
                return "Nem található tanuló a megadott Neptun kóddal."

            self.conn.commit()
            return "Tanuló adatai sikeresen módosítva!"
        except psycopg2.Error as e:
            self.conn.rollback()
            return f"Hiba a módosítás során: {e}"

    def __del__(self):
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'conn'):
            self.conn.close()
