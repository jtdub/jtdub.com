---
layout: post
title: Using a serial console on Mac OS X
date: '2016-02-15'
author: jtdub
tags:
- Serial
- Console
- Mac OS X
- packetgeek.net
---

As a network engineer, a fundamental task is putting a base configuration onto a device via a serial console. In Windows, there are several applications from Hyper Terminal to Putty. In Linux, there is minicom. I've never been a Microsoft fan, but have been a Linux user for many years. Over the last few years have been using Mac OS X full time for work and personal. Given this, I need the ability to access a network device via a serial connection. A quick Google was [fruitful](https://supportforums.cisco.com/discussion/12071321/how-use-mac-connecting-through-console-port).

* Plug your USB to Serial device into the USB port.
*  Open a command termal and execute:
   * `ls /dev/*usb*`

If your Mac recognizes the USB device, it will display a USB device in `/dev`. If not, you may need to download and install a USB driver for your device. I used [this article](http://plugable.com/2011/07/12/installing-a-usb-serial-adapter-on-mac-os-x) to assist me in determining which USB driver to download and install.

* My USB device showed up as `/dev/tty.usbserial`, thus I'll use that for the remainder of this example.
  Connect the other end of your USB to Serial cable into your network device's serial port.
* Execute: `screen /dev/tty.usbserial 9600`
* [Screen](https://kb.iu.edu/d/acuy) is a UNIX utility that allows you to access your local computers VT100 terminal.
* `/dev/tty.usbserial` is the driver to access your USB serial device.
* `9600` is the baud rate.
* Press enter and you should be prompted with your network device prompt.
* To disconnect use the following key sequence: `CTRL+A` followed by `CTRL+\`
