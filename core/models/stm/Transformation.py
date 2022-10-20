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

        string = "Transformation '{id}' (type {type})\n".format( id = self._id, type = self._type)
        return string

    def _read_actions(self, actions):
        
        for a in actions:

            action = Action(item = a, transformation_action = self._type)
            self._actions.append(action)



    '''
    def __init__(self, sdm, item):

        self.__sdm = sdm
        self.item = item

        self.__type = item.getAttribute('type')
        self.__id = item.getAttribute('id')

        self.__actions: list[Action] = list()

        self.__read_actions(item.getElementsByTagName("action"))

    def sdm(self):
        return self.__sdm

    def __read_actions(self, actions):
        
        for a in actions:

            action = Action(sdm = self.__sdm, item = a, transformation_action = self.__type)
            self.__sdm = action.sdm()

            self.__actions.append(action)

    def type(self):
        return self.__type

    def id(self):
        return self.__id

    def actions(self):

        return self.__actions


    def __str__(self) -> str:

        string = "Transformation '{id}' (type {type})\n".format( id = self.__id, type = self.__type)

        return string
    '''