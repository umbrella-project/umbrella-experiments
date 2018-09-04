#!/bin/sh
interfaceName1="spine401-eth1"
interfaceName2="spine402-eth1"
interval=10
for i in {1..5}
do
    echo $i
    sudo ifconfig $interfaceName1  down
    sleep $interval
    sudo ifconfig $interfaceName1  up
    sudo ifconfig $interfaceName2 down
    sleep $interval
    sudo ifconfig $interfaceName2 up

done
