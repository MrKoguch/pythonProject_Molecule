class Molecule:
    def __init__(self):
        self._atoms = {}
        self._bonds = {}

    def add_atom(self, atom: str, *, map_: int = None):
        if map_ is None:
            map_ = max(self._atoms, default=0) + 1
        elif not isinstance(map_, int):
            raise TypeError
        elif map_ < 1:
            raise ValueError
        elif map_ in self._atoms:
            raise KeyError

        if not isinstance(atom, str):
            raise TypeError
        elif atom.upper() not in ("C", "N", "CL", "F", "BR", "S", "O", "I"):
            raise ValueError
        self._atoms[map_] = atom.upper()
        self._bonds[map_] = {}
        return map_  # чтобы значть что это был за атом, чтобы понять, какой это был атом, т.к. мы могли и не знать мап
        # данного атома

    def add_bond(self, map1, map2, bond):
        if not isinstance(bond, int):
            raise TypeError
        if bond not in (1, 2, 3):
            raise ValueError

        # есть ли в селф.атом , что map1 не равно map2, что уже есть связь м\у этими атомами, что одноатомн мол-ла
        neigh1 = self._bonds[map1]
        neigh2 = self._bonds[map2]

        if neigh1 is neigh2:  # что map1 не равно map2
            raise KeyError
        elif map1 in neigh2:  # что уже есть связь м\у этими атомами
            raise KeyError
        neigh1[map2] = bond
        neigh2[map1] = bond

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

# ________________________________________HW 05.03.2021_____________________________________________
class IterBonds:
    def __init__(self, _bonds):
        self._bonds = _bonds

    def __iter__(self):
        seen = set()
        for map1, nb in self._bonds.items():
            for map2 in nb:
                if map2 in seen:
                    continue
                yield map1, map2
            seen.add(map1)

    def __contains__(self, q):
        if isinstance(q, int):
            return q in self._atoms  # выдает № in m true or false
        elif isinstance(q, Atom):
            return q in self._atoms.values()  # q == a
        else:
            raise TypeError


class Atom:
    def __init__(self, isotope=None):
        self._isotope = isotope

    def __eq__(self, other):  # проверяем являемся тем же или ниже по цепи наследования
        return isinstance(self, type(other)) and self._isotope == other._isotope


class C(Atom):
    def __init__(self, atom="C", isotope=None):
        self._isotope = isotope
        self._atom = atom


class Bond:
    def __init__(self, bond=None):
        self._bond = bond


class DoubleBond(Bond):
    def __init__(self, bond=2):
        self._bond = bond


class IterAtoms:
    def __init__(self, _atoms):
        self._atoms = _atoms

    def __iter__(self):
        seen = set()
        for atom, el in self._atoms.items():
            if atom in seen:
                continue
            yield atom, el

    def __contains__(self, atom, el):
        if isinstance(atom, int) and isinstance(el, Atom):
            return atom, el in self._atoms.items()
        else:
            raise TypeError

ol = Molecule()
ol.add_atom("C")
ol.add_atom("c")
ol.add_atom("N")
ol.add_atom("n")
ol.add_atom("O")
ol.add_atom("O")
ol.add_atom("o", map_=8)
print(ol.get_atoms())
ol.add_bond(1, 2, 1)
ol.add_bond(2, 3, 1)
ol.add_bond(3, 4, 1)
ol.add_bond(3, 5, 2)
ol.add_bond(6, 4, 1)
ol.add_bond(6, 5, 2)
print(ol.get_bonds())
bonds = IterBonds(ol._bonds)
for bond in bonds:
    print(bond)
atoms = IterAtoms(ol._atoms)
for atom in atoms:
    print(atom)

# # for i in ol.iter_bonds():
# #     print(i)
# x = ol.iter_bonds()
# while True:
#     try:
#         n = next(x)
#     except StopIteration:
#         break
#     else:
#         print(n)
