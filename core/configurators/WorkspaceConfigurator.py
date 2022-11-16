import os


class WorkspaceConfigurator:

    def __init__(self, name: str = 'default'):

        self._name = name
        self._set_workspace()

    def _set_workspace(self):

        # set workspace environment
        open('.workspace', 'w').close()
        with open('.workspace', "a") as f:
            f.write('WORKSPACE={}'.format(self._name))

        # creating workspace folder
        try:
            os.mkdir("workspaces/{}".format(self._name))
        except:
            pass

        # creating migrations folder into workspace
        try:
            os.mkdir("workspaces/{}/migrations".format(self._name))
        except:
            pass

        # creating models folder into workspace
        try:
            os.mkdir("workspaces/{}/models".format(self._name))
        except:
            pass

        # creating UVL folder into workspace
        try:
            os.mkdir("workspaces/{}/uvl".format(self._name))
        except:
            pass

    def name(self) -> str:
        return self._name
