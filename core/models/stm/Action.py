from typing import Any

from core.models.stm.Filter import Filter
from core.models.stm.Replace import Replace
from core.models.stm.actions.AbstractAction import AbstractAction
from core.models.stm.actions.CopyAttributeAction import CopyAttributeAction
from core.models.stm.actions.CreateAttributeAction import CreateAttributeAction
from core.models.stm.actions.CreateEntityAction import CreateEntityAction
from core.models.stm.actions.DeleteAttributeAction import DeleteAttributeAction
from core.models.stm.actions.DeleteEntityAction import DeleteEntityAction
from core.models.stm.actions.InsertReferenceAction import InsertReferenceAction
from core.models.stm.actions.MoveAttributeAction import MoveAttributeAction
from core.models.stm.actions.RenameAttributeAction import RenameAttributeAction
from core.models.stm.actions.RenameEntityAction import RenameEntityAction
from core.models.stm.actions.RetypeAttributeAction import RetypeAttributeAction
from core.models.stm.actions.UpdateFromFieldAction import UpdateFromFieldAction
from core.models.stm.actions.UpdateFromValueAction import UpdateFromValueAction


class Action:

    def __init__(self, item, transformation_type) -> None:

        self._item = item
        self._transformation_type = transformation_type
        self._type = item.getAttribute('type')
        self._apply: Any = None

        self._read_filter()
        self._read_replace()

    def _read_filter(self):

        try:
            item_filter = self._item.getElementsByTagName("filter")[0]
            self._filter = Filter(item_filter)
        except:
            pass

    def _read_replace(self):

        try:
            item_replace = self._item.getElementsByTagName("replace")[0]
            self._replace = Replace(item_replace)
        except:
            pass

    def type(self) -> str:
        return self._type

    def filter(self) -> Filter:
        return self._filter
    
    def replace(self) -> Replace:
        return self._replace

    def item(self):
        return self._item

    def set_apply(self, apply) -> None:
        self._apply = apply

    def apply(self) -> AbstractAction:

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
                        attribute_from_name = self._item.getElementsByTagName("attribute_from")[0].childNodes[0].data
                        attribute_to_name = self._item.getElementsByTagName("attribute_to")[0].childNodes[0].data
                        primary_key_from = self._item.getElementsByTagName("primary_key_from")[0].childNodes[0].data
                        primary_key_to = self._item.getElementsByTagName("primary_key_to")[0].childNodes[0].data
                        type = self._item.getElementsByTagName("type")[0].childNodes[0].data

                        # create action
                        apply = CopyAttributeAction(entity_from_id=entity_from_id,
                                                    entity_to_id=entity_to_id,
                                                    attribute_from_name=attribute_from_name,
                                                    primary_key_from=primary_key_from,
                                                    primary_key_to=primary_key_to,
                                                    attribute_to_name=attribute_to_name, type=type)

                    case "insert_reference":

                        # basic data
                        entity_from_id = self._item.getElementsByTagName("from")[0].childNodes[0].data
                        entity_to_id = self._item.getElementsByTagName("to")[0].childNodes[0].data
                        primary_key_from = self._item.getElementsByTagName("primary_key_from")[0].childNodes[0].data
                        primary_key_to = self._item.getElementsByTagName("primary_key_to")[0].childNodes[0].data
                        type = self._item.getElementsByTagName("type")[0].childNodes[0].data

                        where_item = None

                        try:
                            where_item = self._item.getElementsByTagName("where")[0]
                        except:
                            pass

                        # create action
                        apply = InsertReferenceAction(entity_from_id=entity_from_id,
                                                    entity_to_id=entity_to_id,
                                                    primary_key_from=primary_key_from,
                                                    primary_key_to=primary_key_to,
                                                    type=type,
                                                    where_item=where_item)

                    case "update_from_field":

                        # basic data
                        entity_from_id = self._item.getElementsByTagName("from")[0].childNodes[0].data
                        entity_to_id = self._item.getElementsByTagName("to")[0].childNodes[0].data
                        attribute_from_name = self._item.getElementsByTagName("attribute_from")[0].childNodes[0].data
                        attribute_to_name = self._item.getElementsByTagName("attribute_to")[0].childNodes[0].data
                        primary_key_from = self._item.getElementsByTagName("primary_key_from")[0].childNodes[0].data
                        primary_key_to = self._item.getElementsByTagName("primary_key_to")[0].childNodes[0].data
                        type = self._item.getElementsByTagName("type")[0].childNodes[0].data

                        filter_item = None
                        replace_item = None

                        try:
                            filter_item = self._item.getElementsByTagName("filter")[0]
                        except:
                            pass

                        try:
                            replace_item = self._item.getElementsByTagName("replace")[0]
                        except:
                            pass

                        # create action
                        apply = UpdateFromFieldAction(entity_from_id=entity_from_id,
                                                      entity_to_id=entity_to_id,
                                                      attribute_from_name=attribute_from_name,
                                                      attribute_to_name=attribute_to_name,
                                                      primary_key_from=primary_key_from,
                                                      primary_key_to=primary_key_to,
                                                      filter_item=filter_item,
                                                      replace_item=replace_item,
                                                      type=type)

                    case "update_from_value":

                        # basic data
                        entity_from_id = self._item.getElementsByTagName("from")[0].childNodes[0].data
                        entity_to_id = self._item.getElementsByTagName("to")[0].childNodes[0].data
                        attribute_to_name = self._item.getElementsByTagName("attribute_to")[0].childNodes[0].data
                        value = self._item.getElementsByTagName("value")[0].childNodes[0].data
                        primary_key_from = self._item.getElementsByTagName("primary_key_from")[0].childNodes[0].data
                        primary_key_to = self._item.getElementsByTagName("primary_key_to")[0].childNodes[0].data
                        type = self._item.getElementsByTagName("type")[0].childNodes[0].data

                        # create action
                        apply = UpdateFromValueAction(entity_from_id=entity_from_id,
                                                      entity_to_id=entity_to_id,
                                                      value=value,
                                                      attribute_to_name=attribute_to_name,
                                                      primary_key_from=primary_key_from,
                                                      primary_key_to=primary_key_to,
                                                      type=type)

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
