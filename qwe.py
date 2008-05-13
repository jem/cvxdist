from cvxmod import *
from cvxmod.atoms import square
from math import sqrt

class system(object):
    def __init__(self, pins):
        self.pins = pins

    def sendbounds(self):
        raise NotImplementedError("need to implement bounds")

    def bregsolve(y, nu, R):
        raise NotImplementedError("need to implement bregsolve")

class controller(object):
    def __init__(self, pins, sc):
        self.pins = pins
        self.sc = sc

class pin(object):
    # Implement data storage with some features of a stack, but richer.
    # (No reason to constrain ourselves to a stack).
    def __init__(self, notify):
        self.notify = notify
        self.dat = []

    def push(self, dat):
        self.dat.append(dat)
        self.notify()

# Prototype of phi system (following ee364b).
# Functions f are defined by their random seed and various sizes.
class phi(object):
    def __init__(self, i, m, n, p):
        # Only use the random seed in the definition, no need to store.
        randseed(i + 5) # cannot set to zero, so add offset.
        self.A = param('A', value=randn(m, n + p))
        self.b = param('b', value=randn(m, 1))
        self.c = param('c', value=sqrt(2)*randn(n + p, 1))
        self.mu = param('mu', value=0.1, pos=True)
        self.m = m
        self.n = n
        self.p = p

    def __call__(self, y):
        # Internal variable.
        x = optvar('x', self.n)
        w = cv(x, y)
        phiy = max(self.A*w + self.b) + self.mu*sum(square(w - self.c))
        if isoptvar(y):
            return phiy
        else:
            p = problem(minimize(phiy))
            # Use ldl solver to prevent kkt matrix singularity issues.
            assert(p.solve(True, kktsolver='ldl') == 'optimal')
            return value(p)

#sys = []
#K = 
#for i in range(5):
#    sys.append(system

m = 20
n = 10
K = 5
ps = (1, 2, 1, 3, 2)
fs = []

# Describe the hypergraph. Indices start from 0.
nets = [[0,1,3], [1,4], [2,3], [3,4]]

# Need to have ordered pairs. Systems might expose labelled pins that need to
# be connected as labels. Or, they might be numbered. How do we do this? Also
# need to think about sizes. Important thing is just to match up the controller
# pins and system pins accurately.

# Generate the controllers: one per net.
cs = []
for i in range(len(cs)):
    for 
    controller

# Generate the 
for i in range(len(ps)):
    fs.append(phi(i, m, n, ps[i]))

# Describe the nets in an intuitive way.
N = 4

