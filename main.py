import argparse
import sys, time

import source_dns
import target_homey
import target_hue

parser = argparse.ArgumentParser(description='Blue/Green deployment publish to Philips Hue.')
parser.add_argument('--dns', metavar='hostname', type=str,
                    help='use DNS approach')
source_dns.add_args(parser)
parser.add_argument('--interval', dest='interval', metavar="SECONDS", default=5, type=int,
                    help='polling interval')

parser.add_argument('--homey', dest='homey', metavar="ID", type=str,
                    help='control Athom Homey (ID e.g. 0123456789abcdef12345678)')
target_homey.add_args(parser)
parser.add_argument('--hue', dest='hue', metavar="IP", type=str,
                    help='control Philips Hue bridge (IP e.g. 192.168.1.11)')
target_hue.add_args(parser)
args = parser.parse_args()
if args.dns:
    source = source_dns.get_source(args)
else:
    print("No valid source specified", file=sys.stderr)
    sys.exit(1)

targets = []
if args.homey:
    targets.append(target_homey.get_target(args))
if args.hue:
    targets.append(target_hue.get_target(args))
if not targets:
    print("No valid target specified", file=sys.stderr)
    sys.exit(1)

try:
    while True:
        ret = source()
        print("is %s" % ret)
        sys.stdout.flush()
        for tgt in targets:
            tgt(ret)
        time.sleep(args.interval)
except KeyboardInterrupt:
    pass
