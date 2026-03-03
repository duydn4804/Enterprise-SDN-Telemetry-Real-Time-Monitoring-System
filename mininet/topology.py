#!/usr/bin/env python3
"""
3-Tier Data Center Topology
Kết nối với OpenDaylight Controller
Core → Aggregation → Access → Hosts
"""
import time
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink


class DataCenterTopo(Topo):
    def build(self):
        info("*** Tạo 3-Tier Data Center Topology\n")

        # ── TIER 1: Core Switch ──
        core = self.addSwitch('s1', dpid='0000000000000001')

        # ── TIER 2: Aggregation Switches ──
        aggr1 = self.addSwitch('s2', dpid='0000000000000002')
        aggr2 = self.addSwitch('s3', dpid='0000000000000003')

        # ── TIER 3: Access Switches ──
        acc1 = self.addSwitch('s4', dpid='0000000000000004')
        acc2 = self.addSwitch('s5', dpid='0000000000000005')
        acc3 = self.addSwitch('s6', dpid='0000000000000006')
        acc4 = self.addSwitch('s7', dpid='0000000000000007')

        # ── HOSTS ──
        h1 = self.addHost('h1', ip='10.0.0.1/8')
        h2 = self.addHost('h2', ip='10.0.0.2/8')
        h3 = self.addHost('h3', ip='10.0.0.3/8')
        h4 = self.addHost('h4', ip='10.0.0.4/8')
        h5 = self.addHost('h5', ip='10.0.0.5/8')
        h6 = self.addHost('h6', ip='10.0.0.6/8')
        h7 = self.addHost('h7', ip='10.0.0.7/8')
        h8 = self.addHost('h8', ip='10.0.0.8/8')

        # ── LINKS ──
        # Core ↔ Aggregation
        self.addLink(core,  aggr1, bw=1000, delay='1ms')
        self.addLink(core,  aggr2, bw=1000, delay='1ms')

        # Aggregation ↔ Access
        self.addLink(aggr1, acc1,  bw=100,  delay='2ms')
        self.addLink(aggr1, acc2,  bw=100,  delay='2ms')
        self.addLink(aggr2, acc3,  bw=100,  delay='2ms')
        self.addLink(aggr2, acc4,  bw=100,  delay='2ms')

        # Access ↔ Hosts
        self.addLink(acc1,  h1,    bw=1000,   delay='5ms')
        self.addLink(acc1,  h2,    bw=1000,   delay='5ms')
        self.addLink(acc2,  h3,    bw=1000,   delay='5ms')
        self.addLink(acc2,  h4,    bw=1000,   delay='5ms')
        self.addLink(acc3,  h5,    bw=1000,   delay='5ms')
        self.addLink(acc3,  h6,    bw=1000,   delay='5ms')
        self.addLink(acc4,  h7,    bw=1000,   delay='5ms')
        self.addLink(acc4,  h8,    bw=1000,   delay='5ms')


def run():
    setLogLevel('info')
    topo = DataCenterTopo()
    net = Mininet(
        topo=topo,
        controller=RemoteController('c0', ip='127.0.0.1', port=6633),
        switch=OVSSwitch,
        link=TCLink,
        autoSetMacs=True
    )

    net.start()

    # Bước 1: Ép OpenFlow 1.3
    info("*** Cấu hình OpenFlow 1.3 cho tất cả switches...\n")
    for sw in net.switches:
        sw.cmd('ovs-vsctl set bridge %s protocols=OpenFlow13' % sw.name)
        info("    %s → OpenFlow13 ✅\n" % sw.name)

    # Bước 2: Chờ ODL học topology
    info("*** Chờ ODL xử lý topology (15 giây)...\n")
    time.sleep(15)


    info("\n*** Mở browser: http://localhost:8181/index.html\n")
    info("*** user: admin | pass: admin\n")

    CLI(net)
    net.stop()


if __name__ == '__main__':
    run()
