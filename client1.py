import socket
import pickle

class FileSharingClient:
    def __init__(self, host, port, client_id):
        self.host = host
        self.port = port
        self.client_id = client_id        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

    def connect_to_server(self):
        self.client_socket.connect((self.host, self.port))
        print("Connected to server {}:{}".format(self.host, self.port))

    def list_files(self, directory):
        self.client_socket.send(pickle.dumps(('LIST', directory)))
        files = pickle.loads(self.client_socket.recv(1024))
        return files

    def upload_file(self, filename, file_data):
        self.client_socket.send(pickle.dumps(('UPLOAD', (filename, file_data))))
        response = pickle.loads(self.client_socket.recv(1024))
        return response

    def download_file(self, filename):
        self.client_socket.send(pickle.dumps(('DOWNLOAD', filename)))
        file_data = pickle.loads(self.client_socket.recv(1024))
        return file_data

    def request_resources(self, request_resources):
        self.client_socket.send(pickle.dumps(('REQUEST', (self.client_id, request_resources))))
        response = self.client_socket.recv(1024)
        if response:
            print("Server response:", pickle.loads(response))
        else:
            print("No response from server.")

    def release_resources(self, release_resources):
        self.client_socket.send(pickle.dumps(('RELEASE', (self.client_id, release_resources))))
        response = self.client_socket.recv(1024)
        if response:
            print("Server response:", pickle.loads(response))
        else:
            print("No response from server.")

if __name__ == "__main__":
    client = FileSharingClient("localhost", 9999, 'client1')
    
    print('Welcome Client-1. What would you like to do?')
    print('Your options : \n1 - List files in directory \n2 - Upload text file \n3 - Download text file\n4 - Request resources \n5 - Release resources \n6 - EXIT')
    
    while(True):
        opt=int(input("Input your option (1-6): "))

        match opt:
            case 1:
                # Example usage: list files
                files = client.list_files('.')
                print("Files in current directory:", files)
            case 2:
                # Example usage: upload file
                # with open('example.txt', 'rb') as f:
                #     file_data = f.read()
                # response = client.upload_file('example.txt', file_data)
                # print("Server response:", response)
                file = str(input("Specify file to be uploaded - "))
                with open(file, 'rb') as f:
                    file_data = f.read()
                response = client.upload_file(file, file_data)
                print("Server response:", response)

            case 3:
                # Example usage: download file
                # downloaded_data = client.download_file('example.txt')
                # with open('downloaded_example.txt', 'wb') as f:
                #     f.write(downloaded_data)
                # print("File downloaded successfully!")
                file = str(input('Which file to be downloaded? '))
                downloaded_data = client.download_file(file)
                with open('downloaded_{}'.format(file), 'wb') as f:
                    f.write(downloaded_data)
                print("File downloaded successfully!")
            case 4:
                # Example usage: request resources
                request_resources = {'A': 1, 'B': 1, 'C': 1}
                response = client.request_resources(request_resources)
            case 5:
                # Example usage: release resources
                release_resources = {'A': 1, 'B': 1, 'C': 1}
                response = client.release_resources(release_resources)
            case 6 :
                break