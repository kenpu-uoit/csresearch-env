#!/bin/bash

#
# Trust all sudoers
#
echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

#
# Create the users in /etc/users.*
#
/bin/createusers
service ssh start
sleep infinity
