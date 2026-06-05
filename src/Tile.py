from dataclasses import dataclass, field

import GameRules


@dataclass
class Tile:
    __contains: None
    __hit: False = field(default=bool)

    @property
    def hit(self) -> bool:
        return self.__hit

    @hit.setter
    def hit(self, value: bool) -> None:
        if not self.hit:
            self.__hit = value

    @property
    def contains(self) -> bool:
        return self.__contains is not None

    @contains.setter
    def contains(self, value) -> None:
        if self.contains is True:
            raise IndexError(f"Location already has {self.contains}")
        self.__contains = value

    @property
    def has(self) -> object:
        return self.__contains

    @property
    def title_logo(self, hidden: bool = True) -> str:
        # TODO: Finish implementation
        raise NotImplemented
        if hidden:
            if self.contains:
                if self.hit:
                    pass
                else:
                    pass
        else:
            if self.contains:
                if self.hit:
                    pass
                else:
                    pass
        return GameRules.EmptyTile
