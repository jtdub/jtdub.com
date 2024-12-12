---
layout: post
title: 'Hierarchical Configuration Version 3'
date: '2024-12-11'
author: jtdub
tags:
- packetgeek.net
- python
- hier_config
- Open Source
- Python Tips
- Network Programmability
- DevOps
- Network DevOps
---

## Introduction

I’ve previously written about the open-source Python library I help maintain, **Hierarchical Configuration (Hier Config)**, in these posts: [Network to Code](https://networktocode.com/blog/hier-config-up-and-running/) and [jtdub.com](https://www.jtdub.com/2016/07/08/network-lifecycle-management-with).

Recently, the library underwent a major refactor that introduced breaking changes. This seemed like the perfect opportunity to revisit Hier Config, discuss the updates, and explain how you can continue using your version 2 configurations with the new version 3.

**Hierarchical Configuration (Hier Config)** is an open-source Python library designed to manage and validate network device configurations. It enables network engineers to parse configurations into structured, hierarchical data that can be easily compared, analyzed, or modified programmatically. This is especially useful for automating tasks such as configuration compliance checks, remediation, and ensuring adherence to organizational standards.

## Quick Start

Here’s a quick walkthrough to get started with **Hier Config version 3**.

### Step 1: Import Required Classes
Start by importing the required classes and utility functions:

```python
from hier_config import WorkflowRemediation, get_hconfig, Platform
from hier_config.utils import read_text_from_file
```

### Step 2: Load Configurations
Load the running and intended configurations into strings from respective files:

```python
running_config_text = read_text_from_file("./tests/fixtures/running_config.conf")
generated_config_text = read_text_from_file("./tests/fixtures/generated_config.conf")
```

### Step 3: Create HConfig Objects
Create HConfig objects for the running and intended configurations, specifying the platform (e.g., `Platform.CISCO_IOS`):

```python
running_config = get_hconfig(Platform.CISCO_IOS, running_config_text)
generated_config = get_hconfig(Platform.CISCO_IOS, generated_config_text)
```

### Step 4: Initialize WorkflowRemediation
Use the `WorkflowRemediation` class to compare the configurations and generate the remediation steps:

```python
workflow = WorkflowRemediation(running_config, generated_config)

print("Remediation Configuration:")
print(workflow.remediation_config)
```

## Platform Driver Objects

In previous versions of Hier Config, there was a concept called [Hier Config options](https://hier-config.readthedocs.io/en/2.3-lts/advanced-topics/#hier_config-options), which allowed users to define custom logic for a device's operating system. These options were used to identify idempotent commands, determine when and how to negate commands, and specify command order.

**Version 3 introduces drivers** as a more structured and powerful approach to managing platform-specific behavior.

### What are Drivers?

A **driver** in Hier Config is a blueprint that encapsulates the rules and behaviors necessary to process and normalize network device configurations specific to a particular platform. It acts as a translator between Hier Config and the device's operating system, ensuring configurations are handled in a way that aligns with the unique syntax and requirements of platforms like Cisco IOS, Juniper JUNOS, or Arista EOS.

**Benefits of Drivers:**

* **Streamlined Operations:** Drivers centralize rules for command negation, ordering, and idempotency, making configuration management efficient and consistent across different devices.
* **Enhanced Maintainability:** By abstracting platform-specific logic, drivers improve the maintainability and scalability of Hier Config.
* **Modular and Reusable:** Drivers offer a modular, reusable approach, eliminating the need for repetitive custom logic for each device.

### Current Drivers in Hier Config

Hier Config includes built-in drivers for the following platforms:

- Cisco IOS
- Cisco NXOS
- Cisco IOSXR
- Arista EOS
- Juniper JUNOS
- HP Procurve (Aruba AOSS)
- VyOS
- Generic (for less common platforms)

These drivers handle platform-specific behaviors, allowing Hier Config to seamlessly normalize and process configurations across diverse network devices.

### Extending Drivers

There are two primary ways to extend a driver:

1. **Subclassing an Existing Driver:**

   Create a new driver class that inherits from an existing one and override the `_instantiate_rules` method to modify or add rules. This allows you to adapt existing logic for your specific needs.

   ```python
   # Example: Extending Cisco IOS driver for custom negation
   from hier_config.platforms.cisco_ios.driver import HConfigDriverCiscoIOS
   from hier_config.models import NegationDefaultWithRule, MatchRule

   class ExtendedIOSDriver(HConfigDriverCiscoIOS):
       @staticmethod
       def _instantiate_rules():
           rules = HConfigDriverCiscoIOS._instantiate_rules()
           # Add a custom negation rule for ntp server commands
           rules.negate_with.append(
               NegationDefaultWithRule(
                   match_rules=(MatchRule(startswith="ntp server "),),
                   use="no ntp server"
               )
           )
           return rules
   ```

2. **Dynamic Rule Updates:**

   Update an instantiated driver object by appending rules to its attributes (e.g., `negate_with`, `sectional_exiting`) without creating a subclass. This is useful for minor adjustments.

   ```python
   from hier_config import Platform, get_hconfig_driver
   from hier_config.models import NegationDefaultWithRule, MatchRule

   driver = get_hconfig_driver(Platform.CISCO_IOS)
   driver.rules.negate_with.append(
       NegationDefaultWithRule(
           match_rules=(MatchRule(startswith="ip route "),),
           use="no ip route"
       )
   )
   ```

### Creating a Custom Driver

For platforms not covered by existing drivers, you can create a custom driver by subclassing the `HConfigDriverBase` class. Define platform-specific rules and logic in the `_instantiate_rules` method and override properties like `negation_prefix` or `declaration_prefix` as needed.

```python
# Example: Custom driver for a new platform
from hier_config.platforms.driver_base import HConfigDriverBase, HConfigDriverRules
from hier_config.models import NegationDefaultWithRule, MatchRule, OrderingRule

class CustomPlatformDriver(HConfigDriverBase):
    @staticmethod
    def _instantiate_rules():
        return HConfigDriverRules(
            negate_with=[
                NegationDefaultWithRule(
                    match_rules=(MatchRule(startswith="custom command "),),
                    use="undo custom command"
                )
            ],
            ordering=[
                OrderingRule(
                    match_rules=(MatchRule(startswith="interface"),),
                    weight=10
                )
            ]
        )

    @property
    def negation_prefix(self):
        return "undo "

    @property
    def declaration_prefix(self):
        return ""
```

## WorkflowRemediation Object

In Hier Config version 2, the `Host` object served as the central orchestrator, processing running and generated configurations to produce remediation and rollback plans. In Hier Config version 3, this functionality has been encapsulated within the `WorkflowRemediation` class.

While the core concept remains similar, the underlying implementation has evolved. The `Host` class in version 2 required a `hostname` and an `os` string for instantiation, which in turn loaded default Hier Config options. The `hostname` attribute, however, was largely unused.

In contrast, the `WorkflowRemediation` class in version 3 operates on two `HConfig` objects. These objects are instantiated using the `get_hconfig` function, which takes a platform driver and a configuration string as input.

Here's an example using a custom driver:

```python
from hier_config import get_hconfig
from .custom_driver import CustomPlatformDriver

running_config_text = """
hostname example.rtr
interface gig0
  ip address 10.0.0.1/31
"""
generated_config_text = """
hostname example.rtr
interface gig0
  ip address 10.0.0.0/31
"""

running_config = get_hconfig(CustomPlatformDriver(), running_config_text)
generated_config = get_hconfig(CustomPlatformDriver(), generated_config_text)
```

With the `HConfig` objects (`running_config` and `generated_config`) instantiated, you can create a `WorkflowRemediation` object:

```python
from hier_config import WorkflowRemediation

wfr = WorkflowRemediation(running_config, generated_config)
```

Once the `WorkflowRemediation` object is created, you can easily generate remediation and rollback configurations:

```python
from hier_config import WorkflowRemediation, get_hconfig
from .custom_driver import CustomPlatformDriver

# ... (same configuration text as above)

wfr = WorkflowRemediation(running_config, generated_config)

print(wfr.remediation_config)
# Output:
# interface gig0
#   undo ip address 10.0.0.1/31
#   ip address 10.0.0.0/31
#   exit

print(wfr.rollback_config)
# Output:
# interface gig0
#   undo ip address 10.0.0.0/31
#   ip address 10.0.0.1/31
#   exit
```

## Version 2 to Version 3 Utilities

Hier Config has been open-sourced for nearly ten years now. Prior to version 3, the underlying architecture was quite dated. Version 3 introduced a revamped architecture and leverages Pydantic for its modeling needs. As a result, the concept of options and tags has evolved in Hier Config. This change introduces breaking changes for users with legacy deployments utilizing custom options and tags.

To facilitate a smoother transition to Hier Config version 3, a set of utilities has been developed to enable users to consume version 2 configurations within the version 3 environment. In `hier_config.utils`, the following functions are available:

### Platform Mapping Utilities

* **`hconfig_v2_os_v3_platform_mapper`**: This utility enables users to input an `os` and receive a corresponding version 3 driver. If no matching driver is found, the `GENERIC` driver is returned.

```python
from hier_config.utils import hconfig_v2_os_v3_platform_mapper

driver = hconfig_v2_os_v3_platform_mapper("ios")
print(driver)  # Output: <Platform.CISCO_IOS: '2'>
```

* **`hconfig_v3_platform_v2_os_mapper`**: This utility allows users to input a version 3 driver and obtain the corresponding version 2 `os`. If no matching platform is found, the `generic` string value is returned as the `os`.

```python
from hier_config.utils import hconfig_v3_platform_v2_os_mapper
from hier_config import Platform

os = hconfig_v3_platform_v2_os_mapper(Platform.CISCO_IOS)
print(os)  # Output: 'ios'
```

### Configuration Conversion Utilities

* **`load_hconfig_v2_options`**: This utility loads v2-style configuration options into a v3-compatible driver.

```python
from hier_config import Platform
from hier_config.utils import load_hconfig_v2_options

v2_options = {
    "negation": "no",
    "ordering": [{"lineage": [{"startswith": "ntp"}], "order": 700}],
    # ... other v2 options
}
platform = Platform.CISCO_IOS
driver = load_hconfig_v2_options(v2_options, platform)

print(driver.rules)
```

* **`load_hconfig_v2_tags`**: This utility converts v2-style tags into a tuple of `TagRule` Pydantic objects compatible with Hier Config v3.

```python
from hier_config.utils import load_hconfig_v2_tags

v3_tags = load_hconfig_v2_tags([
    {
        "lineage": [{"startswith": ["ip name-server", "ntp"]}],
        "add_tags": "ntp"
    }
])

print(v3_tags)
```

## Conclusion

I really like this modernized update to Hier Config. It has come a long way in the past decade. I would invite the user base to help expand and build out the driver and participate in their development lifecycle. For more information, you can view the code on [https://github.com/netdevops/hier_config](Github) and you can view the documentation on [https://hier-config.readthedocs.io/en/latest/](ReadTheDocs)

In future blogs about Hier Config, I will talk about:

* **Config and Interface Views** that are built into Hier Config.
* **Custom Workflows** for instances that don't adhere to negation and idempotent workflows.
* **Experimentation with AI** to farm out some of Hier Config's remediation functions. 
