class Datastore:
    def store(self, id, options):
        raise NotImplementedError()

    def isrunning(self, id, isrunning):
        raise NotImplementedError()

    def jobs(self, plugin_id):
        raise NotImplementedError()

    def set_connection(self, connection):
        raise NotImplementedError()
        self.connection = connection
