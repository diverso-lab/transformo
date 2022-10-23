from core.models.stm.actions.AbstractAction import AbstractAction


class RetypeAttributeAction(AbstractAction):

    def __init__(self, entity_id, attribute_name, retype_name) -> None:
        
        self._entity_id = entity_id
        self._attribute_name = attribute_name
        self._retype_name = retype_name

    def entity_id(self):
        return self._entity_id

    def attribute_name(self):
        return self._attribute_name

    def retype_name(self):
        return self._retype_name

    def info(self):
        return AbstractAction.info(self) + " \n\t retype attribute " + self._attribute_name + " to " + self._retype_name + " in " + self._entity_id

    def transformation_type(self):
        return "attribute"

    def action_type(self):
        return "retype"