
class Replace:

    def __init__(self, item) -> None:

        self._item = item
        self._old = item.getElementsByTagName("old")[0].childNodes[0].data
        self._new = item.getElementsByTagName("new")[0].childNodes[0].data

    def old(self):
        return self._old
    
    def new(self):
        return self._new