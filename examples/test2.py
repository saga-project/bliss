import time
import bliss.saga as saga

def main():
    try:
        c1 = saga.Context()
        c1.type = saga.Context.SSH
        c1.usercert="/Users/s1063117/id_rsa.pub"
        c1.userkey="/Users/s1063117/id_rsa"

        js = saga.job.Service("fork://localhost")
        js.get_session().add_context(c1)

        jd = saga.job.Description()
        jd.set_attribute('Executable', '/bin/sleep')
        jd.set_vector_attribute('Arguments', ["10"])
        
        for att in jd.list_attributes():
            print "%s %s %s %s" % (att, jd.attribute_is_vector(att), jd.attribute_is_readonly(att), jd.attribute_is_writeable(att))
            
        for job in range(10): 
            job = js.create_job(jd)
            job.run()
            print job.get_job_id() + " : " + job.get_state()

        time.sleep(2)

        for job in js.list():
          rjob = js.get_job(job.get_job_id())     
          print rjob.get_job_id() + " : " + rjob.get_state()

        for job in js.list():
          job.cancel()
          print job.get_job_id() + " : " + job.get_state()

        for job in js.list():
          job.run()
          print job.get_job_id() + " : " + job.get_state()


        for job in js.list():
          job.wait()
          print job.get_job_id() + " : " + job.get_state()


    except saga.Exception, ex:
        print str(ex)


if __name__ == "__main__":
    main()



#env, exec, arg, env, stderr, stout, queue, project (allocation), WorkingDirectory, WallTimeLimit

#TotalCPUCount
#ProcessesPerHost
#NumberOfProcesses
