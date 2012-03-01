
  - how does type safety work in python?  
    - How do I define a return type for a method?
    - How do I define a type of a parameter?
    - see manager.create_compute()


  - if(type(url) == str):
      self._url = Url(str(url))
    else:
      self._url = url
    vs. ------------------------------
    self._url = Url(str(url))
    vs. ------------------------------
    self._url = url
    
  - import Manager as SManager
    vs. ------------------------------
    import Manager 


  - if self._plugin is not None:
    vs. ------------------------------
    if self._plugin is None:

  - what is the _* and __ naming convention, for files, types and vars?

  - hidden vs. private (see compute facade)?

  - #!/usr/bin/env python -> #!env python
    Why at all?  These files are not executables!

  - check all FIXMEs

  - self._cores          = None # total or per machine? 
    self._memory         = None # total or per machine?
    -> there is no notion of 'machine'  

- when is _api, when not? (description)
  
