#import logging # for the following line
#logging.getLogger("scapy.runtime").setLevel(logging.ERROR) # suppress IPV6 warning on startup
from scapy.all import * # for sniffing for the ARP packets
import Queue

q = Queue.Queue()


def arp_display(pkt):
  if pkt[ARP].op == 1:
    if pkt[ARP].psrc == "0.0.0.0":
      if pkt[ARP].hwsrc == "74:75:48:01:88:5c":
         print "SLEEP"
  return
 
sniff(prn=arp_display, filter="arp", store=0)
