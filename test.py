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
        #:jd.executable = "/bin/date"

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
        #:assert(jd.executable == "/bin/date")
 
        try: 
            j = saga.job.Job()
            j.get_state()
        except saga.Exception, ex:
            assert(ex.error == saga.Error.NoSuccess)

        print j1.get_state()
        j1.run()
        print j1.get_state()
        j1.cancel()
        print j1.get_state()


        #print j1._get_runtime_info()
        #print c._get_runtime_info()

        del a, b, c 

    except saga.Exception, ex:
        print str(ex)

if __name__ == "__main__":
    main()

