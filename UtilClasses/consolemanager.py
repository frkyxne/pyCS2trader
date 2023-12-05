from datetime import datetime


class ConsoleManager:
    @staticmethod
    def get_input():
        return UserRequest(input('> '))

    @staticmethod
    def print(obj: object):
        if type(obj) is str:
            print(f'{ConsoleManager.__get_time_repr()} {obj}')
            return

        representation = repr(obj)
        representation_lines = representation.split('\n')

        for representation_line in representation_lines:
            representation_line.replace("\n", "")

        top_splitter_len = len(representation_lines[0])
        time_repr = ConsoleManager.__get_time_repr()

        if top_splitter_len < len(time_repr):
            top_splitter = f'--{time_repr}--'
        else:
            side_dash_len = (top_splitter_len - len(time_repr)) // 2
            top_splitter = f'{"-"*side_dash_len}{time_repr}{"-"*side_dash_len}'

        representation_lines.insert(0, top_splitter)
        representation_lines.append('-' * len(representation_lines[-1]))
        representation = ''

        for representation_line in representation_lines:
            representation += f"{representation_line}\n"
        print(representation[0:-2])

    @staticmethod
    def __get_time_repr() -> str:
        now_time = datetime.now()
        return f'[{now_time.hour}:{now_time.minute}:{now_time.second}]'


class UserRequest:
    def __init__(self, request: str):
        if request == '':
            self.__command = None
            return

        request_split = request.split()
        self.__command = request_split[0]

        args = []

        for i in range(1, len(request_split)):
            args.append(request_split[i])

        self.__command_args = args

    @property
    def command(self):
        return self.__command

    @property
    def command_args(self):
        return self.__command_args

    @property
    def command_arg(self):
        return ' '.join(self.__command_args)
