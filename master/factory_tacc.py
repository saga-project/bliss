from buildbot.process.factory import BuildFactory
from buildbot.steps.source import Git
from buildbot.steps.shell import ShellCommand

job_test_urls = ['sge+ssh://ranger.tacc.xsede.org tg802352 development TG-MCB090174', 
                 'sge+ssh://lonestar.tacc.xsede.org tg802352 development TG-MCB090174']

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

    factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"%s && python ./test/compliance/job/01_run_remote_exe.py %s " % (activate_venv+" && "+activate_keychain, url)],
                             description="Running test: job/01_run_remote_exe.py %s" % (url), name="test_job/01", timeout=2400))

    factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"%s && python ./test/compliance/job/02_run_shell_command_newline.py %s" % (activate_venv+" && "+activate_keychain, url)],
                             description="Running test: job/02_run_shell_command_newline.py %s" % (url), name="test_job/02", timeout=2400))

    factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"%s && python ./test/compliance/job/03_run_shell_command_multiline.py %s" % (activate_venv+" && "+activate_keychain, url)],
                             description="Running test: job/03_run_shell_command_multiline.py %s" % (url), name="test_job/03", timeout=2400))

    factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"%s && python ./test/compliance/job/04_run_python_command_newline.py %s" % (activate_venv+" && "+activate_keychain, url)],
                             description="Running test: job/04_run_python_command_newline.py %s" % (url), name="test_job/04", timeout=2400))

    factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"%s && python ./test/compliance/job/05_run_python_command_multiline.py %s" % (activate_venv+" && "+activate_keychain, url)],
                             description="Running test: job/05_run_python_command_multiline.py %s " % (url), name="test_job/05", timeout=2400))


file_test_urls = ['sftp://tg802352@login1.ls4.tacc.utexas.edu/tmp/ /home/sagaproj/.ssh/id_rsa.pub']#, 'sftp://tg802352@lonestar.tacc.xsede.org/tmp/ /home/sagaproj/.ssh/id_rsa.pub']

for url in file_test_urls:

    factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"%s && python ./test/compliance/file/03_copy_local_remote_etc.py %s" % (activate_venv+" && "+activate_keychain, url)],
                             description="Running test: file/03_copy_local_remote_etc.py %s" % (url), name="test_file/03"))

