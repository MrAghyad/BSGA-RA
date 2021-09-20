NET = 'net'
import itertools, collections

from zinc.nets import Marking, mset, dot, hdict
event = collections.namedtuple('event', ['trans', 'mode', 'sub', 'add'])

import random

def m(first, last):
  return random.randint(first, last - 1)

def get_p1(prev_m):
  if (prev_m <= 1287):
    return 0
  elif (prev_m >= 4810):
    return 2
  else:
    return 1

def get_p2(prev_m):
  if (prev_m < 2739):
    return 1
  else:
    return 0

def get_pdltrip(p, c):
  if ((p == 0 or p == 2) and (c == 0)):
    return 0
  else:
    return 1


def addsucc_001 (marking, succ):
    "successors of 't1'"
    if marking('p1') and marking('pressure'):
        for pressure in marking('pressure'):
            for p1 in marking('p1'):
                a = m(0, 5000)
                if isinstance(a, int):
                    b = get_p1(pressure)
                    if isinstance(b, int):
                        sub = Marking({'pressure': mset([pressure]), 'p1': mset([p1])})
                        if sub <= marking:
                            add = Marking({'pressure': mset([a]), 'p1': mset([b])})
                            succ.add(marking - sub + add)

def succ_001 (marking):
    "successors of 't1'"
    succ = set()
    addsucc_001(marking, succ)
    return succ

def itersucc_001 (marking):
    "successors of 't1'"
    if marking('p1') and marking('pressure'):
        for pressure in marking('pressure'):
            for p1 in marking('p1'):
                a = m(0, 5000)
                if isinstance(a, int):
                    b = get_p1(pressure)
                    if isinstance(b, int):
                        sub = Marking({'pressure': mset([pressure]), 'p1': mset([p1])})
                        if sub <= marking:
                            add = Marking({'pressure': mset([a]), 'p1': mset([b])})
                            mode = hdict({'p1': p1, 'pressure': pressure})
                            yield event('t1', mode, sub, add)

def addsucc_002 (marking, succ):
    "successors of 't2'"
    if marking('p2') and marking('power'):
        for power in marking('power'):
            for p2 in marking('p2'):
                a = m(0, 5000)
                if isinstance(a, int):
                    b = get_p2(power)
                    if isinstance(b, int):
                        sub = Marking({'power': mset([power]), 'p2': mset([p2])})
                        if sub <= marking:
                            add = Marking({'power': mset([a]), 'p2': mset([b])})
                            succ.add(marking - sub + add)

def succ_002 (marking):
    "successors of 't2'"
    succ = set()
    addsucc_002(marking, succ)
    return succ

def itersucc_002 (marking):
    "successors of 't2'"
    if marking('p2') and marking('power'):
        for power in marking('power'):
            for p2 in marking('p2'):
                a = m(0, 5000)
                if isinstance(a, int):
                    b = get_p2(power)
                    if isinstance(b, int):
                        sub = Marking({'power': mset([power]), 'p2': mset([p2])})
                        if sub <= marking:
                            add = Marking({'power': mset([a]), 'p2': mset([b])})
                            mode = hdict({'p2': p2, 'power': power})
                            yield event('t2', mode, sub, add)

def addsucc_003 (marking, succ):
    "successors of 't3'"
    if marking('p1') and marking('p3') and marking('pdltrip'):
        for pdltrip in marking('pdltrip'):
            for p1 in marking('p1'):
                for p3 in marking('p3'):
                    a = get_pdltrip(p1, p3[1])
                    if isinstance(a, int):
                        b = (p1, p3[1])
                        if isinstance(b, tuple):
                            if isinstance(p1, int):
                                test = Marking({'p1': mset([p1]), 'pdltrip': mset([pdltrip]), 'p3': mset([p3])})
                                if test <= marking:
                                    sub = Marking({'pdltrip': mset([pdltrip]), 'p3': mset([p3])})
                                    add = Marking({'pdltrip': mset([a]), 'p3': mset([b])})
                                    succ.add(marking - sub + add)

def succ_003 (marking):
    "successors of 't3'"
    succ = set()
    addsucc_003(marking, succ)
    return succ

def itersucc_003 (marking):
    "successors of 't3'"
    if marking('p1') and marking('p3') and marking('pdltrip'):
        for pdltrip in marking('pdltrip'):
            for p1 in marking('p1'):
                for p3 in marking('p3'):
                    a = get_pdltrip(p1, p3[1])
                    if isinstance(a, int):
                        b = (p1, p3[1])
                        if isinstance(b, tuple):
                            if isinstance(p1, int):
                                test = Marking({'p1': mset([p1]), 'pdltrip': mset([pdltrip]), 'p3': mset([p3])})
                                if test <= marking:
                                    sub = Marking({'pdltrip': mset([pdltrip]), 'p3': mset([p3])})
                                    add = Marking({'pdltrip': mset([a]), 'p3': mset([b])})
                                    mode = hdict({'p1': p1, 'p3': p3, 'pdltrip': pdltrip})
                                    yield event('t3', mode, sub, add)

