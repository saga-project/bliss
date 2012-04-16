
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

  - hidden vs. private (see compute resource)?

  - check all FIXMEs

