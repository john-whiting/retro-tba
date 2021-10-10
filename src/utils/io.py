class IO:
    class bcolors:
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        CYAN = '\033[96m'
        PURPLE = '\033[95m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        ENDC = '\033[0m'

    color_lookup = {
        '&1': bcolors.BLUE,
        '&2': bcolors.GREEN,
        '&3': bcolors.CYAN,
        '&5': bcolors.PURPLE,
        '&e': bcolors.YELLOW,
        '&c': bcolors.RED,
        '&l': bcolors.BOLD,
        '&n': bcolors.UNDERLINE,
        '&f': bcolors.ENDC,
    }

    @staticmethod
    def format(msg: str) -> str:
        msg += '&f'
        for k, v in IO.color_lookup.items():
            msg = msg.replace(k, v)
        return msg

    @staticmethod
    def clear_console() -> None:
        print('\n' * 150)

    @staticmethod
    def print(msg: str) -> None:
        print(IO.format(msg))

    @staticmethod
    def prompt(state, msg: str) -> None:
        IO.print(msg)
        inp = ''
        while len(inp) < 1:
            inp = input('> ') # Get command from players

        # Separate command parts
        cmd_sects = inp.split(' ')
        cmd_name = cmd_sects[0].lower()
        cmd_args = [arg.lower() for arg in cmd_sects[1:]]

        return IO.parse_command(state, cmd_name, cmd_args)

    @staticmethod
    def parse_command(state, cmd_name: str, cmd_args: str):
        from commands import commands
        if cmd_name in commands.keys():
            return commands[cmd_name](state, *cmd_args)