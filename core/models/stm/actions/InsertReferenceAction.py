from core.models.stm.actions.AbstractAction import AbstractAction


class InsertReferenceAction(AbstractAction):

    def __init__(self,
                 entity_from_id,
                 entity_to_id,
                 primary_key_from,
                 primary_key_to,
                 type) -> None:
        
        self._entity_from_id = entity_from_id
        self._entity_to_id = entity_to_id
        self._primary_key_from = primary_key_from
        self._primary_key_to = primary_key_to
        self._type = type

    def entity_from_id(self):
        return self._entity_from_id

    def entity_to_id(self):
        return self._entity_to_id

    def primary_key_from(self):
        return self._primary_key_from

    def primary_key_to(self):
        return self._primary_key_to

    def type(self):
        return self._type

    def info(self):
        return AbstractAction.info(self)

    def transformation_type(self):
        return "attribute"

    def action_type(self):
        return "copy"
