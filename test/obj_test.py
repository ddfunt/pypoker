import pytest
import random

from poker.objects import Card, Deck, Hand
from poker.constants import faces, suits, card_set


def fill(hand, fill_to=7):

    deck = Deck()
    for card in hand.hand[1]:
        deck.remove(card)

    for i in range(fill_to- len(hand.hand[1])):
        card = random.choice(deck)
        deck.remove(card)


@pytest.mark.parametrize("test_input", card_set)
def test_cards_from_str(test_input):
    card = Card(test_input)

    assert card.face == test_input[:-1]
    assert card.suit == test_input[-1]
    assert card.face in faces
    assert card.suit in suits


@pytest.mark.parametrize('test_input', card_set)
def test_pair(test_input):

    hand = Hand(hole=[test_input, test_input])

    assert hand.hand[0] == 'pair'
    #fill(test_input)

@pytest.mark.parametrize('test_input,expected', [(Hand(hole=['5d', '3h'], flop=['3s', '3c', '3h']), False),
                                                (Hand(hole=['Qd', 'Qh'], flop=['Ks', 'Qc', 'Kh']), True),
                                             (Hand(hole=['4d', 'Qh'], flop=['Qs', 'Qc', 'Kh'], turn=['Kd']), True),])
def test_full_house(test_input, expected):
    val = (test_input.hand[0] == 'full_house')
    assert val == expected

@pytest.mark.parametrize('test_input,expected', [(Hand(), 'hole'),
                                                 (Hand(hole=['Ad', 'Ah']), 'flop'),
                                        (Hand(hole=['2d', '2h'], flop=['2s', '2c']), 'flop'),
                                        (Hand(hole=['3d', '3h'], flop=['3s', '3c', '3h']), 'turn'),
                                        (Hand(hole=['4d', '4h'], flop=['4s', '4c', '4h'], turn=['4d']), 'river'),
                                        (Hand(hole=['5d', '5h'], flop=['As', '5c', '5h'], turn=['5d'], river=['5c']), None)])
def test_phase(test_input, expected):
    assert test_input.get_phase() == expected

if __name__ == '__main__':
    fill(Hand(hole=['Ah', 'Ad']))