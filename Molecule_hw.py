class Molecule:
    def __init__(self):
        self._atoms = {}
        self._bonds = {}

    def add_atom(self, atom, *, map_=None):
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
        # elif atom not in ('C', 'N', 'Cl', 'Br', 'F', 'I', 'O', 'S'):
        #     raise ValueError
        self._atoms[map_] = atom.get_symbol()
        self._bonds[map_] = {}

    def add_bond(self, map1, map2, bond):
        if not isinstance(bond, Bond):
            raise TypeError
        # if bond not in (1, 2, 3):
        #     raise ValueError
        # есть ли в селф.атом , что мап1 не равно мап2, что уже есть связь м\у этими атомами, что одноатомн мол-ла
        neigh1 = self._bonds[map1]
        neigh2 = self._bonds[map2]

        if neigh1 is neigh2:  # что мап1 не равно мап2
            raise KeyError
        if map1 in neigh2:  # что уже есть связь м\у этими атомами
            raise KeyError
        # neigh1[map2] = bond
        # neigh2[map1] = bond
        neigh1[map2] = bond.get_valence()
        neigh2[map1] = bond.get_valence()

    def print_atom(self):
        return self._atoms

    def print_bond(self):
        return self._bonds

    # добавить метод : del_atom(map_), del_bond(map1, map2)
    def dell_atom(self, map_):
        self._atoms.pop(map_)  # удаляет атом по номеру, если есть в словаре
        for neigh in self._bonds[map_]:
            self._bonds[neigh].pop(map_)

    def dell_bond(self, map1, map2):
        del self._bonds[map1][map2]
        del self._bonds[map2][map1]

    def __iter__(self):
        # возвращает генератор
        return iter(self._atoms)

    # def iter_bonds(self):
        # должен быть генератором возвращающим пару (1,2) (2,1)
        # for atom, neighbors_dict in self._bonds.items():
        #     for neighbor, bond in neighbors_dict.items():
        #         yield atom, neighbor, bond
        # seen = set()
        # for map1, nb in self._bonds.items():
        #     for map2 in nb:
        #         if map2 in seen:
        #             continue
        #         yield map1, map2
        #     seen.add(map1)

    def iter_bonds(self):
        return IterBonds(self._bonds)

    def iter_atom(self):
        return IterAtom(self._atoms)
    def __contains__(self, item):
        if isinstance(item, int):
            return item in self._atoms
        elif isinstance(item, str):
            return item in self._atoms.values()

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

class IterAtom:
    def __init__(self, adj):
        self._atom = adj

    def __iter__(self):
        for map_, atom in self._atom.items():
            yield map_, atom


class Atom:
    def __init__(self, isotope: int = None):
        if not isinstance(isotope, (int, type(None))):
            raise ValueError
        elif isinstance(isotope, int):
            if isotope < 1:
                raise TypeError
        self._isotope = isotope
    def __eq__(self, other):
        return isinstance(self, type(other)) and self._isotope == other._isotope

    def get_symbol(self):
        if not isinstance(self._symbol, str):
            raise TypeError
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
    # порядок связи в init
    def __init__(self, val):
        if not isinstance(val, int):
            raise TypeError
        if val not in (1, 2, 3):
            raise ValueError
        self._val = val

    def get_valence(self):
        return self._val


mol = Molecule()
mol.add_atom(C())
mol.add_atom(C())
mol.add_atom(C())
mol.add_atom(Cl())
print(mol.print_atom())
# => {1: 'C', 2: 'C', 3: 'C', 4: 'Cl'}
mol.add_bond(1, 2, Bond(1))
mol.add_bond(2, 3, Bond(1))
mol.add_bond(1, 4, Bond(1))
print(mol.print_bond())
# => {1: {2: 1, 4: 1}, 2: {1: 1, 3: 1}, 3: {2: 1}, 4: {1: 1}}
for bonds in mol.iter_bonds():
    print(bonds)
# (1, 2)
# (1, 4)
# (2, 3)
for atoms in mol.iter_atom():
    print(atoms)
# (1, 'C')
# (2, 'C')
# (3, 'C')
# (4, 'Cl')

# mol.add_atom(atom = 'C', map_ = 1)
# mol.add_atom(atom = 'C', map_ = 2)
# mol.add_bond(1, 2, 1)
# mol.add_atom(atom = 'C', map_ = 3)
# mol.add_bond(2, 3, 1)
# mol.add_atom(atom = 'Cl', map_ = 4)
# mol.add_bond(1, 4, 1)
# print('Atoms before', mol.print_atom())
# print('Bonds before', mol.print_bond())
# mol.dell_atom(map_=8)
# print('Atoms after', mol.print_atom())
# print('Bonds after', mol.print_bond())
# print('Atoms before', mol.print_atom())
# print('Bonds before', mol.print_bond())
# mol.dell_bond(map1=1, map2=4)
# print('Atoms after', mol.print_atom())
# print('Bonds after', mol.print_bond())

