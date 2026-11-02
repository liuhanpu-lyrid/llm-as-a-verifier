import llm_verifier

problem = "Write a Python function that reverses a string."

candidates = [
    "def rev(s): return s[::-1]",
    "def rev(s): return s",
    "def rev(s): return ''.join(sorted(s))",
]

result = llm_verifier.select(
    problem=problem,
    candidates=candidates,
    criteria={
        "Correctness": "Does the code correctly reverse a string?"
    },
    n_evaluations=1,
    pivots=1,
)

print("Selected candidate:", result.index)
print("Scores:", result.scores)
print("Ranking:", result.ranking)