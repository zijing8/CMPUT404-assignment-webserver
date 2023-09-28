#  coding: utf-8 
import socketserver
import os

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
            requestList = (self.data).split(' ')

        # tests
        # self.request.sendall(requestList[0].encode('utf-8'))
        # self.request.sendall("\n".encode('utf-8'))
        # self.request.sendall(requestList[1].encode('utf-8'))

        # get the method and the requested file
        method = requestList[0]
        requestedFile = requestList[1]
        requestedFile = requestedFile.lstrip('/')

        # check if the request if GET, if not set header and response to 405 Method Not Allowed
        if method != 'GET':
            header = 'HTTP/1.1 405 Method Not Allowed\r\n'
            file = open('www/405.html', 'rb')
            response = file.read().decode('utf-8')
            file.close()
            finalResponse = header
            finalResponse += response
            self.request.sendall(finalResponse.encode('utf-8'))
            return
        
        # check for redirect
        if requestedFile == 'deep':
            header = 'HTTP/1.1 301 Moved Permanently\r\n'
            response = f'Location: deep/\r\n'
            finalResponse = header
            finalResponse += response
            self.request.sendall(finalResponse.encode('utf-8'))
            return
        

        # check if path exist
        if not os.path.exists(f'www/{requestedFile}'):
            header = 'HTTP/1.1 404 Not Found\r\n'
            file = open('www/404.html', 'rb')
            response = file.read().decode('utf-8')
            file.close()
            finalResponse = header
            finalResponse += response
            self.request.sendall(finalResponse.encode('utf-8'))
            return

        # load index.html as default, and check the requested file path
        if requestedFile == '':
            requestedFile = 'index.html'
        elif requestedFile == 'deep/':
            requestedFile = 'deep/index.html'
        elif requestedFile.endswith('/'):
            requestedFile = requestedFile + 'index.html'



        # check if file can be found read it if it can
        try:
            file = open(f'www/{requestedFile}', 'rb')
            response = file.read().decode('utf-8')
            file.close()

            # set header to 200 if its a valid file
            header = 'HTTP/1.1 200 OK\r\n'

            # check the mime type of the file
            if (requestedFile.endswith('.css')):
                mimetype = 'text/css'
            else:
                mimetype = 'text/html'

            header += 'Content-Type: '+ str(mimetype)+ '\r\n'

        # if file not found set header and response to 404 not found
        except Exception as e:
            header = 'HTTP/1.1 404 Not Found\r\n'
            file = open('www/404.html', 'rb')
            response = file.read().decode('utf-8')
            file.close()


        # send the final page
        finalResponse = header
        finalResponse += response
        self.request.sendall(finalResponse.encode('utf-8'))

        return
            



        


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
