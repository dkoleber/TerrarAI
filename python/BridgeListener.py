import http.client
import threading
import time

UPDATE_PERIOD = 1 #in seconds


class Listener(threading.Thread):

    def __init__(self, min_update_period):
        super().__init__()
        self.minimum_update_period = min_update_period


        self.is_running = True
    def run(self):
        url = 'localhost:8001'
        path = '/GetState'

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
            duration = max(self.minimum_update_period - elapsed, 0)
            time.sleep(duration)

    def stop(self):
        self.is_running = False

    def subscribe_to_player_state(self):
        url = 'localhost:8001'
        path = '/SubscribeToPlayerState'
        connection = http.client.HTTPConnection(url)

        connection.request('GET', path)
        response = connection.getresponse()
        if response.status == 200:
            data = response.read()
            print('received data: ' + str(data))

    def unsubscribe_from_player_state(self):
        url = 'localhost:8001'
        path = '/UnsubscribeFromPlayerState'
        connection = http.client.HTTPConnection(url)

        connection.request('GET', path)
        response = connection.getresponse()
        if response.status == 200:
            data = response.read()
            print('received data: ' + str(data))

    def unsubscribe_from_all(self):
        url = 'localhost:8001'
        path = '/UnsubscribeFromAll'
        connection = http.client.HTTPConnection(url)

        connection.request('GET', path)
        response = connection.getresponse()
        if response.status == 200:
            data = response.read()
            print('received data: ' + str(data))

class WorldConfigurer:
    pass




if __name__=='__main__':
    listener = Listener(UPDATE_PERIOD)
    listener.start()
    listener.unsubscribe_from_all()
    listener.subscribe_to_player_state()
