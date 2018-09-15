#!/bin/sh
interfaceName1="A2"
interfaceName2="A4"
interval=2
simTime=100
for j in {2..51..8}
do
	interval=j
	ssh nebula106 "iperf3 -s -p 8080" &
	sleep 3
	ssh nebula105 "iperf3 -c 10.6.0.6 -t $simTime  -i 1 -p 8080 > client-$interval.log" &
	numLoops=($simTime/(2 * $interval)) + 1
	echo $numLoops
	for i in {1..$numLoops}
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
	sleep 2 
	ssh nebula106 "pkill iperf3"
	ssh nebula105 "pkill iperf3"
done
