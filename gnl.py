#!/usr/env python

import requests
import logging

import application

"""
Example original query:

curl "https://language.googleapis.com/v1/documents:analyzeEntitySentiment?key=${API_KEY}" -s 
-X POST -H "Content-Type: application/json" --data-binary @sentiment.json

Example request.json
 "{
  'document':{
    'type':'PLAIN_TEXT',
    'content':'Google, headquartered in Mountain View, unveiled the new Android
    phone at the Consumer Electronic Show.  Sundar Pichai said in his keynote
    that users love their new Android phones.'
  }
}"
"""

sample_text = """Google, headquartered in Mountain View, unveiled the new Android
    phone at the Consumer Electronic Show.  Sundar Pichai said in his keynote
    that users love their new Android phones."""


class Client(object):
    def __init__(self, url=application.gnl_url, token=application.gnl_token):
        self._url = url
        self._params = {'key': token}

    def post(self, uri, data):
        response = requests.post(url=self._url + uri, params=self._params, json=data, allow_redirects=False)
        if not response.ok:
            raise ValueError("Response: {content}".format(content=response.content))
        return response.json()


class Analyzer(object):
    def analyze(self, text):
        """interface"""
        pass


class EntityAnalyzer(Analyzer):
    def __init__(self):
        self._client = Client()
        self._uri = '/documents:analyzeEntities'
        self._result = None

    def analyze(self, text):
        data = {
            'document': {
                'type': 'PLAIN_TEXT',
                'content': text,
            }
        }
        logging.info("Sending Payload: %s", data)
        logging.info("Text is: %s", text)
        logging.info("Text type is: %s", type(text))

        self._result = self._client.post(self._uri, data)

        logging.info("Response is: %s", self._result)

        return self

    @property
    def result(self):
        return self._result

    def ordered_entities(self):
        entities = self._result.get('entities')
        entities.sort(key=lambda x: x.get('salience'), reverse=True)
        return [entity.get("name") for entity in entities]


class DocumentClassify(Analyzer):
    def __init__(self):
        self._client = Client()
        self._uri = '/documents:classifyText'
        self._result = None

    @property
    def result(self):
        return self._result

    def analyze(self, text):
        data = {
            'document': {
                'type': 'PLAIN_TEXT',
                'content': text,
            }
        }
        self._result = self._client.post(self._uri, data)
        return self

