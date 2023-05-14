---
layout: post
title: 'Extracting Specific Key-Value Pairs from a List of Dictionaries in Ansible'
date: '2023-05-13'
author: jtdub
tags:
- packetgeek.net 
- ansible 
- python 
---
Have you ever encountered a situation in Ansible where you had a list of dictionaries, each representing an item with multiple attributes, and you needed to extract only specific key-value pairs while keeping the rest of the data hidden? Such as wanting to specific data from a list of dictionaries that contains secrets that you did not want logged in Ansible stdout or stderr, but also did not to use `no_log`, making troubleshooting difficult? This can be a common requirement when working with sensitive information or when you want to streamline the data passed to a task. In this article, we'll explore how to solve this problem in Ansible, leveraging powerful filters and techniques to extract specific key-value pairs from a list of dictionaries.

Let's dive into an example playbook that demonstrates the solution. Suppose we have a list called `my_list` with dictionaries representing individuals, and we want to extract the `name` and `age` key-value pairs for each person while keeping the other attributes hidden. Here's how we can achieve that:

```yaml
- name: Extract specific key-value pair from a list of dictionaries
  hosts: localhost
  gather_facts: false
  vars:
    my_list:
      - name: John
        age: 25
        country: USA
      - name: Alice
        age: 30
        country: UK
      - name: Bob
        age: 35
        country: Australia
  tasks:
    - name: Extract name-age pair from each item
      debug:
        msg: "{{ my_list | map(attribute='name') | zip(my_list | map(attribute='age')) | list }}"

```

In this example, we define the `my_list` variable containing a list of dictionaries. The `map` filter is used to extract the `name` value from each dictionary, while the `zip` filter combines it with the `age` value extracted from the same list. Finally, the `list` filter is used to convert the result into a list.

When running this playbook, the output will only include the extracted name-age pairs, while the other data in the dictionaries remains hidden:

```shell
TASK [Extract name-age pair from each item] *************************************
ok: [localhost] => {
    "msg": [
        [
            "John",
            25
        ],
        [
            "Alice",
            30
        ],
        [
            "Bob",
            35
        ]
    ]
}

```

By following this approach, you can easily extract specific key-value pairs from a list of dictionaries in Ansible without exposing the remaining data. This provides a clean and secure way to pass only the necessary information to tasks, ensuring privacy and efficiency in your automation workflows.
