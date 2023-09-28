#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# Copyright 2023 Zijing Lu
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).decode('utf-8').strip()
        print ("Got a request of: %s\n" % self.data)

        # spilt self.data into list of strings
        if self.data != '':
            requestList = self.data.split(' ')
        print(requestList)

        # tests
        self.request.sendall(requestList[0].encode('utf-8'))
        self.request.sendall("\n".encode('utf-8'))
        self.request.sendall(requestList[1].encode('utf-8'))

        # get the method and the requested file
        method = requestList[0]
        requestedFile = requestList[1]
        requestedFile = requestedFile.lstrip('/')

        # load index.html as default
        if(requestedFile == '/'):
            requestedFile = 'index.html'

        # check if the request if GET
        if method == 'GET':
            header = 'HTTP/1.1 405 Not Found\r\n'
            response = '<html><body><center><h3>Error 405: Not Found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
            finalResponse = header.encode('utf-8')
            finalResponse += response
            self.request.sendall(finalResponse)
            return

        # check if file can be found
        try:
            file = open(f'www/{requestedFile}', 'rb')
            response = file.read
            file.close()
        except:
            pass

        


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
