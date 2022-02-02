# ZUM_NLP_Sentiment_Analysis
Analiza sentymentu na podstawie ok. 500k polski tweetów o tematyce wirusa covid-19

Celem projektu jest analiza pod kątem polaryzacji w społeczeństwie.

# Kroki projektu

1. Pobranie danych źródłowych
Repozytorium zawiera skrypt, który pobiera tweety łącząc się z API tweetera za pomocą id tweetów.
Identyfikatory Tweetów zostały pobrane ze strony https://zenodo.org/record/5090588#.YZDZdmDMKUn.
Zbiór danych został zapisany w rozszerzeniu pickle.

2. Data cleaning
Dane zostały oczyszczone ze emotikonek, odnośników, retweetów, znaków interpunkcyjnych oraz tak zwanych stop words.

3. Word embeddings
W projkecie podjęto próbę podłączenie wytrenowej przestrzeni wektorów słów GloVe jednak zwracała losowe wyniki i otagowanie na 3 klasy sentymentu nie skuteczne. Następnie stworzono word embeddings za pomocą sieci word2vec.

4. Wykorzystano K-MEANS do stworzenia clustrów (k=3)

5. Dodanie etykiet klasy 
Dane zostały oznaczone jako pozytywne/negatywne/neutralne (3 klasy).

Wybierano 3 modele ML:
* Logistic regression
* Random Forest
* KNN

Na modelach trenowano dane. Wyniki zostały zaprezentowane wykorzystując confusion matrix.
