from dataclasses import dataclass
from enum import Enum


class Operation(Enum):
    PLUS = (0,)
    MULT = (1,)
    SQUARE = 2


@dataclass
class MonkeyInstruction:
    op: Operation
    by: int  # mult or add by
    divisibleBy: int
    gotoTrue: int  # monkey to go to
    gotoFalse: int


AllMonkeyInstructions = list[MonkeyInstruction]
Items = list[list[int]]  # all pending items per monkey


def getline(line: str, startingStr: str) -> str:
    startingStr += " "
    assert line.startswith(startingStr)
    return line[len(startingStr) :].strip()


def readfile(filename: str) -> tuple[list[MonkeyInstruction], Items]:
    items = []
    monkeys: list[MonkeyInstruction] = []
    i = 0
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            assert line == f"Monkey {i}:"
            startingItemsStrList = getline(next(f), "  Starting items:").split(",")
            startingItems = [int(x) for x in startingItemsStrList]
            items.append(startingItems)

            operationStr = getline(next(f), "  Operation: new = old")
            assert operationStr[0] in "+*"
            op = (
                Operation.SQUARE
                if operationStr[2:] == "old"
                else (Operation.MULT if operationStr[0] == '*' else Operation.PLUS)
            )

            by = int(operationStr[2:]) if op != Operation.SQUARE else 0

            divisibleBy = int(getline(next(f), "  Test: divisible by"))

            gotoTrue = int(getline(next(f), "    If true: throw to monkey"))
            gotoFalse = int(getline(next(f), "    If false: throw to monkey"))
            assert gotoTrue != i and gotoFalse != i

            instruction = MonkeyInstruction(op, by, divisibleBy, gotoTrue, gotoFalse)
            monkeys.append(instruction)
            i += 1
        return monkeys, items

modulo = 2*3*5*7*11*13*17*19

def execute_round(monkeys: AllMonkeyInstructions, items: Items, items_inspected: list[int], applyDivBy3: bool) -> Items:
    for i, queue in enumerate(items):
        m = monkeys[i]
        for old in queue:
            items_inspected[i] += 1
            match m.op:
                case Operation.PLUS:
                    new = old + m.by
                case Operation.MULT:
                    new = old * m.by
                case Operation.SQUARE:
                    new = old * old
            new = new // 3 if applyDivBy3 else new
            new = new % modulo
            throwsTo = m.gotoTrue if (new % m.divisibleBy) == 0 else m.gotoFalse
            #print(f'Monkey {i} throws item {old} -> {new} to monkey {throwsTo}')
            items[throwsTo].append(new)
        items[i] = []
    return items


def print_round(items: Items) -> None:
    for i, queue in enumerate(items):
        print(f"Monkey {i}:", ",".join([str(q) for q in queue]))


def main_round1() -> None:
    monkeys, items = readfile("input.txt")
    items_inspected = [0] * len(monkeys)
    for _ in range(20):
        items = execute_round(monkeys, items, items_inspected, True)
    print_round(items)
    print('Items inspected:', items_inspected)
    items_inspected.sort(reverse=True)
    print('Result:', items_inspected[0] * items_inspected[1])

def main_round2() -> None:
    monkeys, items = readfile("input.txt")
    items_inspected = [0] * len(monkeys)
    for round in range(10_000):
        items = execute_round(monkeys, items, items_inspected, False)
    print_round(items)
    print('Items inspected:', items_inspected)
    items_inspected.sort(reverse=True)
    print('Result:', items_inspected[0] * items_inspected[1])


main_round1()
print('--- Part Two ---')
main_round2()