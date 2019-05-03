class ContextManager(object):
  def __enter__(self):
    print "enter it"

  def __exit__(self,exception_type,exception_value,traceback):
    print "exit it"
    if exception_type is None:
      print "without exception"
    else:
      print "with exception %s"% exception_value
      return False

with ContextManager():
  print "testing"
