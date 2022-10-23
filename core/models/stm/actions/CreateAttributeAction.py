from core.models.stm.actions.AbstractAction import AbstractAction


class CreateAttributeAction(AbstractAction):

    def __init__(self, entity_id, attribute_name, type) -> None:
        
        self._entity_id = entity_id
        self._attribute_name = attribute_name
        self._type = type

    def entity_id(self):
        return self._entity_id

    def attribute_name(self) -> str:
        return self._attribute_name

    def type(self):
        return self._type

    def info(self):
        return AbstractAction.info(self) + " \n\t new attribute:  " + self._attribute_name + " : " + self._type + " in entity " + self.entity_id()

    def transformation_type(self):
        return "attribute"

    def action_type(self):
        return "create"
