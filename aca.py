from dataclasses import dataclass
import random
import time
import statistics

# Datos de prueba
@dataclass
class Person:
    id: int
    city: str
    exp: int
    remote: bool
    salary: int

def generate_people(n: int, seed: int = 42):
    random.seed(seed)
    cities = ["Bogotá", "Cali", "Medellín", "Barranquilla"]
    people = []
    for i in range(1, n + 1):
        people.append(Person(
            id=i,
            city=random.choice(cities),
            exp=random.randint(0, 10),
            remote=random.choice([True, False]),
            salary=random.randint(1500, 12000) * 1000
        ))
    random.shuffle(people)
    return people

# Álgebra booleana
def A(p): return p.city == "Bogotá"
def B(p): return p.exp >= 2
def C(p): return p.remote is True

def E1(p):  # (A y B) o C
    return (A(p) and B(p)) or C(p)

def de_morgan_left(p):   # NO (A y B)
    return not (A(p) and B(p))

def de_morgan_right(p):  # (NO A) o (NO B)
    return (not A(p)) or (not B(p))

# Algoritmos
def gcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return abs(a)

def insertion_sort(arr, key=lambda x: x):
    a = arr[:]
    for i in range(1, len(a)):
        current = a[i]
        j = i - 1
        while j >= 0 and key(a[j]) > key(current):
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = current
    return a

def linear_search(arr, target_id: int):
    for item in arr:
        if item.id == target_id:
            return item
    return None

def binary_search(sorted_arr, target_id: int):
    lo, hi = 0, len(sorted_arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        mid_id = sorted_arr[mid].id
        if mid_id == target_id:
            return sorted_arr[mid]
        if target_id < mid_id:
            hi = mid - 1
        else:
            lo = mid + 1
    return None

# BST (Árbol Binario de Búsqueda)
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

def bst_insert(root, key, value):
    if root is None:
        return Node(key, value)
    if key < root.key:
        root.left = bst_insert(root.left, key, value)
    elif key > root.key:
        root.right = bst_insert(root.right, key, value)
    else:
        root.value = value
    return root

def bst_search(root, key):
    while root is not None:
        if key == root.key:
            return root.value
        root = root.left if key < root.key else root.right
    return None

# Experimento básico
def run_experiment(n: int = 10_000, seed: int = 42):
    people = generate_people(n, seed=seed)

    # Validación De Morgan con datos
    de_morgan_ok = all(de_morgan_left(p) == de_morgan_right(p) for p in people)

    # Medición de filtros booleanos
    t0 = time.perf_counter()
    filtered = [p for p in people if E1(p)]
    t1 = time.perf_counter()

    # Ordenamiento built-in
    t2 = time.perf_counter()
    _ = sorted(filtered, key=lambda x: x.salary)
    t3 = time.perf_counter()

    # insertion_sort SOLO para n pequeño
    insertion_sort_s = None
    if n <= 5000:
        t2b = time.perf_counter()
        _ = insertion_sort(filtered, key=lambda x: x.salary)
        t3b = time.perf_counter()
        insertion_sort_s = t3b - t2b

    # Preparación para búsquedas por id
    sorted_by_id = sorted(people, key=lambda x: x.id)
    target = random.randint(1, n)

    t4 = time.perf_counter()
    _ = linear_search(people, target)
    t5 = time.perf_counter()

    t6 = time.perf_counter()
    _ = binary_search(sorted_by_id, target)
    t7 = time.perf_counter()

    # Construcción y búsqueda en BST
    t_build0 = time.perf_counter()
    root = None
    for p in people:
        root = bst_insert(root, p.id, p)
    t_build1 = time.perf_counter()

    t8 = time.perf_counter()
    _ = bst_search(root, target)
    t9 = time.perf_counter()

    return {
        "n": n,
        "de_morgan_ok": de_morgan_ok,
        "filter_E1_s": t1 - t0,
        "sort_builtin_s": t3 - t2,
        "insertion_sort_s": insertion_sort_s,
        "search_linear_s": t5 - t4,
        "search_binary_s": t7 - t6,
        "bst_build_s": t_build1 - t_build0,
        "search_bst_s": t9 - t8,
        "example_gcd": gcd(1071, 462)
    }

if __name__ == "__main__":
    print("Arrancó el script")

    for n in [1000, 10000, 50000]:
        r = run_experiment(n=n, seed=42)
        print(r)
