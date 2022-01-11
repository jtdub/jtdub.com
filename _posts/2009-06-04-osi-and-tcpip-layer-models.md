---
layout: post
title: OSI and TCP/IP Layer Models
date: '2009-06-04'
author: jtdub
tags:
- OSI Model
- TCP/IP Model
- CCNA Study Notes
- packetgeek.net
---

#### Background History

Many vendors were developing proprietary network protocols that would only work with their systems. The International Organization for Standards (ISO) started to work on an open standard network model in the 1970's. This network model was called Open Systems Interconnection (OSI). A less formal effort to create a standardized, public network model came about from a U.S. Defense Department contract. Researchers from various universities worked to further the development of the work done by the department. The efforts resulted in TCP/IP.

By the late 1980's, there were many proprietary, and two standardized network models. Eventually TCP/IP became the standard. The OSI model, in part suffered from a slower formal standardization process as compared with TCP/IP and never succeeded in the market place.

#### TCP/IP

TCP/IP classifies the various protocols into different catagories or layers.

<table border="1" cellpadding="1" width="50%">
 <tr>
  <td>
   <span style="font-weight:bold;">
    TCP/IP Architecture Layer
   </span>
  </td>
  <td>
   <span style="font-weight:bold;">
    Example Protocols
   </span>
  </td>
 </tr>
 <tr>
  <td>
   Application
  </td>
  <td>
   HTTP, SMTP, DNS, DHCP
  </td>
 </tr>
 <tr>
  <td>
   Transport
  </td>
  <td>
   TCP, UDP
  </td>
 </tr>
 <tr>
  <td>
   Internet
  </td>
  <td>
   IP
  </td>
 </tr>
 <tr>
  <td>
   Network access
  </td>
  <td>
   Ethernet, PPP, Frame Relay, IPSEC
  </td>
 </tr>
</table>

If someone makes up a new application, the protocol used directly by the application would be considered to be application layer protocols. Similarly, the network access layer includes protocols and standards such as Ethernet. If someone makes up a new type of LAN, those protocols would be considered to be apart of the network access layer.

#### TCP/IP Application Layer

The TCP/IP application layer provides services to the application software running on a computer. The application layer does not define the application itself, but rather it defines the services that the applications need. The application layer provides an interface between the software running on a computer and the networks.

When one computer wants to communicate with the same layer on another computer, the two computers use headers to hold the information that they want to communicate. The headers are part of what is transmitted between the two computers. This process is called same-layer interaction.

Regardless of what the application layer protocol is, they all use the same concept of communicating with the application layer on the other computer using the application layer headers.

#### The TCP/IP Transport Layer

The TCP/IP transport layer consists of two main protocol options: Transmission Control Protocol (TCP) and User Datagram Protocol (UDP).

TCP/IP needs a mechanism to guarantee delivery of data across a network. TCP provides an error-recovery feature to the application protocols by using acknowledgments.

The benefits of TCP error recovery can not be seen unless the data is lost. TCP will resend data and ensure that it is received successfully. This is demonstrates an example of adjacent-layer interaction, which defines the concept of how adjacent layers in a network model, on the same computer, work together. Higher layer protocols (example, SMTP, HTTP) need to do something that it can not do, error recovery. The higher layer asks the next lower-layer protocol, TCP, to perform the service.

UDP does not perform error recovery.

Same-layer interaction on different computers: Two computers use a protocol to communicate with the same layer on another computer. the protocol defined by each layer uses a header that is transmitted between the computers, to communicate each computer wants to do.

Adjacent-layer interaction on the same computer: A single computer, one layer provides a service to a higher layer. the software or hardware that implements the higher layer requests that the next lower layer perform the needed function.

#### TCP/IP Internet Layer

IP defines logical addresses, called IP addresses, which allow each TCP/IP-speaking device to have an address with which to communicate. IP also defines the routing process of how a router should forward packets of data.

#### TCP/IP Network Access Layer

The network access layer defines the protocol and hardware required to deliver data across some physical network. The term network access refers to the fact that this layer defines how to physically connect a computer to the phyical media over which data can be transmitted. Ethernet is one example protocol at the TCP/IP network access layer. Each layer provides services to the layer above it in the model. (TCP/IP and OSI models)

