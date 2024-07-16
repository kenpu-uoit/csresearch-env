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

if [[ -f /etc/setup.sh ]]
then
	/bin/bash setup.sh
fi

sleep infinity
