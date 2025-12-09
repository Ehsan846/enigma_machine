from EnigmaConstants import ROTOR_PERMUTATIONS, ALPHABET, REFLECTOR_PERMUTATION


def letter_to_number(letter):
    '''Convert a char to a number
    >>> letter_to_number('A')
    0
    >>> letter_to_number('B')
    1
    >>> letter_to_number('Z')
    25
    '''
    return ord(letter) - ord('A')

def number_to_letter(number):
    '''Convert a number to a letter
    >>> number_to_letter(0)
    'A'
    >>> number_to_letter(1)
    'B'
    >>> number_to_letter(25)
    'Z'
    '''
    return ALPHABET[number]

class EnigmaRotor:
    def __init__(self, permutation):
        '''Enigma Rotor. It takes a permutation.
        Implements a function to pass a letter through forwards and backwards.
        Also functions to advance the rotor and get its offset from its initial position.
        >>> rotor = EnigmaRotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ")

        >>> rotor.pass_through(0, True)
        4
        >>> rotor.pass_through(1, True)
        10
        >>> rotor.pass_through(0, False)
        20
        >>> rotor.get_offset()
        0
        >>> rotor.advance()
        False
        >>> rotor.get_offset()
        1
        >>> for _ in range(24):
        ...     _ = rotor.advance()
        >>> rotor.advance()
        True
        >>> rotor.get_offset()
        0
        '''
        self.offset = 0
        self.permutation = list(map(letter_to_number, permutation))
        self.inv_permutation = [0 for _ in range(len(permutation))]
        for key in range(len(self.permutation)):
            self.inv_permutation[self.permutation[key]] = key

    def get_offset(self):
        return self.offset

    def pass_through(self, key, forward):
        permutation = self.permutation if forward else self.inv_permutation
        return (permutation[(key + self.offset) % len(permutation)] - self.offset) % len(permutation)

    def advance(self):
        r = False
        self.offset += 1
        if self.offset >= len(self.permutation):
            r = True
            self.offset = 0
        return r

class EnigmaModel:

    def __init__(self):
        """Creates a new EnigmaModel with no views."""
        self.pressed_keys = [False for _ in range(len(ALPHABET))]
        self.lamps_on     = [False for _ in range(len(ALPHABET))]
        self.rotors = list(map(EnigmaRotor, ROTOR_PERMUTATIONS))


    def update(self):
        """Sends an update request to all the views.
        And encrypts every pressed key.
        """
        for i in range(len(self.lamps_on)):
            self.lamps_on[i] = False
        for key, is_on in enumerate(self.pressed_keys):
            if is_on:
                self.lamps_on[self.encrypt(key)] = True


    def is_key_down(self, letter):
        '''Returns whether a key is pressed down.
        '''
        key = letter_to_number(letter)
        return self.pressed_keys[key]

    def is_lamp_on(self, letter):
        '''Returns whether a lamp is on.
        '''
        key = letter_to_number(letter)
        return self.lamps_on[key]

    def encrypt(self, key):
        '''Encrypts a letter passing it through every rotor and the reflector.
        '''
        for i in reversed(range(len(self.rotors))):
            key = self.rotors[i].pass_through(key, True)
        key = list(map(letter_to_number, REFLECTOR_PERMUTATION))[key]
        for i in range(len(self.rotors)):
            key = self.rotors[i].pass_through(key, False)
        return key

    def key_pressed(self, letter):
        '''Updates the Enigma Machine when a key is pressed.
        It advances the rotor and updates that a key is pressed.
        '''
        i = len(self.rotors) - 1
        while self.rotors[i].advance() and i >= 0:
            i -= 1
        self.pressed_keys[letter_to_number(letter)] = True
        self.update()

    def key_released(self, letter):
        '''Updates the Enigma Machine when a key is pressed.
        It updates that a key is released.
        '''
        self.pressed_keys[letter_to_number(letter)] = False
        self.update()

    def get_rotor_letter(self, index):
        '''Gets the offset for a rotor at a specific index.
        '''
        rotor = self.rotors[index]
        index = rotor.get_offset()
        return ALPHABET[index]

    def rotor_clicked(self, index):
        '''Advance a rotor.
        '''
        self.rotors[index].advance()
        self.update()

def enigma():
    model = EnigmaModel()
    model.key_pressed('A')


# Startup code
if __name__ == "__main__":
    enigma()
