import requests


class HttpHelper:
    @staticmethod
    def send_request(method, url, params=None, data=None, json=None, headers=None):
        complete_url = requests.Request(
            method, url, params=params).prepare().url
        response = requests.request(
            method, url, params=params, data=data, json=json, headers=headers)
        return response

    @staticmethod
    def get(url, params=None, headers=None):
        return HttpHelper.send_request('GET', url, params=params, headers=headers)

    @staticmethod
    def post(url, data=None, json=None, headers=None):
        return HttpHelper.send_request('POST', url, data=data, json=json, headers=headers)

    @staticmethod
    def put(url, data=None, json=None, headers=None):
        return HttpHelper.send_request('PUT', url, data=data, json=json, headers=headers)

    @staticmethod
    def delete(url, params=None, headers=None):
        return HttpHelper.send_request('DELETE', url, params=params, headers=headers)
