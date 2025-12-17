from EnigmaConstants import ROTOR_PERMUTATIONS, ALPHABET, REFLECTOR_PERMUTATION
import time
from itertools import product

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

ALPHABET_LEN = 26

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

    #Encryption function. Returns the index of the encrypted letter
    def pass_through(self, key, forward):
        permutation = self.permutation if forward else self.inv_permutation
        return (permutation[(key + self.offset) % ALPHABET_LEN] - self.offset) % ALPHABET_LEN

    def advance(self):
        r = False
        self.offset += 1
        if self.offset >= ALPHABET_LEN:
            r = True
            self.offset = 0
        return r

class EnigmaModel:

    def __init__(self):
        """Creates a new EnigmaModel with no views."""
        self.pressed_keys = [False for _ in range(len(ALPHABET))]
        self.lamps_on     = [False for _ in range(len(ALPHABET))]
        self.rotors = list(map(EnigmaRotor, ROTOR_PERMUTATIONS))


    def set_rotors(self, setting):
        self.rotors[0].offset = letter_to_number(setting[0])
        self.rotors[1].offset = letter_to_number(setting[1])
        self.rotors[2].offset = letter_to_number(setting[2])

    def update(self):
        """Encrypts every pressed key.
        """
        for i in range(len(self.lamps_on)):
            self.lamps_on[i] = False
        for key in filter(lambda x: x, self.pressed_keys):
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
        #Start with the index of the fast rotor (2)
        i = 2
        #if the methode advance returns true, and we havnt hit rotor slow, change the rotor to medium.
        while self.rotors[i].advance() and i >= 0:
            i -= 1

        # Self.rotors has the length 3
        # reversed order is fast, midium, slow 

        #From left to right
        # The input key goes through the fast, midium and slow rotor, updating the variable key itself. at last we take this  
        key = self.rotors[2].pass_through(key, True)
        key = self.rotors[1].pass_through(key, True)
        key = self.rotors[0].pass_through(key, True)
            #Pass it through the reflector permutation, by find the the element in the reflector at the corresponding index of our key. So it basically finds the letter that sits above it if you imagine the two lists over each other.
        key = letter_to_number(REFLECTOR_PERMUTATION[key])

        #From right to left
        #Now that it has passed through the reflector it goes through the reflectors again, but this time it goes through the slow, medium and at last the fast one. 
        key = self.rotors[0].pass_through(key, False)
        key = self.rotors[1].pass_through(key, False)
        key = self.rotors[2].pass_through(key, False)
        #We have returned the final key.
        return key


    def key_pressed(self, letter):
        '''Updates the Enigma Machine when a key is pressed.
        It advances the rotor and updates that a key is pressed.
        '''
        #Change the value of the index at the lettter to True. 
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

    #Part two
    #___________________________________________________________
    
    def encrypt_message(self: object, message: str, rotors: str = None) -> str:
        """ Encrypts a sequence of letters

        >>> model = EnigmaModel()
        >>> model.encrypt_message("QQQ", "ABC")
        'BWP'
        >>> model = EnigmaModel()
        >>> model.encrypt_message("ABC", "DEF")
        'QJY'
        >>> model.encrypt_message("ABC")
        'LAH'

        Parameters
        ----------
        self: class object 
            The rotor object that contains all the methodes and different permutations
        
        message: str
            The message being encrypted. A sequence of strings.

        rotors: str
            If the rotor settings are given it will set the state of the rotors.
            Otherwise it will use the current settings.
        
        Returns
        -------
        str
            A string that consists of the encrypted message, with regards to the initialization
            of the rotors.
        """
        
        if rotors:
            assert len(rotors) == 3
            self.set_rotors(rotors)

        output = ""
        for i in message.upper():
            if i not in ALPHABET:
              output += i
              continue
            message_number = letter_to_number(i)
            message_number_encrypted = self.encrypt(message_number)
            message_letter = number_to_letter(message_number_encrypted)

            output +=  message_letter

        return output

    def find_rotors(self, message: str, cipher: str) -> str:
        """ Creates different permutations with 3 letters in the alphabet. Tries these different settings,
        and uses the one which has the correct rotor settings for encryption to get the same message. 

        Parameters
        ----------
        self: class object 
            The rotor object that contains all the methodes and different permutations
        
        message: str
            The message being encrypted. A sequence of strings.

        cipher: str
            The encrypted message from with some rotor settings.
        
        Returns
        -------
        str
            A string that consists of the the rotor settings

        Doctests:
        >>> model = EnigmaModel()
        >>> model.find_rotors("HELLO","SYBOU")
        'BFE'

        >>> model.find_rotors("Dhanyavaad", "Namaste")
        

        """
        
        message = [letter_to_number(x) for x in message]
        cipher = [letter_to_number(x) for x in cipher]
        length = len(cipher)
        for rotors in product(ALPHABET, repeat=3):
            self.set_rotors(rotors)
            for i in range(length):
                ctest = self.encrypt(message[i])
                if ctest != cipher[i]:
                    break
            else:
                return "".join(rotors)
        return None


def decrypt(cipher:str) -> str:
    """Decrypts a message that is split by spaces.

    >>> model = EnigmaModel()
    >>> model.encrypt_message("HELLO WORLD", "XYZ")
    'BPJBJ KTXOI'
    >>> decrypt('BPJBJ KTXOI')
    'HELLO WORLD'
    >>> model.encrypt_message("ASDFJKL", "XYZ")
    'RLNTOWD'
    >>> decrypt('RLNTOWD') # Doesnt return anything because its invalid


    Parameters
    ----------
    cipher: str
        The message being decrypted.

    Returns
    -------
    str
      The original message
    """
    words = open("words.txt","r").read()
    words = set(x.upper() for x in words.splitlines())

    cipher = cipher.split()
    model = EnigmaModel()
    for rotors in product(ALPHABET, repeat=3):
        model.set_rotors(rotors)
        for c in cipher:
            out = model.encrypt_message(c)
            if out not in words:
                break
        else:
            return model.encrypt_message(" ".join(cipher), rotors)





def time_decrypt():
    input = "HI MOM AND DAD WHAT THE HELL"
    model = EnigmaModel()
    asd = model.encrypt_message(input, "XYZ")
    s = time.time()
    output = decrypt(asd)
    e = time.time()
    print(e - s, output)
    assert input == output


def enigma():
    pass

# Startup code
if __name__ == "__main__":
    time_decrypt()



