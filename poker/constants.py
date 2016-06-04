possible_hands = ['high', 'pair', 'two_pair', 'three_of', 'straight', 'flush', 'full_house', 'four_of', 'straight_flush', 'royal_flush']

faces = [str(x) for x in range(2,11)]
faces.extend(['J', 'Q', 'K', 'A'])

suits = ['c', 's', 'd', 'h']

card_set = ['%s%s'%(f, s) for f in faces for s in suits]