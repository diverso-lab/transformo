from flamapy.metamodels.fm_metamodel.models import Feature

from core.loaders.WorkspaceLoader import WorkspaceLoader
from core.models.mm import MigrationModel
from core.models.stm.AvailableActionsExtractor import AvailableActionsExtractor
from core.models.stm.AvailableAction import AvailableAction
from core.models.stm.SimpleTransformationModel import SimpleTransformationModel
from core.mutators.SimpleDatabaseModelMutator import SimpleDatabaseModelMutator
from core.writers.MigrationWriter import MigrationWriter


class Migration:

    def __init__(self, migration_model: MigrationModel, feature: Feature):

        # basic
        self._migration_model = migration_model
        self._feature = feature
        self._workspace: str = WorkspaceLoader().name()

        # derivative
        self._migration_name = self._feature.name
        self._current_sdm_source = migration_model.sdm_source()

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

    def define(self, opening=True) -> None:

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

    def _finish(self):
        pass

    def stm(self) -> SimpleTransformationModel:
        return SimpleTransformationModel(stm_file='workspaces/{workspace}/migrations'
                                                  '/{migration_name}/{migration_name}.stm'
                                         .format(workspace=self._workspace, migration_name=self._migration_name))
