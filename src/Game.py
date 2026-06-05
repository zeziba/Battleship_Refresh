from dataclasses import dataclass, field
from Logger import get_logger

import Board
import Fleet
import GameRules
import Player
import Ship
import UI
import AI

TESTING = False
logger = get_logger(__name__)


@dataclass()
class Game:
    """
    Create and maintain the differing objects to enable a game of battleship to be played.

    Objects:
        Player
        Board -> Tile
        Fleet -> Ship

    The rules of the game are "simple."
    """

    players: tuple[bool, bool]
    players_dict: dict[str, Player.Player] = field(default_factory=dict)
    state: GameRules.State = field(default=GameRules.State.STOPPED)

    def __post_init__(self):
        logger.debug("Post-init")
        self._set_up()
        self.UI = UI.UI()

    @property
    def player(self):
        for _p in self.players_dict:
            logger.info(f"yielding {_p}")
            yield self.players_dict[_p]

    def stop(self) -> None:
        self.state = GameRules.State.STOPPED
        logger.info(f"Game set to {self.state}")

    def start(self) -> None:
        self.state = GameRules.State.RUNNING
        logger.info(f"Game set to {self.state}")

    @property
    def stopped(self) -> bool:
        logger.info("Checking if game has stopped")
        return self.state == GameRules.State.STOPPED

    def _set_up(self) -> None:
        logger.info("Setting up game board")
        for index, i in enumerate(self.players):
            logger.debug(f"Attempting to init - {index}\t{i}")
            state = Player.State.AI if i is False else Player.State.PERSON
            name = f"p{index}"
            self.players_dict[name] = Player.Player(
                name, state, Board.Board(), Fleet.GeneralFleet()
            )
            logger.debug(f"Finished init of {name} as {state}")

    def _check(self, x: int, y: int, h_v: str, p: Player.Player) -> bool:
        """
        Checks if the given (x, y, h_v, p) are able to place at the given
        location and directionality
        """
        logger.info(f"Checking {p.name} at ({x}, {y}) with {h_v}")
        good_coords = not GameRules.check_xy(x, y)
        good_h_v = (h_v not in "hv") and (len(h_v) == 1)
        good_place = any(
            s.contains(px, py)
            for s in p.get_ships
            for px, py in Ship.Ship.possible_places(x, y, s.length, s.directionality)
        )
        return not (good_coords or good_h_v or good_place)

    def set_up(self) -> None:
        logger.info("Starting set-up")
        self._set_up()
        for p in self.player:
            logger.info(f"\tPlayer {p}")
            i = 0
            p.board.generate_board()
            p.fleet.generate()
            if TESTING:
                logger.info("\tTesting enabled - generic ship placement")
                for ship in p.get_ships:
                    ship.place_ship(i := i + 1, 0, p.board)
            else:
                if p.state is Player.State.AI:
                    logger.info(f"Player is {p.state} - starting fleet generation")
                    import random

                    p._ai_brain = AI.HuntAndTargetAI()
                    for ship in p.get_ships:
                        logger.debug(f"\tAttemtpting to place {ship.name}")
                        while True:
                            h_v = random.choice(["h", "v"])
                            if "h" == h_v:
                                x = random.randint(0, GameRules.SIZE - 1 - ship.length)
                                y = random.randint(0, GameRules.SIZE - 1)
                            else:
                                x = random.randint(0, GameRules.SIZE - 1)
                                y = random.randint(0, GameRules.SIZE - 1 - ship.length)
                            if self._check(x, y, h_v, p):
                                ship.directionality = (
                                    Ship.Direction.HORIZONTAL
                                    if h_v == "h"
                                    else Ship.Direction.VERTICAL
                                )
                                ship.place_ship(x, y, p.board)
                                logger.debug(f"\tSucceeded to place {ship.name} at ({x}, {y}, {h_v})")
                                break
                            logger.debug(f"\tFailed to place {ship.name} at ({x}, {y}, {h_v})")
                else:
                    logger.info(f"Player is {p.state} - starting fleet generation")
                    ships = [ship for ship in p.get_ships]
                    while ships:
                        logger.debug(f"\tStarting ship placement - ships left {len(ships)}")
                        ship = ships.pop()
                        logger.debug(f"\tShip: {ship.name}")
                        self.UI.output(GameRules.Output.PLACE.format(ship.name))
                        try:
                            x, y = self.UI.get_coords(GameRules.Output.COORD_ENTER)
                        except ValueError as error:
                            self.UI.output(GameRules.Output.MANGLED_PLACE.format(ship.name))
                            self.UI.output(
                                GameRules.Output.WRONG_INPUT.format(GameRules.Output.EXAMPLE_1)
                            )
                            ships.append(ship)
                            continue
                        x = int(x)
                        y = int(y)
                        h_v = self.UI.get_selection(GameRules.Output.DIR_ENTER)
                        if not self._check(x, y, h_v, p):
                            logger.debug("Passed check, failed placing")
                            self.UI.output(
                                GameRules.Output.FAILED_PLACE.format(ship.name, x, y, h_v)
                            )
                            ships.append(ship)
                            continue
                        ship.directionality = (
                            Ship.Direction.HORIZONTAL
                            if h_v == "h"
                            else Ship.Direction.VERTICAL
                        )
                        ship.place_ship(x, y, p.board)
                        logger.debug(f"\tPlaced {ship.name} at ({x}, {y}, {h_v})")
        logger.info("Exiting set-up and starting game loop")
        self.start()

    @property
    def any_won(self) -> bool:
        logger.info("Checking if any player has won")
        for p in self.player:
            if p.destroyed:
                self.stop()
                return True
        return False

    def output_player(self, player: Player.Player, hidden: bool = True):
        logger.info(f"Is {'' if hidden else 'not'} outputing to screen")
        # self.UI.output(player.board.output_readable(hidden=hidden))
        self.UI.print_board(player.board, hidden)

    @property
    def _get_turn(self):
        logger.info("Init turn generator")
        players: list[str] = list(self.players_dict.keys())
        turn = 0
        max_turns = len(self.players) * GameRules.SIZE**2
        while turn < max_turns and not self.any_won:
            attacker = self.players_dict[players[turn % 2]]
            defender = self.players_dict[players[(turn + 1) % 2]]
            logger.debug(f"yielding {turn} {attacker.name} {defender.name}")
            yield turn, attacker, defender
            turn += 1

    def _take_shot(self):
        logger.info("Getting player input for taking a shot")
        while True:
            try:
                x, y = self.UI.get_coords(GameRules.Output.COORD_ENTER)
            except ValueError as error:
                self.UI.output(GameRules.Output.INVALID_COORD)
            else:
                if GameRules.check_xy(x, y):
                    break
                else:
                    self.UI.output(GameRules.Output.INVALID_COORD)
        return x, y

    def _take_turn(self, attacker: Player.Player, defender: Player.Player) -> None:
        """
        Take a turn, the presumption is that the given player is the player being worked on.
        Meaning its the other players turn other than the given player.
        """
        logger.info(f"{attacker.name} is attacking {defender.name}.")
        while True:
            self.UI.output(GameRules.Output.PRE_SHOT.format(defender.name))

            if attacker.state is Player.State.AI:
                x, y = attacker._ai_brain.get_shot()
                self.UI.output(GameRules.Output.AI_SHOT_TAKEN.format(x, y))
            else:
                x, y = self._take_shot()

            if defender.board.get(x, y).hit:
                self.UI.output(GameRules.Output.STRUCK_AGAIN)
                logger.debug("\tLocation already selected")
                continue
            fleet, tile = defender.take_at_self_shot(x, y)
            name = tile.has.name if tile.has is Ship.Ship else "nothing"
            self.UI.output(GameRules.Output.SHOT_AT.format(x, y, name))
            self.output_player(defender)

            if attacker.state is Player.State.AI and tile.has:
                attacker._ai_brain.register_hit(x, y)
            break

    def take_turns(self):
        logger.info("Taking a turn")
        self.UI.clear_screen()
        current: Player.Player | None = None

        for turn, attacker, defender in self._get_turn:
            if turn % 3 == 0:
                self.UI.clear_screen()
            logger.debug(f"Turn: {turn} by {attacker.name} against {defender.name}")
            self.UI.output(GameRules.Output.CURRENT_TURN.format(turn, defender.name))
            self._take_turn(attacker, defender)
            current = attacker
            # self.UI.pause(self.UI.delay)

        if current:
            self.UI.output(GameRules.Output.WON_GAME.format(current.name))


if __name__ == "__main__":
    game = Game((False, False))
    game.set_up()
    game.take_turns()
