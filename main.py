import argparse
import sys, time

import source_dns
import target_homey

parser = argparse.ArgumentParser(description='Blue/Green deployment publish to Philips Hue.')
parser.add_argument('--dns', metavar='hostname', type=str,
                    help='use DNS approach')
source_dns.add_args(parser)
parser.add_argument('--interval', dest='interval', metavar="SECONDS", default=5, type=int,
                    help='polling interval')

parser.add_argument('--homey', dest='homey', metavar="URL", type=str,
                    help='control Athom Homey (URL e.g. http://192.168.1.11)')
target_homey.add_args(parser)
args = parser.parse_args()
if args.dns:
    source = source_dns.get_source(args)
else:
    print("No valid source specified", file=sys.stderr)
    sys.exit(1)

targets = []
if args.homey:
    targets.append(target_homey.get_target(args))
if not targets:
    print("No valid target specified", file=sys.stderr)
    sys.exit(1)

try:
    while True:
        ret = source()
        print(ret)
        for tgt in targets:
            tgt(ret)
        time.sleep(args.interval)
except KeyboardInterrupt:
    pass

