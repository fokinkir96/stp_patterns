class State:
    def handle(self, context, char):
        pass


class CommandState(State):
    def handle(self, context, char):
        if char.isalpha():
            context.command += char
        elif char == ' ':
            context.set_state(ParameterState())
        else:
            context.set_state(None)


class ParameterState(State):
    def handle(self, context, char):
        if char.isalnum() or char == '_':
            context.current_parameter += char
        elif char == ' ':
            if context.current_parameter:
                if context.is_key_parameter is False:
                    context.parameters.append(context.current_parameter)
                else:
                    context.keys_parameters.append(context.current_parameter)
                context.current_parameter = ''
                # context.set_state(KeyState())
        elif char == '"':
            context.set_state(QuoteState())
        elif char == '-':
            context.set_state(KeyState())
        else:
            context.set_state(None)


class QuoteState(State):
    def handle(self, context, char):
        if char != '"':
            if char == '_':
                context.current_parameter += ' '
            else:
                context.current_parameter += char
        else:
            context.set_state(ParameterState())


class KeyState(State):
    def handle(self, context, char):
        if char == '-':
            context.current_key = '-'
        elif char.isalnum():
            context.current_key += char
            if context.current_key in context.valid_keys:
                context.keys.append(context.current_key)
                if context.valid_keys[context.current_key] == 'required':
                    context.is_key_parameter = True
                    context.set_state(ParameterState())
                context.current_key = ''
            else:
                context.set_state(None)
        else:
            context.set_state(None)


class StateContext:
    def __init__(self):
        self.state = CommandState()
        self.command = ''
        self.parameters = []
        self.keys = []
        self.keys_parameters = []
        self.is_key_parameter = False
        self.current_parameter = ''
        self.current_key = ''
        self.valid_keys = {
            'a': 'required',
            'r': 'required',
            'p': 'required',
            'n': 'optional',
            'm': 'optional',
            'l': 'optional',
            's': 'optional',
            'c': 'none'
        }

    def set_state(self, state):
        self.state = state

    def process(self, input_str):
        input_str += ' '
        for char in input_str:
            if self.state is None:
                return False
            self.state.handle(self, char)

        if self.state is not None:
            return True
        return False


input_str = input("Введите команду: ")
context = StateContext()

if context.process(input_str):
    print("Введенная строка соответствует правилам.")
    print("Команда:", context.command)
    print("Параметры команды:", context.parameters)
    print("Ключи:", context.keys)
    print("Параметры ключей:", context.keys_parameters)
else:
    print("Введенная строка не соответствует правилам.")
