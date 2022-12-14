from core.models.sdm.Attribute import Attribute
from core.models.sdm.ForeignKey import ForeignKey
from core.models.sdm.Relationship import Relationship


class Entity:

    def __init__(self, item = None, static = False, id = None):

        if not static:

            self.item = item

            self.__name = item.getElementsByTagName("name")[0].childNodes[0].data

            self.__id = item.getAttribute('id')

            self.__attributes_items : list[Attribute] = list()

            self.__read_attributes(item.getElementsByTagName("attribute"))

            self.__relations_items : list[Relationship] = list()

            self.__foreign_keys : list[ForeignKey] = list()

        else:

            self.item = None

            self.__name = id

            self.__id = id

            self.__attributes_items : list[Attribute] = list()

            self.__relations_items : list[Relationship] = list()

            self.__foreign_keys : list[ForeignKey] = list()

    def __read_attributes(self, attribute_items):

        for a in attribute_items:

            attribute = Attribute(a)

            self.__attributes_items.append(attribute)

    def set_relations(self, relations):

        for r in relations:

            if not r in self.relations():

                if (r.first_entity().id() == self.id()) :
                    self.add_relation(r)

                if (r.second_entity().id() == self.id()) :
                    self.add_relation(r)

    def delete_entity_in_relationships(self, entity):

        for i in range(len(self.__relations_items)):

            if self.__relations_items[i].first_entity().id() == entity.id() or self.__relations_items[i].second_entity().id() == entity.id():
                self.__relations_items.pop(i)
                break


    def clear_relations(self):
        self.__relations_items = list()

    def add_relation(self, relation):
        self.__relations_items.append(relation)

    def set_foreign_keys(self, foreign_keys):
        self.__foreign_keys = foreign_keys

    def name(self):
        return self.__name
    
    def id(self):
        return self.__id

    def attributes(self):
        return self.__attributes_items

    def relations(self):
        return self.__relations_items

    def add_attribute(self, attribute):
        self.__attributes_items.append(attribute)

    def edit_name(self, rename):
        self.__id = rename
        self.__name = rename

    def edit_attribute_type(self, attribute_name, retype):

        for a in self.__attributes_items:

            if a.name() == attribute_name:
                a.set_type(retype)
                break

    def edit_attribute_name(self, attribute_name, rename):

        for a in self.__attributes_items:

            if a.name() == attribute_name:
                a.set_name(rename)
                break

    def delete_attribute_name(self, attribute_name):

        for i in range(len(self.__attributes_items)):

            if self.__attributes_items[i].name() == attribute_name:
                self.__attributes_items.pop(i)
                break

    # Derivated operations
    def related_entities(self):

        related_entities = []

        for r in self.relations():

            print("\t"+str(r))

            if(r.first_entity() != self):
                related_entities.append(r.first_entity() )

            if(r.second_entity() != self):
                related_entities.append(r.second_entity() )

        return set(related_entities)

    def foreign_keys(self):
        return self.__foreign_keys

    def contains_same_attributes(self, entity):

        res = True

        # check attributes list length
        if(len(self.attributes()) == len(entity.attributes())):

            # sort
            self.attributes().sort(key = lambda x: x.name())
            entity.attributes().sort(key = lambda x: x.name())

            for i in range(len(self.attributes())):

                if(self.attributes()[i].name() != entity.attributes()[i].name()):

                    res = False
                    break

        else:

            res = False
        
        return res

    def contains_attribute_by_name(self, attribute_name):

        res = False

        for a in self.attributes():

            if a.name() == attribute_name:
                res = True
                break

        return res

    def contains_attribute(self, attribute):

        res = False

        for a in self.attributes():

            if a.name() == attribute.name() and a.type() == attribute.type():
                res = True
                break

        return res

    def get_attribute_by_name(self, attribute_name):

        res = None

        for a in self.attributes():

            if a.name() == attribute_name:
                res = a
                break
        
        return res

    def __str__(self) -> str:
        return "Entity: " + self.name() + " (id = \"" + self.id() + "\", number of attributes = " +str(len(self.attributes())) + ")"