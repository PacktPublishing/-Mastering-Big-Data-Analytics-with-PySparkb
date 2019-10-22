from pyspark.sql import SparkSession
import requests
import urllib3
import json
from pprint import pprint
from tempfile import TemporaryFile

DATA_SOURCE_URL = "https://s3-eu-west-1.amazonaws.com/csparkdata/ol_cdump.json"

spark = SparkSession.builder.appName('streamingTest').getOrCreate()


r = requests.get(DATA_SOURCE_URL, stream=True)
destination_filepath = 'testdata.json'

with TemporaryFile() as temp_file:
    print(temp_file.__dict__)
    temp_file.
    for l in r.iter_lines():
        temp_file.write(l)

    streaming_df = spark.readStream.json(temp_file.)
    streaming_df.show()

# with open(destination_filepath, "wb") as dest:
#     while True:
#         r.iter_lines()
#         data = r.(CHUNK_SIZE)
#         if not data:
#             print(" - Finished downloading {}".format(filename))
#             break
#         dest.write(data)

# response = requests.get(DATA_SOURCE_URL)
# print(response)

# df = spark.read.json('')
# df.show()

r.close()
spark.close()
