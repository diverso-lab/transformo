from core.models.stm.AvailableAction import AvailableAction
import jinja2
import os


class MigrationWriter:

    def __init__(
        self, 
        migration_model_name:str,
        migration_name:str, 
        available_action: AvailableAction = None,
        opening:bool = False,
        closing:bool = False):

        self._migration_model_name = migration_model_name
        self._migration_name = migration_name
        self._filename = "models/{}/{}.stm".format(migration_model_name, migration_name)
        self._available_action = available_action
        self._opening = opening
        self._closing = closing

        templateLoader = jinja2.FileSystemLoader(searchpath = "./core/writers/migration_templates")
        self._template_env = jinja2.Environment(loader = templateLoader)

        self._write()

    def filename(self):
        return self._filename

    def _write(self):

        

        if self._opening:

            try:
                os.mkdir("models/{}".format(self._migration_model_name))
            except:
                pass

                self._clear()
            self._write_in_template_without_parameter("g_opening.stub", blank_line= False)

        if self._closing:
            self._write_in_template_without_parameter("g_closing.stub", number_blank_lines=2)
            return self._finish()

        transformation_type = self._available_action.action().transformation_type()
        action_type = self._available_action.action().action_type()

        # write transformation of type ENTITY
        if transformation_type == "entity":

            if action_type == "create":

                self._write_in_template("create_entity_action.stub")

            if action_type == "rename":

                self._write_in_template("rename_entity_action.stub")

            if action_type == "delete":

                self._write_in_template("delete_entity_action.stub")

        # write transformation of type ATTRIBUTE
        if transformation_type == "attribute":

            if action_type == "create":

                self._write_in_template("create_attribute_action.stub")

            if action_type == "rename":

                self._write_in_template("rename_attribute_action.stub")

            if action_type == "retype":

                self._write_in_template("retype_attribute_action.stub")

            if action_type == "move":

                self._write_in_template("move_attribute_action.stub")

            if action_type == "delete":

                self._write_in_template("delete_attribute_action.stub")

    def _write_in_template(self, template_file):
        
        template = self._template_env.get_template(template_file)
        render = template.render(action = self._available_action.action())

        with open(self._filename, "a") as f:
            f.write("\n")
            f.write(render)

    def _write_in_template_without_parameter(self, template_file: str, blank_line = True, number_blank_lines = 1):

        template = self._template_env.get_template(template_file)
        render = template.render()

        with open(self._filename, "a") as f:
            if blank_line:
                for i in range(number_blank_lines):
                    f.write("\n")
            f.write(render)

    def _clear(self):
        open(self._filename, 'w').close()

    def _finish(self):
        pass

