from Knights import logic

# Define propositional symbols for characters A, B, and C
AKnight = logic.Symbol("A is a Knight")
AKnave = logic.Symbol("A is a Knave")

BKnight = logic.Symbol("B is a Knight")
BKnave = logic.Symbol("B is a Knave")

CKnight = logic.Symbol("C is a Knight")
CKnave = logic.Symbol("C is a Knave")

# Puzzle 0
# A says “I am both a knight and a knave.”
knowledge0 = logic.And(
    logic.Or(AKnight, AKnave),  # A is either a knight or a knave
    logic.Not(logic.And(AKnight, AKnave))  # A cannot be both a knight and a knave
)

# Puzzle 1
# A says “We are both knaves.”
# B says nothing.
knowledge1 = logic.And(
    logic.Or(AKnight, AKnave),  # A is either a knight or a knave
    logic.Or(BKnight, BKnave),  # B is either a knight or a knave
    logic.Biconditional(AKnight, logic.And(AKnave, BKnave))  # A is a knight if and only if both A and B are knaves
)

# Puzzle 2
# A says “We are the same kind.”
# B says “We are of different kinds.”
knowledge2 = logic.And(
    logic.Or(AKnight, AKnave),  # A is either a knight or a knave
    logic.Or(BKnight, BKnave),  # B is either a knight or a knave
    logic.Biconditional(AKnight, logic.Or(logic.And(AKnight, BKnight), logic.And(AKnave, BKnave))),  # A is a knight if and only if both A and B are the same kind
    logic.Biconditional(BKnight, logic.Or(logic.And(AKnight, BKnave), logic.And(AKnave, BKnight)))  # B is a knight if and only if A and B are of different kinds
)

# Puzzle 3
# A says either “I am a knight.” or “I am a knave.”, but you don’t know which.
# B says “A said ‘I am a knave.’”
# B then says “C is a knave.”
# C says “A is a knight.”
knowledge3 = logic.And(
    logic.Or(AKnight, AKnave),  # A can be either a knight or a knave
    logic.Or(BKnight, BKnave),  # B is either a knight or a knave
    logic.Or(CKnight, CKnave),  # C is either a knight or a knave

    # B's statement about A
    logic.Biconditional(BKnight, logic.Biconditional(AKnight, AKnave)),  # B is a knight if and only if A is a knave

    # B's statement about C
    logic.Biconditional(BKnight, CKnave),  # B is a knight if and only if C is a knave

    # C's statement about A
    logic.Biconditional(CKnight, AKnight)  # C is a knight if and only if A is a knight
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        for symbol in symbols:
            if logic.model_check(knowledge, symbol):
                print(f"    {symbol}: Knight")
            else:
                print(f"    {symbol}: Knave")

if __name__ == "__main__":
    main()
