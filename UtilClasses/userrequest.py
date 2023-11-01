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
