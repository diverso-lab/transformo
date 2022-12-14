from core.models.stm.actions.CreateAttributeAction import CreateAttributeAction
from core.models.stm.actions.DeleteAttributeAction import DeleteAttributeAction
from core.models.sdm.SimpleDatabaseModel import SimpleDatabaseModel
from core.models.stm.AvailableAction import AvailableAction
from core.models.stm.actions.CreateEntityAction import CreateEntityAction
from core.models.stm.actions.DeleteEntityAction import DeleteEntityAction
from core.models.stm.actions.MoveAttributeAction import MoveAttributeAction
from core.models.stm.actions.RenameAttributeAction import RenameAttributeAction
from core.models.stm.actions.RenameEntityAction import RenameEntityAction
from core.models.stm.actions.RetypeAttributeAction import RetypeAttributeAction


class AvailableActionsExtractor:

    def __init__(self, sdm_source: SimpleDatabaseModel, sdm_target: SimpleDatabaseModel) -> None:

        self._A = sdm_source
        self._B = sdm_target
        self._available_actions: list[AvailableAction] = list()

    def A(self):
        return self._A

    def B(self):
        return self._B

    def extract_available_actions(self):

        self.first_priority()
        self.second_priority()
        self.third_priority()

    def available_actions(self):

        # extract entity actions
        self.extract_create_entity_actions()
        self.extract_rename_entity_actions()
        self.extract_delete_entity_actions()

        # extract attributes actions
        self.extract_create_attribute_actions()
        self.extract_rename_attribute_actions()
        self.extract_retype_attribute_actions()
        self.extract_move_attribute_actions()
        self.extract_delete_attribute_actions()

        return self._available_actions

    def first_priority(self):

        self.extract_rename_entity_actions()
        self.extract_rename_attribute_actions()
        self.extract_retype_attribute_actions()
        self.extract_move_attribute_actions()

        return self._available_actions

    def second_priority(self):

        self.extract_create_entity_actions()
        self.extract_create_attribute_actions()

        return self._available_actions

    def third_priority(self):

        self.extract_delete_entity_actions()
        self.extract_delete_attribute_actions()

        return self._available_actions

    def add_action(self, action: any):

        available_action = AvailableAction(action)
        self._available_actions.append(available_action)

    # extractions

    def extract_create_entity_actions(self):

        for e in self._B.entities():
            if not self._A.contains_entity_by_id(e):
                action = CreateEntityAction(entity_id = e.id())
                self.add_action(action)

    def extract_rename_entity_actions(self):

        for eB in self._B.entities():

            for eA in self._A.entities():

                if not eA.id() == eB.id():

                    if eA.contains_same_attributes(eB):
                        action = RenameEntityAction(entity_id=eA.id(), rename_entity_id=eB.id())
                        self.add_action(action)

    def extract_delete_entity_actions(self):

        for e in self._A.entities():
            if not self._B.contains_entity_by_id(e):
                action = DeleteEntityAction(e.id())
                self.add_action(action)

    def extract_create_attribute_actions(self):

        for eB in self._B.entities():

            for eA in self._A.entities():

                if eA.id() == eB.id():

                    for attribute in eB.attributes():

                        if not eA.contains_attribute_by_name(attribute.name()):
                            action = CreateAttributeAction(entity_id=eB.id(), attribute_name=attribute.name(),
                                                           type=attribute.type())
                            self.add_action(action)

    def extract_rename_attribute_actions(self):

        for eB in self._B.entities():

            for eA in self._A.entities():

                if eA.id() == eB.id():

                    for attB in eB.attributes():

                        if not eA.contains_attribute_by_name(attB.name()):

                            for attA in eA.attributes():

                                if attA.type() == attB.type():
                                    action = RenameAttributeAction(entity_id=eB.id(), attribute_name=attA.name(),
                                                                   rename_attribute_name=attB.name(), )
                                    self.add_action(action)

    def extract_retype_attribute_actions(self):

        for eB in self._B.entities():

            for eA in self._A.entities():

                if eA.id() == eB.id():

                    for attB in eB.attributes():

                        if eA.contains_attribute_by_name(attB.name()):

                            attA = eA.get_attribute_by_name(attB.name())

                            if not attA.type() == attB.type():
                                action = RetypeAttributeAction(entity_id=eB.id(), attribute_name=attB.name(), retype_name=attB.type())
                                self.add_action(action)

    def extract_move_attribute_actions(self):

        for eA in self._A.entities():

            for eB in self._B.entities():

                if not eA.id() == eB.id():

                    if self._A.contains_entity(eB):

                        for attA in eA.attributes():

                            if eB.contains_attribute(attA):
                                action = MoveAttributeAction(entity_from_id=eA.id(), entity_to_id=eB.id(), attribute_name=attA.name(),
                                                             type=attA.type())
                                self.add_action(action)

    def extract_delete_attribute_actions(self):

        for eA in self._A.entities():

            for eB in self._B.entities():

                if eA.id() == eB.id():

                    for attA in eA.attributes():

                        if not eB.contains_attribute(attA):
                            action = DeleteAttributeAction(entity_id=eB.id(), attribute_name=attA.name())
                            self.add_action(action)

    def extract_move_relation_actions(self):
        pass

    def print(self):

        print(str(len(self._available_actions)) + " available actions")
        print()

        for i in range(len(self._available_actions)):
            print("\t" + str(i) + " -> " + str(self._available_actions[i]))
            print()
