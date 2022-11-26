
class Filter:

    def __init__(self, item) -> None:

        self._item = item
        self._type = item.getElementsByTagName("type")[0].childNodes[0].data

    def type(self):
        return self._type