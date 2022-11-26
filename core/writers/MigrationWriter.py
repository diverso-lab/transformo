from core.loaders.WorkspaceLoader import WorkspaceLoader
from core.models.stm.AvailableAction import AvailableAction
import jinja2
import os

from core.models.stm.SimpleTransformationModel import SimpleTransformationModel
from core.models.stm.actions.AbstractAction import AbstractAction


class MigrationWriter:

    def __init__(
            self,
            migration_model_name: str,
            migration_name: str,
            abstract_action: AbstractAction = None,
            opening: bool = False):

        self._workspace = WorkspaceLoader().name()
        self._migration_model_name = migration_model_name
        self._migration_name = migration_name
        self._stm_filename = "workspaces/{workspace}/migrations/{migration_name}/{migration_name}.stm".format(
            workspace=self._workspace, migration_name=self._migration_name)
        self._abstract_action = abstract_action
        self._opening = opening

        template_loader = jinja2.FileSystemLoader(searchpath="./core/writers/migration_templates")
        self._template_env = jinja2.Environment(loader=template_loader)

    def stm_filename(self):
        return self._stm_filename

    def stm(self) -> SimpleTransformationModel:

        return SimpleTransformationModel(stm_file=self._stm_filename)

    def write(self):

        if self._opening:

            try:
                os.mkdir("workspaces/{workspace}/migrations/{migration_name}".format(workspace=self._workspace,
                                                                                     migration_name=self._migration_name))
                open(self._stm_filename, "w").close()
            except:
                pass

            self._write_in_template_without_parameter("g_opening.stub", blank_line=False)

        else:

            # delete last "</stm>"
            with open(self._stm_filename, "r+") as f:
                current_position = previous_position = f.tell()
                while f.readline():
                    previous_position = current_position
                    current_position = f.tell()
                f.truncate(previous_position)
                f.close()

        transformation_type = self._abstract_action.transformation_type()
        action_type = self._abstract_action.action_type()

        match transformation_type:

            case "entity":

                match action_type:

                    case "create":
                        self._write_in_template("create_entity_action.stub")

                    case "rename":
                        self._write_in_template("rename_entity_action.stub")

                    case "delete":
                        self._write_in_template("delete_entity_action.stub")

            case "attribute":

                match action_type:

                    case "create":
                        self._write_in_template("create_attribute_action.stub")

                    case "rename":
                        self._write_in_template("rename_attribute_action.stub")

                    case "retype":
                        self._write_in_template("retype_attribute_action.stub")

                    case "move":
                        self._write_in_template("move_attribute_action.stub")

                    case "copy":
                        self._write_in_template("copy_attribute_action.stub")

                    case "delete":
                        self._write_in_template("delete_attribute_action.stub")

        self._write_in_template_without_parameter("g_closing.stub", number_blank_lines=2)

    def _write_in_template(self, template_file):

        template = self._template_env.get_template(template_file)
        render = template.render(action=self._abstract_action)

        with open(self._stm_filename, "a") as f:
            f.write("\n")
            f.write(render)

    def _write_in_template_without_parameter(self, template_file: str, blank_line=True, number_blank_lines=1):

        template = self._template_env.get_template(template_file)
        render = template.render()

        with open(self._stm_filename, "a") as f:
            if blank_line:
                for i in range(number_blank_lines):
                    f.write("\n")
            f.write(render)

    def _finish(self):
        pass
