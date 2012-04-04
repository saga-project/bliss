Version 0.1.20 released 2012-04-04
----------------------------------------------------------------------

* Swapped urlparse with furl in saga.Url class This hopefully fixes
  the problem with inconsistent parsing accross different Python versions
* Merged SGE plug-in development branch 
* Removed sagacompat compatibility API
* Log source names now all start with 'bliss.'. This should make 
  filtering much easier
* Moved SD package into development branch features/servicediscovery

Version 0.1.19 released 2012-02-29
----------------------------------------------------------------------

* Hotfix - removed experimental Resource plug-in from release

Version 0.1.18 released 2012-02-29
----------------------------------------------------------------------

* Fixed issue with plugin introspection 
* Added template for job plug-in

Version 0.1.17 released 2012-01-04
----------------------------------------------------------------------

* Hotfix

Version 0.1.16 released 2012-01-03
----------------------------------------------------------------------

* Fixed issue: https://github.com/oweidner/bliss/issues/9

Version 0.1.15 released 2012-01-03
----------------------------------------------------------------------

* Fixed issue: https://github.com/oweidner/bliss/issues/8
* Fixed issue: https://github.com/oweidner/bliss/issues/6
* First version of a bigjob plugin. See wiki for details.
* Fixed Python 2.4 compatibility issue

Version 0.1.14 released 2011-12-08
----------------------------------------------------------------------

* Added bliss.sagacompat module for API compatibility.
  API documentation: http://oweidner.github.com/bliss/apidoc-compat/
* Added examples for 'compat' API, e.g.:
  https://github.com/oweidner/bliss/tree/master/examples/job-api/compat/
* Added configuration files for epydoc

Version 0.1.13 released 2011-12-07
----------------------------------------------------------------------

* Fixed executable & argument handling for the local job plugin
* Added support for jd.output and jd.error to local job plugin

Version 0.1.12 released 2011-12-06
----------------------------------------------------------------------

* Fixed bug in URL.get_host()
* Fixed issues with extremely short running PBS jobs 
  in conjunction with scheduler configruations that 
  remove the job from the queue the second it finishes execution.
* First working version of an SFTP file API plugini based on Paramiko
* Two advance bfast examples incl. output file staging:
  https://github.com/oweidner/bliss/blob/master/examples/advanced/bfast_workflow_01.py
  https://github.com/oweidner/bliss/blob/master/examples/advanced/bfast_workflow_02.py

Version 0.1.11 released 2011-11-28
----------------------------------------------------------------------

* Fixed issues with PBS working directory 
* Added simple job API example that uses BFAST:
  https://github.com/oweidner/bliss/blob/master/examples/job-api/pbs_via_ssh_bfast_job.py
* Updated apidoc: http://oweidner.github.com/bliss/apidoc/
* First prototype of a job container. Example can be found here:
  https://github.com/oweidner/bliss/blob/master/examples/job-api/pbs_via_ssh_container.py  
* Implemented CPU and Memory information via PBS service discovery
* Changed job.Description.walltime_limit to 
  job.Description.wall_time_limit

Version 0.1.10 released 2011-11-16
----------------------------------------------------------------------

* Fixed issue with local job plugin

Version 0.1.9 released 2011-11-16
----------------------------------------------------------------------

* Prototype of a Service Discovery packages
* PBS/SSH support for service discovery

Version 0.1.8 released 2011-11-09
----------------------------------------------------------------------

* Fixed issue with PBS plugin job.wait()

Version 0.1.7 released 2011-11-09
----------------------------------------------------------------------

* More or less stable job API    
* First functional PBS over SSH plugin 
