import re
from pathlib import Path
from pprint import pprint

ifile = Path("inputs/input1.txt")
with open(ifile, "r", encoding="utf-8") as f_in:
    text = f_in.read()


numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
num2regx = {value: re.compile(num) for value, num in enumerate(numbers, start=1)}

lines = text.split("\n")

# behold inefficiency -- regexes cannot be used because of shared characters
start = 0

while start < len(text):
    for num in numbers:
        if text[start : start + len(num)] == num:
            text = text[:start] + num2ind[num] + text[start + len(num) :]
            break
    start += 1

print(text)

# same as before now
total = sum(
    map(lambda x: int(f"{x[0]}{x[-1]}"), re.sub(r"[a-z]", "", text).split("\n")[:-1])
)
print(total)
