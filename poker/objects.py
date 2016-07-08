from collections import OrderedDict, Counter
from itertools import groupby
from operator import itemgetter
import itertools
import warnings

from poker.constants import possible_hands


class Deck(list):
    num_decks = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for n in range(self.num_decks):
            for face in Card.faces:
                for suit in Card.suits:
                    self.append(Card(face=face, suit=suit))


class Card:
    faces = [(str(x), x) for x in range (1, 11)]
    faces.extend([('J', 11), ('Q', 12), ('K', 13), ('A', 14)])
    faces = OrderedDict(faces)
    suits = OrderedDict([('d', 'diamonds'), ('h', 'hearts'),
                         ('s', 'spades'), ('c', 'clubs')])

    def __init__(self, face, suit=None):

        if face and suit:
            self.face = face
            self.suit = suit
        else:
            self.face, self.suit = self._from_str(face)

    def _from_str(self, string):
        suit = string[-1]
        face = string[:-1]
        return face, suit

    def __repr__(self):
        return '<Card: %s of %s>' % (self.face, self.suits[self.suit])

    def __lt__(self, other):
        return int(self) < int(other)

    def __int__(self):
        return self.faces[self.face]

    def __eq__(self, other):
        this = '%s%s' % (self.face, self.suit)
        other = '%s%s' %(other.face, other.suit)
        return this == other

