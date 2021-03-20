# UDP_Carrier

Project 4: Simple Transport Protocol

3700 send
First, we have to keep track of all of the packets sent in an array
In send-next-packet add the packet to the list

Need a method to check if the packet timed out(delayed packet)
Keep track of the RTO Estimation or use a static value to check if the packet timed out
If the packet timed out Retransmit it

Might need to keep track of the RTT(saw in piazza)

Method for packet retransmission if the packets are delayed
Call after we know a packet is delayed
I think we can either use RTO, RTT, or a static value and I guess change the threshold for the packet timeout

I guess we can keep track of the time using a variable and update it every time we send a packet.  We can check the difference in the current time and the time we sent the packet and compare it to the time it should be under, idk what value it should be tho, maybe RTT?
Then we retransmit the packet.

3700 recv

First, we have to keep track of all of the packets using a list of packets received

Print out the received data to when end of file is sent.
Use a for loop to go through all of the packets
sys.stdout.write() the data in the packet

Check to see if the packets are in order by using information from decoded[‘sequence’’] in the while loop listening for packets at the end of the file
Have a variable that keeps track of the sequence
Check if the sequence is in the right order(compare decoded[‘sequence’] to the variable or to the packets in the array)
If it is in the right order,  append it to packets
Then update the sequence variable
Option 1: The sequence given in decoded starts at 0 and is incremented up by the length of data,
If we set a variable to 0 and then add the length of decoded[‘data’] after we can check it against the give sequence we can see if it is in the right order and then we append it to packets.  If it isn’t in the right order we might have to hold on to it so we can organize the packets by increasing sequence order when we reach the end of file.
Also, we can add a check to make sure the given sequence isn’t in packets to avoid duplicates.
Option 2: Actually, we might just be able to just do the one check for duplicates based on the sequence number, add any packet if it isn’t already in the list and then sort the list at the end of file by increasing order.
