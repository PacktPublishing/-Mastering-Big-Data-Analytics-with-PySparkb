import requests
import requests_oauthlib
import json
import socket

# SETTINGS
# Replace the values below with your own
# Twitter Consumer API keys
CONSUMER_KEY = "CU6EPwruBYrr14v9r0HCbExoD"
CONSUMER_SECRET = "4N3KpvZWZXNgkKZFiC1BfCmgJgKsYL8kBGJTM8i3uKCH0Ewut2"
# Twitter Access token & access token secret
ACCESS_TOKEN = "1152234679065595906-3V15SxGQEOdmuLtvBseoe7iOiDMqDY"
ACCESS_SECRET = "lkBPjGbjzeM442Jx14mN94Nrb2L9bfRY5OLW2gPG1GRTt"
# You may customize the IP and Port, defaults should suffice though
TCP_IP = "localhost"
TCP_PORT = 9009

# Establish connection
my_auth = requests_oauthlib.OAuth1(
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET
)


def get_tweets():
    url = "https://stream.twitter.com/1.1/statuses/filter.json"

    # Stream parameters
    # https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters
    stream_params = "&".join(
        [
            "%s=%s" % params
            for params in [
                # English Language
                ("language", "en"),
                # San Fransisco or New York
                ("locations", "-122.75,36.8,-121.75,37.8,-74,40,-73,41"),
                # Has to have a hashtag
                # ("track", '#'),
            ]
        ]
    )
    query_url = "{url}?{stream_params}".format(url=url, stream_params=stream_params)
    response = requests.get(query_url, auth=my_auth, stream=True)
    print(query_url, response)
    return response


def bind_listen_on_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    print("Waiting for TCP connection...")
    connection, address = s.accept()
    return connection, address


conn, addr = bind_listen_on_port(TCP_IP, TCP_PORT)

print("Connected... Starting getting tweets.")
http_resp = get_tweets()

for line in http_resp.iter_lines():
    print("------------------------------------------")
    try:
        full_tweet = json.loads(line)
        tweet_text = full_tweet["text"]
        entities = full_tweet["entities"]
        print("Tweet Text:", tweet_text)
        print("Entities:", entities)
        conn.send(line)
    except json.JSONDecodeError as e:
        print("Unable to parse tweet.. Skipping..", e)
    except BrokenPipeError as e:
        print("Connection broken.. Retrying", e)
        retry_attemps = 3
        retry_successful = False
        while retry_attemps > 0 and not retry_successful:
            conn, addr = bind_listen_on_port(TCP_IP, TCP_PORT)
        else:
            if retry_successful:
                print("Connection re-established!")
                pass
            else:
                raise

print("Oh My God!!!11")
