import re
from pathlib import Path

ifile = Path("inputs/input1.txt")
with open(ifile, "r", encoding="utf-8") as f_in:
    text = f_in.read()

# One liner ftw
total = sum(
    map(lambda x: int(f"{x[0]}{x[-1]}"), re.sub(r"[a-z]", "", text).split("\n")[:-1])
)
print(total)
