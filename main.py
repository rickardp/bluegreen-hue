import argparse
import sys, time

parser = argparse.ArgumentParser(description='Blue/Green deployment publish to Philips Hue.')
parser.add_argument('--dns', metavar='hostname', type=str,
                    help='use DNS approach')
parser.add_argument('--dns-match-blue', metavar='regex', dest='dnsmatchblue', type=str, default='blue',
                    help='the DNS response that matches Blue (default is "blue")')
parser.add_argument('--dns-match-green', metavar='regex', dest='dnsmatchgreen', type=str, default='green',
                    help='the DNS response that matches Blue (default is "green")')
parser.add_argument('--cname', metavar='NUMLEVELS', dest='cname', type=int, default=0,
                    help='pre-resolves NUMLEVELS levels of CNAME')
parser.add_argument('--interval', dest='interval', metavar="SECONDS", default=5, type=int,
                    help='polling interval')

args = parser.parse_args()
if args.dns:
    import source_dns
    source = source_dns.get_source(args)
else:
    print("No valid source specified", file=sys.stderr)
    sys.exit(1)

while True:
    ret = source()
    print(ret)
    time.sleep(args.interval)
print(source)
#print(args.accumulate(args.integers))
