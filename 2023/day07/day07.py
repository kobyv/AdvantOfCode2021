from collections import Counter
from dataclasses import dataclass


@dataclass(order=True, frozen=True, slots=True)
class Hand:
    rank: int  # output of get_card_rank (not their order)
    card: str
    bid: int


JOKER = "1"
ACE = "e"


def get_card_rank(c: str) -> int:
    l = [x for x in c]
    n = len(set(l))
    hand_type = sorted(Counter(l).values())
    match n:
        case 5:  # high card
            return 1
        case 4:  # one pair
            return 2
        case 3:  # two pair | three of a kind
            if hand_type == [1, 2, 2]:  # two pair
                return 3
            if hand_type == [1, 1, 3]:  # three of a kind
                return 4
        case 2:
            if hand_type == [2, 3]:  # full house
                return 5
            if hand_type == [1, 4]:  # four of a kind
                return 6
            assert False
        case 1:  # five of a kind
            return 7
    assert False


def get_card_rank_with_joker(c: str) -> int:
    if c == JOKER * 5:
        return 7
    l = [x for x in c]
    for pos, card_type in enumerate(c):
        if card_type == JOKER:
            counters = Counter(l)
            v = [(v, k) for k, v in counters.items() if k != JOKER]
            v.sort()
            winner_cardtype = v[-1][1]
            l[pos] = winner_cardtype
    c = "".join(l)
    n = len(set(l))
    hand_type = sorted(Counter(l).values())
    match n:
        case 5:  # high card
            return 1
        case 4:  # one pair
            return 2
        case 3:  # two pair | three of a kind
            if hand_type == [1, 2, 2]:  # two pair
                return 3
            if hand_type == [1, 1, 3]:  # three of a kind
                return 4
        case 2:
            if hand_type == [2, 3]:  # full house
                return 5
            if hand_type == [1, 4]:  # four of a kind
                return 6
            assert False
        case 1:  # five of a kind
            return 7
    assert False


hands: list[Hand] = []
with open("input.txt") as f:
    for line in f:
        card, bid = line.split()
        assert len(card) == 5
        card = (
            card.replace("T", "a")
            .replace("J", "b")
            .replace("Q", "c")
            .replace("K", "d")
            .replace("A", "e")
        )
        rank = get_card_rank(card)
        hands.append(Hand(rank, card, int(bid)))

hands.sort()
total = 0
for i, h in enumerate(hands):
    total += (i + 1) * h.bid

print(total)

# PART 2
print("--- PART 2 ---")

hands = []
with open("input.txt") as f:
    for line in f:
        card, bid = line.split()
        assert len(card) == 5
        card = (
            card.replace("T", "a")
            .replace("J", JOKER)  # joker is 1
            .replace("Q", "c")
            .replace("K", "d")
            .replace("A", ACE)
        )
        rank = get_card_rank_with_joker(card)
        hands.append(Hand(rank, card, int(bid)))
        # print(rank, card_jokered, int(bid), card)

hands.sort()
total = 0
for i, h in enumerate(hands):
    total += (i + 1) * h.bid

print(total)
