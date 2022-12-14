from core.models.stm.actions.AbstractAction import AbstractAction


class CreateEntityAction(AbstractAction):

    def __init__(self, entity_id: str) -> None:

        self._entity_id = entity_id

    def entity_id(self):
        return self._entity_id

    def info(self):
        return AbstractAction.info(self) + " \n\t new entity:  " + self._entity_id

    def transformation_type(self):
        return "entity"

    def action_type(self):
        return "create"
