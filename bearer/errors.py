class MissingAuthId(Exception):
    def __init__(self):
        super().__init__('No Auth ID has been set. Please call `auth`')
