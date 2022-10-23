from core.models.stm.actions.AbstractAction import AbstractAction


class DeleteAttributeAction(AbstractAction):

    def __init__(self, entity_id, attribute_name) -> None:
        
        self._entity_id = entity_id
        self._attribute_name = attribute_name

    def entity_id(self):
        return self._entity_id

    def attribute_name(self):
        return self._attribute_name

    def info(self):
        return AbstractAction.info(self) + " \n\t delete attribute " + self._attribute_name + " from " + self.entity_id()

    def transformation_type(self):
        return "attribute"

    def action_type(self):
        return "delete"
