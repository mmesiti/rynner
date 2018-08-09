import unittest
from unittest.mock import patch, MagicMock
from host_adapter import *


class TestConnection(unittest.TestCase):
    def setUp(self):
        self.cluster_host = 'example.cluster.com'
        self.cluster_user = 'user'
        self.context = MagicMock()

        self.patcher = patch('host_adapter.fabric.Connection')
        self.FabricMock = self.patcher.start()

        self.connection = Connection(
            host=self.cluster_host, user=self.cluster_user)

    def tearDown(self):
        self.patcher.stop()

    def test_connection(self):
        pass

    def test_run_command_ls(self):
        self.connection.run_command("ls")

    def test_run_command_creates_connection(self):
        self.connection.run_command("ls")
        self.FabricMock.assert_called_once_with(
            host=self.cluster_host, user=self.cluster_user)

    def test_run_command_calls_run(self):
        cmd = "ls"
        self.connection.run_command(cmd)
        self.FabricMock().run.assert_called_once_with(cmd)

    def test_run_command_calls_sets_dir(self):
        cmd = "ls"
        pwd = "/some/working/dir"
        self.connection.run_command(cmd, pwd=pwd)
        self.FabricMock().cd.assert_called_once_with(pwd)

    def test_put_uploads_file(self):
        local = "/some/local/file"
        remote = "/some/remote/file"
        self.connection.put_file(local, remote)
        self.FabricMock().put.assert_called_once_with(local, remote)

    def test_call_get_file(self):
        local = "/some/local/file"
        remote = "/some/remote/file"
        self.connection.get_file(remote, local)

    def test_file_downloads_file(self):
        remote = "/some/remote/file"
        local = "some/local/path"
        self.connection.get_file(remote, local)
        self.FabricMock().get.assert_called_once_with(remote, local)


class TestHostAdapter(unittest.TestCase):
    def setUp(self):
        # patch fabric
        self.patcher = patch('host_adapter.fabric')
        fabric = self.patcher.start()
        self.FabricMock = fabric.Connection

    def tearDown(self):
        self.patcher.stop()

    def instantiate(self):
        # instantiate HostAdapter
        self.mock_behaviour = MagicMock()
        self.mock_connection = MagicMock()
        self.host_adapter = HostAdapter(self.mock_behaviour,
                                        self.mock_connection)

        self.context = MagicMock()

    def test_exposes_behaviour(self):
        self.instantiate()
        assert self.host_adapter.behaviour == self.mock_behaviour


class TestHostAdapterConnection(TestHostAdapter):
    def setUp(self):
        self.conn_patch = patch('host_adapter.Connection')
        self.MockConnection = self.conn_patch.start()

    def tearDown(self):
        self.conn_patch.stop()

    def test_file_upload_connection(self):
        self.instantiate()
        local = MagicMock()
        remote = MagicMock()
        self.host_adapter.upload_file(self.context, local, remote)
        self.MockConnection().put_file.called_once_with(local, remote)

    def test_get_context(self):
        self.instantiate()
        assert self.host_adapter.get_context(self.context['id']) == {
            'id': self.context['id']
        }

    def test_run_host_adapter(self):
        self.instantiate()
        behaviour_context = MagicMock()
        self.host_adapter.run(self.context, behaviour_context)

    def test_remember_uploaded_files(self):
        self.instantiate()
        local = MagicMock()
        remote = MagicMock()
        id = 243545
        context = self.host_adapter.get_context(id)
        self.host_adapter.upload_file(context, local, remote)
        assert self.host_adapter.uploaded_files[id] == [(local, remote)]

    def test_remember_files_to_download(self):
        self.instantiate()
        local = MagicMock()
        remote = MagicMock()
        id = 243545
        context = self.host_adapter.get_context(id)
        self.host_adapter.download_file(context, local, remote)
        assert self.host_adapter.files_to_download[id] == [(local, remote)]

    def test_remember_multiple_files_to_download(self):
        self.instantiate()
        local, remote, local2, remote2 = (MagicMock(), MagicMock(),
                                          MagicMock(), MagicMock())
        id = 243545
        context = self.host_adapter.get_context(id)
        self.host_adapter.download_file(context, local, remote)
        self.host_adapter.download_file(context, local2, remote2)
        assert self.host_adapter.files_to_download[id] == [(local, remote),
                                                           (local2, remote2)]

    def test_remember_multiple_uploaded_files(self):
        self.instantiate()
        local, remote, local2, remote2 = (MagicMock(), MagicMock(),
                                          MagicMock(), MagicMock())
        local, remote, local2, remote2 = ('l', 'r', 'l2', 'r2')
        id = 243545
        context = self.host_adapter.get_context(id)
        self.host_adapter.upload_file(context, local, remote)
        self.host_adapter.upload_file(context, local2, remote2)
        assert self.host_adapter.uploaded_files[id] == [(local, remote),
                                                        (local2, remote2)]


if __name__ == '__main__':
    unittest.main()
