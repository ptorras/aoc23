from typing import Any, List, Tuple, Dict
from enum import Enum, auto
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint

# I think the best course of action first is creating a simple recursive descent parser
# for the input to count boxes

# This would be amazing in awk but I am on a windows machine rn


class TT(Enum):
    DIGIT = auto()
    COLOR = auto()
    NEWLINE = auto()
    COLON = auto()
    SEMICOLON = auto()
    COMMA = auto()
    GAME = auto()
    EOF = auto()


class Tokeniser:
    TOKEN_MAP = {
        "\n": TT.NEWLINE,
        ":":  TT.COLON,
        ",":  TT.COMMA,
        ";":  TT.SEMICOLON,
    }
    DIGITS = {str(x) for x in range(10)}

    @classmethod
    def tokenise(cls, in_text: str) -> List[Tuple[TT, Any]]:
        out = []
        curr = 0
        while curr < len(in_text):
            if in_text[curr] in {" "}:
                curr += 1
                continue
            elif in_text[curr] in cls.DIGITS:
                digit = in_text[curr]
                curr += 1
                while in_text[curr] in cls.DIGITS:
                    digit += in_text[curr]
                    curr += 1
                out.append((TT.DIGIT, int(digit)))
            elif in_text[curr] in {"G"}:
                out.append((TT.GAME, "Game"))
                curr += 4
            elif in_text[curr] in {"r"}:
                out.append((TT.COLOR, "red"))
                curr += 3
            elif in_text[curr] in {"g"}:
                out.append((TT.COLOR, "green"))
                curr += 5
            elif in_text[curr] in {"b"}:
                out.append((TT.COLOR, "blue"))
                curr += 4
            elif in_text[curr] in cls.TOKEN_MAP.keys():
                out.append((cls.TOKEN_MAP[in_text[curr]], in_text[curr]))
                curr += 1
            else:
                raise ValueError("IMPOSSIBLE CHARACTER")
        out.append((TT.EOF, ""))
        return out



class Parser:
    def __init__(self) -> None:
        self.tokenised: List[Tuple[TT, Any]]
        self.index: int = 0

    def _current(self) -> Tuple[TT, Any]:
        return self.tokenised[self.index]

    def _forward(self) -> Tuple[TT, Any]:
        token = self._current()
        self.index += 1
        return token

    def _previous(self) -> Tuple[TT, Any]:
        return self.tokenised[self.index - 1] 

    def parse(self, tokenised: List[Tuple[TT, Any]]) -> Dict:
        self.tokenised = tokenised
        output = {}
        while self._current()[0] != TT.EOF:
            output |= self.game()
            if self._current()[0] == TT.NEWLINE:
                self._forward()
        return output

    def game(self) -> Dict:      
        game_id = self.game_id()
        draws = []
        while self._current()[0] not in {TT.NEWLINE, TT.EOF}:
            if self._current()[0] == TT.SEMICOLON:
                self._forward()
            draws.append(self.draw())

        return {game_id: draws}

    def game_id(self) -> int:
        assert self._current()[0] == TT.GAME, f"{self._current()[0].name} is not a game token"
        self._forward()
        assert self._current()[0] == TT.DIGIT, f"{self._current()[0].name} is not a digit token"
        game_id = self._forward()
        self._forward()     # Remove the colon
        return game_id[1]

    def draw(self) -> Dict:
        draw = {}
        while self._current()[0] not in {TT.SEMICOLON, TT.NEWLINE, TT.EOF}:
            if self._current()[0] == TT.COMMA:
                self._forward()
            draw |= self.color_set()

        return draw

    def color_set(self) -> Dict:
        number = self._forward()[1]
        color = self._forward()[1]

        return {color: number}

# process
budget = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

ifile = Path("inputs/input1.txt")
with open(ifile, "r", encoding="utf-8") as f_in:
    text = f_in.read()

tokenised = Tokeniser.tokenise(text)
pprint(tokenised)

parser = Parser()
parsed = parser.parse(tokenised)

pprint(parsed)

valid = []
for game, draws in parsed.items():
    for draw in draws:
        wrong = False
        for color, allowed in budget.items():
            if color in draw and draw[color] > allowed:
                wrong = True
                break
        if wrong:
            break
    else:
        valid.append(game)
print(valid)
print(sum(valid))

