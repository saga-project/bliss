from buildbot.process.factory import BuildFactory
from buildbot.steps.source import Git
from buildbot.steps.shell import ShellCommand

job_test_urls = ['torque+gsissh://kraken.nics.xsede.org']

activate_keychain = "keychain $HOME/.ssh/id_rsa --host sagaproj && source $HOME/.keychain/sagaproj-sh"
activate_venv = ". blissenv/bin/activate"

factory = BuildFactory()

import factory_common_steps
factory.addStep(factory_common_steps.run_git_checkout)
factory.addStep(factory_common_steps.run_bootstrap_virtualenv)
factory.addStep(factory_common_steps.run_pip_install)
factory.addStep(factory_common_steps.run_unittests)

# check if the keychain is active. fail and skip remaining tests if not.
factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"keychain  --quiet --eval ~/.ssh/id_rsa | grep false;"],
                             name="check_x509proxy",
                             description="Check for valid/active X.509 proxy", haltOnFailure=True))


for url in job_test_urls:

    factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"%s && python ./test/compliance/job/01_run_remote_exe.py %s" % (activate_venv+" && "+activate_keychain, url)],
                             description="Running test: job/01_run_remote_exe.py %s" % (url), name="test_job/01"))

    factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"%s && python ./test/compliance/job/02_run_shell_command_newline.py %s" % (activate_venv+" && "+activate_keychain, url)],
                             description="Running test: job/02_run_shell_command_newline.py %s" % (url), name="test_job/02"))

    factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"%s && python ./test/compliance/job/03_run_shell_command_multiline.py %s" % (activate_venv+" && "+activate_keychain, url)],
                             description="Running test: job/03_run_shell_command_multiline.py %s" % (url), name="test_job/03"))

    factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"%s && python ./test/compliance/job/04_run_python_command_newline.py %s" % (activate_venv+" && "+activate_keychain, url)],
                             description="Running test: job/04_run_python_command_newline.py %s" % (url), name="test_job/04"))

    factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"%s && python ./test/compliance/job/05_run_python_command_multiline.py %s" % (activate_venv+" && "+activate_keychain, url)],
                             description="Running test: job/05_run_python_command_multiline.py %s " % (url), name="test_job/05"))


