class TextReader:
    def __init__(self):
        self.data = None

    def read_txt(self, file_path, lines=False):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                if lines:
                    self.data = file.readlines()  # Чтение по строкам
                else:
                    self.data = file.read()  # Чтение всего файла

                return self.data

        except FileNotFoundError:
            print(f"Ошибка: Файл '{file_path}' не найден.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def read_txt_raw(self, file, encoding='utf-8', lines=False):
        try:
            if lines:
                # Декодируем каждую строку отдельно
                self.data = [line.decode(encoding) for line in file.readlines()]
            else:
                # Декодируем весь файл
                self.data = file.read().decode(encoding)

            return self.data

        except Exception as e:
            print(f"Произошла ошибка: {e}")



