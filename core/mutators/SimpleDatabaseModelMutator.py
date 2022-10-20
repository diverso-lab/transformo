
from core.models.sdm.SimpleDatabaseModel import SimpleDatabaseModel
from core.models.stm.AvailableAction import AvailableAction


class SimpleDatabaseModelMutator:

    def __init__(
        self, 
        current_sdm_source:SimpleDatabaseModel,
        available_action: AvailableAction,
        actions_counter: int) -> None:

        self._current_sdm_source = current_sdm_source
        self._available_action = available_action
        self._actions_counter = actions_counter

    def mutate(self):
        pass