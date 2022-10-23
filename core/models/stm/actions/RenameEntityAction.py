from core.models.stm.actions.AbstractAction import AbstractAction


class RenameEntityAction(AbstractAction):

    def __init__(self, entity_id, rename_entity_id) -> None:
        
        self._entity_id = entity_id
        self._rename_entity_id = rename_entity_id

    def entity_id(self):
        return self._entity_id

    def rename_entity_id(self):
        return self.rename_entity_id

    def info(self):
        return AbstractAction.info(self) + " \n\t old entity:  " + self._entity_id + ", new entity: " + self._rename_entity_id

    def transformation_type(self):
        return "entity"

    def action_type(self):
        return "rename"