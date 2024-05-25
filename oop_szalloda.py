from abc import ABC, abstractmethod
from datetime import datetime

class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=10000, szobaszam=szobaszam)
        self.agy = "Egyágyas szoba"
        self.extra = "Nincs"

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=15000, szobaszam=szobaszam)
        self.agy = "Kétágyas szoba"
        self.extra = "Masszázs kád"

class Hotel:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def szoba_letrehozasa(self, szoba):
        self.szobak.append(szoba)

    def szoba_foglalas(self, szobaszam, date):
        if datetime.strptime(date, '%Y-%m-%d') <= datetime.now():
            return "Nem megengedett dátom (múltbéli)."
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                for foglalas in self.foglalasok:
                    if foglalas.szoba.szobaszam == szobaszam and foglalas.date == date:
                        return "Ez a szoba már foglalt."
                uj_foglalas = Foglalas(szoba, date)
                self.foglalasok.append(uj_foglalas)
                return f"A foglalás ára: {uj_foglalas.szoba.ar} Ft"
        return "Nem létező szoba!"

    def foglalas_lemondas(self, szobaszam, date):
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.date == date:
                self.foglalasok.remove(foglalas)
                return "Foglalás lemondva"
        return "Nem létező foglalás."

    def list_foglalasok(self):
        if not self.foglalasok:
            return "Nincsenek foglalások."
        return [(foglalas.szoba.szobaszam, foglalas.szoba.agy, foglalas.date) for foglalas in self.foglalasok]
    
    def szabad_szobak(self, date):
        try:
            valid_date = datetime.strptime(date, '%Y-%m-%d')
            if valid_date <= datetime.now():
                return "Múltbeli dátom nem megengedett."
        except ValueError:
            return "Nem jó formátum, következő formátum megengedett: yyyy-mm-dd."

        available_szobak = [szoba for szoba in self.szobak if not any(foglalas.date == date and foglalas.szoba.szobaszam == szoba.szobaszam for foglalas in self.foglalasok)]
        if not available_szobak:
            return "Nincsenek szabad szobák erre a dátumra"
        return available_szobak
    
class Foglalas:
    def __init__(self, szoba, date):
        self.szoba = szoba
        self.date = date

# Induló adatok betöltése
hotel = Hotel("Star Hotel")
hotel.szoba_letrehozasa(EgyagyasSzoba(101))
hotel.szoba_letrehozasa(EgyagyasSzoba(102))
hotel.szoba_letrehozasa(KetagyasSzoba(103))
hotel.szoba_foglalas(101, "2024-07-07")
hotel.szoba_foglalas(102, "2024-07-07")
hotel.szoba_foglalas(103, "2024-07-07")
hotel.szoba_foglalas(101, "2024-05-03")
hotel.szoba_foglalas(102, "2024-08-08")

def main():
    print("Üdvözlöm a Teszt Hotelben. Kérem tesztelje az alkalmazás a menük segítségével.\n")

    while True:
        print("\nVálassz a menuből egy funkciót:")
        print("1 - Foglalások listázása")
        print("2 - Elérhető szobák keresése egy dátumra")
        print("3 - Szoba foglalása")
        print("4 - Szoba lemondása")
        print("9 - Kilépés")

        option = input("Válassz egy menüpontot (1-4, 9): ")

        if option == "1":
            foglalasok = hotel.list_foglalasok()
            if isinstance(foglalasok, str):
                print(foglalasok)
            else:
                for foglalas in foglalasok:
                    print(f"Szobaszám: {foglalas[0]}, Típus: {foglalas[1]}, Dátum: {foglalas[2]}")

        elif option == "2": 
            date = input("Melyik dátumra keresünk? (ÉÉÉÉ-HH-NN): ")
            result = hotel.szabad_szobak(date)
            if isinstance(result, str):
                print(result)
            else:
                print("Elérhető szobák a megadott dátumra: " + date)
                for szoba in result:
                    print(f"Szobaszám: {szoba.szobaszam}, Típus: {szoba.agy}, Extra: {szoba.extra}, Ár: {szoba.ar} Ft")

        elif option == "3":
            try:
                szobaszam = int(input("Szobaszám megadása: "))
                print("Nincs ilyen szoba!")
                date = input("Foglalás dátumának mgadása (ÉÉÉÉ-HH-NN): ")
                valid_date = datetime.strptime(date, '%Y-%m-%d')
                if valid_date <= datetime.now():
                    raise ValueError("Múltbeli dátom nem megengedett.")
                print(hotel.szoba_foglalas(szobaszam, date))
            except ValueError as e:
                print(f"A dátum vagy szobaszám nem megfelelő!")

        elif option == "4":
            try:
                szobaszam = int(input("Add meg a szobaszámot: "))
                date = input("Foglalás dátuma (ÉÉÉÉ-HH-NN): ")
                print(hotel.foglalas_lemondas(szobaszam, date))
            except ValueError as e:
                print(f"A dátum vagy szobaszám nem megfelelő!")

        elif option == "9":
            print("Kilépés.")
            break
        else:
            print("Nem létező menupont, válassz a listából!")

if __name__ == "__main__":
    main()