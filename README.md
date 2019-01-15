# The API (web service) for counting dogs in New York City

This is a simple API written in python using framework Tornado.

## Dependencies & requirements
+ Python 3.+
+ [tornado 5.0.2](https://www.tornadoweb.org/en/stable/) 
+ [requests 2.18.4](http://docs.python-requests.org/en/master/)

You can easily use `pip install` to install these libraries

## My environment
+ Python version: Python 3.6 (Anaconda)
+ OS: MacOS Mojave 10.14.1


## How to use the code
First of all, you need a <b><u>Google Fusion Tables API key</b></u>:

[Google Fusion Tables REST API](https://developers.google.com/fusiontables/docs/v2/using)

Replace the value of `api_key` with your key in the [scripts](https://github.com/ReehcQ/backend_exe/blob/master/dogAPI.py).

Go to the project directory and run the server with bash:
~~~
python dogAPI.py
~~~

You can access the api by typing the following address:
~~~
http://localhost:5000/count?[category]=[value]
~~~
or quering with multiply categories connected by mark '&'
~~~
http://localhost:5000/count?[category1]=[value1]&[category2]=[value2]&[category3]=[value3]
~~~

*Example*:
~~~
http://localhost:5000/count?Dog_name=Buddy
~~~

which returns:
~~~
{"count": 599}
~~~

There are 11 categories can be queried:
+ dog_name
+ gender
+ breed
+ birth
+ dominant_color
+ secondary_color
+ third_color
+ spayed_or_neutered
+ guard_or_trained
+ borough
+ zip_code

The query is <b>case insensitive</b>.

## How to do the unittest
Open a new command prompt, go to the project directory and run the unittest file (for Linux or Unix):
~~~
READY_TEST_BASE_URL=http://localhost:5000 python apitest.py
~~~

For windows, set path READY_TEST_BASE_URL=http://localhost:5000 first then run:
`python apitest.py`


## Source
Dataset: [Dogs of NYC](https://fusiontables.google.com/data?docid=1pKcxc8kzJbBVzLu_kgzoAMzqYhZyUhtScXjB0BQ#rows:id=1)

Test: [A quick test for back-end engineer](https://gist.github.com/aparrish/691b0301f6737d65b01db9920a60a0a5)
