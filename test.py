from bliss import saga

u = saga.Url('fork://localhost')
print str(u)

s = saga.job.Service(u)
print s.url

try:
    j = saga.job.Service("g")
except saga.Exception, ex:
    print str(ex)
