import socket
import sys
import requests
import requests_oauthlib
import json

# SETTINGS
# Replace the values below with your own
# Twitter Consumer API keys
CONSUMER_KEY = "szt9ytUAMAlEyqHiJH0c8hWas"
CONSUMER_SECRET = "0m4A3izC3brsO0rto7C2A6Q52BgPVKxTRmbMJvJvdcHsedBVzY"
# Twitter Access token & access token secret
ACCESS_TOKEN = "1152234679065595906-9nqvBvHPtxyiTZ7aNDLbHkDHkU7wm5"
ACCESS_SECRET = "qQUkhyx72Ktz09KJ6j2etRfk4PcaocCtwyt0VtEGEE79U"
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
                ("track", "marvel"),
            ]
        ]
    )
    query_url = "{url}?{stream_params}".format(url=url, stream_params=stream_params)

    response = requests.get(query_url, auth=my_auth, stream=True)
    print(query_url, response)
    return response


def send_tweets_to_spark(http_resp, tcp_connection):
    for line in http_resp.iter_lines():
        try:
            # print(line)
            full_tweet = json.loads(line)
            tweet_text = full_tweet["text"]
            print("Tweet Text: " + tweet_text)
            print("------------------------------------------")
            # tcp_connection.send(tweet_text + "\n")
        except:
            e = sys.exc_info()[0]
            print("Error: %s" % e)


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    print("Waiting for TCP connection...")
    # connection, address = s.accept()
    print("Connected... Starting getting tweets.")
    resp = get_tweets()
    send_tweets_to_spark(resp, "connection")
