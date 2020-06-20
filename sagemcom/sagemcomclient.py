from sagemcom.sagemcombaseclient import SagemcomBaseClient
import re


class Sagemcomclient(SagemcomBaseClient):
    def get_values_tree(self, tree: str) -> dict:
        params = {
            "xpath": tree,
            "options": {
                "capability-flags": {
                    "interface": True
                }
            }
        }
        return self._request(self._createAction('getValue', params))

    def get_hosts(self) -> list:
        response = self.get_values_tree('Device/Hosts/Hosts')
        hosts = []
        re_interface = re.compile(r'\[(RADIO\dG\d?|PHY\d)\]$')
        for device in response['parameters']['value']:
            if device['Active']:
                hosts.append({
                    'ipAddress': device['IPAddress'],
                    'macAddress': device['PhysAddress'],
                    'hostName': device['HostName'],
                    'friendlyName': device['UserFriendlyName'],
                    'static': True if device['AddressSource'] == 'STATIC' else False,
                    'interfaceType': device['InterfaceType'],
                    'interfacePort': re_interface.findall(device['Layer1Interface'])[0],
                    'deviceType': device['DetectedDeviceType']
                })
        return hosts
