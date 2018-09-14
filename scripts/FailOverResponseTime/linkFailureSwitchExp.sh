#!/bin/sh
interfaceName1="A2"
interfaceName2="A4"
interval=20
for i in {1..2}
do
./procurve-commander.sh nebula 10.10.0.7 "config","interface $interfaceName1 disable","exit";
sleep $interval
./procurve-commander.sh nebula 10.10.0.7 "config","interface $interfaceName1 enable","exit";
sleep 3
./procurve-commander.sh nebula 10.10.0.7 "config","interface $interfaceName2 disable","exit";
sleep $interval
./procurve-commander.sh nebula 10.10.0.7 "config","interface $interfaceName2 enable","exit" ;
sleep 3
echo $i
done
