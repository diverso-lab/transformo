class Action:

    def __init__(self, item, transformation_action:str) -> None:

        self._item = item
        self._transformation_action = transformation_action
        self._type = item.getAttribute('type')

    def type(self):
        return self._type

    def item(self):
        return self._item

    def __str__(self) -> str:

        string = "Type = {type}".format(type=self._type)
        return string
