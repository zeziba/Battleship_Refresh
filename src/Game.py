from dataclasses import dataclass, field

import Board as Board
import Fleet as Fleet
import GameRules as GameRules
import Player as Player
import Ship
import UI as UI

TESTING = False


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
    __players: dict = field(default_factory=dict)
    state: GameRules.State = field(default=GameRules.State.STOPPED)

    def __post_init__(self):
        self.__set_up()
        self.UI = UI.UI()

    @property
    def player(self) -> iter:
        for _p in self.__players:
            yield self.__players[_p]

    def stop(self) -> None:
        self.state = GameRules.State.STOPPED

    def start(self) -> None:
        self.state = GameRules.State.RUNNING

    @property
    def stopped(self) -> bool:
        return self.state == GameRules.State.STOPPED

    def __set_up(self) -> None:
        for index, i in enumerate(self.players):
            state = Player.State.AI if i is False else Player.State.PERSON
            name = f"p{index}"
            self.__players[name] = Player.Player(
                name, state, Board.Board(), Fleet.GeneralFleet()
            )

    def __check(self, x: int, y: int, h_v: str, p: Player.Player):
        good_coords = not GameRules.check_xy(x, y)
        good_h_v = (h_v not in "hv") and (len(h_v) == 1)
        good_place = any(
            s.contains(px, py)
            for s in p.get_ships
            for px, py in Ship.Ship.possible_places(x, y, s.length, s.directionality)
        )
        return good_coords or good_h_v or good_place

    def set_up(self) -> None:
        self.__set_up()
        for p in self.player:
            i = 0
            p.board.generate_board()
            p.fleet.generate()
            if TESTING:
                for ship in p.get_ships:
                    ship.place_ship(i := i + 1, 0, p.board)
            else:
                if p.state is Player.State.AI:
                    for ship in p.get_ships:
                        ship.place_ship(i := i + 1, 0, p.board)
                else:
                    ships = [ship for ship in p.get_ships]
                    while ships:
                        ship = ships.pop()
                        self.UI.output(GameRules.OUTPUTS[3].format(ship.name))
                        try:
                            x, y = self.UI.get_coords(GameRules.OUTPUTS[0])
                        except ValueError as error:
                            self.UI.output(GameRules.OUTPUTS[5].format(ship.name))
                            self.UI.output(
                                GameRules.OUTPUTS[6].format(GameRules.OUTPUTS[7])
                            )
                            ships.append(ship)
                            continue
                        x = int(x)
                        y = int(y)
                        h_v = self.UI.get_selection(GameRules.OUTPUTS[1])
                        if self.__check(x, y, h_v, p):
                            self.UI.output(
                                GameRules.OUTPUTS[4].format(ship.name, x, y, h_v)
                            )
                            ships.append(ship)
                            continue
                        ship.directionality = (
                            Ship.Direction.HORIZONTAL
                            if h_v == "h"
                            else Ship.Direction.VERTICAL
                        )
                        ship.place_ship(x, y, p.board)
        self.start()

    @property
    def any_won(self) -> bool:
        for p in self.player:
            if p.destroyed:
                self.stop()
                return True
        return False

    def output_player(self, player: Player.Player, hidden: bool = True):
        self.UI.output(player.board.output_readable(hidden=hidden))

    @property
    def __get_turn(self) -> iter:
        turn = 0
        max_turns = GameRules.SIZE ** 2
        while turn < max_turns and not self.any_won:
            for player in self.player:
                yield turn, player
            turn += 1

    def __take_shot(self):
        while True:
            try:
                x, y = self.UI.get_coords(GameRules.OUTPUTS[0])
            except ValueError as error:
                self.UI.output(GameRules.OUTPUTS[11])
            else:
                if GameRules.check_xy(x, y):
                    break
                else:
                    self.UI.output(GameRules.OUTPUTS[11])
        return x, y

    def __take_turn(self, _player: Player.Player) -> None:
        """
        Take a turn, the presumption is that the given player is the player being worked on.
        Meaning its the other players turn other than the given player.
        """
        while True:
            self.UI.output(GameRules.OUTPUTS[9].format(_player.name))
            x, y = self.__take_shot()
            if _player.board.get(x, y).hit:
                self.UI.output(GameRules.OUTPUTS[14])
                continue
            tile_state = _player.take_at_self_shot(x, y)
            name = tile_state[1].has.name if tile_state[1].contains else "nothing"
            self.UI.output(GameRules.OUTPUTS[10].format(x, y, name))
            self.output_player(_player)
            break

    def take_turns(self):
        for turn, player in self.__get_turn:
            self.UI.output(GameRules.OUTPUTS[12].format(turn, player.name))
            self.__take_turn(player)
        self.UI.output(GameRules.OUTPUTS[13].format(next(self.player)))


if __name__ == "__main__":
    game = Game((False, False))
    game.set_up()
    game.take_turns()
