#Create a simulator object
set ns [new Simulator]

# Define colour scheme for different flow at the beginning after the
# simulator object has been created. Notes: The numeric number will
# be the flow ID for the traffic flows in the simulation later.

$ns color 1 Red
$ns color 2 green
$ns color 3 Yellow
$ns color 4 Black

#Open the nam trace file
set nf [open out2.nam w]
$ns namtrace-all $nf

#Open trace file
set f0 [open throughput.tr w]
set f1 [open queuesize.tr w]

#Define a 'finish' procedure
proc finish {} {
   global ns nf f0 f1

   $ns flush-trace

   #Close the output files
   close $nf
   close $f0
   close $f1

   #Execute nam on the trace file
   exec nam out2.nam &

   #Call Xgraph to display the results
   exec xgraph throughput.tr -t "ThroughPut" -geometry 800x400 &
   exec xgraph queuesize.tr -t "QueueSize" -geometry 800x400 &

   exit 0
}

#Configuring the routing protocol used by the nodes
set r1 [$ns node]
set r2 [$ns node]

$r1 label r1
$r2 label r2

for {set i 1} {$i < 9} {incr i} {
    set n($i) [$ns node]
}

for {set i 1} {$i < 9} {incr i} {
    $n($i) label node_$i
}

#Create links between the nodes
$ns duplex-link $n(1) $r1 30Mb 1ms DropTail
$ns duplex-link $n(2) $r1 75Mb 0.4ms DropTail
$ns duplex-link $n(3) $r1 40Mb 1.2ms DropTail 
$ns duplex-link $n(4) $r1 65Mb 1.6ms DropTail

$ns duplex-link $r2 $n(5) 55Mb 1.8ms DropTail
$ns duplex-link $r2 $n(6) 70Mb 0.5ms DropTail
$ns duplex-link $r2 $n(7) 80Mb 2.5ms DropTail
$ns duplex-link $r2 $n(8) 95Mb 2.9ms DropTail

$ns duplex-link $r1 $r2 75Mb 3.1ms RED

$ns queue-limit $r1 $r2 30

# You may orient the node's position, you will be able to see the
# effect when you run the NAM visualizer
#$ns duplex-link-op $n1 $r1 orient 290deg
#$ns duplex-link-op $n2 $r1 orient 350deg
#$ns duplex-link-op $n3 $r1 orient 50deg
#$ns duplex-link-op $n4 $r1 orient 110deg

#$ns duplex-link-op $n5 $r2 orient 290deg
#$ns duplex-link-op $n6 $r2 orient 230deg
#$ns duplex-link-op $n7 $r2 orient 170deg
#$ns duplex-link-op $n8 $r2 orient 110deg

$ns duplex-link-op $r1 $r2 orient 0deg

#Monitor the queue for the link from r1 to r2.
$ns duplex-link-op $r1 $r2 queuePos 0.5

#Create a queue monitor object to monitor internal queue state between node r1 and
#node r2
set qmon [$ns monitor-queue $r1 $r2 [open queue.tmp w] 0.01]

#Initialize old_bdeparture to zero
set old_bdeparture 0 

proc record {} {
    #Global variables needed to be accessed in this procedure
    global ns old_bdeparture f0 f1 qmon 
    
    #Queue monitor objects to be accessed in this procedure
    $qmon instvar bdepartures_
    
    #Set the time after which the procedure should be called again
    set time 0.01
    
    #Get the current time
    set now [$ns now]
    $qmon instvar size_ pkts_ barrivals_ bdepartures_ parrivals_ pdepartures_ bdrops_ pdrops_
    
    puts $f1 "$now  [$qmon set size_]"
    #Calculate throughput (in Mbps) and write it to the files
    puts $f0 "$now [expr ($bdepartures_-$old_bdeparture)*8/$time]"
    
    #Set old_bdeparture to new value
    set old_bdeparture $bdepartures_
    
    #Re-schedule the procedure
    $ns at [expr $now+$time] "record"
} 

for {set i 1} {$i < 5} {incr i} {
    set tcp($i) [new Agent/TCP/Newreno]
    $tcp($i) set class_ $i
    $ns attach-agent $n($i) $tcp($i)
    set sink($i) [new Agent/TCPSink] 
    set j [expr $i+4]
    $ns attach-agent $n($j) $sink($i)
    $ns connect $tcp($i) $sink($i)
    #$tcp1 set fid_ 1

    set ftp($i) [new Application/FTP]
    $ftp($i) set packetSize_ 1000
    #$ftp set interval_ 0.005
    $ftp($i) attach-agent $tcp($i) 
    #$ftp1 set type_ FTP 

}

#Schedule procedure "record" to get throughput
$ns at 0.0 "record"

#Schedule events for the CBR traffic
$ns at 0.0 "$ftp(1) start"
$ns at 0.0 "$ftp(2) start"
$ns at 0.0 "$ftp(3) start"
$ns at 0.0 "$ftp(4) start"
#$ns at 10.0 "$ftp1 stop"
#$ns at 10.0 "$ftp2 stop"
#$ns at 10.0 "$ftp3 stop"
#$ns at 10.0 "$ftp4 stop"

#Call the finish procedure after 10 seconds of simulation time
$ns at 50.0 "finish"

#Run the simulation
$ns run


