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

        try:
            os.mkdir("workspaces/{}".format(self._name))
        except:
            pass

        try:
            os.mkdir("workspaces/{}/models".format(self._name))
        except:
            pass

    def name(self) -> str:
        return self._name
