class Field:
    perf = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    def __init__(self, l, parent=[]):
        self.count = 0
        self.list = l
        self.metrik = 0
        self.parent = parent
        for i in range(9):
            if l[i] == 0:
                self.npos = i
            else:
                self.metrik += abs((l[i] - 1) // 3 - i // 3) + abs((l[i] - 1) % 3 - i % 3)

    def __lt__(self, o):
        if self.metrik + self.count < o.metrik + o.count:
            return True
        else:
            return False

    def pos_moves(self):
        l = []

        if self.npos + 3 <= 8:
            copy = self.list.copy()
            copy[self.npos] = copy[self.npos + 3]
            copy[self.npos + 3] = 0
            l.append(copy)
        if self.npos - 3 >= 0:
            copy = self.list.copy()
            copy[self.npos] = copy[self.npos - 3]
            copy[self.npos - 3] = 0
            l.append(copy)
        if (self.npos + 1) // 3 == self.npos // 3:
            copy = self.list.copy()
            copy[self.npos] = copy[self.npos + 1]
            copy[self.npos + 1] = 0
            l.append(copy)
        if (self.npos - 1) // 3 == self.npos // 3:
            copy = self.list.copy()
            copy[self.npos] = copy[self.npos - 1]
            copy[self.npos - 1] = 0
            l.append(copy)
        return l

    def __str__(self):
        return f"{self.list[0]} {self.list[1]} {self.list[2]}" + "\n" + f"{self.list[3]} {self.list[4]} {self.list[5]}" + "\n"+f"{self.list[6]} {self.list[7]} {self.list[8]}"


start = [4, 1, 2,
         8, 7, 3,
         0, 5, 6]
l = [Field(start)]

while 1:
    min = l[0]
    for i in l:
        if i < min:
            min = i
    min.count += 1
    new_parent = min.parent
    new_parent.append(min.list)
    for j in min.pos_moves():
        a = Field(j,new_parent)
        a.count = min.count

        if a not in l:
            l.append(a)
    if min.list == Field.perf:
        for i in min.parent:
            print(f"{i[0]} {i[1]} {i[2]}")
            print(f"{i[3]} {i[4]} {i[5]}")
            print(f"{i[6]} {i[7]} {i[8]}")
            print()
        break
    l.remove(min)