def addsucc_004 (marking, succ):
    "successors of 't4'"
    if marking('p2') and marking('p3') and marking('pdltrip'):
        for pdltrip in marking('pdltrip'):
            for p2 in marking('p2'):
                for p3 in marking('p3'):
                    a = get_pdltrip(p3[0], p2)
                    if isinstance(a, int):
                        b = (p3[0], p2)
                        if isinstance(b, tuple):
                            if isinstance(p2, int):
                                test = Marking({'p2': mset([p2]), 'pdltrip': mset([pdltrip]), 'p3': mset([p3])})
                                if test <= marking:
                                    sub = Marking({'pdltrip': mset([pdltrip]), 'p3': mset([p3])})
                                    add = Marking({'pdltrip': mset([a]), 'p3': mset([b])})
                                    succ.add(marking - sub + add)

def succ_004 (marking):
    "successors of 't4'"
    succ = set()
    addsucc_004(marking, succ)
    return succ

def itersucc_004 (marking):
    "successors of 't4'"
    if marking('p2') and marking('p3') and marking('pdltrip'):
        for pdltrip in marking('pdltrip'):
            for p2 in marking('p2'):
                for p3 in marking('p3'):
                    a = get_pdltrip(p3[0], p2)
                    if isinstance(a, int):
                        b = (p3[0], p2)
                        if isinstance(b, tuple):
                            if isinstance(p2, int):
                                test = Marking({'p2': mset([p2]), 'pdltrip': mset([pdltrip]), 'p3': mset([p3])})
                                if test <= marking:
                                    sub = Marking({'pdltrip': mset([pdltrip]), 'p3': mset([p3])})
                                    add = Marking({'pdltrip': mset([a]), 'p3': mset([b])})
                                    mode = hdict({'p2': p2, 'p3': p3, 'pdltrip': pdltrip})
                                    yield event('t4', mode, sub, add)

def addsucc (marking, succ):
    'successors for all transitions'
    addsucc_001(marking, succ)
    addsucc_002(marking, succ)
    addsucc_003(marking, succ)
    addsucc_004(marking, succ)

def succ (marking):
    'successors for all transitions'
    succ = set()
    addsucc(marking, succ)
    return succ

def itersucc (marking):
    return itertools.chain(itersucc_001(marking),
                           itersucc_002(marking),
                           itersucc_003(marking),
                           itersucc_004(marking))

def init ():
    'initial marking'
    return Marking({'pressure': mset([2000]), 'power': mset([2000]), 'pdltrip': mset([0]), 'p3': mset([(1, 1)]), 'p1': mset([1]), 'p2': mset([1])})

# map transitions names to successor procs
# '' maps to all-transitions proc
succproc = {'': addsucc,
            't1': addsucc_001,
            't2': addsucc_002,
            't3': addsucc_003,
            't4': addsucc_004}

# map transitions names to successor funcs
# '' maps to all-transitions func
succfunc = {'': succ,
            't1': succ_001,
            't2': succ_002,
            't3': succ_003,
            't4': succ_004}

# map transitions names to successor iterators
# '' maps to all-transitions iterator
succiter = {'': itersucc,
            't1': itersucc_001,
            't2': itersucc_002,
            't3': itersucc_003,
            't4': itersucc_004}

def dumpmarking (m) :
    if hasattr(m, "ident") :
        return "[%s] %s" % (m.ident, {p : list(t) for p, t in m.items()})
    else :
        return str({p : list(t) for p, t in m.items()})

def statespace (print_states, print_succs, print_dead) :
    i = init()
    i.ident = 0
    todo = collections.deque([i])
    seen = {i : 0}
    dead = 0
    while todo:
        state = todo.popleft()
        succ = set()
        addsucc(state, succ)
        if not succ :
            dead += 1
        if (print_dead and not succ) or print_states :
            print(dumpmarking(state))
        for s in succ :
            if s in seen :
                s.ident = seen[s]
            else :
                s.ident = seen[s] = len(seen)
                todo.append(s)
            if print_succs :
                print(" >", dumpmarking(s))
    return len(seen), dead

def lts () :
    i = init()
    i.ident = 0
    todo = collections.deque([i])
    seen = {i : 0}
    while todo:
        state = todo.popleft()
        print(dumpmarking(state))
        for trans, mode, sub, add in itersucc(state) :
            succ = state - sub + add
            if succ in seen :
                succ.ident = seen[succ]
            else :
                succ.ident = seen[succ] = len(seen)
                todo.append(succ)
            print("@ %s = %s" % (trans, mode))
            print(" -", dumpmarking(sub))
            print(" +", dumpmarking(add))
            print(" >", dumpmarking(succ))

def main () :
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", dest="size",
                        default=False, action="store_true",
                        help="only print size")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-g", dest="mode", action="store_const", const="g",
                       help="print marking graph")
    group.add_argument("-l", dest="mode", action="store_const", const="l",
                       help="print LTS (detailled marking graph)")
    group.add_argument("-m", dest="mode", action="store_const", const="m",
                       help="only print markings")
    group.add_argument("-d", dest="mode", action="store_const", const="d",
                       help="only print deadlocks")
    args = parser.parse_args()
    if args.mode in "gml" and args.size :
        n, _ = statespace(False, False, False)
        print("%s reachable states" % n)
    elif args.mode == "d" and args.size :
        _, n = statespace(False, False, False)
        print("%s deadlocks" % n)
    elif args.mode == "g" :
        statespace(True, True, False)
    elif args.mode in "m" :
        statespace(True, False, False)
    elif args.mode in "d" :
        statespace(False, False, True)
    elif args.mode == "l" :
        lts()

if __name__ == '__main__':
    main()
