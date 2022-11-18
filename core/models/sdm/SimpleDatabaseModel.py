import os
from xml.dom import minidom

from core.loaders.WorkspaceLoader import WorkspaceLoader
from core.models.sdm.Attribute import Attribute
from core.models.sdm.Entity import Entity
from core.models.sdm.ForeignKey import ForeignKey
from core.models.sdm.Relationship import Relationship


class SimpleDatabaseModel:

    def __init__(self, filename: str):

        # files
        self._filename = filename
        self._doc = minidom.parse(self._filename)

        # basic info
        self._database_name : str = ""
        self.entities_items: list[Entity] = list()
        self.relationships_items: list[Relationship] = list()

        # reading
        self._read_database_info()
        self._read_entities()
        self._read_relationships()

        # matching
        self.match_relations_and_entities()
        self.detect_foreign_keys()

        # transformo kernel
        self._workspace = WorkspaceLoader().name()

    def reload_sdm(self):
        self.__init__(self._filename)

    def _read_database_info(self) -> None:
        database_info = self._doc.getElementsByTagName('database')[0]
        self._database_name = database_info.getElementsByTagName("name")[0].childNodes[0].data

    def database_name(self):
        return self._database_name

    def _read_entities(self) -> None:
        items = self._doc.getElementsByTagName('entity')

        for i in items:
            entity = Entity(i)
            self.entities_items.append(entity)

    def entities(self) -> list[Entity]:
        return self.entities_items

    def _read_relationships(self) -> None:
        items = self._doc.getElementsByTagName('relation')

        for i in items:
            relation = Relationship(i)
            self.relationships_items.append(relation)

    def match_relations_and_entities(self) -> None:

        self.match_relationships()

        self.match_entities()

    def match_relationships(self) -> None:

        for r in self.relationships_items:
            r.set_entities(self.entities_items)

    def match_entities(self) -> None:

        for e in self.entities_items:
            e.set_relations(self.relationships_items)

    def detect_foreign_keys(self):

        for e in self.entities_items:

            foreign_keys: list[ForeignKey] = list()

            for r in e.relations():
                if r.second_entity().id() == e.id():
                    foreign_key = ForeignKey(r.first_entity())
                    foreign_keys.append(foreign_key)

            e.set_foreign_keys(foreign_keys)

    def relationships(self) -> list[Relationship]:
        return self.relationships_items

    def get_entity_by_id(self, id) -> Entity:
        res = None

        for e in self.entities():
            if e.id() == id:
                res = e
                break

        return res

    def contains_entity(self, entity) -> bool:

        res = False

        if self.get_entity_by_id(entity.id()) is not None:
            res = True

        return res

    '''On change properties '''

    def add_entity(self, entity_name):

        entity = Entity(static=True, id=entity_name)
        self.entities_items.append(entity)

    def edit_entity_name(self, entity, rename):

        entity.edit_name(rename)

    def delete_entity(self, entity):

        # delete entities in relations
        for e in self.entities_items:
            e.delete_entity_in_relationships(entity)

        # delete entity in all entities
        for i in range(len(self.entities_items)):

            if self.entities_items[i].id() == entity.id():
                self.entities_items.pop(i)
                break

        # delete entities in all relations
        for i in range(len(self.relationships_items)):

            if self.relationships_items[i].first_entity().id() == entity.id() or \
                    self.relationships_items[i].second_entity().id() == entity.id():
                self.relationships_items.pop(i)
                break

    def add_relationship(self, relationships) -> Relationship:

        first_entity = self.get_entity_by_id(relationships[0].getElementsByTagName("entity")[0].childNodes[0].data)
        second_entity = self.get_entity_by_id(relationships[1].getElementsByTagName("entity")[0].childNodes[0].data)
        first_entity_cardinality = relationships[0].getElementsByTagName("cardinality")[0].childNodes[0].data
        second_entity_cardinality = relationships[1].getElementsByTagName("cardinality")[0].childNodes[0].data

        # create relation
        relation = Relationship(
            static=True,
            first_entity=first_entity,
            second_entity=second_entity,
            first_entity_cardinality=first_entity_cardinality,
            second_entity_cardinality=second_entity_cardinality)

        # add to list
        self.relationships_items.append(relation)

        # matching between entities
        self.match_entities()

        return relation

    def add_attribute(self, entity, attribute_name, attribute_type):

        attribute = Attribute(static=True, attribute_name=attribute_name, attribute_type=attribute_type)

        entity.add_attribute(attribute=attribute)

    def edit_attribute_type(self, entity, attribute_name, retype):

        entity.edit_attribute_type(attribute_name=attribute_name, retype=retype)

    def edit_attribute_name(self, entity, attribute_name, rename):

        entity.edit_attribute_name(attribute_name=attribute_name, rename=rename)

    def delete_attribute(self, entity, attribute_name):

        entity.delete_attribute_name(attribute_name=attribute_name)

    # methods for actions extraction
    def contains_entity_by_id(self, entity: Entity):

        res = False

        for e in self.entities():

            if e.id() == entity.id():
                res = True
                break

        return res

    def filename(self) -> str:
        return self._filename

    def _set_context(self, context: str):

        new_filename = 'workspaces/{workspace}/models/{context}.sdm'.format(workspace=self._workspace, context=context)
        os.rename(self._filename, new_filename)
        self._filename = new_filename

    def set_as_source(self) -> None:
        self._set_context('source')

    def set_as_target(self) -> None:
        self._set_context('target')

    def print(self) -> str:

        print()

        print("########################################")

        print("original SDM file: " + self._filename)

        print("########################################")

        print()

        for e in self.entities():

            print(e)

            print("\n\t-- Attributes --")

            for attr in e.attributes():
                print("\t" + str(attr))

            print()

            print("\t-- Related entities --")

            for re in e.related_entities():
                print("\t" + str(re))

            print()

        print("-- All relationships --")
        for r in self.relationships():
            print(r)

        print()
