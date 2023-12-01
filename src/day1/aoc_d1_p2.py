import re
from pathlib import Path
from pprint import pprint

ifile = Path("inputs/input1.txt")
with open(ifile, "r", encoding="utf-8") as f_in:
    text = f_in.read()

print(text)

numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
num2int = {num: str(ind) for ind, num in enumerate(numbers, start=1)}

lines = text.split("\n")

# Highly inefficient, but gets the job done - same idea can be applied with regex

# If one were to code this in - say C - this can be computed in a single pass with an
# automaton that keeps track of the first and last parsed elements. I am writing python
# lazily, so this is as good as it gets.

# (given the scale of the problem it really does not matter)
start = 0
cleanstr = ""

while start < len(text):
    if text[start] == "\n":
        cleanstr += "\n"  # Keep the line structure
    elif text[start] in [str(x) for x in range(10)]:
        cleanstr += text[start]
    else:
        # More pythonic would be to use the in operator maybe. Idunno
        for num in numbers:
            strslice = text[start : start + len(num)]
            if strslice == num:
                cleanstr += num2int[strslice]
    start += 1

print(cleanstr)

# same as before now
total = sum(map(lambda x: int(f"{x[0]}{x[-1]}"), cleanstr.split("\n")[:-1]))
print(total)
