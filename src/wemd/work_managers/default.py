from __future__ import division
__metaclass__ = type
import cPickle as pickle
import numpy
import string, time, datetime
from copy import copy   
from itertools import izip     

from wemd.work_managers import WEWorkManagerBase
from wemd.core.we_sim import WESimIter
from wemd.core.particles import Particle, ParticleCollection
from wemd.core.segments import Segment
from wemd.core.errors import PropagationIncompleteError
from wemd.rc import RC_SIM_STATE_KEY

import logging
log = logging.getLogger(__name__)

class DefaultWorkManager(WEWorkManagerBase):
    def propagate_particles(self, we_iter, segments):
        for segment in map(None, *(iter(segments),) * self.worker_blocksize):
            if type(segment) is tuple:
                self.backend_driver.propagate_segments(list(segment))
            else:    
                self.backend_driver.propagate_segments([segment])

        return segments
    
    def post_iter(self, we_iter):
        self.backend_driver.post_iter(we_iter)
        
    def finalize_iteration(self):
        pass
        