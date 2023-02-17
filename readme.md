TCP Server

This is a simple TCP server built with Python that can handle up to 5 clients. Clients are assigned ranks based on the order they connect to the server, with the first client being assigned the highest rank.

Clients can send commands to the server, which distributes them among the clients based on their ranks. Only low-rank clients can execute commands from high-rank clients. If a client disconnects, the server adjusts the ranks of the remaining clients to ensure that there are no gaps in the ranks.
Getting Started

To use this TCP server, you'll need Python 3 installed on your system. You can download Python 3 from the official website.

Once you have Python 3 installed, you can run the server by executing the following command in your terminal:

python server.py

This will start the server on the default host (localhost) and port (8000). You can customize the host and port by modifying the HOST and PORT constants in the server.py file.
Usage

Once the server is running, clients can connect to it by using any TCP client, such as telnet or netcat. For example, you can connect to the server using telnet by executing the following command in your terminal:

yaml

telnet localhost 8000

Once connected, you can send commands to the server. The commands should be formatted as a string of the following format:

ruby

<rank>:<command>

Where <rank> is the rank of the client sending the command, and <command> is the command to be executed. For example, if the client has rank 1 and wants to execute the command print("Hello, world!"), they would send the following command to the server:

python

1:print("Hello, world!")

If a low-rank client receives a command from a high-rank client, they can execute it by sending the following command to the server:

bash

execute:<command>

Where <command> is the command to be executed. For example, if a client with rank 2 wants to execute the command print("Hello, world!") sent by a client with rank 1, they would send the following command to the server:

lua

execute:print("Hello, world!")

If a high-rank client receives a command from a low-rank client, the command is rejected and added to a list of rejected commands. The rejected commands can be retrieved by sending the following command to the server:

rejected

If a client disconnects, the server adjusts the ranks of the remaining clients to ensure that there are no gaps in the ranks.

Dependencies

The server script uses Python's built-in socket and threading modules, so no external dependencies are required.
Credits

This TCP server was created by [your name] as a programming exercise. Feel free to use it or modify it for your own purposes.

License

This TCP server is licensed under the MIT License. Feel free to use, modify, and distribute it as you wish.