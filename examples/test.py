import bliss.saga as saga

def main():
    try:
        u = saga.Url('fork://localhost')

        #s = saga.job.Service(u)
        z = saga.job.Service(u)
        a = saga.job.Service(u)
        b = saga.job.Service("dummy://localhost")
        c = saga.job.Service("dummy://localhost")

        z = saga.job.Service(u)

        jd = saga.job.Description()
        jd.executable = "/bin/sleep"
        jd.arguments = ["10"]

        j1 = z.create_job(jd)
        j2 = z.create_job(jd)
        j3 = z.create_job(jd)
        j4 = z.create_job(jd)


        j1 = a.create_job(jd)
        j2 = a.create_job(jd)
        j3 = a.create_job(jd)
        j4 = a.create_job(jd)

        b.create_job(jd)
        k = c.create_job(jd)
        
        try: 
            k.get_stdout()
        except saga.Exception, ex:
            assert(ex.error == saga.Error.NotImplemented)

        try: 
            k.get_stderr()
        except saga.Exception, ex:
            assert(ex.error == saga.Error.NotImplemented)

        assert(repr(jd) == repr(k.get_description()))
        assert(jd.executable == "/bin/sleep")
 
        try: 
            j = saga.job.Job()
            j.get_state()
        except saga.Exception, ex:
            assert(ex.error == saga.Error.NoSuccess)

        print j1.get_state()
        j1.run()
        print j1.get_job_id()
        print j1.get_state()
        j1.wait()         
        print j1.get_state()

        js = saga.job.Service("fork://localhost")
        jd = saga.job.Description()
        jd.executable = "/usr/bin/false"
        myjob = js.create_job(jd)
        print myjob.get_state()
        myjob.run()
        print myjob.get_state()
        myjob.wait()
        print myjob.get_state()

        jd = saga.job.Description()
        jd.executable = "/usr/bin/true"
        myjob = js.create_job(jd)
        print myjob.get_state()
        myjob.run()
        print myjob.get_state()
        myjob.wait()
        print myjob.get_state()
        print myjob.get_job_id()

        print j1.get_state()
        j1.run()
        print j1.get_job_id()
        print j1.get_state()
        j1.cancel()         
        print j1.get_state()

#        j1.cancel()
#        print j1.get_state()


        #print j1._get_runtime_info()
        #print c._get_runtime_info()

        del a, b, c 

    except saga.Exception, ex:
        print str(ex)

    ## do it the new style - slightly more pythonic
    
    try: 
        # start a local job service
        js = saga.job.Service("fork://localhost")

        # describe our job
        jd = saga.job.Description()
        jd.executable  = '/bin/sleep'
        jd.arguments   = ['10']

        # create & run the job
        myjob = js.create_job(jd)

        print "Job State : %s".format(myjob.get_state())

        myjob.run()

        print "Job ID    : %s".format(myjob.get_job_id())
        print "Job State : %s".format(myjob.get_state())
        print "waiting for job ..."

        myjob.wait()

        print "Job State : %s".format(myjob.get_state())

    except saga.Exception, ex:
        print "Oh, snap! An error occured: %s".format(str(ex))

    ## do it the old-school way 
    ## (compatible with CCT's SAGA Python bindings
    
    try: 
        # define lower-case aliases 
        saga.exception = saga.exception.Exception
        saga.job.service = saga.job.service.Service
        saga.job.description = saga.job.description.Description

        # start a local job service
        js = saga.job.service("fork://localhost")

        # describe our job
        jd = saga.job.description()
        jd.executable  = '/bin/sleep'
        jd.arguments   = ['10']

        # create & run the job
        myjob = js.create_job(jd)

        print "Job State : %s".format(myjob.get_state())

        myjob.run()

        print "Job ID    : %s".format(myjob.get_job_id())
        print "Job State : %s".format(myjob.get_state())
        print "waiting for job ..."

        myjob.wait()

        print "Job State : %s".format(myjob.get_state())

    except saga.exception, ex:
        print "Oh, snap! An error occured: %s".format(str(ex))



if __name__ == "__main__":
    main()

