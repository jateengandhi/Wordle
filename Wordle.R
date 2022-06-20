
library(data.table)
library(dplyr)

setwd("C:/Users/jatee/Documents/R/JG/Practice/Wordle")

rm(list = ls())

chkPastWordle <-  function(word){
  # Assumes word is a string of 5 characters
  # Returns a boolean if word exists in previous wordle answers
  word %in% w$Ans
}

getP <- function(dt){
  # Assumes dt is a data.table of words split into letters in each column
  # Returns positional and total probability of top 6 letters
  t <-  dim(dt)[[1]]
  n <- dim(dt)[[2]]
  nms <- names(dt)
  lst <- sapply(dt, table)
  
  if (is.matrix(lst)){
    tab <- as.data.frame.matrix(lst)
  } else {
    tab <- sapply(lst, as.data.frame.list)
    tab <- as.data.frame.matrix(
      t(rbindlist(tab, fill = TRUE))
    )
  }
  
  tab[is.na(tab)] <- 0
  tab['total'] <-  rowSums(tab)
  for (i in 1:n){
    tab[paste0('p',nms[i])] <- tab[,i]/t
  }
  tab$p <- tab$'total'/(t*n)
  tab
  head(setorder(tab, -p))[(n+2):(2*n+1)]
}

w <- as_tibble(read.csv('data/all2.csv')) # past wordle answers
names(w) <- c('No.', 'Ans', 'Date')

# w_l <- data.table(w$Ans)
# w_l <- w_l[,tstrsplit(w_l$V1, "")]

# Import 5 letter popular words
g <- as_tibble(read.csv('data/g.csv'))
g_w <- setdiff(g$x, w$Ans)#remove past wordle answers
g_w <- data.table(g_w)

# Split letters of each word and save into 5 columns according to position
g_w <- g_w[,tstrsplit(g_w,"")]

# All: https://github.com/dwyl/english-words
d <- as_tibble(read.csv('data/d.csv'))
d_w <- setdiff(d$x, w$Ans)

d_w <- data.table(d_w)
d_w <- d_w[,tstrsplit(d_w,"")]


# gP <- getP(g_w)
# dP <- getP(d_w)
# wP <- getP(w_l)

elim <- c('r', 's')

cur_g <- g_w %>%
  filter((V1 == 'a') &
         !(V2 %in% c(elim)) &
         (V3 == 'o') &
         !(V4 %in% c(elim)) &
         (V5 == 'e'))


# cur_g$V2 <- NULL

cur_d <- d_w %>%
  filter(!(V1 %in% c(elim)) &
           !(V2 %in% c(elim, 'r')) &
           !(V3 %in% c(elim, 'o')) &
           !(V4 %in% c(elim)) &
           !(V5 %in% c(elim)) &
           (V1 == 'r' | V3 == 'r' | V4 == 'r' | V5 == 'r') &
           (V1 == 'o' | V2 == 'o' | V4 == 'o' | V5 == 'o'))


# cur_d$V3 <-  NULL
# cur_d$V4 <-  NULL
# cur_d$V5 <- NULL

gP <- getP(cur_g)
dP <- getP(cur_d)

# g_opt <-  cur_g %>%
#   filter(V4 == 'l')

# d_opt <-  cur_d %>%
#   filter(V2 == 'a' & V3 == 'n')

elim <- c('c', 'u', 't')

cur_g <-  cur_g %>%
  filter(!(V1 %in% c(elim)) &
           (V2 == 'o') &
           !(V3 %in% c(elim)) &
           !(V4 %in% c(elim, 'r')) &
           !(V5 %in% c(elim)))
         


cur_d <-  cur_d %>%
  filter(!(V1 %in% c(elim)) &
           (V2 == 'o'))

cur_d$V2 <-  NULL
# cur_d$V4 <-  NULL
# cur_d$V5 <-  NULL

dP <- getP(cur_d)


d_opt <-  cur_d %>%
  filter(V2 == 'i' & V3 == 'n')

elim <- c('p', 'm', 'o')

cur_g <-  cur_g %>%
  filter(!(V1 %in% c(elim)) &
           # (V2 == 'r') &
           # (V3 == 'o') &
           !(V4 %in% c(elim)) &
           !(V5 %in% c(elim)))

cur_d <-  cur_d %>%
  filter(!(V1 %in% c(elim)) &
           # (V2 == 'r') &
           # (V3 == 'o') &
           !(V4 %in% c(elim)) &
           !(V5 %in% c(elim)))


elim <- c('u')

cur_g <-  cur_g %>%
  filter(!(V1 %in% c(elim, 't')) &
           # (V2 == 'r') &
           # (V3 == 'o') &
           (V4 == 't') &
           !(V5 %in% c(elim, 't')))

cur_d <-  cur_d %>%
  filter(!(V1 %in% c(elim, 't')) &
           # (V2 == 'r') &
           # (V3 == 'o') &
           (V4 == 't') &
           !(V5 %in% c(elim, 't')))

dP<- getP(cur_d)

cur_d <-  cur_d %>%
  filter(V2 == 'h')
cur_g <- cur_g %>%
  filter(V2 == 'h' &
           V4 != 'd')