class Hand(dict):
    phases = ['hole', 'flop', 'turn', 'river']
    maxes = {'hole': 2, 'flop': 3, 'turn': 1, 'river': 1}
    _hand = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hole = []

        for obj in self.phases:
            if obj in kwargs.keys():
                if kwargs[obj]:
                    if type(kwargs[obj][0]).__name__ == 'Card':
                        self[obj] = [x for x in kwargs[obj]]

                    elif type(kwargs[obj]) is list:
                        self[obj] = [Card(x) for x in kwargs[obj]]
                    else:
                        self[obj] = Card(kwargs[obj])
                else:
                    self[obj] = []
            else:
                self[obj] = []

    def append(self, cards):
        if type(cards) is not list:
            cards = [cards]

        for card in cards:
            phase = self.get_phase()
            if phase:
                if type(card).__name__ != 'Card':
                    card = Card(card)
                self[phase].append(card)
            else:
                warnings.warn('Hand full!! %s not added'%card, Warning)


    def get_phase(self ):
        cards = self._consolidate()
        #print('CARDS', cards)
        count = len(cards)

        if count < 2:
            return 'hole'
        elif count < 5:
            return 'flop'
        elif count < 6:
            return 'turn'
        elif count < 7:
            return 'river'
        else:
            return None

    def calc_outs(self, players=False):
        deck = Deck()
        if players:
            table = self._consolidate(outs=True)
            for card in self.hole:
                deck.remove(card)
        else:
            table = self._consolidate()

        for card in table:
            deck.remove(card)

        combinations = itertools.combinations(deck, 7-len(table))
        outs = [Hand(hole=self.hole, flop=self.flop, turn=self.turn,
                     river=self.river, fill=x) for x in combinations]

        bests = [(x, self._get_best(x.make_hand()[1])) for x in outs]

    @property
    def hand(self):
        if not self._hand:
            self._hand = self.make_hand()[0]
        return self._hand

    def make_hand(self):
        hand = self._consolidate()
        pair = self._pair(hand)
        if pair:
            two_pair = self._two_pair(hand)
            three_of = self._three_of_a_kind(hand)
        else:
            two_pair = []
            three_of = []

        if three_of:
            four_of = self._four_of_a_kind(hand)
            full_house = self._full_house(hand)
        else:
            four_of = []
            full_house = []

        straight = self._straight(hand)
        flush = self._flush(hand)

        if flush and straight:
            if all([x==y for x, y in zip(flush, straight)]):
                straight_flush = flush
            else:
                straight_flush = []
        else:
            straight_flush = []

        if straight_flush:
            if sorted(straight_flush)[-1].face == 'A':
                royal_flush = straight_flush

            else:
                royal_flush = []
        else:
            royal_flush = []

        result = {
                  'pair': pair,
                  'two_pair': two_pair,
                  'three_of': three_of,
                  'straight': straight,
                  'flush': flush,
                  'full_house': full_house,
                  'four_of': four_of,
                  'straight_flush': straight_flush,
                  'royal_flush': royal_flush,
                  'high':hand}

        best = self._trim(self._get_best(result), hand)

        return best, result

    def _trim(self, best, hand):
        for card in best[1]:
            hand.remove(card)

        #TODO write test for this logic
        needed = 5 - len(best[1])
        if needed < 0:
            return (best[0], sorted(best[1])[-5:])
        elif needed == 0 or len(hand) == 0:
            return best
        elif len(hand) <= needed:
            best[1].extend(hand)
            return best
        else:
            best[1].extend(sorted(hand)[-needed:])
            return best

        return best

    def _get_best(self, hands):
        for hand in reversed(possible_hands):
            if hands[hand]:
                return (hand, hands[hand])

        return ('high', None)

    def _high(self, hand):
        pass

    def _consolidate(self, outs=False):
        full_hand = []
        phases = self.phases
        if outs:
            phases.remove('hole')
        for phase in phases:
            cards = self[phase]
            if cards:
                for card in cards:
                    full_hand.append(card)

        return full_hand

    def _full_house(self, hand):

        three = self._three_of_a_kind(hand)
        two = self._two_pair(hand)

        if three and two:
            if len(two) < 4:
                return []
            else:
                highest = sorted(three)[-1]
                cut_three = [x for x in three if x.face == highest.face]
                cut_twos = [x for x in two if x.face != highest.face]

                if len(cut_twos) > 0:
                    cut_three[-3:].extend(sorted(cut_twos)[-2:])
                    return cut_three
                else:
                    return []

    def _pair(self, hand):
        faces = [card.face for card in hand]
        dups = [item for item, count in Counter(faces).items() if count > 1]
        return [card for card in hand if card.face in dups]

    def _two_pair(self, hand):
        result = self._pair(hand)
        if len(result) >= 4:
            return result
        else:
            return []

    def _three_of_a_kind(self, hand):
        faces = [card.face for card in hand]
        dups = [item for item, count in Counter(faces).items() if count > 2]
        return [card for card in hand if card.face in dups]

    def _straight(self, hand):
        hand = sorted(hand)

        for k, g in groupby(enumerate(hand), lambda ix: int(ix[0])-int(ix[1])):
            sequence = list(map(itemgetter(1), g))
            if len(sequence) >= 5:
                break
            else:
                sequence = []
        if not sequence:
            return sequence
        else:
            return sequence[-5:]

    def _flush(self, hand):
        suits = [card.suit for card in hand]
        dups = [item for item, count in Counter(suits).items() if count > 4]
        cards = sorted([card for card in hand if card.suit in dups])[-5:]
        return cards

    def _four_of_a_kind(self, hand):
        faces = [card.face for card in hand]
        dups = [item for item, count in Counter(faces).items() if count > 3]
        cards = [card for card in hand if card.face in dups]
        return cards

    def _straight_flush(self):
        pass

    def _royal_flush(self):
        pass

    def __lt__(self, other):
        this_rank = possible_hands.index(self.hand[0])
        other_rank = possible_hands.index(other.hand[0])
        if this_rank == other_rank:
            for this, o in reversed(list(zip(sorted(self.hand[1]),
                                             sorted(other.hand[1])))):
                if this < o:
                    return True
            return False
        else:
            return this_rank < other_rank


if __name__ == '__main__':


    h = Hand(hole=['10h', 'Jh'], flop=['Qh', 'Kh', 'Ah'], turn=['1h'])
    #h1
    h2 = Hand(hole=['5h', '6d'], flop=['7d', '8c', '9h'])

    print(h.make_hand())
    print(h2.make_hand())
