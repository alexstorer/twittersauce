# This is an exploration of topic modeling

# Some graphing components

#source("http://bioconductor.org/biocLite.R")
#biocLite("Rgraphviz")

# First, let's load up this pile of things.

Sys.setenv(NOAWT=TRUE) 

# This is a workaround for Macs

library(tm) 
#library(Snowball) 
library(RWeka) 
#library(rJava) 
#library(RWekajars) 
library(Rgraphviz)

#library("topicmodels")
#library("XML")

readvanilla <- function (elem, language, id) 
{
  # ideally, add in metadata for each piece of lexisnexis
  doc <- PlainTextDocument(elem$content, id = id, language = language)
}

tweets <- read.csv('/Users/astorer/Work/presentations/twitter/example_tweets.csv')
corpus <- Corpus(VectorSource(tweets$text),readerControl=list(reader = readvanilla))


Sys.setlocale("LC_COLLATE", "C")

dtm <- DocumentTermMatrix(corpus, control = list(stemming = FALSE,
                                                 tokenize = WordTokenizer,
                                                 stopwords = TRUE, 
                                                 minWordLength = 3,
                                                 removeNumbers = TRUE, 
                                                 removePunctuation = TRUE))
dim(dtm)


ft <- findFreqTerms(dtm, lowfreq = 150, highfreq = 500)

plot(dtm, terms = ft, corThreshold = 0.05)

summary(col_sums(dtm))
term_tfidf <-
  tapply(dtm$v/row_sums(dtm)[dtm$i], dtm$j, mean) *
  log2(nDocs(dtm)/col_sums(dtm > 0))
summary(term_tfidf)
sub_dtm <- dtm[,term_tfidf >= 0.1]
sub_dtm <- sub_dtm[row_sums(sub_dtm) > 0,]
summary(col_sums(sub_dtm))

dim(sub_dtm)

# 2 topics

k <- 10
SEED <- 2010
sub_TM <-
  list(VEM = LDA(sub_dtm, k = k, control = list(seed = SEED)),
       VEM_fixed = LDA(sub_dtm, k = k,
                       control = list(estimate.alpha = FALSE, seed = SEED)),
       Gibbs = LDA(sub_dtm, k = k, method = "Gibbs",
                   control = list(seed = SEED, burnin = 1000,
                                  thin = 100, iter = 1000)),
       CTM = CTM(sub_dtm, k = k,
                 control = list(seed = SEED,
                                var = list(tol = 10^-4), 
                                em = list(tol = 10^-3))))

sapply(sub_TM[1:2], slot, "alpha")

Terms <- terms(sub_TM[["VEM"]], 5)


combmachine <- function(x) {
  if (length(x)<2) {
    return(data.frame())
  }
  as.data.frame(t(combn(x,2)))
}

Reduce(rbind,lapply(l,combmachine))