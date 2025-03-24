# tremote
Simple, fast (at least attempting to be) remote control system written in Python and C.

## Contents
**m_serv.py** = the main server - the middleman in the whole operation

**l_serv.py** = the local server - a server which can be assigned to a client

**l_client.py** = the client - the file meant to be run on the other computer, gets commands from the local server and runs them.

**l_wrapper.py** = a GUI based application used to manage one or more local server instances. (UNSTABLE)

**l_client_silent.c** = the local server, but hidden, running in the background (Windows only)

## Tutorial
First, you need to start the main server. Then run a local server which will automatically connect to the main server to register itself in the queue. Then run the local client on the other computer, it will automatically connect and register with the main server, then recieve a local server's connection data and connect to it. It needs to be done in this exact order. 
The local server can be run from the GUI.
