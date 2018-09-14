from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.node import RemoteController, Host, OVSKernelSwitch
import time
import os
from mininet.link import TCLink

class IpHost(Host):
    def __init__(self, name, gateway, *args, **kwargs):
        super(IpHost, self).__init__(name, *args, **kwargs)
        self.gateway = gateway


class LeafAndSpine(Topo):
    def __init__(self, spine=2, leaf=2, fanout=2, **opts):
        "Create Leaf and Spine Topo."

        Topo.__init__(self, **opts)

        # Add spine switches


        spines = {}
        for s in range(spine):
            spines[s] = self.addSwitch('spine40%s' % (s + 1))
        # Set link speeds to 100Mb/s
        linkopts = dict(bw=1000)
        linkopts2 = dict(bw=1000)
        #linkopts = dict()
        #linkopts2 = dict();

        # Add Leaf switches
        for ls in range(leaf):
            leafSwitch = self.addSwitch('leaf%s' % (ls + 1))
            # Connect leaf to all spines
            for s in range(spine):
                switch = spines[s]
                self.addLink(leafSwitch, switch, **linkopts)
            # Add hosts under a leaf, fanout hosts per leaf switch
            for f in range(fanout):
                host = self.addHost('h%s' % (ls * fanout + f + 1), mac='00:00:00:00:00:0%s' %(ls * fanout + f + 1))  # ,
                # cls=IpHost,
                # gateway='10.0.%s.254' % ((ls + 1)),
                # ip='10.0.%s.%s/24' % ((ls + 1), (f + 1)))

                self.addLink(host, leafSwitch, **linkopts2)

#topos = { 'leaf_spine' : ( lambda: LeafAndSpine(2,3,2) ) }
if __name__ == '__main__':
    topo = LeafAndSpine(2, 2, 1)
    controllerIp = "128.10.135.42"
    net = Mininet(topo, autoSetMacs=True, xterms=False, controller=RemoteController, switch=OVSKernelSwitch,link=TCLink)
    net.addController('c', ip='128.10.135.42', port=6680)  # localhost:127.0.0.1 vm-to-mac:10.0.2.2 server-to-mac:128.112.93.28
   

    #net = Mininet(topo, link=TCLink, switch=OVSKernelSwitch)
    print "\nHosts configured with IPs, switches pointing to OpenVirteX at 128.112.93.28 port 6633\n"

    interval = 10;
    net.start()
    time.sleep(4)
    net.pingAll()
    time.sleep(15)
    hosts = net.hosts;

    for h in hosts:
       if h.name == 'h1':
          h1 = h
       if h.name == 'h2':
           hN = h

    switches = net.switches
    links = net.links;
    c = net.controller;

    for j in range(2,51, 8):
      interval = j
      for i in range(5): 
          simTime = 100
          numConnections = 5
          hN.cmd("iperf3 -s -p 80 &")
          time.sleep(2)
          h1.cmd("iperf3 -c 10.0.0.2 -t " + str(simTime)+ "  -p 80 -b 1000Mb  > client" + str(interval)+ "-" + str(i) +".log &")
        
          time.sleep(5)

          numLoops = (simTime/(2 *interval)) + 1
          interfaceName1="spine401-eth1"
          interfaceName2="spine402-eth1"

          for i in range(1,numLoops):
            os.system("sudo ifconfig " + interfaceName1+ " down")
            time.sleep(interval)
            os.system("sudo ifconfig " + interfaceName1 + " up")
            os.system("sudo ifconfig " + interfaceName2+ " down")
            time.sleep(interval)
            os.system("sudo ifconfig " + interfaceName2+ " up")

            print j,i
            #CLI(net)
          os.system('pkill -f \'iperf\'')

    net.stop()
