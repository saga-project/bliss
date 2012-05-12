from buildbot.process.factory import BuildFactory
from buildbot.steps.source import Git
from buildbot.steps.shell import ShellCommand

job_test_urls = ['pbs+ssh://india.futuregrid.org', 'pbs+ssh://alamo.futuregrid.org']

activate_keychain = "keychain $HOME/.ssh/id_rsa --host sagaproj && source $HOME/.keychain/sagaproj-sh"
activate_venv = ". blissenv/bin/activate"

factory = BuildFactory()
# check out the source
factory.addStep(Git(repourl='git://github.com/saga-project/bliss.git', mode='copy', progress=True))

factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"/usr/bin/curl --insecure -s https://raw.github.com/pypa/virtualenv/master/virtualenv.py | python - blissenv"],
                             description="Bootstrapping virtualenv.py via cURL"))

factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,". blissenv/bin/activate && pip install -e git://github.com/saga-project/bliss.git#egg=bliss"],
                             description="pip install -e git://github.com/saga-project/bliss.git#egg=bliss"))

factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,". blissenv/bin/activate && python ./test/unittests.py"],
                             description="Running Bliss unit-tests in test/unittests"))

for url in job_test_urls:

    factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"%s && python ./test/compliance/job/01_run_remote_exe.py %s" % (activate_venv+" && "+activate_keychain, url)],
                             description="Running test: job/01_run_remote_exe.py %s" % (url) ))

    factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"%s && python ./test/compliance/job/02_run_shell_command_newline.py %s" % (activate_venv+" && "+activate_keychain, url)],
                             description="Running test: job/02_run_shell_command_newline.py %s" % (url)))

    factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"%s && python ./test/compliance/job/03_run_shell_command_multiline.py %s" % (activate_venv+" && "+activate_keychain, url)],
                             description="Running test: job/03_run_shell_command_multiline.py %s" % (url)))

    factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"%s && python ./test/compliance/job/04_run_python_command_newline.py %s" % (activate_venv+" && "+activate_keychain, url)],
                             description="Running test: job/04_run_python_command_newline.py %s" % (url)))

    factory.addStep(ShellCommand(command=["/bin/bash", "-l", "-c" ,"%s && python ./test/compliance/job/05_run_python_command_multiline.py %s" % (activate_venv+" && "+activate_keychain, url)],
                             description="Running test: job/05_run_python_command_multiline.py %s " % (url)))

