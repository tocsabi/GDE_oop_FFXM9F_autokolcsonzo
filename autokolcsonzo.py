from abc import ABC, abstractmethod
from datetime import date

class Auto(ABC):
    def __init__(self, rendszam, tipus, berleti_dij):
        self.rendszam = rendszam
        self.tipus = tipus
        self.berleti_dij = berleti_dij
        self.berelheto = True

    @abstractmethod
    def __str__(self):
        pass


class Szemelyauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, ajtok_szama):
        super().__init__(rendszam, tipus, berleti_dij)
        self.ajtok_szama = ajtok_szama

    def __str__(self):
        return f"Személyautó - \n Rendszám: {self.rendszam}, \n Típus: {self.tipus}, \n Ajtók száma: {self.ajtok_szama}, \n Bérleti díj: {self.berleti_dij} Ft/nap \n"


class Teherauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, teherbiras):
        super().__init__(rendszam, tipus, berleti_dij)
        self.teherbiras = teherbiras

    def __str__(self):
        return f"Teherautó - \n Rendszám: {self.rendszam}, \n Típus: {self.tipus}, \n Teherbírás: {self.teherbiras} kg, \n Bérleti díj: {self.berleti_dij} Ft/nap \n"


class Autokolcsonzo:
    def __init__(self, nev):
        self.nev = nev
        self.autok = []
        self.berlesek = []

    def autok_listazasa(self):
        print(f"\n{self.nev} autói:")
        for auto in self.autok:
            status = "Elérhető" if auto.berelheto else "Foglalt"
            print(f"{auto} - Állapot: {status}")

    def hozzaad_auto(self, auto):
        self.autok.append(auto)

    def keres_auto(self, rendszam):
        for auto in self.autok:
            if auto.rendszam == rendszam:
                return auto
        return None


class Berles:
    def __init__(self, auto, berlo_nev, datum):
        self.auto = auto
        self.berlo_nev = berlo_nev
        self.datum = datum

    def __str__(self):
        return f"Bérlés - Autó: {self.auto.rendszam}, Bérlő: {self.berlo_nev}, Dátum: {self.datum}"


def main():
    kolcsonzo = Autokolcsonzo("Tóth autó kölcsönző")

    kolcsonzo.hozzaad_auto(Szemelyauto("AAA-111", "Személyautó1", 10000, 4))
    kolcsonzo.hozzaad_auto(Szemelyauto("BBB-222", "Személyautó2", 12000, 4))
    kolcsonzo.hozzaad_auto(Teherauto("CCC-333", "Teherautó2", 20000, 1500))
    kolcsonzo.hozzaad_auto(Teherauto("DDD-444", "Teherautó2", 22000, 20000))

    auto = kolcsonzo.keres_auto("AAA-111")
    if auto:
        auto.berelheto = False
        kolcsonzo.berlesek.append(Berles(Auto, "Kis Pista", date.today()))

    auto = kolcsonzo.keres_auto("CCC-333")
    if auto:
        auto.berelheto = False
        kolcsonzo.berlesek.append(Berles(Auto, "Teszt Elek", date.today()))

    auto = kolcsonzo.keres_auto("DDD-444")
    if auto:
        auto.berelheto = False
        kolcsonzo.berlesek.append(Berles(Auto, "Bér Elek", date.today()))

    while True:
        print("\n--- Menü ---")
        print("1. Autók listázása")
        print("2. Autó bérlése")
        print("3. Bérlés lemondása")
        print("4. Bérlések listázása")
        print("5. Kilépés")
        valasztas = input("Választás: ")

        match valasztas:
            case "1":
                kolcsonzo.autok_listazasa()

            case "2":
                rendszam = input("Adja meg a bérelni kívánt autó rendszámát: ")
                auto = kolcsonzo.keres_auto(rendszam)
                if auto and auto.berelheto:
                    berlo_nev = input("Adja meg a nevét: ")
                    auto.berelheto = False
                    kolcsonzo.berlesek.append(Berles(auto, berlo_nev, date.today()))
                    print(f"Sikeresen kibérelte az autót! Ár: {auto.berleti_dij} Ft/nap")
                else:
                    print("Az autó nem található vagy nem elérhető!")

            case "3":
                rendszam = input("Adja meg a lemondani kívánt bérléshez tartozó rendszámot: ")
                berles = next((b for b in kolcsonzo.berlesek if b.auto.rendszam == rendszam), None)
                if berles:
                    kolcsonzo.berlesek.remove(berles)
                    berles.auto.berelheto = True
                    print("Sikeresen lemondta a bérlést!")
                else:
                    print("Nem található ilyen bérlés!")

            case "4":
                print("\nAktuális bérlések:")
                for berles in kolcsonzo.berlesek:
                    print(berles)

            case "5":
                print("Kilépés...")
                break

            case _:
                print("Érvénytelen választás!")


if __name__ == "__main__":
    main()
