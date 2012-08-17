from command_wrapper import CommandWrapper
import logging

cw = CommandWrapper.initAsSSHWrapper(logging.getLogger('hello'), hostname='lonestar.tacc.utexas.edu', username='tg802352')
cw.connect()
print cw.run(executable="/bin/date")
print cw.run(executable="/bin/date")


