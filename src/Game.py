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

Difficulty = Player.Difficulty


@dataclass
class GameConfig:
    board_width: int = GameRules.SIZE
    board_height: int = GameRules.SIZE
    fleet_composition: dict = field(default_factory=lambda: GameRules.FLEET)


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

    players: tuple[Difficulty, Difficulty]
    players_dict: dict[str, Player.Player] = field(default_factory=dict)
    state: GameRules.State = field(default=GameRules.State.STOPPED)
    config: GameConfig = field(default_factory=GameConfig)

    def __post_init__(self):
        logger.debug("Post-init")
        self._set_up()
        self.UI = UI.UI()

    @property
    def iter_players(self):
        logger.info("yielding players")
        yield from self.players_dict.values()

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
        for index, difficulty in enumerate(self.players):
            logger.debug(f"Attempting to init - {index}\t{difficulty}")
            name = f"p_{difficulty}_{index}"
            self.players_dict[name] = Player.Player(
                name,
                difficulty,
                Board.Board(width=self.config.board_width, height=self.config.board_height),
                Fleet.GeneralFleet(self.config.fleet_composition),
            )
            logger.debug(f"Finished init of {name} as {difficulty}")

    def _check(self, coords: tuple[int, int], h_v: str, p: Player.Player, ship: Ship.Ship) -> bool:
        """
        Validates whether a ship can be placed at the given coordinates and orientation.

        :Args:
            :p: The Player object placing the ship.
            :ship: The Ship object being placed.
            :coords: A tuple of (x, y) integers representing the starting position.
            :h_v: A string ('h' or 'v') representing the orientation.

        :Returns:
            bool: True if the placement is valid, False otherwise.
        """
        x, y = coords
        h_v = h_v.strip().lower()
        logger.debug(f"Checking {p.name} at ({x}, {y}) with {h_v}")
        if h_v not in ("h", "v") or len(h_v) != 1:
            self.UI.output(GameRules.Output.DIR_INVALID)
            return False
        directionality = Ship.Direction.HORIZONTAL if h_v == "h" else Ship.Direction.VERTICAL
        if not GameRules.check_xy(x, y):
            return False

        try:
            projected_coords = list(Ship.Ship.possible_places(x, y, ship.length, directionality))
        except Exception as ex:
            self.UI.output(GameRules.Output.FAILED_PLACE.format(ship.name, x, y, directionality))
            logger.warning(ex)
            return False

        for px, py in projected_coords:
            for existing_ship in p.get_ships:
                if existing_ship.is_placed and existing_ship.contains(px, py):
                    self.UI.output(GameRules.Output.OVERLAP.format(x, y, existing_ship.name))
                    return False

        return True

    def _testing_ship_placer(self, p: Player.Player, i: int = 0):
        for ship in p.get_ships:
            ship.place_ship(i := i + 1, 0, p.board)

    def set_up(self) -> None:
        logger.info("Starting set-up")
        self._set_up()
        for p in self.iter_players:
            logger.info(f"\tPlayer {p}")
            logger.info(f"Player is {p.difficulty} - starting fleet generation")
            if TESTING:
                logger.info("\tTesting enabled - generic ship placement")
                self._testing_ship_placer(p)
                continue
            if p.is_ai:

                if p.difficulty == Difficulty.EASY:
                    p._ai_brain = AI.Random()
                elif p.difficulty == Difficulty.MEDIUM:
                    p._ai_brain = AI.HuntAndTargetAIAdv()
                # elif p.difficulty == Difficulty.HARD:
                #     p._ai_brain = AI.ProbabilityAI()

                p.auto_ship_placement()
                continue
            # Is player
            for ship in p.get_ships:
                valid_placement = False
                logger.debug(f"\tAttempting to place Ship: {ship.name}")
                while not valid_placement:
                    self.UI.output(GameRules.Output.PLACE.format(ship.name))
                    raw_coords = self.UI.get_selection(GameRules.Output.COORD_ENTER_GENERIC)
                    parsed_coord = self.UI.parse_coord(raw_coords)
                    if parsed_coord is None:
                        self.UI.output(GameRules.Output.MANGLED_PLACE.format(ship.name))
                        self.UI.output(GameRules.Output.WRONG_INPUT.format(GameRules.Output.EXAMPLE_1))
                        continue
                    x, y = parsed_coord
                    if not GameRules.check_xy(x, y):
                        self.UI.output(GameRules.Output.OUTSIDE_BOARD.format(x, y))
                        continue
                    h_v = self.UI.get_selection(GameRules.Output.DIR_ENTER)
                    valid_placement = self._check((x, y), h_v, p, ship)

                    if valid_placement:
                        _d = Ship.Direction.HORIZONTAL if h_v.strip().lower() == "h" else Ship.Direction.VERTICAL
                        ship.directionality = _d

                        ship.place_ship(x, y, p.board)
                        logger.debug(f"\tPlaced {ship.name} at ({x}, {y}, {h_v})")
        logger.info("Exiting set-up and starting game loop")
        self.start()

    @property
    def any_won(self) -> bool:
        logger.info("Checking if any player has won")
        for p in self.iter_players:
            if p.fleet.all_sunk:
                return True
        return False

    def output_player(self, player: Player.Player, hidden: bool = True):
        logger.info(f"Is {'' if hidden else 'not'} outputing to screen")
        # self.UI.output(player.board.output_readable(hidden=hidden))
        self.UI.print_board(player.board, hidden)

    @property
    def _get_turn(self):
        """
        Infinite Turn Generator that yields the turn number, the attacking player
        and the defending player
        """
        logger.info("Init turn generator")

        if len(self.players_dict) != 2:
            logger.debug("Game failed to have two players")
            raise ValueError("Game requires exactly two players!")

        player_list = list(self.players_dict.values())
        attacker = player_list[0]
        defender = player_list[1]

        turn = 1

        while not self.stopped:
            yield turn, attacker, defender

            attacker, defender = defender, attacker
            turn += 1

    def _get_valid_shot(self, attacker: Player.Player, defender: Player.Player):
        while True:
            self.UI.output(GameRules.Output.PRE_SHOT.format(defender.name))
            x, y = attacker.choose_target(self.UI)

            if defender.is_already_targeted(x, y):
                logger.debug("\tLocation already selected")
                self.UI.output(GameRules.Output.TRY_AGAIN)
                continue

            return x, y

    def _take_turn(self, attacker: Player.Player, defender: Player.Player) -> None:
        """
        Take a turn, the presumption is that the given player is the player being worked on.
        Meaning its the other players turn other than the given player.
        """
        logger.info(f"{attacker.name} is attacking {defender.name}.")
        x, y = self._get_valid_shot(attacker, defender)
        while True:
            _, tile = defender.take_at_self_shot(x, y)
            if tile.has:
                if tile.has.is_sunk:
                    self.UI.output(GameRules.Output.SUNK_SHIP.format(tile.has.name))
                else:
                    self.UI.output(GameRules.Output.SHOT_AT.format(x, y, tile.has.name))
            else:
                self.UI.output(GameRules.Output.SHOT_AT.format(x, y, "nothing"))
            self.output_player(defender)

            if hasattr(attacker, "process_shot"):
                attacker.process_shot_result(x, y, tile)
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
            if turn == 100:
                self.UI.prompt_to_continue()
            if self.any_won:
                break

        if current:
            self.UI.output(GameRules.Output.WON_GAME.format(current.name))


if __name__ == "__main__":
    game = Game((Difficulty.MEDIUM, Difficulty.MEDIUM))
    game.set_up()
    game.take_turns()
