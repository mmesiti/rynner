class Runner:
    def __init__(self, logic):
        pass

    def type(self, classname):
        '''Convenience method for determining the type of an object'''
        return isinstance(self, classname)

    def run(self, options, config, downloads, uploads):
        pass
        # actually


##### HOW DOES THE DATA GET INTO HERE???

#        jobID = self.runner_logic.reserve()  # <= instantiated with runner_logic
#
#        # create base dir - different ordering => manages downloads, also manages "remembering" stuff and sync behaviour
#        # needs to be called later to "finish" the job
#        manager = JobManager(jobID, uploads, downloads)
#
#        # store relevant data for later
#        self.database.store(jobID, options, config, uploads, downloads)
#
#        for option, value in options.items:
#            # options are just passed on to the runner_logic => runner_logic + Run are VERY coupled, runner_logic and runner are not
#            self.runner_logic.set_option(option, value)
#
#        self.runner_logic.start(jobID)
#
#        return jobID

# ALTERNATIVE
# Runner has all the logic for all the submission types
# setup manipulates runner
# default runner is read from from data (if exists)

#################################### NOTES ####################################

# System has lots of runners (i.e. one per cluster)
# Job is configured with a runner
# available runners can be made available to all...
# Runners are all configured with some logic (i.e. RunnerLogic), and thus have a type ('slurm', 'pbs', etc..)
# Job/Run are created (with a given standard interface). A job specifies supported set of runner types
# Job ID is a UUID (a random one...)
# Runs are passed into a runner (with Runner.run) to run # any "NoOps" are collected and the user is notified with a message

# HostAdapter(behaviour='slurm', )
