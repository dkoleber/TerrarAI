import http.client
import threading
import time

UPDATE_PERIOD = 1 #in seconds


class Listener(threading.Thread):

    def __init__(self):
        super().__init__()
        self.is_running = True
    def run(self):
        url = 'localhost:8001'
        path = '/Echo'

        while(self.is_running):
            start_time = time.time()
            try:

                connection = http.client.HTTPConnection(url)

                connection.request('GET', path)
                response = connection.getresponse()
                if response.status == 200:
                    data = response.read()
                    print('received data: ' + str(data))
            except Exception as e:
                print('Failed: ' + str(e))

            end_time = time.time()
            elapsed = end_time - start_time
            duration = max(UPDATE_PERIOD - elapsed, 0)
            time.sleep(duration)

    def stop(self):
        self.is_running = False


if __name__=='__main__':
    listener = Listener()
    listener.start()