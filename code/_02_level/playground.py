

class Bewohner:
    def __init__(self, name):
        self.name = name

    def rede(self):
        print(f"Hallo! Mein name ist {self.name}.")

class Arbeiter:
    def __init__(self, arbeit):
        self.arbeit = arbeit

    def klage(self):
        print(f"Ich muss dauernd uff Maloche! Kack {self.arbeit}-Job!")


class Mensch(Bewohner, Arbeiter):
    def __init__(self, name, arbeit):
        Bewohner.__init__(self, name=name)
        Arbeiter.__init__(self, arbeit=arbeit)

    def leben(self):
        self.rede()
        self.klage()


mensch = Mensch(name="Pedda", arbeit="Kartoffeltraeger")
mensch.leben()