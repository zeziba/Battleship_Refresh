import configparser
import os

BASELOCAION = os.path.dirname(__file__)
CONFIGFILE = "config.ini"

defaultconfig = {
    "settings": {
        "base location": BASELOCAION,
        "config file": CONFIGFILE,
        "board size": 10,
        "ship count": 5,
        "ships": """battleship:1,carrier:1,patrol boat:1,submarine:1,destroyer:1""",
        "Battleship": 4,
        "Carrier": 5,
        "Patrol Boat": 2,
        "Submarine": 3,
        "Destroyer": 3,
    }
}


class ConfigManager:
    def __init__(self, base=BASELOCAION):
        self.config = configparser.ConfigParser()
        self.configfile = os.path.join(base if base else os.getcwd(), CONFIGFILE)

    def create(self):
        with open(self.configfile, "w+") as file:
            confighandle = configparser.ConfigParser()
            for header in defaultconfig.keys():
                confighandle.add_section(f"{header}")
                for option in defaultconfig[header].keys():
                    confighandle.set(header, option, str(defaultconfig[header][option]))
            confighandle.write(file)

    def open(self):
        try:
            import os

            if not os.path.exists(self.configfile):
                raise FileNotFoundError()
            self.config.read(self.configfile)
            return True
        except FileNotFoundError:
            print("File not found, creation of file is required!")
        return False

    def get_config(self, selection=None):
        rn_dict = dict()

        self.open()

        if selection is not None:
            options = self.config.options(selection)
            for option in options:
                try:
                    rn_dict[option] = self.config.get(selection, option)
                    if rn_dict[option] == -1:
                        print("Skip: {}".format(option))
                except Exception as err:
                    print("Exception: {}\n{}".format(option, err))
        else:
            for section in self.config:
                if section != "DEFAULT":
                    rn_dict[section] = dict()
                    for option in self.config.options(section):
                        rn_dict[section][option] = self.config[section][option]

        return rn_dict

    def __str__(self):
        return str(self.get_config())


if __name__ == "__main__":
    config = ConfigManager()
    config.create()
    print(config)
