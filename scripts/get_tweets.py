import os
import time
import pickle
import tweepy
import pandas as pd
from yaml import load
from typing import List, Dict


def fetch_tweets(dataDF, datapath):
    """Function downloads tweets and stores them in batches of 45000 tweets in pickle format."""

    tweetids: List = []
    data: List = [("id", "text")]

    dataDF = dataDF.reset_index()

    for index, line in dataDF.iterrows():

        # Use this if script has been interrupted and you don't want to start all over again.
        # batch_num = 2
        # if index < (45000 * batch_num):
        #     continue

        # There is limit of 100 tweets in for one request.
        if (index + 1) % 100 == 0:
            isfetched = False
            while not isfetched:
                # There is a limit of 900 requests in 15 minutes window for tweets lookup endpoint in twitter API.
                # In order to download all tweets the code below will wait until limit window resets and continue.
                try:
                    response = client.get_tweets(",".join(tweetids))
                    data.extend([(tweet.id, tweet.text) for tweet in response.data])
                    isfetched = True
                except tweepy.errors.TooManyRequests as e:
                    print(len(data))
                    print(index)
                    wait_in_seconds = int(
                        e.response.headers["x-rate-limit-reset"]
                    ) - int(time.time())
                    print(
                        f"{e}. Waiting for {wait_in_seconds//60} minutes and {wait_in_seconds%60} seconds"
                    )
                    time.sleep(wait_in_seconds)
                    
            tweetids = []
            # Store batch of 45000 tweets in pickle format List(tuple(int, str)) in case script is interrupted.
            if (index + 1) % 45000 == 0:
                filename = f"{datapath}/tweets_{(index+1)//45000}.pickle"
                with open(filename, "wb") as file:
                    pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
                print(f"File: {filename}")
                data: List = [("id", "text")]
        tweetids.append(str(line["tweet_id"]))

if __name__ == "__main__":

    # CONFIG file contains secrets therefore is not stored in repo. Please attach you own.
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader

    with open("CONFIG.yaml") as config:
        config: Dict = load(config, Loader=Loader)
        BEARER_TOKEN: str = config["BEARER_TOKEN"]

    # You can authenticate as your app with just your bearer token
    client = tweepy.Client(bearer_token=BEARER_TOKEN)

    BASE_DIR: str = os.path.dirname(os.path.dirname(__file__))
    datapath: str = f"{BASE_DIR}/data"
    filepath: str = f"{BASE_DIR}/data/pl_covid_tweets_clean.tsv"
    dataDF: pd.DataFrame = pd.read_csv(filepath, sep="\t")

    fetch_tweets(dataDF, datapath)
