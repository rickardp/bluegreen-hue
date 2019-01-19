import dns.name
import dns.resolver
import random, sys, re

def add_args(parser):
    parser.add_argument('--dns-match-blue', metavar='regex', dest='dnsmatchblue', type=str, default='blue',
                        help='the DNS response that matches Blue (default is "blue")')
    parser.add_argument('--dns-match-green', metavar='regex', dest='dnsmatchgreen', type=str, default='green',
                        help='the DNS response that matches Blue (default is "green")')
    parser.add_argument('--cname', metavar='NUMLEVELS', dest='cname', type=int, default=0,
                        help='pre-resolves NUMLEVELS levels of CNAME')

def get_source(args):
    rec = args.dns
    if not rec: raise ValueError()
    if args.cname:
        rec = unwind_cname(rec, args.cname)
    ns = get_nameservers(rec)
    blue_expr = re.compile(args.dnsmatchblue)
    green_expr = re.compile(args.dnsmatchgreen)
    if not ns: raise ValueError("Unable to find name server(s)")
    print("Will poll %s using nameservers %s" % (rec, ', '.join(ns)))
    def poll():
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = list(map(str, ns))
        try:
            r = list(resolver.query(rec, 'CNAME', raise_on_no_answer=False))
        except dns.resolver.NXDOMAIN:
            pass
        if not r:
            r = list(resolver.query(rec, 'A', raise_on_no_answer=False))
        is_blue = False
        is_green = False
        for rr in r:
            m = blue_expr.search(str(rr))
            if m:
                is_blue = True
            m = green_expr.search(str(rr))
            if m:
                is_green = True
        if is_blue:
            if is_green: return "mix"
            return "blue"
        else:
            if is_green: return "green"
            return "none"
    poll()
    return poll

def get_nameservers(rec):
    rec = dns.name.from_text(str(rec))
    recs = set()
    while True:
        if recs: break # Stop as soon as we have nameservers
        try:
            for r in dns.resolver.query(rec, 'NS', raise_on_no_answer=False):
                try:
                    for raddr in dns.resolver.query(r.target, 'A', raise_on_no_answer=False):
                        recs.add(str(raddr.address))
                except dns.resolver.NXDOMAIN:
                    pass
        except dns.resolver.NXDOMAIN:
            # No NS records, try parent
            pass
        if len(rec.labels) <= 3: # no more parents to try
            break
        rec = rec.parent()

    return recs


def unwind_cname(rec, ct):
    print("Unwinding %s" % rec)
    rec = dns.name.from_text(str(rec))
    for _ in range(ct):
        recs = set()
        try:
            for r in dns.resolver.query(rec, 'CNAME'):
                print("  " + str(r))
                if r.target:
                    recs.add(str(r.target))
            if recs:
                rec = list(recs)[0]
            else:
                break
        except dns.resolver.NXDOMAIN:
            # No more CNAME records
            break
    return rec


def perform():

    n = dns.name.from_text('www.dnspython.org')
    o = dns.name.from_text('dnspython.org')
    print(n.is_subdomain(o))         # True
    print(n.is_superdomain(o))       # False
    print(n > o)                     # True
    rel = n.relativize(o)            # rel is the relative name www
    n2 = rel + o
    print(n2 == n)                   # True
    print(n.labels)                  # ['www', 'dnspython', 'org', '']  


    r = dns.resolver.query('tennis.cmbsports.net', 'CNAME')
    for answer in r:
        print(answer)