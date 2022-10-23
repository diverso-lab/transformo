import jinja2

from core.models.mm.Migration import Migration


class MySQLWriter:

    def __init__(self, selected_migrations: list[Migration], root: str) -> None:
        self._selected_migrations = selected_migrations
        self._root = root
        self._sql_filename = "models/{}/{}.sql".format(self._root, self._root)

        template_loader = jinja2.FileSystemLoader(searchpath="./core/writers/mysql_templates")
        self._template_env = jinja2.Environment(loader=template_loader)

    def filename(self):
        return self._sql_filename

    def write(self):

        # delete previous MySQL file
        open(self._sql_filename, "w").close()

        for migration in self._selected_migrations:

            for transformation in migration.stm().transformations():

                transformation_type = transformation.type()

                for action in transformation.actions():

                    action_type = action.type()

                    match transformation_type:

                        case "entity":

                            match action_type:

                                case "create":
                                    self._write_action(transformation, action, "create_entity_action.stub")

                                case "rename":
                                    self._write_action(transformation, action, "rename_entity_action.stub")

                                case "delete":
                                    self._write_action(transformation, action, "delete_entity_action.stub")

                        case "attribute":

                            match action_type:

                                case "create":
                                    self._write_action(transformation, action, "create_attribute_action.stub")

                                case "rename":
                                    self._write_action(transformation, action, "rename_attribute_action.stub")

                                case "retype":
                                    self._write_action(transformation, action, "retype_attribute_action.stub")

                                case "move":
                                    self._write_action(transformation, action, "move_attribute_action.stub")

                                case "delete":
                                    self._write_action(transformation, action, "delete_attribute_action.stub")

    def _write_action(self, transformation, action, template_file):

        template = self._template_env.get_template(template_file)
        render = template.render(
            transformation_name=transformation.id(),
            database_name_from="DATABASE_FROM",
            database_name_to="DATABASE_TO",
            action=action.apply())

        with open(self._sql_filename, "a") as f:
            f.write("\n\n")
            f.write(render)
