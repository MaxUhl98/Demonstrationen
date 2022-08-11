"""Dieses Programm ist eine heuristische Suche, deren Zweck es ist auf einem 3x3 Feld mit 8 Plättchen
   diese mit möglichst wenigen Zügen in die Reihenfolge von perf zu bringen, wobei 0 ein leeres Feld repräsentiert
   (man kann nur links/rechts/oben/unten zur 0 angrenzende Felder mit der 0 tauschen).
   Ich habe als Heuristik die Summe der Manhattenabstände aller Zahlen außer der Null zu ihren gehörigen Feldern summiert.
   Die Kosten für einen Austauschschritt betragen 1.
"""
import random as r
import time as t


class Field:
    perf = [1, 2, 3,
            4, 5, 6,
            7, 8, 0]

    def __init__(self, position, parent=[], count=0):
        # Der count ist die Anzahl der Schritte die benötigt wurden, um die jetztige Position zu erreichen
        self.count = count
        self.list = position
        self.parent = parent
        # Die metrik ist die Summe der Manhattanabstände aller Zahlen zu ihrer Position in perf
        self.metrik = 0
        for i in range(9):
            if position[i] == 0:
                # npos ist die Position der Null, die wir noch benötigen werden, um Vertauschungen auszuführen
                self.npos = i
            else:
                self.metrik += abs((position[i] - 1) // 3 - i // 3) + abs((position[i] - 1) % 3 - i % 3)

    # Magic Method um heuristischen Vergleich von Positionen einfacher zu machen (Kosten von einem Tausch = 1)
    def __lt__(self, o):
        if self.metrik + self.count < o.metrik + o.count:
            return True
        else:
            return False

    # pos_moves gibt mir alle möglichen Züge der betrachteten Position als Liste zurück
    def pos_moves(self):
        moves = []

        if self.npos + 3 <= 8:
            copy = self.list.copy()
            copy[self.npos] = copy[self.npos + 3]
            copy[self.npos + 3] = 0
            moves.append(copy)
        if self.npos - 3 >= 0:
            copy = self.list.copy()
            copy[self.npos] = copy[self.npos - 3]
            copy[self.npos - 3] = 0
            moves.append(copy)
        if (self.npos + 1) // 3 == self.npos // 3:
            copy = self.list.copy()
            copy[self.npos] = copy[self.npos + 1]
            copy[self.npos + 1] = 0
            moves.append(copy)
        if (self.npos - 1) // 3 == self.npos // 3:
            copy = self.list.copy()
            copy[self.npos] = copy[self.npos - 1]
            copy[self.npos - 1] = 0
            moves.append(copy)
        return moves

    def __str__(self):
        return f"{self.list[0]} {self.list[1]} {self.list[2]}" + "\n" + f"{self.list[3]} {self.list[4]} {self.list[5]}" + "\n" + f"{self.list[6]} {self.list[7]} {self.list[8]}"

    # Findet vertauschungsärmsten Weg von start zu perf und gibt diesen falls gewollt aus. Gibt Liste aller Positionen von start --> perf zurück
    def find_opt_moves(start, output=True):
        moves = [Field(start)]
        # A* Algorithmus
        while 1:
            min = moves[0]
            for i in moves:
                if i < min:
                    min = i
            min.count += 1
            new_parent = min.parent
            new_parent.append(min.list)
            for j in min.pos_moves():
                a = Field(j, new_parent, min.count)

                if a not in moves:
                    moves.append(a)
            # Abbruchkriterium
            if min.list == Field.perf:
                cur_dex = len(min.parent) - 1
                # Die while Schleife sortiert alle Positionen, die kein Teil des Lösungsweges sind aus
                while 1:
                    if min.parent[cur_dex] == start:
                        break
                    if min.parent[cur_dex - 1] not in Field(min.parent[cur_dex]).pos_moves():
                        min.parent.pop(cur_dex - 1)
                        cur_dex -= 1
                    else:
                        cur_dex -= 1
                if output:
                    for i in min.parent:
                        print(f"{i[0]} {i[1]} {i[2]}")
                        print(f"{i[3]} {i[4]} {i[5]}")
                        print(f"{i[6]} {i[7]} {i[8]}")
                        print()
                    print(f"Es werden {len(min.parent)} Schritte benötigt")
                break
            moves.remove(min)
        return min.parent

    # Funktion um Startliste mit perm zufälligen Vertauschungen zu generieren
    def create_start(perm=20):
        copy = Field.perf.copy()
        for i in range(perm):
            copy = Field(copy).pos_moves()
            copy = copy[r.randrange(0, len(copy))]
        return copy

# Testen
if __name__ == "__main__":
    start = [3, 0, 6,
             2, 1, 8,
             4, 5, 7]
    t0 = t.time()
    # start = Field.create_start(30)
    print("Start:\n")
    Field.find_opt_moves(start)
    print(f"Benötigte Zeit: {t.time() - t0} Sekunden")
