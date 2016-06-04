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



@pytest.mark.parametrize('test_input,expected', [(Hand(hole=['5d', '3h'], flop=['As', '2c', 'Qh']), False),
                                                (Hand(hole=['Qd', 'Qh'], flop=['7s', '4c', 'Kh']), True),
                                             (Hand(hole=['8d', '2h'], flop=['4s', '6c', 'Kh'], turn=['Kd']), True),])
def test_pair(test_input, expected):
    val = (test_input.hand[0] == 'pair')
    assert val == expected



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



@pytest.mark.parametrize('test_inputs,target', [(Hand(), ('hole', 'hole')),
                                         (Hand(hole=['Ad', 'Ah']), ('flop', 'flop')),
                                         (Hand(hole=['2d', '2h'], flop=['2s', '2c']), ('flop', 'turn')),
                                         (Hand(hole=['3d', '3h'], flop=['3s', '3c', '3h']), ('turn', 'river')),
                                         (Hand(hole=['4d', '4h'], flop=['4s', '4c', '4h'], turn=['4d']), ('river', None)),
                                         ])
def test_append_hand_from_str(test_inputs, target):

    new_cards = ['9h', '10d']
    test_inputs.append(new_cards)
    if target[0]:
        assert Card('9h') in test_inputs[target[0]]
    if target[1]:
        assert Card('10d') in test_inputs[target[1]]


