from Game import Game, Difficulty


def run():
    print("Welcome to Battleship")
    game = Game((Difficulty.MEDIUM, Difficulty.MEDIUM))
    game.set_up()
    game.take_turns()


if __name__ == "__main__":
    run()
