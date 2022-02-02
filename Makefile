all: fetch_tweets download_glove unpack_glove

download_glove:
	wget https://github.com/sdadas/polish-nlp-resources/releases/download/v1.0/glove.zip -P ./data/

unpack_glove:
	unzip ./data/glove.zip -d ./data/
	rm ./data/glove.zip

fetch_tweets:
	mkdir -p data
	mkdir -p models
	mv ./pl_covid_tweets_clean.tsv ./data/
	./scripts/get_tweets.py 
