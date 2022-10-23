from core.models.stm.Action import Action


class Transformation:

    def __init__(self, item):

        self._item = item

        self._type = self._item.getAttribute('type')
        self._id = self._item.getAttribute('id')

        self._actions: list[Action] = list()

        self._read_actions(item.getElementsByTagName("action"))

    def type(self) -> str:
        return self._type

    def id(self) -> str:
        return self._id

    def actions(self) -> list[Action]:
        return self._actions

    def __str__(self) -> str:

        string = "Transformation '{id}' (type {type})\n".format(id=self._id, type=self._type)
        return string

    def _read_actions(self, actions):
        
        for a in actions:

            action = Action(item=a, transformation_type=self._type)
            self._actions.append(action)
