from abc import ABC, abstractmethod


class FileHandler(ABC):
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    @abstractmethod
    def handle(self, file_path, output_file):
        pass

    def handle_pattern(self, file_path, output_file, name):
        if file_path.endswith("."+name):
            print(f"обработчик {name} получил файл {file_path}")
            with open(file_path, "r") as f, open(output_file, "a") as out:
                out.write(f.read()+"\n")
        elif self.next_handler:
            self.next_handler.handle(file_path, output_file)
    def set_next(self, handler):
        self.next_handler = handler


class XMLHandler(FileHandler):
    def handle(self, file_path, output_file):
        self.handle_pattern(file_path, output_file, 'xml')


class JSONHandler(FileHandler):
    def handle(self, file_path, output_file):
        self.handle_pattern(file_path, output_file, 'json')


class CSVHandler(FileHandler):
    def handle(self, file_path, output_file):
        self.handle_pattern(file_path, output_file, 'csv')


class TXTHandler(FileHandler):
    def handle(self, file_path, output_file):
        self.handle_pattern(file_path, output_file, 'txt')


def main(input_list, output_file):
    xml_handler = XMLHandler()
    json_handler = JSONHandler()
    csv_handler = CSVHandler()
    txt_handler = TXTHandler()

    xml_handler.set_next(json_handler)
    json_handler.set_next(csv_handler)
    csv_handler.set_next(txt_handler)

    with open(input_list, "r") as f:
        for file_path in f:
            file_path = file_path.strip()
            xml_handler.handle(file_path, output_file)


input_list = 'input.txt'
output_file = 'result.txt'
main(input_list, output_file)
