
import eventlet
import requests
import json

from st2reactor.sensor.base import Sensor

class ServiceSensor(Sensor):
    def __init__(self, sensor_service, config):
        super(ServiceSensor, self).__init__(sensor_service=sensor_service, config=config)
        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)
        self._stop = False

    def setup(self):
        pass

    def run(self):
        self._host="sj1010010247137.corp.adobe.com"
        self._uri="/_cluster/health?pretty"
        self._port="9200"
        self._url="http://"+self._host+":"+self._port+self._uri
        while not self._stop:
            try:
                self._logger.debug("Sensor dispatching trigger")
                http_resp=json.loads(requests.get(self._url).text)
                payload = {"service": http_resp['cluster_name'], "status": http_resp['status']}
            except Exception as e:
                payload = {"service": "elasticsearch", "status": "Not Available"}
            self.sensor_service.dispatch(trigger="service_check.service_event", payload=payload)
            eventlet.sleep(30)

    def cleanup(self):
        self._stop = True

    # Methods required for programmable sensors.
    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass
