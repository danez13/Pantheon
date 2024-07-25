import socket
import logging

logging.basicConfig(filename="LoggingData/pantheon_main.log",
                    format="%(asctime)s - %(levelname)s: %(message)s",
                    filemode="w")

logger = logging.getLogger()

logger.setLevel(logging.NOTSET)

def scanDomain(parts,limit:int,fileStoreBool:bool,openPortBool:bool):
        target=socket.gethostbyname(parts.hostname)
        
        # if fileStoreBool is True: open the file
        if fileStoreBool:
                logger.debug(f"opening [Files/{parts.hostname}/portScan.txt] for writing")
                outputfile = open(f"Files/{parts.hostname}/portScan.txt","w")

        # will scan ports between 1 to 65,535
        for port in range(1,limit):
                logger.debug("creating socket")
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)
                # returns an error indicator
                logger.debug(f"connecting to {parts.hostname}/{target}")
                result = s.connect_ex((target,port))
                # if openPortBool is True: print or write only open ports
                if openPortBool:
                        if result == 0:
                                # if fileStoreBool is True write to file
                                if fileStoreBool:
                                        logger.debug(f"writing to {outputfile}")
                                        outputfile.write(f"port {port} is open\n")
                                else:
                                        print(f"Port {port} is open")
                else:
                        if result ==0:
                                # if fileStoreBool is true: write to file
                                if fileStoreBool:
                                        logger.debug(f"writing to {outputfile}")
                                        outputfile.write(f"port {port} is open\n")
                                else:
                                        print(f"Port {port} is open")
                        else:
                                # if fileStoreBool is True write to File
                                if fileStoreBool:
                                        logger.debug(f"writing to {outputfile}")
                                        outputfile.write(f"port {port} is closed\n")
                                else:
                                        print(f"port {port} is closed")
        s.close()

def scanIP(target:str,limit:int,fileStoreBool:bool,openPortBool:bool):
        # if fileStoreBool is True: open the file
        if fileStoreBool:
                logger.debug(f"opening [Files/{target}/portScan.txt] for writing")
                outputfile = open(f"Files/{target}/portScan.txt","w")

        # will scan ports between 1 to 65,535
        for port in range(1,limit):
                logger.debug("creating socket")
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)
                
                # returns an error indicator
                logger.debug(f"connecting to {target}")
                result = s.connect_ex((target,port))
                
                # if openPortBool is True: print or write only open ports
                if openPortBool:
                        if result == 0:
                                # if fileStoreBool is True write to file
                                if fileStoreBool:
                                        logger.debug(f"writing to {outputfile}")
                                        outputfile.write(f"port {port} is open\n")
                                else:
                                        print(f"Port {port} is open")
                else:
                        if result ==0:
                                # if fileStoreBool is true: write to file
                                if fileStoreBool:
                                        logger.debug(f"writing to {outputfile}")
                                        outputfile.write(f"port {port} is open\n")
                                else:
                                        print(f"Port {port} is open")
                        else:
                                # if fileStoreBool is True write to File
                                if fileStoreBool:
                                        logger.debug(f"writing to {outputfile}")
                                        outputfile.write(f"port {port} is closed\n")
                                else:
                                        print(f"port {port} is closed")
        s.close()