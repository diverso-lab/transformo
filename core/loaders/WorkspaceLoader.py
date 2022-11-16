from dotenv import dotenv_values


class WorkspaceLoader:

    def __init__(self):

        # load environment file
        dotenv_values_dict = dotenv_values('.workspace')

        self._name = dotenv_values_dict['WORKSPACE']

    def name(self) -> str:
        return self._name
