import jinja2

from core.extractors.mysql.Table import Table
from core.informers.DatabaseInformer import DatabaseInformer


class SimpleDatabaseModelWriter:

    def __init__(self, tables: list[Table], database_informer: DatabaseInformer):

        self._sdm_filename = "{}.sdm".format(database_informer.database())

        template_loader = jinja2.FileSystemLoader(searchpath="./core/writers/sdm_templates")
        self._template_env = jinja2.Environment(loader=template_loader)

    def write(self) -> None:

        self._clear()

        self._write_in_template_without_parameter("g_opening.stub")

        self._write_in_template_without_parameter("g_closing.stub")

    def _write_in_template_without_parameter(self, template_file: str, blank_line=True, number_blank_lines=1):

        template = self._template_env.get_template(template_file)
        render = template.render()

        with open(self._sdm_filename, "a") as f:
            if blank_line:
                for i in range(number_blank_lines):
                    f.write("\n")
            f.write(render)

    def _clear(self):
        open(self._sdm_filename, 'w').close()