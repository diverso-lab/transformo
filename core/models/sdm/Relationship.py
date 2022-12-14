class Relationship:

    def __init__(self, item = None, static = False, first_entity = None, second_entity = None, first_entity_cardinality = None, second_entity_cardinality = None):

        if not static:

            self.item = item

            self.one_1 = None
            self.one_2 = None

            self.many_1 = None
            self.many_2 = None

            self.__first_entity = None
            self.__second_entity = None

            self.__first_entity_cardinality = None
            self.__second_entity_cardinality = None

            self.__get_value(item = item, type = "one")

            self.__get_value(item = item, type = "many")

            if(not self.__check_max_counter()):
                raise('There must be exactly two entities involved in a relationship')

        else:

            self.__first_entity = first_entity
            self.__second_entity = second_entity

            self.__first_entity_cardinality = first_entity_cardinality
            self.__second_entity_cardinality = second_entity_cardinality

            self.__get_value_static()

    def __check_max_counter(self):
        counter = 0

        if (self.one_1 != None):
            counter = counter + 1

        if (self.one_2 != None):
            counter = counter + 1

        if (self.many_1 != None):
            counter = counter + 1

        if (self.many_2 != None):
            counter += 1

        return counter == 2

    def __get_value(self, item, type):

        ones_manies = item.getElementsByTagName(type)

        if len(ones_manies) == 2:

            if type == "one":
                setattr(self, "one_1", item.getElementsByTagName(type)[0].getAttribute('id') )
                setattr(self, "one_2", item.getElementsByTagName(type)[1].getAttribute('id') )

            if type == "many":
                setattr(self, "many_1", item.getElementsByTagName(type)[0].getAttribute('id') )
                setattr(self, "many_2", item.getElementsByTagName(type)[1].getAttribute('id') )

        if len(ones_manies) == 1:

            if type == "one":
                setattr(self, "one_1", item.getElementsByTagName(type)[0].getAttribute('id') )

            if type == "many":
                setattr(self, "many_1", item.getElementsByTagName(type)[0].getAttribute('id') )

    def __get_value_static(self):

        self.one_1 = None
        self.one_2 = None

        self.many_1 = None
        self.many_2 = None

        if self.__first_entity_cardinality == "one" :

            self.one_1 = self.first_entity().id()

        if self.__first_entity_cardinality == "many" :

            self.many_1 = self.first_entity().id()

        if self.__second_entity_cardinality == "one" :

            self.one_2 = self.second_entity().id()

        if self.__second_entity_cardinality == "many" :

            self.many_2 = self.second_entity().id()


    def set_entities(self, entities):
        
        max_entity = 0

        for e in entities:

            if(self.one_1 == e.id()):

                max_entity = self.__associate_entity(entity = e, cardinality = "one", max_entity = max_entity)

            if(self.one_2 == e.id()):

                max_entity = self.__associate_entity(entity = e, cardinality = "one", max_entity = max_entity)

            if(self.many_1 == e.id()):

                max_entity = self.__associate_entity(entity = e, cardinality = "many", max_entity = max_entity)

            if(self.many_2 == e.id()):

                max_entity = self.__associate_entity(entity = e, cardinality = "many", max_entity = max_entity)

        if not max_entity == 2:
            raise('One or more relationships could not be created. Check the identifiers.')

    def __associate_entity(self, entity, cardinality, max_entity):

        if max_entity == 0:
            self.__first_entity = entity
            self.__first_entity_cardinality = cardinality

        if max_entity == 1:
            self.__second_entity = entity
            self.__second_entity_cardinality = cardinality

        max_entity = max_entity + 1

        return max_entity

    def first_entity(self):
        return self.__first_entity

    def first_entity_cardinality(self):
        return self.__first_entity_cardinality

    def second_entity(self):
        return self.__second_entity

    def second_entity_cardinality(self):
        return self.__second_entity_cardinality

    def __str__(self) -> str:

        string = "Relationship: "

        string = string + str(self.__first_entity_cardinality) + "(" + str(self.__first_entity.name()) + ")"

        string = string + " to "

        string = string + str(self.__second_entity_cardinality) + "(" + str(self.__second_entity.name()) + ")"

        return string
