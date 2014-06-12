"""
Adapt some Python types to the core protocol.
"""

from core import call, vtables

def install():
    vtables[type(None)] = {}
    vtables[bool]  = bool_vtable
    for t in num_types: vtables[t] = num_vtable
    for t in str_types: vtables[t] = str_vtable

str_types = (str, unicode)
num_types = (int, long, float)

bool_vtable = {('if-so', 'if-not'): lambda rcvr, args, k: call(args[not rcvr], ('run',), (), k)}

num_vtable = {('+',): lambda rcvr, (other,), k: (k, rcvr + as_number(other)),
              ('*',): lambda rcvr, (other,), k: (k, rcvr * as_number(other)),
              ('-',): lambda rcvr, (other,), k: (k, rcvr - as_number(other)),
              ('=',): lambda rcvr, (other,), k: (k, rcvr == other), # XXX object method
              ('<',): lambda rcvr, (other,), k: (k, rcvr < other),
             }

def as_number(thing):
    if isinstance(thing, num_types):
        return thing
    assert False, "Not a number: %r" % (thing,)

def find_default(rcvr, (other, default), k):
    try:
        return k, rcvr.index(other)
    except ValueError:
        return call(default, ('run',), (), k)

def has(rcvr, (other,), k):  return (k, other in rcvr)
def at(rcvr, (i,), k):       return (k, rcvr[i])
def find(rcvr, (other,), k): return (k, rcvr.index(other))
def size(rcvr, _, k):        return (k, len(rcvr))
def add(rcvr, (other,), k):  return (k, rcvr + other)
def eq(rcvr, (other,), k):   return (k, rcvr == other)
def lt(rcvr, (other,), k):   return (k, rcvr < other)

def as_string(thing):
    if isinstance(thing, str_types):
        return thing
    assert False, "Not a string: %r" % (thing,)

str_vtable = {('has',):  has,
              ('at',):   at,
              ('find',): find,
              ('find', 'default',): find_default,
              ('size',): size,
              ('++',):   add,
              ('=',):    eq,
              ('<',):    lt,
}