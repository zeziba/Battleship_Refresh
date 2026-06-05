from random import randint

board = []
boats = []
guesses = []
sunk_boats = []
board_size = 10
boat_sizes = [2, 3, 3, 4, 5]
turns = 25

# Create the board
for x in range(0,board_size):
    board.append(['0']*board_size)

# Clean up the formatting, and print board
def print_board(board):
    for row in board:
        print " ".join(row)
    
print_board(board)

# Create a random row position on the board
def random_row(board):
    return randint(0, len(board) - 1)

# Create a column position on the board     
def random_col(board):
    return randint(0, len(board[0]) - 1)

# Create a single boat
def generate_boat(size):
    
    # Generate a 0 for horizontal boat, 1 for a vertical boat
    position = randint(0,1)
    
    # Holds the position of the generated boat in a string
    single_boat = []
    
    # Generate random boat starting position
    row_pos = random_row(board)
    col_pos = random_col(board)
    
    # Creates a boat based on size of the boat and direction
    if position == 1 and (len(board) - 1 - row_pos) >= size:
        for x in range(0,size):
            single_boat.append([row_pos, col_pos])
            row_pos += 1
            
    elif position == 1 and (len(board) - 1 - row_pos) < size:
        for x in range(0,size):
            single_boat.append([row_pos, col_pos])
            row_pos -= 1
            
    elif position == 0 and (len(board[0]) - 1 - col_pos) >= size:
        for x in range(0,size):
            single_boat.append([row_pos, col_pos])
            col_pos += 1
            
    else:
        for x in range(0,size):
            single_boat.append([row_pos, col_pos])
            col_pos -= 1
    return single_boat

# Checks to make sure boats don't overlap
def boat_check(size):
    x = size
    one_boat = generate_boat(x)
    # print one_boat
    # Compares value in generated boat to values in boat string
    for val in one_boat:
        # print val
        if val in boats or val < 0:
            # If value exists, clear the one_boat string and recreate another boat
            one_boat[:] = []
            one_boat = boat_check(x)
    else:
        # If no duplicates, return the single boat string
        return one_boat

def create_boats(sizes):
    for val in sizes:
        # Doesn't generate a new boat until it passes the boat check
        boats.extend(boat_check(val))

create_boats(boat_sizes)

# print boats

# Function that determines which boat was hit

boat_data = {"PT Boat": 2,
             "Destroyer": 3, "Submarine": 3,
             "Battleship": 4, "Carrier": 5}
hit_cords = []

def get_cord(valid=False):
    while not valid:
        try:
            cord = int(raw_input("Pick a number 1-10")), int(raw_input("Pick a number 1-10"))
            if 0 < (cord[0] and cord[1]) <= 10:
                valid = True
                return cord
        except ValueError:
            print("You failed to select a valid number!"

def boat_hit(cord_data):
    if cord_data[0] in ship_data[cord_data[1]]:

def fire_shot():



        
for turn in range(turns):
    if len(sunk_boats) == 5:
        print "You Win The Game!"
        break
    else:
        print "Turn", turn + 1
        print "Type '1000' if you want to end the game early"
    # User makes a guess. If user enters nothing, value is -1
    guess_row = int(raw_input("Guess the row:") or -1) 
    guess_col = int(raw_input("Guess the column:") or -1) 
    
    # Catches errors if user doesn't guess, or guesses below 0
    if guess_row < 0 or guess_col < 0:
        print "You have to guess both a row and a column"
    
    # End the game early
    elif guess_row == 1000 or guess_col == 1000:
        print "You lose."
        break
        
    # Checks to see if guess already exists in guesses string
    elif [guess_row, guess_col] in guesses:
        print "You guessed that already"
    
    # Checks to see if guess is on the board
    elif guess_row > len(board) or guess_col > len(board[0]):
        print "That's not on the board"
    
    # If no errors are found with guess, this will run    
    else:
        # If guess exists in boat string, change board position to X
        if [guess_row, guess_col] in boats:
            board[guess_row][guess_col] = "X"
            # Assigns hit location to a variable
            hit = boats.index([guess_row, guess_col])
            # print hit
            # runs hit location through boat_hit function to see which boat was hit
            boat_hit(hit)
            # Assigns guess to guesses string
            guesses.append([guess_row,guess_col])
            
        else:
            print 'Miss'
            board[guess_row][guess_col] = "M"
            guesses.append([guess_row, guess_col])
        print_board(board)
        print "You have guessed", guesses