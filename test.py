from bliss import saga

u = saga.Url('fork://localhost')
print str(u)

s = saga.job.Service(u)

j = saga.job.Service("g")
