from command_wrapper import CommandWrapper
import logging

cw = CommandWrapper.initAsLocalWrapper(logging.getLogger('hello'))
cw.connect()
print cw.run(executable="/bin/date")

cw = CommandWrapper.initAsSSHWrapper(logging.getLogger('hello'), hostname='localhost')
cw.connect()
print cw.run(executable="/bin/date")
print cw.run(executable="/bin/date")

#cw = CommandWrapper.initAsGSISSHWrapper(logging.getLogger('hello'), hostname='osg-xsede.grid.iu.edu')
#cw.connect()
#print cw.run(executable="/bin/date")
#print cw.run(executable="uname -a")
#print cw.run(executable="condor_q")

#print cw.run(executable="false")


