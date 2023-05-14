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

```liquid
{% raw %}
- name: Extract name and age using json_query 
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
        msg: "{{ my_list | json_query('[].{name: name, age: age}') }}"
{% endraw %}
```
In this example, we use the `json_query` filter with the JMESPath query `[].{name: name, age: age}`. This query instructs Ansible to iterate over each element in the `my_list` variable and create a new dictionary with the keys `name` and `age`, using the corresponding values from each dictionary in the original list.

When running this playbook, the output will only include the extracted name-age pairs, while the other data in the dictionaries remains hidden:

```shell
TASK [Extract name and age using json_query] ***********************************
ok: [localhost] => {
    "msg": [
        {
            "age": 25,
            "name": "John"
        },
        {
            "age": 30,
            "name": "Alice"
        },
        {
            "age": 35,
            "name": "Bob"
        }
    ]
}
```
By following this approach, you can easily extract specific key-value pairs from a list of dictionaries in Ansible without exposing the remaining data. This provides a clean and secure way to pass only the necessary information to tasks, ensuring privacy and efficiency in your automation workflows.
