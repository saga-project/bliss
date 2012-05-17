from buildbot.process.factory import BuildFactory
from buildbot.steps.source import Git
from buildbot.steps.shell import ShellCommand

job_test_urls = ['pbs+ssh://eric.loni.org oweidner single', 
                 'pbs+ssh://oliver.loni.org oweidner single',
                 'pbs+ssh://louie.loni.org oweidner single',
                 'pbs+ssh://poseidon.loni.org oweidner single',
                 'pbs+ssh://painter.loni.org oweidner single',
                 'pbs+ssh://queenbee.loni.org oweidner single']

activate_keychain = "keychain $HOME/.ssh/id_rsa && source $HOME/.keychain/faust-sh"
activate_venv = ". blissenv/bin/activate"

factory = BuildFactory()

import factory_common_steps
factory.addStep(factory_common_steps.run_git_checkout)
factory.addStep(factory_common_steps.run_bootstrap_virtualenv)
factory.addStep(factory_common_steps.run_pip_install)
factory.addStep(factory_common_steps.run_unittests)

# check if the keychain is active. fail and skip remaining tests if not.
factory.addStep(factory_common_steps.run_check_keychain)


for url in job_test_urls:

    factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"%s && SAGA_VERBOSE=5 python ./test/compliance/job/01_run_remote_exe.py %s" % (activate_venv+" && "+activate_keychain, url)],
                             description="Running test: job/01_run_remote_exe.py %s" % (url), name="test_job/01"))

    factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"%s && SAGA_VERBOSE=5 python ./test/compliance/job/02_run_shell_command_newline.py %s" % (activate_venv+" && "+activate_keychain, url)],
                             description="Running test: job/02_run_shell_command_newline.py %s" % (url), name="test_job/02"))

    factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"%s && SAGA_VERBOSE=5 python ./test/compliance/job/03_run_shell_command_multiline.py %s" % (activate_venv+" && "+activate_keychain, url)],
                             description="Running test: job/03_run_shell_command_multiline.py %s" % (url), name="test_job/03"))

    factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"%s && SAGA_VERBOSE=5 python ./test/compliance/job/04_run_python_command_newline.py %s" % (activate_venv+" && "+activate_keychain, url)],
                             description="Running test: job/04_run_python_command_newline.py %s" % (url), name="test_job/04"))

    factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"%s && SAGA_VERBOSE=5 python ./test/compliance/job/05_run_python_command_multiline.py %s" % (activate_venv+" && "+activate_keychain, url)],
                             description="Running test: job/05_run_python_command_multiline.py %s " % (url), name="test_job/05"))



file_test3_urls = ['sftp://oweidner@eric.loni.org/tmp/ /home/sagaproj/.ssh/id_rsa.pub', 
                   'sftp://oweidner@oliver.loni.org/tmp/ /home/sagaproj/.ssh/id_rsa.pub']

for url in file_test3_urls:

    factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"%s && SAGA_VERBOSE=5 python ./test/compliance/file/03_copy_local_remote_etc.py %s" % (activate_venv+" && "+activate_keychain, url)],
                             description="Running test: file/03_copy_local_remote_etc.py %s" % (url), name="test_file/03"))

file_test4_urls = ['sftp:///tmp/ sftp://oweidner@eric.loni.org/etc/passwd', 'sftp:///tmp/ sftp://oweidner@oliver.org/etc/passwd']

for url in file_test4_urls:

    factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"%s && SAGA_VERBOSE=5 python ./test/compliance/file/04_copy_remote_local_etc.py %s" % (activate_venv+" && "+activate_keychain, url)],
                             description="Running test: file/04_copy_remote_local_etc.py %s" % (url), name="test_file/04"))

