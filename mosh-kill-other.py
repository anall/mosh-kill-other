#!/usr/bin/env python
import psutil, os, sys

def find_server():
    ps = psutil.Process(os.getpid())
    while ( ps != None ):
        if ( ps.name == "mosh-server" ):
            return ps
        ps = ps.parent
    return None

def get_mosh_processes():
    mosh_processes = filter( lambda x: x.name == "mosh-server", psutil.process_iter() )
    uid = os.getuid()
    
    return filter( lambda x: x.uids.effective == uid, mosh_processes )

def main():
    server = find_server()
    if ( server == None ):
        print("Cannot find parent mosh-server process.")
        exit(-1)
    
    print("You are mosh-server PID", server.pid)
    
    processes = get_mosh_processes()
    processes = list(filter( lambda x: x.pid != server.pid, get_mosh_processes() ))

    if ( len(processes) == 0 ):
        print("No other mosh-server processes")
        exit(0)

    print("Other mosh-server processes:", ", ".join(map( lambda x: str(x.pid), processes )))

    print("Hit Ctrl-C to cancel, or enter to kill these")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        print("")
        exit(-1)

    for proc in processes:
        print("Killing",proc.pid)
        proc.kill()

if __name__ == "__main__":
    main()
