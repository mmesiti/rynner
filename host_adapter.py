import fabric

# TODO HostAdapter.create_directory(string) => creates directory relative to base
# TODO init should take host,user, BASEDIR (i.e. directory every relative path is translated to)
# TODO connect should be deferred until required...
# TODO all paths should be relative to BASEDIR
# TODO put_file should have a relative=True default...and be absolute if specified


class Connection():
    def __init__(self, host, user):
        self.conn = fabric.Connection(host=host, user=user)

    def run_command(self, cmd, pwd=None):
        if pwd is not None:
            self.conn.cd(pwd)
        self.conn.run(cmd)

    def put_file(self, local_path, remote_path):
        self.conn.put(local_path, remote_path)

    def get_file(self, remote_path, local_path):
        self.conn.get(remote_path, local_path)

    def put_file_content(self, remote_path, content):
        raise NotImplementedError()


class HostAdapter:
    def __init__(self, behaviour, connection):
        self.behaviour = behaviour
        self.connection = connection
        self.uploaded_files = {}
        self.files_to_download = {}

    def upload_file(self, context, local, remote):
        self.connection.put_file(local, remote)
        self.uploaded_files[context['id']].append((local, remote), )

    def download_file(self, context, local, remote):
        self.files_to_download[context['id']].append((local, remote), )

    def run(self, context, behaviour_context):
        #self.behaviour.run(behaviour_context)
        pass

    def get_context(self, id):
        self.files_to_download[id] = []
        self.uploaded_files[id] = []
        return {'id': id}


# TODO - read and delete me
# build the job as Run(data['host']) => this is just a tuple of behaviour and connection...?
# or Run(HostAdapter(host, behaviour='slurm', user=..., port=...))
# host adapter => ssh_connection (easy)

# HostAdapter
#    HostAdapter just manipulates a context sent by Run and stored in Run
#
#    Behaviour handles the following setter methods:
#     * walltime
#     * memory
#     * num_nodes
#     * any others that it wants to...how do I handle this??
#    Behaviour manipulates connection as well??
#    HostAdapter can tell us its behaviour
#     * behaviour == 'slurm' (i.e. override behaviour equality)
#    HostAdapter can construct/submit jobcards (behaviour)
#    HostAdapter can upload/download files (itself)
#    HostAdapter(Behaviour, Connection)
#    HostAdapter persistent state is things like the files and stuff..
