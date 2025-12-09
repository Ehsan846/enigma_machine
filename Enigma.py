from EnigmaConstants import ROTOR_PERMUTATIONS, ALPHABET, REFLECTOR_PERMUTATION

#returns the index of the letter 
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
        #Forstår ikke denne del
        for key in range(len(self.permutation)):
            self.inv_permutation[self.permutation[key]] = key

    def get_offset(self):
        return self.offset

    #Encryption function. Returns the index of the encrypted letter
    def pass_through(self, key, forward):
        permutation = self.permutation if forward else self.inv_permutation
        return (permutation[(key + self.offset) % len(permutation)] - self.offset) % len(permutation)

    def advance(self):
        r = False
        self.offset += 1
        if self.offset == len(self.permutation):
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
        # Self.rotors has the length 3
        # reversed order is fast, midium, slow 

        #From left to right
        # The input key goes through the fast, midium and slow rotor, updating the variable key itself. at last we take this  
        for i in reversed(range(len(self.rotors))):
            key = self.rotors[i].pass_through(key, True)
            #Pass it through the reflector permutation, by find the the element in the reflector at the corresponding index of our key. So it basically finds the letter that sits above it if you imagine the two lists over each other.
        key = list(map(letter_to_number, REFLECTOR_PERMUTATION))[key]

        #From right to left
        #Now that it has passed through the reflector it goes through the reflectors again, but this time it goes through the slow, medium and at last the fast one. 
        for i in range(len(self.rotors)):
            key = self.rotors[i].pass_through(key, False)
        #We have returned the final key.
        return key


    def key_pressed(self, letter):
        '''Updates the Enigma Machine when a key is pressed.
        It advances the rotor and updates that a key is pressed.
        '''
        #Start with the index of the fast rotor (2)
        i = len(self.rotors) - 1
        #if the methode advance returns true, and we havnt hit rotor slow, change the rotor to medium.
        while self.rotors[i].advance() and i >= 0:
            i -= 1
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
    #Rotors is the initial settigs. Ex: A C D

    #Thinking process:
    #I need to initialize the rotors offset. 
    # So i need to convert the letter to the ord value, and set it to the offset for the given rotor.
    # Also i need to go through the letters in message and set them to True in  key_pressed function
    # I also need to return the encrypted letter 
    # Since i have multiple letters i have to store them, so ill create a variable where i concatinate the encrypted letters
    def encrypt_message(self,rotors:str,message:str)-> str:
        #You need to write this
        output = ""
        self.rotors[2].offset = ord(rotors[0])
        self.rotors[1].offset = ord(rotors[1])
        self.rotors[0].offset = ord(rotors[2])

        for i in message:
            self.key_pressed(i)
            #The encrypt function takes an integer as an input not a str, so i am getting an ValueError message. If i use the already existing function letter_to_number it will be fixed
            #Temp is apparently a map object, (touple). I am getting a TypeError, because i am trying to concatinate a touple with a string.
            # Ill use list() to convert it to a list
            
        message_numbers = list(map(letter_to_number, message))

        for numbers in message_numbers:
            temp = number_to_letter(self.encrypt(numbers))
            output = output + temp

        print(output)
        return output



def enigma():
    model = EnigmaModel()
    model.key_pressed('A')
    model.encrypt_message("ABC","JJHHSSAAEE")


# Startup code
if __name__ == "__main__":
    enigma()
