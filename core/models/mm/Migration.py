import os

from flamapy.metamodels.fm_metamodel.models import Feature

from core.loaders.WorkspaceLoader import WorkspaceLoader
from core.models.mm import MigrationModel
from core.models.sdm.SimpleDatabaseModel import SimpleDatabaseModel
from core.models.stm.AvailableActionsExtractor import AvailableActionsExtractor
from core.models.stm.AvailableAction import AvailableAction
from core.models.stm.SimpleTransformationModel import SimpleTransformationModel
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
        self._current_sdm_source: SimpleDatabaseModel = migration_model.sdm_source()
        self._sdm_target = migration_model.sdm_target()

        # for operations
        self._selected_actions: list[AvailableAction] = list()
        self._actions_counter: int = 0

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

    def current_sdm_source(self) -> SimpleDatabaseModel:
        return self._current_sdm_source

    def sdm_target(self) -> SimpleDatabaseModel:
        return self._sdm_target

    def define(self, opening=True) -> None:
        os.system('cls')
        print("########################################")
        print("{workspace}: MIGRATION WIZARD".format(workspace=self._workspace))
        print("########################################")
        print()
        print("-> Working on migration: {}".format(self._migration_name))
        print()
        print('-> Current actions')
        print('\t-> TODO')

        print()
        print("[0] Create entity")
        print("[1] Rename entity")
        print("[2] Delete entity")
        print()
        print("[3] Create attribute")
        print("[4] Rename attribute")
        print("[5] Retype attribute")
        print("[6] Move attribute")
        print("[7] Copy attribute")
        print("[8] Delete attribute")

        print("")

        inputted = str(input("Select an action ('q' for quit): "))

        if inputted == "q":
            return

        match int(inputted):
            case 7:
                self._define_copy_attribute_action()
            case _:
                pass

        return self.define()

        '''
        print(self._migration_model.root())

        extractor = AvailableActionsExtractor(sdm_source=self._current_sdm_source,
                                              sdm_target=self._migration_model.sdm_target())

        extractor.extract_available_actions()

        if len(extractor.available_actions()) == 0:
            return self._finish()

        # show migration info
        print()
        print("########################################")
        print("Current migration: {}".format(self._migration_name))
        print("########################################")
        print()

        # show available actions
        extractor.print()

        print("")

        inputted = str(input("Select an available action ('q' for quit): "))

        if inputted == "q":
            return self._finish()

        option = None
        try:
            option = int(inputted)
        except:
            self.define(opening=True)

        # selection of action from available actions in current SDM
        selected_action = extractor.available_actions()[option]
        self._selected_actions.append(selected_action)
        print("Selected action: \n")
        print(selected_action)

        # write transformation in STM file
        migration_writer = MigrationWriter(
            migration_model_name=self._migration_model.root(),
            migration_name=self._migration_name,
            available_action=selected_action,
            opening=opening,
            closing=False
        )
        migration_writer.write()
        last_stm = migration_writer.stm()

        # mutates previous SDM
        sdm_mutator = SimpleDatabaseModelMutator(
            current_sdm_source=self._current_sdm_source,
            last_stm=last_stm,
            actions_counter=self._actions_counter,
            migration_name=self._migration_name,
            folder="{}/{}".format(self._migration_model.root(), self._migration_name))

        sdm_mutator.mutate()
        self._current_sdm_source = sdm_mutator.new_sdm()

        # increments actions counter
        self._actions_counter = self._actions_counter + 1

        # recursive call
        self.define(opening=False)
        '''

    def _define_copy_attribute_action(self):

        # TODO: Refactoring

        entities_source = self.current_sdm_source().entities()
        entities_target = self.sdm_target().entities()

        #### SELECT ENTITY FROM SOURCE
        os.system('cls')
        print("[**] Select entity from source")
        print("[  ] Select attribute from source")
        print("[  ] Select entity from target")
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
        os.system('cls')
        print("[OK] Select entity from source ({entity_from})".format(entity_from=entity_from))
        print("[**] Select attribute from source")
        print("[  ] Select entity from target")
        print()

        counter = 0
        for attr in entity_from.attributes():
            print("[{counter}] {attr_name} ({type})".format(counter=counter, attr_name=attr.name(), type=attr.type()))
            counter = counter + 1

        print()
        inputted = str(input("Select attribute from entity ('q' for quit):"))

        if inputted == "q":
            return self.define()

        attribute = entity_from.attributes()[int(inputted)]


        #### SELECT ENTITY FROM TARGET
        os.system('cls')
        print("[OK] Select entity from source ({entity_from})".format(entity_from=entity_from))
        print("[OK] Select attribute from source")
        print("[**] Select entity from target")
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
        action = CopyAttributeAction(entity_from_id=entity_from.id(), entity_to_id=entity_to.id(),
                                    attribute_name=attribute.name(), type=attribute.type())


        print("[{}]Entity")

    def _finish(self):
        pass

    def stm(self) -> SimpleTransformationModel:
        return SimpleTransformationModel(stm_file='workspaces/{workspace}/migrations'
                                                  '/{migration_name}/{migration_name}.stm'
                                         .format(workspace=self._workspace, migration_name=self._migration_name))