IP, an TCP/IP Internet Layer, relies on the network access layer to deliver IP packets across a physical network.

The network access layer includes a large number of protocols, such as Ethernet, PPP, IPSEC, Frame Relay, etc.

IP uses the network access layer protocols to deliver an IP packet to the next router or host, with each router repeating the process until the packet arrives at the destination. Each network access protocol uses headers to encode the information needed to successfully deliver the data across the physical network, in much the same way as other layers use headers to achieve their goals.

#### Data Encapsulation Terminalolgy

As you can see from the explanations of how HTTP, TCP, IP and the network access protocols, Ethernet and PPP do their jobs, each layer adds its own header (and sometimes trailer) to the data supplied by the higher layer. Encapsulation refers to the process of putting headers and trailers around some data.

#### Five steps of Data Encapsulation

<table border="1" cellpadding="1" width="50%">
 <tr>
  <td>
   1.
  </td>
  <td>
   <div align="center">
    | Data |
   </div>
  </td>
  <td>
   <div align="center">
    Application
   </div>
  </td>
  <td>
   <div align="center">
   </div>
  </td>
 </tr>
 <tr>
  <td>
   2.
  </td>
  <td>
   <div align="center">
    | TCP | Data |
   </div>
  </td>
  <td>
   <div align="center">
    Transport
   </div>
  </td>
  <td>
   <div align="center">
    Segment
   </div>
  </td>
 </tr>
 <tr>
  <td>
   3.
  </td>
  <td>
   <div align="center">
    | IP | TCP | Data |
   </div>
  </td>
  <td>
   <div align="center">
    Internet
   </div>
  </td>
  <td>
   <div align="center">
    Packet
   </div>
  </td>
 </tr>
 <tr>
  <td>
   4.
  </td>
  <td>
   <div align="center">
    | LH | IP | TCP | Data | LT |
   </div>
  </td>
  <td>
   <div align="center">
    Network Access
   </div>
  </td>
  <td>
   <div align="center">
    Frame
   </div>
  </td>
 </tr>
 <tr>
  <td>
   5.
  </td>
  <td colspan="3">
   <div align="center">
    Transmit Bits
   </div>
  </td>
 </tr>
</table>

<span style="font-style:italic;">
*LH and LT stand for link header and link trailer*
*Segment, packet, and frame* refer to the headers and possibly trailers defined by a particular layer. Only the network access layer provides a trailer in it's encapsulation, called a frame.

#### The OSI Reference Model

The Open System Interconnection (OSI) model consists of seven layers. Each layer defines a set of typical networking functions.

<table border="1" cellpadding="1" width="50%">
 <tr>
  <td>
   <div align="center">
    <span style="font-weight:bold;">
     OSI Model
    </span>
   </div>
  </td>
  <td>
   <div align="center">
    <span style="font-weight:bold;">
     TCP/IP
    </span>
   </div>
  </td>
 </tr>
 <tr>
  <td>
   <div align="center">
    Application
   </div>
  </td>
  <td rowspan="3">
   <div align="center">
    Application
   </div>
   <div align="center">
   </div>
   <div align="center">
   </div>
  </td>
 </tr>
 <tr>
  <td>
   <div align="center">
    Presentation
   </div>
  </td>
 </tr>
 <tr>
  <td>
   <div align="center">
    Session
   </div>
  </td>
 </tr>
 <tr>
  <td>
   <div align="center">
    Transport
   </div>
  </td>
  <td>
   <div align="center">
    Transport
   </div>
  </td>
 </tr>
 <tr>
  <td>
   <div align="center">
    Network
   </div>
  </td>
  <td>
   <div align="center">
    Internet
   </div>
  </td>
 </tr>
 <tr>
  <td>
   <div align="center">
    Data Link
   </div>
  </td>
  <td rowspan="2">
   <div align="center">
    Network Access
   </div>
   <div align="center">
   </div>
  </td>
 </tr>
 <tr>
  <td>
   <div align="center">
    Physical
   </div>
  </td>
 </tr>
