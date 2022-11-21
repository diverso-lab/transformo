from typing import Any

from core.models.stm.actions.CopyAttributeAction import CopyAttributeAction
from core.models.stm.actions.CreateAttributeAction import CreateAttributeAction
from core.models.stm.actions.CreateEntityAction import CreateEntityAction
from core.models.stm.actions.DeleteAttributeAction import DeleteAttributeAction
from core.models.stm.actions.DeleteEntityAction import DeleteEntityAction
from core.models.stm.actions.MoveAttributeAction import MoveAttributeAction
from core.models.stm.actions.RenameAttributeAction import RenameAttributeAction
from core.models.stm.actions.RenameEntityAction import RenameEntityAction
from core.models.stm.actions.RetypeAttributeAction import RetypeAttributeAction


class Action:

    def __init__(self, item, transformation_type) -> None:

        self._item = item
        self._transformation_type = transformation_type
        self._type = item.getAttribute('type')
        self._apply: Any = None

    def type(self):
        return self._type

    def item(self):
        return self._item

    def set_apply(self, apply) -> None:
        self._apply = apply

    def apply(self):

        apply = None

        match self._transformation_type:

            case "entity":

                match self._type:

                    case "create":

                        # basic data
                        entity_id = self._item.getElementsByTagName("entity")[0].childNodes[0].data

                        # create action
                        apply = CreateEntityAction(entity_id=entity_id)

                    case "rename":

                        # basic data
                        entity_id = self._item.getElementsByTagName("entity")[0].childNodes[0].data
                        rename_entity_id = self._item.getElementsByTagName("rename")[0].childNodes[0].data

                        # create action
                        apply = RenameEntityAction(entity_id=entity_id, rename_entity_id=rename_entity_id)

                    case "delete":

                        # basic data
                        entity_id = self._item.getElementsByTagName("entity")[0].childNodes[0].data

                        # create action
                        apply = DeleteEntityAction(entity_id=entity_id)

            case "attribute":

                match self._type:

                    case "create":

                        # basic data
                        entity_id = self._item.getElementsByTagName("entity")[0].childNodes[0].data
                        attribute_name = self._item.getElementsByTagName("attribute")[0].childNodes[0].data
                        type = self._item.getElementsByTagName("type")[0].childNodes[0].data

                        # create action
                        apply = CreateAttributeAction(entity_id=entity_id, attribute_name=attribute_name, type=type)

                    case "rename":

                        # basic data
                        entity_id = self._item.getElementsByTagName("entity")[0].childNodes[0].data
                        attribute_name = self._item.getElementsByTagName("attribute")[0].childNodes[0].data
                        rename_attribute_name = self._item.getElementsByTagName("rename")[0].childNodes[0].data

                        # create action
                        apply = RenameAttributeAction(entity_id=entity_id, attribute_name=attribute_name,
                                                      rename_attribute_name=rename_attribute_name)

                    case "retype":

                        # basic data
                        entity_id = self._item.getElementsByTagName("entity")[0].childNodes[0].data
                        attribute_name = self._item.getElementsByTagName("attribute")[0].childNodes[0].data
                        retype_name = self._item.getElementsByTagName("retype")[0].childNodes[0].data

                        # create action
                        apply = RetypeAttributeAction(entity_id=entity_id, attribute_name=attribute_name,
                                                      retype_name=retype_name)

                    case "move":

                        # basic data
                        entity_from_id = self._item.getElementsByTagName("from")[0].childNodes[0].data
                        entity_to_id = self._item.getElementsByTagName("to")[0].childNodes[0].data
                        attribute_name = self._item.getElementsByTagName("attribute")[0].childNodes[0].data
                        type = self._item.getElementsByTagName("type")[0].childNodes[0].data

                        # create action
                        apply = MoveAttributeAction(entity_from_id=entity_from_id, entity_to_id=entity_to_id,
                                                    attribute_name=attribute_name, type=type)

                    case "copy":

                        # basic data
                        entity_from_id = self._item.getElementsByTagName("from")[0].childNodes[0].data
                        entity_to_id = self._item.getElementsByTagName("to")[0].childNodes[0].data
                        attribute_name = self._item.getElementsByTagName("attribute")[0].childNodes[0].data
                        type = self._item.getElementsByTagName("type")[0].childNodes[0].data

                        # create action
                        apply = CopyAttributeAction(entity_from_id=entity_from_id, entity_to_id=entity_to_id,
                                                    attribute_name=attribute_name, type=type)

                    case "delete":

                        # basic data
                        entity_id = self._item.getElementsByTagName("entity")[0].childNodes[0].data
                        attribute_name = self._item.getElementsByTagName("attribute")[0].childNodes[0].data

                        # create action
                        apply = DeleteAttributeAction(entity_id=entity_id, attribute_name=attribute_name)

        return apply

    def __str__(self) -> str:

        string = "Type = {type}".format(type=self._type)
        return string
