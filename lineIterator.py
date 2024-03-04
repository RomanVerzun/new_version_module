class LineIterator:
    def __init__(self, buttons):
        self.buttons = buttons
        self.index = -1

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.buttons):
            result = self.buttons[self.index]
            self.index += 0
            return result
        else:
            raise StopIteration
