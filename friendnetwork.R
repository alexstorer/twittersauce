library(igraph)

ds <- read.csv('/Users/astorer/Work/presentations/twitter/code/Mining-the-Social-Web/python_code/twitter.csv',header = FALSE, col.names=c("source","destination"), stringsAsFactors=FALSE)

ds <- read.csv('/Users/astorer/Work/presentations/twitter/code/Mining-the-Social-Web/python_code/iqssrtc_net.csv',header = FALSE, col.names=c("source","destination"), stringsAsFactors=FALSE)


m <- as.matrix(ds)
g <- graph.edgelist(m)

myid <- 'iqssrtc'

nVertices <- length(V(g))
vcolors <- rep("white",nVertices)
vcolors[V(g)$name==myid] <- "red"

V(g)$color <- vcolors

#plot(g,layout=layout.kamada.kawai(g))
#plot(g,layout=layout.lgl(g))
#plot(g,layout=layout.circle(g))

b <- betweenness(g, v=V(g), directed = TRUE, weights = NULL,
            nobigint = TRUE, normalized = FALSE)

palette(rainbow(seq(.75,.15,len=1000)))
palette(heat.colors(100)[seq(100,1,-1)])
V(g)$color <- round(100 * b/max(b))
V(g)$color[V(g)$color==0] <- 1

## pdf('iqssrtc_network_lgl.pdf')
## plot(g,layout=layout.kamada.kawai(g))
## dev.off()


## pdf('iqssrtc_network_lgl.pdf')
## plot(g,layout=layout.lgl(g))
## dev.off()

jpeg('iqssrtc_network_kamada.jpg',width = 800, height = 800,quality=90)
plot(g,layout=layout.kamada.kawai(g),vertex.label=V(g)$name)
dev.off()


jpeg('iqssrtc_network_lgl.jpg',width = 800, height = 800)
plot(g,layout=layout.lgl(g))
dev.off()
