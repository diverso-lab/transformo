from xml.dom import minidom

from core.models.stm.Transformation import Transformation


class SimpleTransformationModel:

    def __init__(self, stm_file) -> None:

        self._stm_file = stm_file
        doc = minidom.parse(self._stm_file)
        self._transformations = []
        self._read_transformations(doc)

    def _read_transformations(self, doc) -> None:
        items = doc.getElementsByTagName('transformation')

        for i in items:
            transformation = Transformation(item=i)
            self._transformations.append(transformation)

    def transformations(self) -> list[Transformation]:
        return self._transformations

    def last_transformation(self) -> Transformation:
        return self._transformations[-1]

    def print(self) -> None:
        for t in self._transformations:
            print("\n" + str(t))

            print("\tActions:")
            for a in t.actions():
                print("\t" + str(a))
