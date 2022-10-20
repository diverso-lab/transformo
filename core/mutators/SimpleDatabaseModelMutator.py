
from core.models.sdm.SimpleDatabaseModel import SimpleDatabaseModel
from core.models.stm.AvailableAction import AvailableAction


class SimpleDatabaseModelMutator:

    def __init__(
        self, 
        current_sdm_source:SimpleDatabaseModel,
        available_action: AvailableAction,
        actions_counter: int,
        migration_name: str) -> None:

        self._current_sdm_source = current_sdm_source
        self._available_action = available_action
        self._actions_counter = actions_counter
        self._migration_name = migration_name

    def mutate(self):
        
        transformation_type = self._available_action.action().transformation_type()
        action_type = self._available_action.action().action_type()

        match transformation_type:

            case "entity":
                
                match action_type:

                    case "create":
                        pass

                    case "rename":
                        pass

                    case "delete":
                        pass

            case "attribute":

                match action_type:

                    case "create":
                        pass

                    case "rename":
                        pass

                    case "retype":
                        pass

                    case "move":
                        pass

                    case "delete":
                        pass