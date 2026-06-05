from Game import Game

def run():
    print("Welcome to Battleship")
    game = Game((False, False))
    game.set_up()
    game.take_turns()

if __name__ == "__main__":
    run()