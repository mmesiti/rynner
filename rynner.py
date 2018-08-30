import os
from unittest.mock import patch, call, ANY
from unittest.mock import MagicMock as MM
from tests.qtest_helpers import *
from rynner.host import SlurmHost
from rynner.datastore import Datastore
from rynner.behaviour import Behaviour
from rynner.main import MainView
from rynner.create_view import RunCreateView, TextField
from rynner.plugin import Plugin, PluginCollection, RunAction
from rynner.run import RunManager
from rynner.option_maps import slurm1711_option_map as option_map
from rynner.logs import Logger
from tests.host_env import *

defaults = []

#---------------------------------------------------------
# PLUGIN SCRIPT
#---------------------------------------------------------

# Create a fake run_create_view
view1 = RunCreateView(
    [TextField('Message', 'message', default='Hello, World!')])


def runner(run_manager, data):
    run = run_manager.new(
        ntasks=1,
        memory_per_task_MB=10000,
        host=hosts[0],
        script='echo "Hello from Sunbird!" > "my-job-output"')


# create Plugin objects
plugin1 = Plugin('swansea.ac.uk/1', 'Hello, World!', view1, runner)

#---------------------------------------------------------
# PLUGIN 2 SCRIPT
#---------------------------------------------------------

view2 = RunCreateView([
    TextField('Velocity', 'velocity', default="10"),
    TextField('Altitude', 'altitude', default="40,000"),
    TextField('Angle', 'angle', default='10'),
])


def runner2(run_manager, data):
    print('running...')


plugin2 = Plugin(
    'swansea.ac.uk/2',
    'simpleCFD',
    view2,
    runner2,
    view_keys=("id", "name", "some-other-data"))

#---------------------------------------------------------
# INITIALISATION
#---------------------------------------------------------

# submit the job and write output to
submit_cmd = 'echo 1234 > jobid'
# Set up some hosts

rsa_file = f'{homedir}/.ssh/id_rsa'
hosts = [SlurmHost(test_host, test_user, rsa_file)]

print('create plugins')

plugins = [PluginCollection("All Runs", [plugin1, plugin2]), plugin1, plugin2]


def update_plugins():
    print('update')
    for plugin in [plugin1, plugin2]:
        plugin_id = plugin.plugin_id
        for host in hosts:
            host.update(plugin_id)


timer = QTimer()
timer.timeout.connect(update_plugins)
secs = 10
timer.start(secs * 1000)

main = MainView(hosts, plugins)
main.show()
app.exec_()
