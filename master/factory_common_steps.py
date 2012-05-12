from buildbot.process.factory import BuildFactory
from buildbot.steps.source import Git
from buildbot.steps.shell import ShellCommand


run_git_checkout = Git(repourl='git://github.com/saga-project/bliss.git', mode='copy', progress=True)

run_bootstrap_virtualenv = ShellCommand(command=["/bin/bash", "-l", "-c" ,"/usr/bin/curl --insecure -s https://raw.github.com/pypa/virtualenv/master/virtualenv.py | python - blissenv"],
                             description="Bootstrapping virtualenv.py via cURL", haltOnFailure=True, name="virtualenv")

run_pip_install = ShellCommand(command=["/bin/bash", "-l", "-c" ,". blissenv/bin/activate && pip install -e git://github.com/saga-project/bliss.git#egg=bliss"],
                             description="pip install -e git://github.com/saga-project/bliss.git#egg=bliss", haltOnFailure=True, name="pip")

run_unittests = ShellCommand(command=["/bin/bash", "-l", "-c" ,". blissenv/bin/activate && python ./test/unittests.py"],
                             description="Running Bliss unit-tests in test/unittests", name="unittests")

run_check_keychain = ShellCommand(command=["/bin/bash", "-l", "-c" ,"! keychain  --quiet --eval ~/.ssh/id_rsa | grep false;"],
                             name="check_keychain",
                             description="Check for valid/active SSH keychain", haltOnFailure=True)
