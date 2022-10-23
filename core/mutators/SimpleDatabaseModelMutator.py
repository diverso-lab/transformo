from core.models.sdm.SimpleDatabaseModel import SimpleDatabaseModel
from core.models.stm.SimpleTransformationModel import SimpleTransformationModel
from core.writers.SimpleDatabaseModelWriter import SimpleDatabaseModelWriter


class SimpleDatabaseModelMutator:

    def __init__(
            self,
            current_sdm_source: SimpleDatabaseModel,
            last_stm: SimpleTransformationModel,
            actions_counter: int,
            migration_name: str,
            folder: str) -> None:

        self._current_sdm_source = current_sdm_source
        self._last_stm = last_stm
        self._actions_counter = actions_counter
        self._migration_name = migration_name
        self._folder = folder
        self._new_sdm_file = None

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

                        # basic data
                        element = action_item.getElementsByTagName("entity")[0].childNodes[0].data
                        rename = action_item.getElementsByTagName("rename")[0].childNodes[0].data
                        entity = self._current_sdm_source.get_entity_by_id(element)

                        # update entity
                        self._current_sdm_source.edit_entity_name(entity, rename)

                    case "delete":

                        # basic data
                        element = action_item.getElementsByTagName("entity")[0].childNodes[0].data
                        entity = self._current_sdm_source.get_entity_by_id(element)

                        # update entity
                        self._current_sdm_source.delete_entity(entity)

            case "attribute":

                match action_type:

                    case "create":

                        # basic data
                        element = action_item.getElementsByTagName("entity")[0].childNodes[0].data
                        entity = self._current_sdm_source.get_entity_by_id(element)
                        attribute_name = action_item.getElementsByTagName("attribute")[0].childNodes[0].data
                        type = action_item.getElementsByTagName("type")[0].childNodes[0].data

                        # update attribute
                        self._current_sdm_source.add_attribute(entity=entity, attribute_name=attribute_name, attribute_type=type)

                    case "rename":

                        # basic data
                        element = action_item.getElementsByTagName("entity")[0].childNodes[0].data
                        entity = self._current_sdm_source.get_entity_by_id(element)
                        attribute = action_item.getElementsByTagName("attribute")[0].childNodes[0].data
                        rename = action_item.getElementsByTagName("rename")[0].childNodes[0].data

                        # update attribute
                        self._current_sdm_source.edit_attribute_name(entity=entity, attribute_name=attribute, rename=rename)

                    case "retype":

                        # basic data
                        element = action_item.getElementsByTagName("entity")[0].childNodes[0].data
                        entity = self._current_sdm_source.get_entity_by_id(element)
                        attribute = action_item.getElementsByTagName("attribute")[0].childNodes[0].data
                        retype = action_item.getElementsByTagName("retype")[0].childNodes[0].data

                        # update attribute
                        self._current_sdm_source.edit_attribute_type(entity=entity, attribute_name=attribute, retype=retype)

                    case "move":

                        # basic data
                        element_from = action_item.getElementsByTagName("from")[0].childNodes[0].data
                        element_to = action_item.getElementsByTagName("to")[0].childNodes[0].data
                        entity_from = self._current_sdm_source.get_entity_by_id(element_from)
                        entity_to = self._current_sdm_source.get_entity_by_id(element_to)
                        attribute = action_item.getElementsByTagName("attribute")[0].childNodes[0].data
                        type = action_item.getElementsByTagName("type")[0].childNodes[0].data

                        # update attribute
                        self._current_sdm_source.add_attribute(entity=entity_to, attribute_name=attribute, attribute_type=type)
                        self._current_sdm_source.delete_attribute(entity=entity_from, attribute_name=attribute)

                    case "delete":

                        # basic data
                        element = action_item.getElementsByTagName("entity")[0].childNodes[0].data
                        entity = self._current_sdm_source.get_entity_by_id(element)
                        attribute = action_item.getElementsByTagName("attribute")[0].childNodes[0].data

                        # update attribute
                        self._current_sdm_source.delete_attribute(entity=entity, attribute_name=attribute)

        self._new_sdm_file = "models/{}/{}_{}.sdm".format(self._folder, self._migration_name, self._actions_counter)
        sdm_writer = SimpleDatabaseModelWriter(sdm=self._current_sdm_source, sdm_filename=self._new_sdm_file,
                                               folder=self._folder)
        sdm_writer.write()

        self._current_sdm_source = self._current_sdm_source.reload_sdm()

    def new_sdm(self):
        return SimpleDatabaseModel(self._new_sdm_file)
