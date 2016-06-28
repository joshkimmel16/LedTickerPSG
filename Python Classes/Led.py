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

        self.led_message = self.convert_message_led()

    #compute substring of message that will fit on board based on current position in message
    #CURRENTLY DOES NOT ISOLATE BY WORD
    def compute_sub_message (position):

        #validate inputs
        if ((not type(position) is int) or position < 0 or position > len(self.message)-1):
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

    #for given input string return length of its LED matrix
    def compute_matrix_length(self, input_string):

        #validate input
        if (not type(input_string) is str or len(input_string) == 0):
            raise LedError("Input must be a non-empty string")

        length = 0
        for c in input_string:
            temp = self.char_map[c]
            if (temp):
                length += temp.n

        return length

    #get substring of message that will fit on board based on current position in message and stop at last full word that fits
    def compute_sub_message_byword (position):
        
        #validate inputs
        if ((not type(position) is int) or position < 0 or position > len(self.message)-1):
            raise LedError("Invalid position")

        target_length = self.board_length - 2
        current_length = 0
        current_word = ""
        result = ""
        for char in s[position : len(s)]:
            current_word += char
            if (char == ' '):
                if ((current_length + self.compute_matrix_length(current_word)) > target_length):
                    return (result, position+1)
                else:
                    result += current_word
                    current_length += len(current_word)
                    current_word = ""
            position += 1
        if (position == len(s))
            self.end = True
        else
            self.end = False
        return (result, position)
        

    #given an input string, compute its LED matrix equivalent (with padding pixels on either side)
    def compute_led_screen (text, padding):

        #validate inputs
        if (not type(text) is str or not type(padding) is int or padding <= 0):
            raise LedError("Only message strings are supported and padding must be a positive, non-zero integer")
        
        #pad pixels left
        output = Matrix(self.board_height, padding)

        for char in text:
            addition = self.char_map[char]
            output = output.concatenate(addition)

        #pad pixels right
        output = output.concatenate(Matrix(self.board_height, padding))

        return output

    ##### SLIDING MESSAGE FUNCTIONS #####

    #compute LED matrix corresponding to the entire message
    #any character not found in char_map is skipped
    #ASSUMPTION: height of the matrix for each char is the same and equal to height of the board
    def convert_message_led(self):

        checker = False
        output = Matrix(1,1)
        for char in self.message:
            temp = self.char_map[char]
            if (temp):
                if (checker):
                    output = output.concatenate(temp)
                else:
                    output.copy(temp)
                    checker = True
        return output

    #pad given matrix with off bits on either side
    def add_padding(self, padding, matrix):

        #validate inputs
        if (not type(padding) is int or padding <= 0 or not type(matrix) is Matrix):
            raise LedError("Invalid inputs. Padding must be a positive, non-zero integer")

        output = Matrix(matrix.m, padding)
        output = output.concatenate(matrix)
        output = output.concatenate(matrix.m, padding)

        return output

    #compute LED matrix corresponding to the longest substring in message (from the start) that will fit on the screen
    def compute_start_screen(self, padding, threshold):

        #validate inputs
        if (not type(padding) is int or padding <= 0 or not type(threshold) is int or threshold <= 0):
            raise LedError("Padding and threshold must be positive, non-zero integers")

        target_length = self.board_length - (2*padding)
        if (target_length < threshold):
            raise LedError("Padding and/or board length is insufficient to fit a reasonable number of pixels")

        output = output.concatenate(self.led_message.get_submatrix(self.board_height, target_length))
        if (target_length > output.n):
            #pad with off bits
            output = output.concatenate(Matrix(self.board_height, (target_length - output.n)))

        result = self.add_padding(padding, output)

        return (result, output, target_length)

    #compute new LED matrix by shifting current display 1 pixel to the left
    def shift_display_left(self, current_screen, position, padding):

        #validate inputs
        if (not type(current_screen) is Matrix or (not current_screen.m == self.board_height) or (not current_screen.n == self.board_length) or not type(position) is int or position < 0):
            raise LedError("Invalid inputs. Input matrix must match screen dimensions and position must be a non-negative integer")

        if (not type(padding) is int or padding <= 0):
            raise LedError("Padding must be a positive, non-zero integer")

        if (position >= self.led_message.n):
            #reached end of message
            result = None
        else:
            #shift message 1 pixel to the left
            current_screen.shift_horizontal(True, self.led_message.getcolumn(position))
            position += 1
            result = self.add_padding(padding, current_screen)

        return (result, current_screen, position)

#error class       
class LedError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
     
        
