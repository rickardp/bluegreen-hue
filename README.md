# bluegreen-hue

Visualize the state of blue/green deployment using the Athom Homey or Philips Hue.


## How to use it

To build and run, use


     # Control Homey using Azure Traffic Manager as source
     docker run -it $(docker build -q .) --dns my-site.trafficmanager.net --homey 12345abcde

     # Ditto Philips Hue
     docker run -it $(docker build -q .) --dns my-site.trafficmanager.net --hue 192.168.0.1 --hue-lights 1,3,6

     # my-site.com is cname to traffic manager
     docker run -it $(docker build -q .) --dns my-site.com --cname 1 --hue 192.168.0.1

The easiest way to have it run as a service is probably to create a `docker-compose.yml` file and run it with `docker-compose up --build -d`. Set restart policy to `always` to have it start up automatically after a reboot.

### How to control Homey

Homey supports webhooks from the cloud API. You can control the event names in the webhooks by adjusting `--homey-*-event`. Create a flow for each event you want to support. In this flow you can adjust lamps, lightstrips, change LED ring color, speak, or whatever.

You can either have the webhook sent with every poll, or only when it is changed (the latter is the default).

### How to control Hue

Hue support is very basic. Specify the IP and username, and which lamps to control. The colors are hard coded.

## Usage

    usage: main.py [-h] [--dns hostname] [--dns-match-blue regex]
               [--dns-match-green regex] [--cname NUMLEVELS]
               [--interval SECONDS] [--homey ID] [--homey-blue-event EVENT]
               [--homey-green-event EVENT] [--homey-mix-event EVENT]
               [--homey-mix-error EVENT] [--homey-webhook-repeat] [--hue IP]
               [--hue-username USERNAME] [--hue-lights ARRAY]
