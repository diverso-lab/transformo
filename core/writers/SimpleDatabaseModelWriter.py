import os

import jinja2

from core.models.sdm.SimpleDatabaseModel import SimpleDatabaseModel


class SimpleDatabaseModelWriter:

    def __init__(self, sdm: SimpleDatabaseModel, sdm_filename: str, folder:str) -> None:
        self._sdm = sdm
        self._sdm_filename = sdm_filename
        self._folder = folder

        template_loader = jinja2.FileSystemLoader(searchpath="./core/writers/sdm_templates")
        self._template_env = jinja2.Environment(loader=template_loader)

    def write(self) -> None:

        self._clear()

        try:
            os.mkdir("models/{}".format(self._folder))
        except:
            pass

        self._write_in_template_without_parameter("g_opening.stub")

        for entity in self._sdm.entities():
            pass

        self._write_in_template_without_parameter("g_closing.stub")

    def _write_in_template(self, template_file: str) -> None:

        template = self._template_env.get_template(template_file)
        render = template.render(action=self._available_action.action())

        with open(self._sdm_filename, "a") as f:
            f.write("\n")
            f.write(render)

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
