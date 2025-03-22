import http.server
import requests
import logging

logging.basicConfig(filename='proxy.log', level=logging.INFO)

class Proxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.handle_request('GET')

    def do_POST(self):
        self.handle_request('POST')

    def handle_request(self, method):
        url = self.path[1:]
        if not url.startswith('http://'):
            url = 'http://' + url

        try:
            if method == 'GET':
                response = requests.get(url)
            elif method == 'POST':
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length)
                response = requests.post(url, data=body)

            logging.info(f'URL: {url}, Response Code: {response.status_code}')

            self.send_response(response.status_code)
            self.send_header('Content-type', response.headers['Content-Type'])
            self.end_headers()
            self.wfile.write(response.content)

        except requests.exceptions.RequestException as e:
            logging.error(f'Error: {e}')
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'Internal Server Error')

def run(server_class=http.server.HTTPServer, handler_class=Proxy, port=8888):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    proxy_url = f'http://localhost:{port}'
    print(f'Запуск прокси-сервера по адресу: {proxy_url}')
    logging.info(f'Starting proxy server at: {proxy_url}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()