import os

from flamapy.metamodels.fm_metamodel.models import Feature

from core.loaders.WorkspaceLoader import WorkspaceLoader
from core.models.mm import MigrationModel
from core.models.sdm.SimpleDatabaseModel import SimpleDatabaseModel
from core.models.stm.AvailableActionsExtractor import AvailableActionsExtractor
from core.models.stm.AvailableAction import AvailableAction
from core.models.stm.SimpleTransformationModel import SimpleTransformationModel
from core.models.stm.actions.AbstractAction import AbstractAction
from core.models.stm.actions.CopyAttributeAction import CopyAttributeAction
from core.mutators.SimpleDatabaseModelMutator import SimpleDatabaseModelMutator
from core.writers.MigrationWriter import MigrationWriter


class Migration:

    def __init__(self, migration_model: MigrationModel, feature: Feature):

        # basic
        self._migration_model: MigrationModel = migration_model
        self._feature: Feature = feature
        self._workspace: str = WorkspaceLoader().name()

        # derivative
        self._migration_name: str = self._feature.name
        self._current_sdm_source: SimpleDatabaseModel = self.current_sdm_source()
        self._sdm_target = migration_model.sdm_target()

        # for operations
        self._selected_actions: list[AvailableAction] = list()

    def __str__(self):
        return self._feature.__str__()

    # facades method
    def name(self):
        return self._feature.name

    def is_root(self):
        return self._feature.is_root()

    def is_abstract(self):
        return self._feature.is_abstract

    def is_leaf(self):
        return self._feature.is_leaf()

    def _calculate_actions_counter(self) -> int:

        stm = self.stm()

        if stm is None:
            return 0
        else:
            return len(stm.transformations()) - 1

    def current_sdm_source(self) -> SimpleDatabaseModel:

        stm = self.stm()

        if stm is None:
            return self._migration_model.sdm_source()
        else:

            suffix = len(stm.transformations()) - 1

            sdm_file = 'workspaces/{workspace}/migrations/{migration_name}/{migration_name}_{suffix}.sdm'.format(
                workspace=self._workspace,
                migration_name=self._migration_name,
                suffix=suffix)

            if not os.path.isfile(sdm_file):
                return None
            else:
                return SimpleDatabaseModel(filename=sdm_file)

    def sdm_target(self) -> SimpleDatabaseModel:
        return self._sdm_target

    def _is_opening(self) -> bool:

        return not os.path.isfile('workspaces/{workspace}/migrations/{migration_name}/{migration_name}.stm'.format(
            workspace=self._workspace,
            migration_name=self._migration_name))

    def _show_basic_info(self) -> None:

        os.system('clear')
        print("########################################")
        print("{workspace}: MIGRATION WIZARD".format(workspace=self._workspace))
        print("########################################")
        print()
        print("-> Working on migration: {}".format(self._migration_name))
        print()
        print('-> Current actions')
        print()

        stm = self.stm()
        if not stm is None:

            for t in stm.transformations():
                for a in t.actions():
                    print("\t" + a.apply().info())
                    print()

        else:

            print("No actions defined")

    def _show_and_select_abstract_action(self) -> AbstractAction | None:

        abstract_action = None

        print("-> Available action(s)")
        print()
        print("\t[0] Create entity")
        print("\t[1] Rename entity")
        print("\t[2] Delete entity")
        print()
        print("\t[3] Create attribute")
        print("\t[4] Rename attribute")
        print("\t[5] Retype attribute")
        print("\t[6] Move attribute")
        print("\t[7] Copy attribute")
        print("\t[8] Delete attribute")

        print("")

        inputted = str(input("Select an action ('q' for quit): "))

        if inputted == "q":
            return abstract_action

        match int(inputted):
            case 7:
                abstract_action = self._define_copy_attribute_action()
            case _:
                pass

        return abstract_action

    def define(self) -> None:

        self._show_basic_info()

        abstract_action = self._show_and_select_abstract_action()

        if abstract_action is None:
            return

        # write transformation in STM file
        migration_writer = MigrationWriter(
            migration_model_name=self._migration_model.root(),
            migration_name=self._migration_name,
            abstract_action=abstract_action,
            opening=self._is_opening()
        )
        migration_writer.write()
        last_stm = migration_writer.stm()

        # mutates previous SDM
        sdm_mutator = SimpleDatabaseModelMutator(
            current_sdm_source=self._current_sdm_source,
            last_stm=last_stm,
            actions_counter=self._calculate_actions_counter(),
            migration_name=self._migration_name,
            folder="{}/{}".format(self._migration_model.root(), self._migration_name))

        sdm_mutator.mutate()
        self._current_sdm_source = sdm_mutator.new_sdm()

        # recursive call
        return self.define()

    def _define_copy_attribute_action(self) -> AbstractAction:

        # TODO: Refactoring

        entities_source = self.current_sdm_source().entities()
        entities_target = self.sdm_target().entities()

        #### SELECT ENTITY FROM SOURCE
        os.system('clear')
        print("[**] Select entity from source")
        print("[  ] Select attribute from source")
        print("[  ] Select entity from target")
        print("[  ] Select attribute from target")
        print()

        counter = 0
        for e in entities_source:
            print("[{counter}] {entity_name}".format(counter=counter, entity_name=e.name()))
            counter = counter + 1

        print()
        inputted = str(input("Select entity from source database ('q' for quit):"))

        if inputted == "q":
            return self.define()

        entity_from = entities_source[int(inputted)]

        #### SELECT ATTRIBUTE
        os.system('clear')
        print("[OK] Select entity from source ({entity_from})".format(entity_from=entity_from))
        print("[**] Select attribute from source")
        print("[  ] Select entity from target")
        print("[  ] Select attribute from target")
        print()

        counter = 0
        for attr in entity_from.attributes():
            print("[{counter}] {attr_name} ({type})".format(counter=counter, attr_name=attr.name(), type=attr.type()))
            counter = counter + 1

        print()
        inputted = str(input("Select attribute from entity ('q' for quit):"))

        if inputted == "q":
            return self.define()

        attribute_from = entity_from.attributes()[int(inputted)]

        #### SELECT ENTITY FROM TARGET
        os.system('clear')
        print("[OK] Select entity from source ({entity_from})".format(entity_from=entity_from.name()))
        print("[OK] Select attribute from source")
        print("[**] Select entity from target")
        print("[  ] Select attribute from target")
        print()

        counter = 0
        for e in entities_target:
            print("[{counter}] {entity_name}".format(counter=counter, entity_name=e.name()))
            counter = counter + 1

        print()
        inputted = str(input("Select entity from target database ('q' for quit):"))

        if inputted == "q":
            return self.define()

        entity_to = entities_target[int(inputted)]

        #### SELECT ATTRIBUTE FROM TARGET
        os.system('clear')
        print("[OK] Select entity from source ({entity_from})".format(entity_from=entity_from.name()))
        print("[OK] Select attribute from source")
        print("[OK] Select entity from target")
        print("[  ] Select attribute from target")
        print()

        counter = 0
        for attr in entity_to.attributes():
            print("[{counter}] {attr_name} ({type})".format(counter=counter, attr_name=attr.name(), type=attr.type()))
            counter = counter + 1

        print()
        inputted = str(input("Select attribute from entity ('q' for quit):"))

        if inputted == "q":
            return self.define()

        attribute_to = entity_to.attributes()[int(inputted)]

        action = CopyAttributeAction(entity_from_id=entity_from.id(),
                                     entity_to_id=entity_to.id(),
                                     attribute_from_name=attribute_from.name(),
                                     attribute_to_name=attribute_to.name(),
                                     type=attribute_from.type())

        return action

    def _finish(self):
        pass

    def stm(self) -> SimpleTransformationModel | None:

        stm_file = 'workspaces/{workspace}/migrations/{migration_name}/{migration_name}.stm'.format(
            workspace=self._workspace, migration_name=self._migration_name)

        if not os.path.isfile(stm_file):
            return None
        else:
            return SimpleTransformationModel(stm_file=stm_file)

