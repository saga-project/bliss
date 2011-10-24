from bliss import saga

try:
    u = saga.Url('fork://localhost')

    s = saga.job.Service(u)
    z = saga.job.Service(u)

    jd = saga.job.Description()
    jd.executable = "/bin/date"

    j1 = z.create_job(jd)

except saga.Exception, ex:
    print str(ex)
