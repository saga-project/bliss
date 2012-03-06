import bliss.saga as saga

def main():
    try:
        js = saga.job.Service("fork://localhost")
        jd = saga.job.Description()
        print repr(js.get_session())
        print repr(jd.get_session())

        c1 = saga.Context()
        c1.type = saga.Context.SSH
        c1.userkey="/Users/s1063117/id_rsa"
        s1 = saga.Session()
        s1.add_context(c1)

        assert(len(s1.list_contexts()) == 1)
        s1.remove_context(c1)
        assert(len(s1.list_contexts()) == 0)


        s2 = saga.Session()


        js = saga.job.Service("fork://localhost", session=s1)
        jd = saga.job.Description()
        print repr(js.get_session())


        js = saga.job.Service("fork://localhost", session=s2)
        jd = saga.job.Description()
        print repr(js.get_session())

        s1.add_context(c1)
        s1.add_context(c1)

        js = saga.job.Service("fork://localhost")
        js_s = js.get_session()
        js_s.add_context(c1)

        jk = saga.job.Service("fork://localhost")
        jk_c = js.get_session().list_contexts()[0]
        assert(jk_c.userkey == "/Users/s1063117/id_rsa")
        print jk_c.type
       
    except saga.Exception, ex:
        print str(ex)


if __name__ == "__main__":
    main()

