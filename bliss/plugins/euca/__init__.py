# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# NOTE AM:
#   - why is there 
#       Plugin.compute_resource_get_state_detail()
#     but
#       Compute.get_state()
#     ?
#   - Plugin.compute_resource_get_description() vs. Compute.get_description?
#   - What is _Compute__init_from_manager(mgr_obj, descr) ?    Brrr....
#

__author__    = "Ashley Zebrowski"
__copyright__ = "Copyright 2012, Ashley Zebrowski"
__license__   = "MIT"

from bliss.plugins.euca.resource import EucaResourcePlugin

