from core.models.stm.actions.AbstractAction import AbstractAction


class RenameAttributeAction(AbstractAction):

    def __init__(self, entity_id, attribute_name, rename_attribute_name) -> None:
        
        self._entity_id = entity_id
        self._attribute_name = attribute_name
        self._rename_attribute_name = rename_attribute_name

    def entity_id(self):
        return self._entity_id

    def attribute_name(self):
        return self._attribute_name

    def rename_attribute_name(self):
        return self._rename_attribute_name

    def info(self):
        return AbstractAction.info(self) + " \n\t rename attribute " + self._attribute_name + " to " + self._rename_attribute_name + " in " + self.entity_id()

    def transformation_type(self):
        return "attribute"

    def action_type(self):
        return "rename"