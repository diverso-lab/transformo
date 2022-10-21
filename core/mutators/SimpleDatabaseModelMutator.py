
from core.models.sdm.SimpleDatabaseModel import SimpleDatabaseModel
from core.models.stm.AvailableAction import AvailableAction
from core.models.stm.SimpleTransformationModel import SimpleTransformationModel
from core.writers.SimpleDatabaseModelWriter import SimpleDatabaseModelWriter


class SimpleDatabaseModelMutator:

    def __init__(
        self, 
        current_sdm_source:SimpleDatabaseModel,
        last_stm: SimpleTransformationModel,
        actions_counter: int,
        migration_name: str) -> None:

        self._current_sdm_source = current_sdm_source
        self._last_stm = last_stm
        self._actions_counter = actions_counter
        self._migration_name = migration_name

    def mutate(self):
        
        last_transformation = self._last_stm.last_transformation()
        action = last_transformation.actions()[0]
        action_item = action.item()

        transformation_type = last_transformation.type()
        action_type = action.type()

        match transformation_type:

            case "entity":
                
                match action_type:

                    case "create":

                        # basic data
                        element = action_item.getElementsByTagName("entity")[0].childNodes[0].data

                        # update entity
                        self._current_sdm_source.add_entity(element)

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

        # TODO: generate new SDM (file) after applying action
        sdm_filename = "models/{}_{}".format(self._migration_name, self._actions_counter)
        sdm_writer = SimpleDatabaseModelWriter(sdm = self._current_sdm_source, sdm_filename=sdm_filename)
        sdm_writer.write()

        self._current_sdm_source = self._current_sdm_source.reload_sdm()
