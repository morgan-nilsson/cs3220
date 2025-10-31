from src.CSPclass import CSP
from src.algorithms import AC3

# Asterisk Sudoku CSP
# ie sudoku with additional asterisk constraint
class AstSodokuCSP(CSP):
    def __init__(self, s: int, initial: dict[str, int]):
        if s <= 0:
            raise ValueError("Size must be positive")
        if s >= 27:
            raise ValueError("Size must be less than 27(I don't have enough letters!)")
            
        rows = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:s])
        columns = range(1, s + 1)

        all_cells = [f"{r}{c}" for r in rows for c in columns]

        sudokuNeighbors = {}

        for cell1 in all_cells:
            sudokuNeighbors[cell1] = []
            for cell2 in all_cells:
                if cell1 != cell2:
                    sudokuNeighbors[cell1].append(cell2)

        for val in initial.values():
            if val < 1 or val > s:
                raise ValueError(f"Initial values must be between 1 and {s}")

        sudokuDomains = {var: [initial[var]] if var in initial else [ch for ch in range(1, 10)] for var in sudokuNeighbors.keys()}

        super().__init__(sudokuNeighbors.keys(), sudokuDomains, sudokuNeighbors, lambda A, a, B, b: asteriskSodokuConstraint(A, a, B, b))

        self.ac3result = AC3(self)

def asteriskSodokuConstraint(A: str, a: int, B: str, b: int) -> bool:
    if A[0] == B[0] or A[1] == B[1]:
        return a != b

    # if the cells are in the same 3x3 box
    if (ord(A[0]) - ord('A')) // 3 == (ord(B[0]) - ord('A')) // 3 and (int(A[1]) - 1) // 3 == (int(B[1]) - 1) // 3:
        return a != b

    # if the cells are in asterisk positions
    asterisk_positions = ['B5', 'C3', 'C7', 'E2', 'E5', 'E8', 'G3', 'G7', 'H5']
    if A in asterisk_positions and B in asterisk_positions:
        return a != b

    return True
