import os

import jinja2
from dotenv import load_dotenv

from core.extractors.mysql.Table import Table
from core.informers.DatabaseInformer import DatabaseInformer
from core.models.sdm.Attribute import Attribute
from core.models.sdm.Entity import Entity
from core.models.sdm.SimpleDatabaseModel import SimpleDatabaseModel


class SimpleDatabaseModelWriter:

    def __init__(self, tables: list[Table], database_informer: DatabaseInformer):

        load_dotenv('.workspace')

        self._tables = tables
        self._workspace = os.getenv('WORKSPACE')
        self._sdm_filename = "workspaces/{workspace}/models/{database_name}.sdm".format(workspace = self._workspace, database_name= database_informer.database())
        self._database_informer = database_informer

        template_loader = jinja2.FileSystemLoader(searchpath="./core/writers/sdm_templates")
        self._template_env = jinja2.Environment(loader=template_loader)

    def write(self) -> None:

        self._clear()

        self._write_in_template_without_parameter("g_opening.stub")

        # writing basic info
        self._write_in_template_without_parameter("database_info_opening.stub")
        self._write_in_template_simple_parameter("database_info_name.stub", self._database_informer.database())
        self._write_in_template_without_parameter("database_info_closing.stub")

        # writing entities
        for table in self._tables:

            entity_mockup = Entity(static=True, id=table.name())

            self._write_in_template("entity_opening.stub", entity=entity_mockup)

            # writing attributes
            for column in table.columns():

                attribute_mockup = Attribute(static=True, attribute_name=column.field(), attribute_type=column.type())

                self._write_in_template("attribute.stub", attribute=attribute_mockup)

            self._write_in_template("entity_closing.stub", entity=entity_mockup)

            self._insert_blank_line()

        self._write_in_template_without_parameter("g_closing.stub")

    def _write_in_template(self, template_file: str, entity: Entity = None, attribute: Attribute = None) -> None:

        template = self._template_env.get_template(template_file)
        render = template.render(entity=entity, attribute=attribute)

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

    def _write_in_template_simple_parameter(self, template_file: str, parameter: str):
        template = self._template_env.get_template(template_file)
        render = template.render(parameter=parameter)

        with open(self._sdm_filename, "a") as f:
            f.write("\n")
            f.write(render)

    def _clear(self):
        open(self._sdm_filename, 'w').close()

    def _insert_blank_line(self):
        with open(self._sdm_filename, "a") as f:
            f.write("\n")

    def sdm(self) -> SimpleDatabaseModel:
        return SimpleDatabaseModel(self._sdm_filename)
