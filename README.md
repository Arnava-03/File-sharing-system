File Sharing System

**Description:**
The File Sharing System is a distributed application designed to facilitate file management, resource allocation, and collaboration in networked environments. It allows clients to upload, download, and share files securely over the network while managing resource allocation to prevent conflicts and ensure efficient utilization of resources.

**Features:**
File Operations: Clients can perform file-related operations such as listing files in a directory, uploading files to the server, and downloading files from the server.
Resource Allocation: Clients can request resources from the server to perform specific tasks and release previously allocated resources back to the server.
Process Synchronization: Implements process synchronization algorithms to handle critical sections for concurrent access to shared resources, ensuring mutual exclusion and preventing race conditions.
Real-time Communication: Facilitates real-time communication between clients and the server, enabling seamless interaction and data exchange.

**Usage:**
Clone the repository to your local machine.
Run the server script (server.py) on a host machine.
Run the client script (client.py) on client machines to connect to the server.
Follow the on-screen prompts on the client to perform file operations and resource requests. (6 options provided for file management and resource requesting/releasing)

Requirements:

Python v3 installed on the system
TCP/IP sockets - sockets library for Python
