#!/usr/env python

import requests
import logging

import application

"""
Example original query:

curl "https://language.googleapis.com/v1/documents:analyzeEntitySentiment?key=${API_KEY}" -s 
-X POST -H "Content-Type: application/json" --data-binary @sentiment.json

Example request.json
{
  "config": {
      "encoding":"FLAC",
      "sample_rate": 16000,
      "language_code": "en-US"
  },
  "audio": {
      "uri":"gs://cloud-samples-tests/speech/brooklyn.flac"
  }
}
"""

sample_text = """Google, headquartered in Mountain View, unveiled the new Android
    phone at the Consumer Electronic Show.  Sundar Pichai said in his keynote
    that users love their new Android phones."""


class Client(object):
    def __init__(self, url=application.gs_url, token=application.token):
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


class SpeechAnalyzer(Analyzer):
    def __init__(self):
        self._client = Client()
        self._uri = '/speech:recognize'
        self._result = None

    def analyze(self, uri, language="en-US"):
        data = {
            "config": {
                "encoding": "FLAC",
                "sampleRateHertz": 48000,
                "languageCode": language,
                "enableWordTimeOffsets": "false"
            },
            "audio": {
                "uri": uri
            }
        }

        logging.info("Sending Payload: %s", data)

        self._result = self._client.post(self._uri, data)

        logging.info("Response is: %s", self._result)

        return self

    @property
    def result(self):
        return self._result

    @property
    def alternatives(self):
        """
        {
          "results": [
            {
              "alternatives": [
                {
                  "transcript": "I want to know what is foreclosure",
                  "confidence": 0.9682592
                }
              ]
            }
          ]
        }
        """
        return self._result.get('results')[0].get('alternatives')

    @property
    def best_fit(self):
        alternatives = self.alternatives
        alternatives.sort(key=lambda x: x.get('confidence'), reverse=True)
        alts = [alternative.get("transcript") for alternative in alternatives]
        return next(iter(alts), '')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    uri = "gs://heroic-calculus-198812.appspot.com/record.flac"
    r = SpeechAnalyzer().analyze(uri).best_fit
    print(r)