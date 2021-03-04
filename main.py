class Molecule:
    def __init__(self):
        self._atoms = {}
        self._bonds = {}

    def add_atom(self, atom, *, map_: int = None):
        if map_ is None:
            map_ = max(self._atoms, default=0) + 1
        elif not isinstance(map_, int):
            raise TypeError
        elif map_ < 1:
            raise ValueError
        elif map_ in self._atoms:
            raise KeyError

        if not isinstance(atom, Atom):
            raise TypeError
        self._atoms[map_] = atom.get_symbol()
        self._bonds[map_] = {}
        return map_  # чтобы значть что это был за атом, чтобы понять, какой это был атом, т.к. мы могли и не знать мап
        # данного атома

    def add_bond(self, map1, map2, bond):
        if not isinstance(bond, Bond):
            raise TypeError
        # есть ли в селф.атом , что map1 не равно map2, что уже есть связь м\у этими атомами, что одноатомн мол-ла
        neigh1 = self._bonds[map1]
        neigh2 = self._bonds[map2]

        if neigh1 is neigh2:  # что map1 не равно map2
            raise KeyError
        elif map1 in neigh2:  # что уже есть связь м\у этими атомами
            raise KeyError
        neigh1[map2] = bond.get_valence()
        neigh2[map1] = bond.get_valence()

    def get_atom(self, map_):
        return self._atoms[map_]

    def get_bonds(self):
        return self._bonds

    def get_atoms(self):
        return self._atoms

    def del_bond(self, map1, map2):
        del self._bonds[map1][map2]
        del self._bonds[map2][map1]

    def del_atom(self, map_):
        self._atoms.pop(map_)
        nab = self._bonds.pop(map_)
        for i in nab.keys():
            self._bonds[i].pop(map_)

    def __iter__(self):
        # возвращает генератор
        return iter(self._atoms)

    def iter_bonds(self):
        return IterBonds(self._bonds)

    def iter_atoms(self):
        return IterBonds(self._atoms)

    def __contains__(self, item):
        if isinstance(item, int):
            return item in self._atoms
        elif isinstance(item, Atom):
            return item.get_symbol() in self._atoms.values()


class Atom:
    def __init__(self, isotope: int = None):
        # isotope >= 1
        if not isinstance(isotope, (int, type(None))):
            raise ValueError
        elif isinstance(isotope, int):
            if isotope < 1:
                raise TypeError
        self._isotope = isotope

    def __eq__(self, other):
        return isinstance(self, type(other)) and self._isotope == other._isotope

    def get_symbol(self):
        return self._symbol


class C(Atom):
    def __init__(self, isotope: int = None):
        super().__init__(isotope)
        self._symbol = "C"


class O(Atom):
    def __init__(self, isotope: int = None):
        super().__init__(isotope)
        self._symbol = "O"


class N(Atom):
    def __init__(self, isotope: int = None):
        super().__init__(isotope)
        self._symbol = "N"


class Cl(Atom):
    def __init__(self, isotope: int = None):
        super().__init__(isotope)
        self._symbol = "Cl"


class Bond:
    # порядок связи в инит
    def __init__(self, valence):
        if not isinstance(valence, int):
            raise TypeError
        if valence not in (1, 2, 3):
            raise ValueError
        self._valence = valence

    def get_valence(self):
        return self._valence


class IterBonds:
    def __init__(self, adj):
        self._bonds = adj

    def __iter__(self):
        seen = set()
        for map1, nb in self._bonds.items():
            for map2 in nb:
                if map2 in seen:
                    continue
                yield map1, map2
            seen.add(map1)


class IterAtoms:
    def __init__(self, adj):
        self._atoms = adj

    def __iter__(self):
        for map_, name in self._atoms.items():
            yield map_, name



ol = Molecule()
ol.add_atom(C())
ol.add_atom(C())
ol.add_atom(N())
ol.add_atom(N())
ol.add_atom(O())
ol.add_atom(O())
ol.add_atom(O(), map_=8)
print(ol.get_atoms())
ol.add_bond(1, 2, Bond(1))
ol.add_bond(2, 3, Bond(1))
ol.add_bond(3, 4, Bond(1))
ol.add_bond(3, 5, Bond(2))
ol.add_bond(6, 4, Bond(1))
ol.add_bond(6, 5, Bond(2))
print(ol.get_bonds())

carbon = C(13)
holy_carbon = C()
holy_carbon2 = C()
oxygen = O()
print(f"carbon == holy_carbon:", carbon == holy_carbon)
print(f'holy_carbon2 == holy_carbon:', holy_carbon2 == holy_carbon)
print(f"oxygen == holy_carbon2: ", oxygen == holy_carbon2)
print(f"C() in ol:", C() in ol)
print(f"Cl() in ol:", Cl() in ol)
print(f"1 in ol:", 1 in ol)
print(f"10 in ol", 10 in ol)

for i in ol.iter_bonds():
    print(i)

for i in ol.iter_atoms():
    print(i)

for i in ol:
    print(i)
