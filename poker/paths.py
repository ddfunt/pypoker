import os


class Paths:
    __slots__ = []

    @classmethod
    def image_path(cls, filename='default.png'):
        image_path = os.path.join(os.path.expanduser('~'), 'poker_images')
        if not os.path.exists(image_path):
            os.mkdir(image_path)
        if filename:
            return os.path.join(image_path, filename)
        return image_path

    @classmethod
    def ahk_path(cls):
        return os.path.join(os.path.expanduser('~'), 'PycharmProjects', 'poker', 'poker', 'exes')

