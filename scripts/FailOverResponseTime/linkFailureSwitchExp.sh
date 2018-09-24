#!/bin/sh
interfaceName1="A2"
interfaceName2="A4"
interval=20
simTime=100
switchIP=10.10.0.6
for j in {26..27..8}
do
	for k in {1..5}
	do
		interval=$j
		echo "interval-round:" $interval "," $k
		 
		ssh nebula106 "iperf3 -s -p 8080" &
		sleep 3
		ssh nebula105 "iperf3 -c 10.6.0.6 -t $simTime  -i 1 -p 8080 -P 30 > client-$interval-$k.log" &
		let "numLoops=(($simTime/(2 * ($interval) + 6)))"
		#echo "numLoops:" $numLoops 
		#echo $interval
		for i in $( eval echo {1..$numLoops} )
		do
			./procurve-commander.sh nebula 10.10.0.7 "config","interface $interfaceName1 disable","exit" > /dev/null;
			sleep $interval
			./procurve-commander.sh nebula 10.10.0.7 "config","interface $interfaceName1 enable","exit" > /dev/null;
			sleep 4
			./procurve-commander.sh nebula 10.10.0.7 "config","interface $interfaceName2 disable","exit" > /dev/null;
			sleep $interval
			./procurve-commander.sh nebula 10.10.0.7 "config","interface $interfaceName2 enable","exit" > /dev/null ;
			sleep 4
			echo "loops:" "$i"
		done
	
	
		ssh nebula105 "pkill iperf3"
		ssh nebula106 "pkill iperf3"
		sleep 2
       done
done
