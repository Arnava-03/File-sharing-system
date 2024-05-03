import socket
import threading
import os
import pickle

class FileSharingServer:
    def __init__(self, host, port, num_resources=3):
        self.host = host
        self.port = port
        self.num_resources = num_resources
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.lock = threading.Lock()
        self.turn = 0
        self.want = [False] * 2  # One for each client
        self.available_resources = {'A': 10, 'B': 10, 'C': 10}  # Initial available resources
        # self.max_claim = {}  # Dictionary to store maximum claim of each client
        self.max_claim = {'client1': {'A': 5, 'B': 5, 'C': 5},
                          'client2': {'A': 5, 'B': 5, 'C': 5}}
        # self.allocated = {}  # Dictionary to store currently allocated resources to each client
        self.allocated = {'client1': {'A': 0, 'B': 0, 'C': 0},
                          'client2': {'A': 0, 'B': 0, 'C': 0}}
        self.initialize_server()

    def initialize_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Server started and listening on {}:{}".format(self.host, self.port))

    def handle_client(self, client_socket, addr):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    print("Connection closed by {}:{}".format(addr[0], addr[1]))
                    break
                command, params = pickle.loads(data)
                if command == 'LIST':
                    with self.lock:
                        files = os.listdir(params)
                    client_socket.send(pickle.dumps(files))
                elif command == 'UPLOAD':
                    filename, file_data = params
                    with open(filename, 'wb') as f:
                        f.write(file_data)
                    client_socket.send(pickle.dumps("File uploaded successfully!"))
                elif command == 'DOWNLOAD':
                    filename = params
                    with open(filename, 'rb') as f:
                        file_data = f.read()
                    client_socket.send(pickle.dumps(file_data))
                elif command == 'REQUEST':
                    client_id, request_resources = params
                    with self.lock:
                        if self.check_safe(client_id, request_resources):
                            self.allocate_resources(client_id, request_resources)
                            response = "Resource allocation successful!"
                        else:
                            response = "Resource allocation failed. Unsafe state detected!"
                    client_socket.send(pickle.dumps(response))
                elif command == 'RELEASE':
                    client_id, release_resources = params
                    with self.lock:
                        self.release_resources(client_id, release_resources)
                        response = "Resources released successfully!"
                    client_socket.send(pickle.dumps(response))
            except Exception as e:
                print("Error occurred:", e)
                break
        client_socket.close()

    def check_safe(self, client_id, request_resources):
        temp_avail = self.available_resources.copy()
        temp_alloc = self.allocated.copy()
        temp_max = self.max_claim.copy()

        for resource, amount in request_resources.items():
            if amount > temp_avail[resource]:
                return False
            temp_avail[resource] -= amount
            temp_alloc.setdefault(client_id, {}).setdefault(resource, 0)
            temp_alloc[client_id][resource] += amount

        work = list(temp_avail.values())
        finish = [False] * len(temp_max)

        while True:
            safe_found = False
            for i, (client, max_claim) in enumerate(temp_max.items()):
                if not finish[i]:
                    # if all(temp_alloc.get(client, {}).get(resource, 0) <= work[j] for resource in range(self.num_resources) for j in range(len(work))):
                    #     for resource, amount in temp_alloc.get(client, {}).items():
                    #         work[resource] += amount
                    #     finish[i] = True
                    #     safe_found = True
                    if all(temp_alloc[client][resource] <= work[j] for resource in self.available_resources for j in range(len(work))):
                            # Add allocated resources back to work
                            for resource, amount in temp_alloc[client].items():
                                work[list(temp_avail.keys()).index(resource)] += amount
                            finish[i] = True
                            safe_found = True
            if not safe_found:
                break

        return all(finish)

    def allocate_resources(self, client_id, request_resources):
        for resource, amount in request_resources.items():
            self.available_resources[resource] -= amount
            # self.allocated.setdefault(client_id, {}).setdefault(resource, 0)
            self.allocated[client_id][resource] += amount

    def release_resources(self, client_id, release_resources):
        for resource, amount in release_resources.items():
            self.available_resources[resource] += amount
            if client_id in self.allocated and resource in self.allocated[client_id]:
                self.allocated[client_id][resource] -= amount

    def request_cs(self, pid):
        other = 1 - pid
        self.want[pid] = True
        self.turn = pid
        while self.want[other] and self.turn == pid:
            pass

    def release_cs(self, pid):
        self.want[pid] = False

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print("Connection established from {}:{}".format(addr[0], addr[1]))
            # pid = len(self.clients)
            # self.clients[pid] = client_socket
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            client_thread.start()

if __name__ == "__main__":
    # server = FileSharingServer("localhost", 9999, 3)  # Number of resources = 3
    server = FileSharingServer("172.31.4.87", 9999, 3)  # Number of resources = 3
    server.start()
