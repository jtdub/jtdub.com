---
layout: post
title: 'PCAP or It Didnt Happen'
date: '2025-01-25'
author: jtdub
tags:
- packetgeek.net
- MPLS
- PCAP
- BGP
- EVPN
- VXLAN
- VLAN
- GRE
- Networking
---
In the world of IP networking, everything boils down to packets. Without a solid understanding of how packets are structured, diagnosing issues, optimizing performance, or even designing a robust network can feel like shooting in the dark. That’s why understanding packet structures isn’t just helpful—it’s essential.

In this blog, we’ll break down packet structures, explore the basics of framing and tagging, and examine how advanced networking features like VLAN tagging, MPLS, GRE, IPsec, BGP, and VXLAN are ultimately just clever manipulations of these packet structures. To keep things engaging, we’ll use ASCII diagrams and workflows.

## **Why You Need to Understand Packets**

At its core, networking is the process of moving data from one place to another. Packets are the vehicles that carry this data. Understanding what these vehicles look like, how they’re built, and what happens to them as they traverse the network is critical for troubleshooting, configuring, and designing modern networks.

Key reasons to understand packet structures:
1. **Troubleshooting**: Tools like Wireshark or `tcpdump` require knowledge of packet headers to diagnose network issues.
2. **Optimization**: Knowing how packets are structured helps in understanding overhead and optimizing performance.
3. **Advanced Features**: Features like VLANs, MPLS, GRE, IPsec, and VXLAN rely on additional headers and tags. If you understand packet structures, these features are easier to conceptualize.

## **Packet Structure Breakdown**

Let’s start with a simple IP packet and break it down:

```
+-----------------+-----------------+-----------------+ 
| Ethernet Header | IP Header       | Payload         | 
+-----------------+-----------------+-----------------+
```

### 1. **Ethernet Header**
The Ethernet header provides Layer 2 (Data Link) information. It includes:
- **Destination MAC**: Where the frame is going.
- **Source MAC**: Where the frame came from.
- **Type**: Indicates the type of payload (e.g., IPv4, ARP).

### 2. **IP Header**
The IP header provides Layer 3 (Network) information. Key fields include:
- **Source IP**: IP address of the sender.
- **Destination IP**: IP address of the recipient.
- **Protocol**: Indicates the type of Layer 4 payload (e.g., TCP, UDP).

### 3. **Payload**
The payload carries the actual data, which could be a TCP segment, UDP datagram, or something else.

## **It’s All Framing and Tagging**

As we add advanced networking features, we’re essentially adding new headers to packets. These headers allow devices to make more intelligent decisions about how to handle traffic. Let’s dive into some examples.

### **VLAN Tagging**

VLAN tagging adds a 4-byte 802.1Q header to the Ethernet frame.

```
+------------+------+----------+-----------+ 
| Eth Header | VLAN | IP Hdr   | Payload   |
+------------+------+----------+-----------+
```

#### **VLAN Tagging Workflow**

```
Host A -> Switch -> Add VLAN Tag -> Switch -> Remove VLAN Tag -> Host B
```

### **GRE (Generic Routing Encapsulation)**

GRE encapsulates Layer 3 packets inside another Layer 3 packet, allowing tunneling of traffic over an IP network.

```
+------------+-----------+----------+-----------+ 
| Eth Header | Outer IP  | GRE Hdr  | Inner Pkt | 
+------------+-----------+----------+-----------+
```

**GRE Header Fields**:
- **Flags**: Indicate optional fields.
- **Protocol**: Specifies the encapsulated protocol (e.g., IPv4, IPv6).

**Workflow:**
1. A router receives a packet to be tunneled.
2. The router encapsulates the original packet with a new IP header and a GRE header.
3. The encapsulated packet is sent over the network.
4. The receiving router removes the GRE and outer IP headers, forwarding the original packet.

#### GRE Workflow

```
Host A -> Router -> Encapsulate with GRE -> Transit Network -> Decapsulate -> Host B
```

### **IPsec (IP Security)**

IPsec secures IP packets by encrypting and authenticating them. It works in two modes:
1. **Transport Mode**: Secures only the payload of the IP packet.
2. **Tunnel Mode**: Encapsulates the entire original IP packet, adding a new IP header.

#### **IPsec in Tunnel Mode**

```
+------------+-----------+------------+------------+
| Eth Header | Outer IP  | ESP Hdr    | Inner Pkt  | 
+------------+-----------+------------+------------+
```

#### **ESP Header Fields (Encapsulating Security Payload)**:
- **SPI (Security Parameters Index)**: Identifies the security association.
- **Sequence Number**: Protects against replay attacks.
- **Encrypted Payload**: Contains the encrypted inner packet.

**Workflow:**
1. A router applies IPsec to a packet.
2. The original packet is encrypted, and an IPsec header (ESP) is added.
3. A new IP header is added for tunneling purposes.
4. The packet is transmitted over the network securely.
5. The receiving router decrypts the packet, removing the ESP and outer IP headers.

#### IPSec Workflow

```
Host A -> Router -> Encrypt + Add ESP Header -> Transit Network -> Decrypt -> Host B
```

### **MPLS (LDP and SR)**

In MPLS, labels are added between the Ethernet and IP headers to create label-switched paths (LSPs).

```
+------------+------+----------+-----------+
| Eth Header | MPLS | IP Hdr   | Payload   | 
+------------+------+----------+-----------+
```

#### MPLS Workflow

```
Ingress Router -> Add MPLS Label -> Transit Router -> Swap MPLS Label -> Egress Router -> Remove MPLS Label
```

### **BGP IPv4 Unicast**

For standard IPv4 unicast, BGP advertises routes with specific attributes.

```
+------------+----------+----------+
| Eth Header | IP Hdr   | BGP Msg  |
+------------+----------+----------+
```

### **BGP EVPN and VXLAN**

BGP EVPN (Ethernet VPN) is commonly used with VXLAN to create virtual Layer 2 networks over Layer 3.

```
+------------+------+----------+------+-----------+
| Eth Header | VLAN | IP Hdr   | UDP  | VXLAN Hdr | 
+------------+------+----------+------+-----------+
```

#### BGP EVPN and VXLAN Workflow

```
Host A -> VTEP1 -> Encapsulate in VXLAN -> Route Through L3 -> VTEP2 -> Decapsulate -> Host B
```

## **Why “PCAP or it Didn’t Happen”?**

Tools like Wireshark, `tcpdump`, or even modern telemetry platforms allow you to see packet headers in action. By capturing and analyzing packets, you can:
- Verify configurations (e.g., VLANs, GRE, IPsec).
- Diagnose problems (e.g., routing loops, packet drops).
- Understand advanced features in real-world deployments.

If you can’t prove it in a packet capture, did it really happen?

## **Conclusion**

Whether you’re troubleshooting a VLAN issue, configuring GRE, securing traffic with IPsec, or deploying BGP EVPN with VXLAN, everything in networking starts and ends with packets. By understanding packet structures and how framing and tagging work, you’ll not only be a better network engineer—you’ll also have the power to demystify complex problems.
