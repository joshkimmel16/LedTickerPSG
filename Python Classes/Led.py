from Matrix import Matrix

#class to facilitate data transmission to LED board
class Led(object):

    #constructor
    def __init__(self, message, height, length, char_map):

        #validate inputs
        if (not type(message) is str or not type(height) is int or height <= 0 or not type(length) is int or length <=0 or not type(char_map) is dict):
            raise LedError("At least one invalid input")
        
        self.message = message
        self.end = True

        self.board_height = height
        self.board_length = length
        self.char_map = char_map

    #compute substring of message that will fit on board based on current position in message
    #CURRENTLY DOES NOT ISOLATE BY WORD
    def compute_sub_message (position):

        #validate inputs
        if ((not type(position) is int) or position < 0 or position > self.message.length-1):
            raise LedError("Invalid position")
        
        target_length = self.board_length - 2
        current_length = 0
        result = ""
        for char in s[position : len(s)]:
            if ((current_length + self.char_map[char].n) > target_length):
                return (result, position)
            else:
                result += char
                current_length += self.char_map[char].n
            position += 1
        if (position == len(s))
            self.end = True
        else
            self.end = False
        return (result, position)

    #given an input string, compute its LED matrix equivalent (with padding pixels on either side)
    def compute_led_screen (text):

        #validate inputs
        if (not type(text) is str):
            raise LedError("Only message strings are supported")
        
        #pad 1 pixel left
        output = Matrix(self.board_height, 1)

        for char in text:
            addition = self.char_map[char]
            output.concatenate(addition)

        #pad 1 pixel right
        output.concatenate(Matrix(self.board_height, 1))

        return output

        
class LedError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
     
        
