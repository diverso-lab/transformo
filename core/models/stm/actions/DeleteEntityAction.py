from core.models.sdm.Entity import Entity
from core.models.stm.actions.AbstractAction import AbstractAction


class DeleteEntityAction(AbstractAction):

    def __init__(self, entity_id) -> None:
        
        self._entity_id = entity_id

    def entity_id(self):
        return self._entity_id

    def info(self) -> str:
        return AbstractAction.info(self) + " \n\t delete entity:  " + self._entity_id

    def transformation_type(self) -> str:
        return "entity"

    def action_type(self) -> str:
        return "delete"