################ ENIGMA SIM ##########################
# https://www.cryptomuseum.com/crypto/enigma/wiring.htm

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class Rotor:
    def __init__(self, name, wiring, turnover, position):
        self.name = name
        self.wiring = wiring
        self.turnover = turnover
        self.notch = turnover
        self.position = position

    @property
    def turnover_index(self):
        return letters.index(self.turnover)

    @property
    def notch_index(self):
        return letters.index(self.notch)

    def set_position(self, position):
        self.position = position % 26

    def encode_forward(self, letter):
        index = (letters.index(letter) + self.position) % 26
        encoded_letter = self.wiring[index]
        return letters[(letters.index(encoded_letter) - self.position) % 26]

    def encode_backward(self, letter):
        index = (letters.index(letter) + self.position) % 26
        encoded_letter = letters[self.wiring.index(letters[index])]
        return letters[(letters.index(encoded_letter) - self.position) % 26]

    def step(self):
        self.position = (self.position + 1) % 26
        # print(f"Rotor {self.name} stepped to position: {self.position}")
        return self.position == self.turnover_index

class Reflector:
    def __init__(self, name, wiring):
        self.name = name
        self.pairs = {}
        for i in range(26):
            a = letters[i]
            b = wiring[i]
            self.pairs[a] = b
            self.pairs[b] = a

    def reflect(self, letter):
        return self.pairs.get(letter, letter)

class Plugboard:
    def __init__(self, pairs):
        self.plugboard = {}
        for pair in pairs:
            a, b = pair
            self.plugboard[a] = b
            self.plugboard[b] = a

    def swap(self, letter):
        return self.plugboard.get(letter, letter)

def enigma_encode(input_text, rotors, plugboard=None, reflector=None, positions=None):
    # check 3 rotors
    if len(rotors) != 3:
        print('3 rotors not added')
        return

    # set positions
    if positions:
        for i in range(len(rotors)):
            rotors[i].set_position(positions[i])
            
    encoded_text = ""
    for letter in input_text:
        # step the rotors, step next if turnover
        if rotors[2].step():
            if rotors[1].step():
                rotors[0].step()
        if plugboard:
            letter = plugboard.swap(letter)
            print(f"After in plugboard: \t{letter}")
        for rotor in reversed(rotors):
            letter = rotor.encode_forward(letter)
            print(f"After fwd {rotor.name}: \t{letter}")
        if reflector:
            letter = reflector.reflect(letter)
            print(f"After reflector: \t{letter}")
        for rotor in rotors:
            letter = rotor.encode_backward(letter)
            print(f"After back {rotor.name}: \t{letter}")
        if plugboard:
            letter = plugboard.swap(letter)
            print(f"After out plugboard: \t{letter}")
        encoded_text += letter
        print('--------------------------------')
    return encoded_text

def main():
    # Enigma I standard rotor turnover letters (notches)
    rotor_I = Rotor('Rotor I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q', 12)
    rotor_II = Rotor('Rotor II', 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E', 5)
    rotor_III = Rotor('Rotor III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V', 1)

    # Extra 2 rotors
    rotor_IV = Rotor('Rotor IV', 'ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J', 2)
    rotor_V = Rotor('Rotor V', 'VZBRGITYUPSDNHLXAWMJQOFECK', 'Z', 3)

    # types of reflectors: UKW-A, UKW-B, UKW-C
    reflector_A = Reflector('UKW-A', 'EJMZALYXVBWFCRQUONTSPIKHGD')
    reflector_B = Reflector('UKW-B', 'YRUHQSLDPXNGOKMIEBFZCWVJAT')
    reflector_C = Reflector('UKW-C', 'FVPJIAOYEDRZXWGCTKUQSBNMHL')

    plugboard = Plugboard(['AB', 'CD', 'HE'])

    # input_text = "HELLO"
    # print(f"Input Text: {input_text}") 
    # encoded_text = enigma_encode(input_text, [rotor_I, rotor_II, rotor_III], plugboard, reflector_B)
    # print(f"Encoded Text: {encoded_text}")

    running = True
    while running:
        input_text = input('Enter text to encode, empty to exit: ')
        if input_text != '':
            encoded_text = enigma_encode(input_text, [rotor_I, rotor_II, rotor_III], None, reflector_B, [0, 0, 0])
            print('--------------------------------')
            print(f"Input Text: \t{input_text}")
            print(f"Encoded Text: \t{encoded_text}")
            print('--------------------------------')
        else:
            print('Exiting...')
            running = False

if __name__ == "__main__":
    main()