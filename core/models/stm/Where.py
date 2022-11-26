
class Where:

    def __init__(self, item) -> None:

        self._item = item
        self._attribute_from = item.getElementsByTagName("attribute_from")[0].childNodes[0].data
        self._value = item.getElementsByTagName("value")[0].childNodes[0].data

    def attribute_from(self):
        return self._attribute_from

    def value(self):
        return self._value
