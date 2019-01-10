# A quick test for our backend engineer candidates

Hi there! Your task is to write a small web service (API). Here's the brief:

* The service must use data from [this Dogs of NYC CSV file](https://fusiontables.google.com/data?docid=1pKcxc8kzJbBVzLu_kgzoAMzqYhZyUhtScXjB0BQ#rows:id=1)
* The service must respond to requests on a `/count` endpoint, which returns a JSON object in the following format: `{"count": n}` where `n` is an integer.
* Query string parameters to the `/count` endpoint name fields in the CSV. The value of `n` in the response should be exactly the number of rows in the CSV for which the values for each parameter in the request is equal to the corresponding value in the row, using case-insensitive comparison. For example, the query `/count?dominant_color=brown` should return a response of `{"count": 9181}`, because there are 9181 rows in the database where the `dominant_color` column is "brown."
* If any invalid query string parameters are provided (i.e., parameters that do not correspond to column names in the CSV), the service should respond with a `400` status code and an error message that supplies a list of names of the unknown fields as the value for a key `unknown fields`. For example, a request to `/count?fleas=no` should return a message in the following format: `{"unknown fields": ["fleas"]}`
* All responses should include a `Content-Type` header appropriate to the data in the response (i.e., `application/json`).
* The service must be written in Python. (You can choose the framework.) It should be possible to run the web service on any reasonable modern UNIX-ey operating system that Python supports (i.e., Linux and macOS).

## Integration testing

The `apitest.py` file in this gist is a test script for a web service with the characteristics described above. You should be able to run this test against your web service with no failed tests. The script requires the `requests` library to be installed, and is designed to run on Python 3. (It might run as written on Python 2 as well; I haven't checked.)

To supply the base URL to your API for the tests, set an environment variable `READY_TEST_BASE_URL` before running the script. E.g., with bash:

    READY_TEST_BASE_URL=http://localhost:5000 python apitest.py
  
Note that you're on the hook to implement *all* of the features in the brief, not just the correct responses to these particular requests!

## Deliverables

Here's what you need to give us:

1. The base URL of your web service, deployed somewhere on the Internet. I should be able to run the `apitest.py` script with your base URL and have all of the tests pass. (If this is a hardship for you for privacy or financial reasons, no worries---include instead a description of how you would deploy the code with the items from (2) below.)
2. The source code for your web service, along with instructions on how to run it. This can be supplied as a ZIP file or a link to a git repository or whatever. Include a `requirements.txt` file so I can easily `pip`-install your dependencies (if any).