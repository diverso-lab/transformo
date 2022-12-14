import os

import jinja2

from core.models.sdm.Attribute import Attribute
from core.models.sdm.Entity import Entity
from core.models.sdm.SimpleDatabaseModel import SimpleDatabaseModel


class SimpleDatabaseModelWriter:

    def __init__(self, sdm: SimpleDatabaseModel, sdm_filename: str, folder: str) -> None:
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

        # writing basic info
        self._write_in_template_without_parameter("database_info_opening.stub")
        self._write_in_template_simple_parameter("database_info_name.stub", self._sdm.database_name())
        self._write_in_template_without_parameter("database_info_closing.stub")

        # writing entities
        for entity in self._sdm.entities():

            self._write_in_template("entity_opening.stub", entity=entity)

            # writing attributes
            for attribute in entity.attributes():
                self._write_in_template("attribute.stub", attribute=attribute)

            self._write_in_template("entity_closing.stub", entity=entity)

            self._insert_blank_line()

        self._write_in_template_without_parameter("g_closing.stub")

    def _write_in_template(self, template_file: str, entity: Entity = None, attribute: Attribute = None) -> None:

        template = self._template_env.get_template(template_file)
        render = template.render(entity=entity, attribute=attribute)

        with open(self._sdm_filename, "a") as f:
            f.write("\n")
            f.write(render)

    def _write_in_template_simple_parameter(self, template_file: str, parameter: str):
        template = self._template_env.get_template(template_file)
        render = template.render(parameter=parameter)

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

    def _insert_blank_line(self):
        with open(self._sdm_filename, "a") as f:
            f.write("\n")
