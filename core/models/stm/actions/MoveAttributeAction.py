from core.models.stm.actions.AbstractAction import AbstractAction


class MoveAttributeAction(AbstractAction):

    def __init__(self, entity_from_id, entity_to_id, attribute_name, type) -> None:
        
        self._entity_from_id = entity_from_id
        self._entity_to_id = entity_to_id
        self._attribute_name = attribute_name
        self._type = type

    def entity_from_id(self):
        return self._entity_from_id

    def entity_to_id(self):
        return self._entity_to_id

    def attribute_name(self):
        return self._attribute_name

    def type(self):
        return self._type

    def info(self):
        return AbstractAction.info(self) + " \n\t move attribute " + self._attribute_name + " : " + self._type + ", from " + self._entity_from_id + " to " + self._entity_to_id

    def transformation_type(self):
        return "attribute"

    def action_type(self):
        return "move"
