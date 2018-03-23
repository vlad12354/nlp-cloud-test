# Copyright 2016 Google Inc.
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

# [START app]
import logging
import similarity_output
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
def search():
    return render_template('home.html')


@app.route('/', methods=['POST'])
def my_form_post():
    text = [request.form['text'].upper()]
    print(text)
    result = similarity_output.match_and_output(text)
    print(result)
    return render_template("result.html", result=result)


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500


if __name__ == "__main__":
    app.run()

# [END app]
