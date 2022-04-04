class Stopafstand:
    def __init__(self, snelheid, reactietijd, wegdek):
        self.snelheid = snelheid
        self.reactietijd = reactietijd
        self.wegdek = wegdek
        self.stopafstand = None

    def __str__(self):
        if self.stopafstand is None:
            return f"Stopafstand is onbekend"
        else:
            return f"Stopafstand is {self.stopafstand}"

    def __eq__(self, other):
        return (self.stopafstand == other.stopafstand)


