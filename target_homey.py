import requests

def add_args(parser):
    parser.add_argument('--homey-blue-event', metavar='EVENT', dest='homey_blue_event', type=str, default="blue",
                        help='the webhook event to send when blue')
    parser.add_argument('--homey-green-event', metavar='EVENT', dest='homey_green_event', type=str, default="green",
                        help='the webhook event to send when green')
    parser.add_argument('--homey-mix-event', metavar='EVENT', dest='homey_mix_event', type=str, default="mix",
                        help='the webhook event to send when both blue and green (gradual rollout)')
    parser.add_argument('--homey-mix-error', metavar='EVENT', dest='homey_error_event', type=str, default="error",
                        help='the webhook event to send when indeterminate')
    parser.add_argument('--homey-webhook-repeat', dest='homey_repeat', action="store_true",
                        help='repeat the webhook (default is to only run when changed)')

last = None
def get_target(args):
    id = args.homey
    print("Will control Athom Homey @ %s" % id)
    def send_webhook(state):
        global last
        if state == "blue":
            evt = args.homey_blue_event
        elif state == "green":
            evt = args.homey_green_event
        elif state == "mix":
            evt = args.homey_mix_event
        else:
            evt = args.homey_error_event
        if args.homey_repeat or last != evt:
            last = evt
            wh = 'https://%s.connect.athom.com/api/manager/logic/webhook/%s' % (args.homey, state)
            print("Sending webhook %s" % wh)
            try:
                requests.get(wh, timeout=10.0)
            except requests.exceptions.Timeout:
                print("timeout sending webhook")
    return send_webhook
