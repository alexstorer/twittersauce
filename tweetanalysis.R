# This is an exploration of topic modeling

# Some graphing components

#source("http://bioconductor.org/biocLite.R")
#biocLite("Rgraphviz")

# First, let's load up this pile of things.

Sys.setenv(NOAWT=TRUE) 

# This is a workaround for Macs

library(tm) 
library(RWeka) 
library(Rgraphviz)
library(slam)

readvanilla <- function (elem, language, id) 
{
  # ideally, add in metadata for each document as well
  doc <- PlainTextDocument(elem$content, id = id, language = language)
}

# Load in the tweets
tweets <- read.csv('/Users/astorer/Work/presentations/twitter/finalcode/twittersauce/example_tweets.csv')

# Read just the tweet text into the corpus
corpus <- Corpus(VectorSource(tweets$text),readerControl=list(reader = readvanilla))

# This should turn off locale-specific sorting
Sys.setlocale("LC_COLLATE", "C")

# Make our document-term matrix
dtm <- DocumentTermMatrix(corpus, control = list(stemming = FALSE,
                                                 tokenize = WordTokenizer,
                                                 stopwords = TRUE, 
                                                 minWordLength = 3,
                                                 removeNumbers = TRUE, 
                                                 removePunctuation = TRUE))

# How many documents and terms do we have?
dim(dtm)

# What are the frequent terms?
ft <- findFreqTerms(dtm, lowfreq = 150, highfreq = 5000)

# We can get the most frequent terms
sorted_terms <- sort(col_sums(dtm),decreasing=T)

# We can plot them
barplot(sorted_terms[1:20],las=2)

# Here are the 100 most popular terms in alphabetical order:
sort(names(sorted_terms[1:100]))

# We can also plot the terms with lines indicating if they correlate
plot(dtm, terms = names(sorted_terms[3:20]), corThreshold = 0.075)

# Here are terms that correlate with debt
findAssocs(dtm,term="debt",0.3)

# Here is a plot of some debt terms and how they are related
plot(dtm, terms = names(findAssocs(dtm,term="debt",0.2)), corThreshold = 0.30)
