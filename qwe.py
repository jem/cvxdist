from cvxmod import *
from cvxmod.atoms import square
from math import sqrt

class system(object):
    def __init__(self, f=None):
        self.f = f

    def notify(self):
        raise NotImplementedError("need to implement notify")

    def sendbounds(self):
        raise NotImplementedError("need to implement bounds")

    def bregsolve(self, y, nu, R):
        raise NotImplementedError("need to implement bregsolve")

class controller(object):
    def __init__(self, pinstojoin):
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

class bound(object):
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper

# Phi systems are characterized by having p scalar variables and a single
# function f.
class phisys(system):
    def __init__(self, f, p):
        self.f = f
        # Create wire dictionary.
        self.wires = {}
        for i in range(p):
            self.wires[i] = None

    def attachwire(self, i, w):
        self.wires[i] = w

    def sendbounds(self):
        BIGM = 100
        for w in self.wires:
            w.send(bound(-BIGM, BIGM))

    def notify(self):
        pass

    def marshall(self):
        # Pull the data off the wires and put it together for bregsolve.
        for w in self.wires.keys():
            w.

    def bregsolve(self, y, nu, R):
        p = problem(minimize(

m = 20
n = 10
K = 5
ps = (1, 2, 1, 3, 2)
fs = []

# Describe the hypergraph. Indices start from 0.
#nets = [[0,1,3], [1,4], [2,3], [3,4]]

# Generate the functions.
for i in range(len(ps)):
    fs.append(phi(i, m, n, ps[i]))

ss = []
# Generate the systems, one corresponding to each function. Note: don't
# necessarily need to generate systems in this way.
for f in len(fs):
    ss.append(system(f, ps[i]))

# Create the controllers by joining relevant nets. Second one in the list, for
# example, means join the pin labelled 1 in system 1 with the pin labelled 0 in
# system 4.
cs = [controller([(ss[0], 0), (ss[1], 0), (ss[3], 0)]),
      controller([(ss[1], 1), (ss[4], 0)]),
      controller([(ss[2], 0), (ss[3], 1)]),
      controller([(ss[3], 2), (ss[4], 1)])]

