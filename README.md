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

## Usage

    usage: main.py [-h] [--dns hostname] [--dns-match-blue regex]
               [--dns-match-green regex] [--cname NUMLEVELS]
               [--interval SECONDS] [--homey ID] [--homey-blue-event EVENT]
               [--homey-green-event EVENT] [--homey-mix-event EVENT]
               [--homey-mix-error EVENT] [--homey-webhook-repeat] [--hue IP]
               [--hue-username USERNAME] [--hue-lights ARRAY]