</table>
*OSI Layers in reference to the TCP/IP Layers*

TCP/IP's internet layer, as implemented mainly by IP, equates most directly to the protocol, using OSI terminology and numbers for the layer.

OSI network layer defines logical addressing and routing, as does the TCP/IP internet layer. Similarly, the TCP/IP transport layer defines many functions, including error recovery, as does the OSI transport layer - so TCP is called a transport layer, or Layer 4 protocol.

Not all TCP/IP layers correspond to a single OSI layer. In particular, the TCP/IP network access layer defines both physical network specifications and the protocols used to control the physical network.

**Note:** be aware of both views about whether TCP/IP has a single network access layer or two lower layers (data link and physical).

The upper layers of the OSI reference model (application, presentation, and session - Layers 7 - 5) define functions focused on the application. the lower four layers (transport, network, data link, and physical - Layers 4 - 1) define functions focused on the end-to-end delivery of the data.

<table border="1" cellpadding="1" width="80%">
 <tr>
  <td>
   <span style="font-weight:bold;">
    Layer
   </span>
  </td>
  <td>
   <span style="font-weight:bold;">
    Functional Description
   </span>
  </td>
 </tr>
 <tr>
  <td valign="top">
   7
  </td>
  <td>
   Layer 7 provides an interface between the communications software and any applications that need to communicate outside the computer on which the application resides. It also defines processes for user authentication.
  </td>
 </tr>
 <tr>
  <td valign="top">
   6
  </td>
  <td>
   The layers's main purpose is to define negotiate data formats, such as ASCII text, EBCDIC text, binary, BCD, and JPEG. Encryption also is defined by OSI as a presentation layer service.
  </td>
 </tr>
 <tr>
  <td valign="top">
   5
  </td>
  <td>
   The session layer defines how to start, control, and end conversations (called sessions). This includes the control and management of multiple bidirectional messages so that the application can be notified if only some of the series of messages are completed. this allows the presentation layer to have a seamless view of an incoming stream of data.
  </td>
 </tr>
 <tr>
  <td valign="top">
   4
  </td>
  <td>
   Layer 4 protocols provide a large number of services, as described of Chapter 6 of this book. Although OSI Layer 5 through 7 focus on issues related to the application, Layer 4 focuses on issues related to data delivery to another computer - for instance, error recovery and flow contol.
  </td>
 </tr>
 <tr>
  <td valign="top">
   3
  </td>
  <td>
   The network layer defines three main features: logical addressing, routing (forwarding), and path determination. The routing concepts define how devices (typically routers) forward packets to their final destination. Logical addressing defines how each device can have an address that can be used by the routing process. Path determination refers to the work done by routing protocols by which all possible routers are learned, but the best route is chosen for use.
  </td>
 </tr>
 <tr>
  <td valign="top">
   2
  </td>
  <td>
   The data link layer defines the rules (protocols) that determine when a device can send data over a particular medium. Data link protocols also define the format of a header and trailer that allows devices attached to the medium to send and reeive data successfully. The data link trailer, which follows the encapsulated data, typically defines a Frame Check Sequence (FCS) field, which allows the receiving device to detect transmission errors.
  </td>
 </tr>
 <tr>
  <td valign="top">
   1
  </td>
  <td>
   The layer typically refers to standards from other organizations. These standards deal with the physical characteristics of the transmission medium, including connectors, pins, use of pins, electrical currents, encoding, light modulation, and the rules for how to activate and deactivate the use of the physical medium.
  </td>
 </tr>
</table>
*The CCNA focuses on issues in the lower (4-1) layers in the OSI.*
*OSI Layering Concepts and Benefits*

Many benefits can be gained from the process of breaking up functions or tasks of networking into smaller chunks and defining standard interfaces between these layers. The layers break a large, complex set of concepts and protocols into smaller pieces, making it easier to talk about, easier to implement with hardware and software, and easier to *troubleshoot*

"**A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing." (Layers 7 - 1) - A mnemonic phrase to help remember the OSI layer names.
