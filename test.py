from bliss import saga



def main():
    try:
        u = saga.Url('fork://localhost')

        #s = saga.job.Service(u)
        z = saga.job.Service(u)
        a = saga.job.Service(u)
        b = saga.job.Service(u)
        c = saga.job.Service(u)

        z = saga.job.Service(u)

        jd = saga.job.Description()
        jd.executable = "/bin/date"

        j1 = z.create_job(jd)

        print j1._get_runtime_info()

        del a, b, c 

    except saga.Exception, ex:
        print str(ex)

if __name__ == "__main__":
    main()

