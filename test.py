from bliss import saga

u = saga.Url('fork://localhost')

s = saga.job.Service(u)

z = saga.job.Service(u)
j1 = z.create_job("jd")

#try:
#    j = saga.job.Service("g")
#except saga.Exception, ex:
#    print str(ex)
