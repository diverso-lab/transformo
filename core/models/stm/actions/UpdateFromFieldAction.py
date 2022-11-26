from core.models.stm.Filter import Filter
from core.models.stm.Where import Where
from core.models.stm.actions.AbstractAction import AbstractAction


class UpdateFromFieldAction(AbstractAction):

    def __init__(self,
                 entity_from_id,
                 entity_to_id,
                 attribute_from_name,
                 attribute_to_name,
                 type,
                 primary_key_from,
                 primary_key_to,
                 filter_item) -> None:
        self._entity_from_id = entity_from_id
        self._entity_to_id = entity_to_id
        self._attribute_from_name = attribute_from_name
        self._attribute_to_name = attribute_to_name
        self._primary_key_from = primary_key_from
        self._primary_key_to = primary_key_to
        self._type = type

        self._read_filter(filter_item)




    def _read_filter(self, filter_item):

        if not filter_item is None:
            self._filter = Filter(filter_item)
        else:
            self._filter = None

    def filter(self):
        return self._filter

    def entity_from_id(self):
        return self._entity_from_id

    def entity_to_id(self):
        return self._entity_to_id

    def attribute_from_name(self):
        return self._attribute_from_name

    def attribute_to_name(self):
        return self._attribute_to_name

    def primary_key_to(self):
        return self._primary_key_to

    def primary_key_from(self):
        return self._primary_key_from

    def type(self):
        return self._type

    def info(self):
        return AbstractAction.info(
            self) + " \n\t move attribute " + self._attribute_from_name + " : " + self._type + ", from " + self._entity_from_id + " to " + self._entity_to_id

    def transformation_type(self):
        return "attribute"

    def action_type(self):
        return "update_from_field"
