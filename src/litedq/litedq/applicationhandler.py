from ._types import Application


class ApplicationHanler:
    def __init__(self):
        self._apps = []

    def __getitem__(self, key):
        return self._apps[key]

    def apply(self, **kwargs):
        # Store applications
        self._apps.append(
            Application(
                {k: x for k, x in kwargs.items() if k != "metadata"},
                kwargs.get("metadata"),
            )
        )

    def __repr__(self):
        return str(self._apps)
