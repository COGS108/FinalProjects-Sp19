# Spreadspoke 
setwd("~/Documents/R/nfl regression/spreadspoke")
## update date line 188 for splitting historic and forecast nfl data

nfl <- read.csv("spreadspoke_scores.csv", stringsAsFactors=F)
nfl$schedule_date<-as.Date(nfl$schedule_date, "%m/%d/%Y") # format as date

library(xlsx)
#fileUrl <- "http://www.aussportsbetting.com/historical_data/nfl.xlsx" # money line, open/close lines historic info
#download.file(fileUrl)
#nfl_asb <- read.csv("nfl_2014_2017_asb.csv") 

# pro football reference game info
library(XML)
library(RCurl)
library(rvest)
#filename <- NA
#for(year in 1966:2017){
#        filename[year] <- paste("https://www.pro-football-reference.com/years/",year,"/games.htm#games::none",sep="")
#} # read seasons 1966 to 2017
#url_pfr_games <- getURL(filename[1966:2017])  #getURL("https://www.pro-football-reference.com/years/2014/games.htm#games::none")
#pfr_games_raw <- readHTMLTable(url_pfr_games, trim=T, as.data.frame=T, header=T)
#pfr_games <-bind_rows(pfr_games_raw)
#my_df <- as.data.frame(read_html(url_pfr_games) %>% html_table(fill=TRUE))


# Add team IDs which are a 2 or 3 letter team id for each team
teams <- read.csv("nfl_teams.csv",stringsAsFactors= F) # team data
team_names <- teams$team_name # vector of team names
team_ids <- teams$team_id # vector of team IDs

nfl$team_home_id <- NA # initialize the team home id
nfl$team_away_id <- NA  # initialize the team away id

for (i in 1:nrow(nfl)) {
        for(j in 1:length(team_ids)){
                if(nfl$team_home[i]==team_names[j]){
                        nfl$team_home_id[i]<-team_ids[j]
                }
        }
}

for (i in 1:nrow(nfl)) {
        for(j in 1:length(team_ids)){
                if(nfl$team_away[i]==team_names[j]){
                        nfl$team_away_id[i]<-team_ids[j]
                }
        }
}

nfl$team_away_id <- as.factor(nfl$team_away_id)  # factor class team away id
nfl$team_home_id <- as.factor(nfl$team_home_id)  # factor class team home id
nfl$team_favorite_id <- as.factor(nfl$team_favorite_id) # factor class team favorite id

# game unique id
library(stringr)
nfl$game_id <- NA 
schedule_first_game_date <- min(nfl$schedule_date)
for(i in 1:nrow(nfl)){
        nfl$game_id[i] <- paste(as.Date(nfl$schedule_date[i],format='%m/%d/%Y'),nfl$team_away_id[i],nfl$team_home_id[i],sep="") # set unique id for each game 
}  
nfl$game_id <- gsub("-","",nfl$game_id) # remove - from game id

# stadium type info
stadiums <- read.csv("nfl_stadiums.csv",stringsAsFactors=F) # stadium data
stadiums_names <- as.character(stadiums$stadium_name)
stadiums_types <- as.character(stadiums$stadium_type)
nfl$stadium_type <- NA # initialize
nfl$stadium <- as.character(nfl$stadium)

for (i in 1:nrow(nfl)) {
        for(j in 1:length(stadiums_names)){
                if(as.character(nfl$stadium[i]) %in% stadiums_names[j]){
                        nfl$stadium_type[i]<-stadiums_types[j]
                }
        }
}

nfl$stadium_type <- as.factor(nfl$stadium_type) # initialize

# playoff game
#nfl$schedule_playoff <- !is.finite(nfl$schedule_week) # if not a week number

# Create dummy variables for first week of season and last week of season [consider week after bye week, or short week ie, sunday>thursday game]
nfl$schedule_week_1<-ifelse(nfl$schedule_week==1,TRUE,FALSE) # first week of season
nfl$schedule_week_last<-NA
for (i in 1:nrow(nfl)) {
        if(nfl$schedule_season[i]==1993|1999){
                nfl$schedule_week_last[i]<-ifelse(nfl$schedule_week[i]==18,TRUE,FALSE)
        }
} # 1993 & 1998 seasons had 18 weeks

for (i in 1:nrow(nfl)) {
        if(nfl$schedule_season[i] %in% 1987){
                nfl$schedule_week_last[i]<-ifelse(nfl$schedule_week[i]==16,TRUE,FALSE)
        }
} # 1987 seasons had week 3 cancelled, weeks 4-6 used replacement players which are excluded from data set, and 16 weeks total

for(i in 1:nrow(nfl)){
        if(nfl$schedule_season[i]!=1987|1993|1999){
                nfl$schedule_week_last[i]<-ifelse(nfl$schedule_week[i]==17,TRUE,FALSE)        
        }
}

# add day of week info
require(lubridate)
nfl$schedule_day <- wday(nfl$schedule_date, label=TRUE) 
nfl$schedule_month <- month(nfl$schedule_date, label=TRUE)
nfl$schedule_sunday <- ifelse(nfl$schedule_day%in%c("Sun"),TRUE,FALSE) 

# divisional game True/False
team_divisions <- teams$team_division
nfl$team_home_division <- NA
nfl$team_away_division <- NA

for (i in 1:nrow(nfl)) {
        for(j in 1:length(team_divisions)){
                if(nfl$team_home[i]==team_names[j]){
                        nfl$team_home_division[i]<-team_divisions[j]
                }
        }
}

for (i in 1:nrow(nfl)) {
        for(j in 1:length(team_ids)){
                if(nfl$team_away[i]==team_names[j]){
                        nfl$team_away_division[i]<-team_divisions[j]
                }
        }
}

nfl$team_away_division <- as.factor(nfl$team_away_division)  # factor class team away id
nfl$team_home_division <- as.factor(nfl$team_home_division)  # factor class team home id

## 2002 division and ## pre2002 division
team_divisions_pre2002 <- teams$team_division_pre2002

for (i in 1:nrow(nfl)) {
        for(j in 1:length(team_divisions_pre2002)){
                if(nfl$team_home[i]==team_names[j]){
                        nfl$team_home_division_pre2002[i]<-team_divisions_pre2002[j]
                }
        }
}

for (i in 1:nrow(nfl)) {
        for(j in 1:length(team_divisions_pre2002)){
                if(nfl$team_away[i]==team_names[j]){
                        nfl$team_away_division_pre2002[i]<-team_divisions_pre2002[j]
                }
        }
}

nfl$team_away_division_pre2002 <- as.factor(nfl$team_away_division)  # factor class team away id
nfl$team_home_division_pre2002 <- as.factor(nfl$team_home_division)  # factor class team home id

### division matchup true or false
nfl$division_matchup <- NA
nfl$division_matchup <- ifelse(nfl$team_away_division==nfl$team_home_division,
                               TRUE, ifelse(nfl$team_away_division_pre2002==nfl$team_home_division_pre2002,TRUE,FALSE))
nfl$team_home_division <- NULL # no longer need
nfl$team_away_division <- NULL # no longer need
nfl$team_home_division_pre2002 <- NULL # no longer need
nfl$team_away_division_pre2002 <- NULL # no longer need

# spread types
nfl$team_home_favorite <- as.character(nfl$team_favorite_id)==as.character(nfl$team_home_id) 
nfl$spread_home <- ifelse(nfl$team_home_favorite==TRUE, nfl$spread_favorite,-nfl$spread_favorite)
nfl$spread_away <- -nfl$spread_home

nfl$spread_type<-ifelse(nfl$spread_home==0,'Pick',
                           ifelse(nfl$spread_home>0,'Home Underdog','Home Favorite'))
nfl$spread_type<-as.factor(nfl$spread_type)
nfl$spread_outlier <- ifelse(abs(nfl$spread_favorite) > 14.1, '2TD+',
                                ifelse(abs(nfl$spread_favorite) > 10.1, '1TD1FG+',
                                       ifelse(abs(nfl$spread_favorite) > 7.1, '1TD+','No Outlier')))
nfl$spread_outlier <- as.factor(nfl$spread_outlier)

# over under types
nfl$over_under_outlier <- ifelse(nfl$over_under_line<33,"Under 2sd",
                                    ifelse(nfl$over_under_line<37,"Under 1sd",
                                           ifelse(nfl$over_under_line>50,"Over 2sd",
                                                  ifelse(nfl$over_under_line>46,"Over 1sd","No Outlier"))))
nfl$over_under_outlier <- as.factor(nfl$over_under_outlier)


# subset into games played versus future games
nflForecast <- subset(nfl,nfl$schedule_date > as.Date('2018-12-31')) # data for forecast games
nfl <- subset(nfl,nfl$schedule_date < as.Date('2018-12-31')) # data for played games


# elo ratings
require(EloRating) # use the elo rating package
require(zoo)
nfl$tie <- nfl$score_away==nfl$score_home
nfl$team_winner <- ifelse(nfl$score_away==nfl$score_home,as.character(nfl$team_home_id),
                           ifelse(nfl$score_away>nfl$score_home,as.character(nfl$team_away_id),as.character(nfl$team_home_id)))
nfl$team_loser <- ifelse(nfl$score_away==nfl$score_home,as.character(nfl$team_away_id),
                          ifelse(nfl$score_away<nfl$score_home,as.character(nfl$team_away_id),as.character(nfl$team_home_id)))
nfl$team_winner <- as.factor(nfl$team_winner)
nfl$team_loser <- as.factor(nfl$team_loser)

# Home/Away team result-----
nfl$team_home_result<-ifelse(nfl$score_home>nfl$score_away,"Win",
                              ifelse(nfl$score_home==nfl$score_away,"Tie", "Loss"))
nfl$team_away_result<-ifelse(nfl$score_home<nfl$score_away,"Win",
                              ifelse(nfl$score_home==nfl$score_away,"Tie", "Loss"))
nfl$team_home_result<-as.factor(nfl$team_home_result)
nfl$team_away_result<-as.factor(nfl$team_away_result)

seqcheck(winner=nfl$team_winner,loser=nfl$team_loser,Date=nfl$schedule_date,draw=nfl$tie)
seq <- elo.seq(winner=nfl$team_winner, loser=nfl$team_loser,draw=nfl$tie,Date=nfl$schedule_date)
#eloplot(seq, from="2016-09-01",interpolate="no") #plots the elo ratings

nfl$team_win_elo_pre<-1000 # sets the initial elo rating at 1000
nfl$team_lose_elo_pre<-1000
elo_winners<-seq[[6]][4] # elo score before game for winning team
nfl$team_win_elo_pre <- as.numeric(unlist(elo_winners))
elo_losers<-seq[[6]][5] # elo score before game for losing team
nfl$team_lose_elo_pre <- as.numeric(unlist(elo_losers))

# home team and away team elo scores
nfl$team_home_elo_pre <- NA
nfl$team_away_elo_pre <- NA
nfl$team_home_id <- as.character(nfl$team_home_id)
nfl$team_winner <- as.character(nfl$team_winner)
for(i in 1:nrow(nfl)){
        nfl$team_home_elo_pre[i]<-ifelse(nfl$tie[i]==TRUE,nfl$team_win_elo_pre[i],ifelse(nfl$team_home_id[i]==nfl$team_winner[i],nfl$team_win_elo_pre[i],nfl$team_lose_elo_pre[i]))
        nfl$team_away_elo_pre[i]<-ifelse(nfl$tie[i]==TRUE,nfl$team_lose_elo_pre[i],ifelse(nfl$team_away_id[i]==nfl$team_winner[i],nfl$team_win_elo_pre[i],nfl$team_lose_elo_pre[i]))        
}

nfl$team_winner <- as.factor(nfl$team_winner)
nfl$team_loser <- as.factor(nfl$team_loser)

# difference between home team's pre-game elo and away team's pre-game elo
nfl$elo_pre_difference<-0
for(i in 1:nrow(nfl)){
        nfl$elo_pre_difference[i] <- nfl$team_home_elo_pre[i]-nfl$team_away_elo_pre[i] #  value of difference in pre game elo scores between home and away team)
}
nfl$team_home_elo_pre_diff <- nfl$elo_pre_difference
nfl$team_away_elo_pre_diff <- -nfl$elo_pre_difference
nfl$team_home_win_prob <- winprob(nfl$team_home_elo_pre+ifelse(nfl$stadium_neutral==c("TRUE"),0,55),nfl$team_away_elo_pre) # adj for home team historically wins 58% games equivalent to 55 ELO pts
nfl$team_away_win_prob <- 1-nfl$team_home_win_prob
nfl$team_home_win_prob_diff <- nfl$team_home_win_prob-nfl$team_away_win_prob

# score total & post game win/loss/tie
nfl$score_total <- nfl$score_home + nfl$score_away
nfl$team_home_win_count <- ifelse(nfl$team_home_result %in% c("Tie"),0.5,
                                      ifelse(nfl$team_home_result %in% c("Win"),1,0)) # 1 = win, 0.5 = tie, 0 = loss
nfl$team_away_win_count <- ifelse(nfl$team_home_result %in% c("Tie"),0.5,
                                      ifelse(nfl$team_away_result %in% c("Win"),1,0)) # 1 = win, 0.5 = tie, 0 = loss


# over/under analysis
nfl$over_under_result <- ifelse(nfl$score_total==nfl$over_under_line, 'Push', 
                                   ifelse(nfl$score_total > nfl$over_under_line,
                                          'Over','Under'))
nfl$over_under_result <- as.factor(nfl$over_under_result)
nfl$over_under_result_count<- ifelse(nfl$over_under_result=="Push",0.5,
                                     ifelse(nfl$over_under_result=="Over",1,0)) # 1 = over, 0.5 = push, 0 = under

# spread analysis
nfl$spread_home_result<-nfl$score_away-nfl$score_home # spread home team result, i.e., away score less home score
nfl$spread_away_result<-nfl$score_home-nfl$score_away # spread away team result

nfl$score_favorite <- ifelse(nfl$team_favorite_id %in% c("PICK"),0,
                                    ifelse(nfl$team_favorite_id==nfl$team_home_id,nfl$score_home,nfl$score_away)) # favorite spread result = underdog score - favorite score
nfl$score_underdog <- ifelse(nfl$team_favorite_id %in% c("PICK"),0,
                             ifelse(nfl$team_favorite_id==nfl$team_home_id,nfl$score_away,nfl$score_home)) # favorite spread result = underdog score - favorite score

nfl$spread_favorite_result <- ifelse(nfl$team_favorite_id %in% c("PICK"),0,
                                     ifelse(nfl$spread_home_result==nfl$spread_favorite,0,
                                     ifelse(nfl$team_favorite_id==nfl$team_home_id,nfl$spread_home_result,nfl$spread_away_result))) # favorite spread result = underdog score - favorite score
nfl$spread_favorite_cover_result <- ifelse(nfl$spread_favorite_result %in% c("PICK"),"Push",
                                          ifelse(nfl$spread_home_result==nfl$spread_favorite,"Push",
                                          ifelse((nfl$score_favorite+nfl$spread_favorite)>nfl$score_underdog,"Cover","Did Not Cover"))) # 1 = cover, 0.5 = push, 0 = did not cover
nfl$spread_favorite_cover_count <- ifelse(nfl$spread_favorite_result %in% c("Push"),0.5,
                                    ifelse(nfl$spread_favorite_result %in% c("Cover"),1,0)) # 1 = cover, 0.5 = push, 0 = did not cover
nfl$spread_underdog_cover_result <- ifelse(nfl$spread_favorite_result %in% c("Push"),"Push",
                                           ifelse(nfl$spread_away_result==nfl$spread_favorite,"Push",
                                           ifelse((nfl$score_favorite+nfl$spread_favorite)>nfl$score_underdog,"Did Not Cover","Cover"))) # 1 = cover, 0.5 = push, 0 = did not cover
nfl$spread_underdog_cover_count <- ifelse(nfl$spread_favorite_result %in% c("Push"),0.5,
                                          ifelse(nfl$spread_favorite_result %in% c("Cover"),0,1)) # 1 = cover, 0.5 = push, 0 = did not cover

nfl$spread_home_cover_result <- ifelse(nfl$team_home_favorite==TRUE,
                                          nfl$spread_favorite_cover_result,
                                          nfl$spread_underdog_cover_result)
nfl$spread_away_cover_result <- ifelse(nfl$team_home_favorite==FALSE,
                                          nfl$spread_favorite_cover_result,
                                          nfl$spread_underdog_cover_result)  

nfl$spread_home_cover_result <- as.factor(nfl$spread_home_cover_result)
nfl$spread_away_cover_result <- as.factor(nfl$spread_away_cover_result)

nfl$spread_home_cover_count <- ifelse(nfl$spread_home_cover_result %in% c("Push"),0.5,
      ifelse(nfl$spread_home_cover_result %in% c("Cover"),1,0)) # 1 = cover, 0.5 = push, 0 = did not cover
nfl$spread_away_cover_count <- ifelse(nfl$spread_away_cover_result %in% c("Push"),0.5,
                                      ifelse(nfl$spread_away_cover_result %in% c("Cover"),1,0)) # 1 = cover, 0.5 = push, 0 = did not cover

# team rolling stats data prep team v opponent format
require(plyr)
require(dplyr)
require(FSA)
require(zoo)

nflCalc<-rbind(
        nflHome=data.frame(game_id=nfl[,'game_id'],
                           season=nfl[,'schedule_season'], 
                           schedule_week=nfl[,'schedule_week'], 
                           team=nfl[,'team_home_id'], 
                           opponent=nfl[,'team_away_id'],
                           schedule_date=nfl[,'schedule_date'],
                           venue=rep("home", n=nrow(nfl)), 
                           score=nfl$score_home,
                           score_against=nfl$score_away,
                           score_margin=nfl$score_home-nfl$score_away,
                           spread=nfl$spread_home,
                           overunder=nfl$over_under_line,
                           elo=nfl$team_home_elo_pre,
                           win_count=nfl$team_home_win_count,
                           cover_count=nfl$spread_home_cover_count,
                           over_count=nfl$over_under_result_count,
                           game_count=1,
                           duplicate=FALSE
        )
        ,
        
        nflAway=data.frame(game_id=nfl[,'game_id'],
                           season=nfl[,'schedule_season'],
                           schedule_week=nfl[,'schedule_week'], 
                           team=nfl[,'team_away_id'], 
                           opponent=nfl[,'team_home_id'],
                           schedule_date=nfl[,'schedule_date'],
                           venue=rep("away", n=nrow(nfl)), 
                           score=nfl$score_away,
                           score_against=nfl$score_home,
                           score_margin=nfl$score_away-nfl$score_home,
                           spread=nfl$spread_away,
                           overunder=nfl$over_under_line,
                           elo=nfl$team_away_elo_pre,
                           win_count=nfl$team_away_win_count,
                           cover_count=nfl$spread_away_cover_count,
                           over_count=nfl$over_under_result_count,
                           game_count=1,
                           duplicate=TRUE
        )
)

nflCalc <- arrange(nflCalc,schedule_date)

        


k=16 # constant for number of games i.e., 4 = last 4 games
nflCalc<-nflCalc %>%
        group_by(team) %>%
        mutate(days_since_last_game=lead(schedule_date)-schedule_date) %>% # days since last game used to calculate bye week
        mutate(win_pct=(cumsum(win_count)/cumsum(game_count))) %>% # winning %
        mutate(win_pct_roll_lag=(pcumsum(win_count)/pcumsum(game_count))) %>% # winning % prior-to
        mutate(win_pct_roll=rollapply(win_count, k, FUN=sum, 
                                      fill=NA, align="right")/k) %>% # winning % last k games
        
#        mutate(covers_roll=cumsum(cover_count)) %>% # covers
#        mutate(pushes_roll=cumsum(spread_push)) %>% # pushes
#        mutate(nocovers_roll=cumsum(spread_loss)) %>% # did not cover
        mutate(cover_pct=cumsum(cover_count)/cumsum(game_count)) %>% # % covers the spreads 
        mutate(cover_pct_roll_lag=pcumsum(cover_count)/pcumsum(game_count)) %>% # % covers the spreads prior-to 
        mutate(cover_pct_roll=rollapply(cover_count, k, FUN=sum, 
                                        fill=NA, align="right")/k) %>% # % covers last k games
#        mutate(overs_roll=cumsum(over)) %>% # overs
#        mutate(over_pushes_roll=cumsum(over_under_push)) %>% # over under pushes
#        mutate(unders_roll=cumsum(under)) %>% # unders
        mutate(over_pct=cumsum(over_count)/cumsum(game_count)) %>% # % overs
        mutate(over_pct_roll_lag=pcumsum(over_count)/pcumsum(game_count)) %>% # % overs prior-to
        mutate(over_pct_roll=rollapply(over_count, k, FUN=sum, 
                                       fill=NA, align="right")/k) %>% # % overs last k games
        # points scored for, against 
        mutate(score_avg_pts_for=cummean(score)) %>% 
        mutate(score_avg_pts_for_roll=rollapply(score,width=k,FUN=mean,fill=NA,align="right")) %>%
        mutate(score_avg_pts_for_roll_lag=lag(rollapply(score,width=k,FUN=mean,fill=NA,align="right"))) %>%
        mutate(score_avg_pts_against=cummean(score_against)) %>%
        mutate(score_avg_pts_against_roll=rollapply(score_against,width=k,FUN=mean,fill=NA,align="right")) %>%
        mutate(score_avg_pts_against_roll_lag=lag(rollapply(score_against,width=k,FUN=mean,fill=NA,align="right"))) %>%

        group_by(team,season) %>%
        mutate(wins_roll_season=cumsum(ifelse(win_count==1,1,0))) %>% # wins
        mutate(losses_roll_season=cumsum(ifelse(win_count==0.5,0,ifelse(win_count==1,0,1)))) %>% # losses
        mutate(ties_roll_season=cumsum(ifelse(win_count==0.5,1,0))) %>% # ties
        mutate(win_pct_roll_season=(cumsum(win_count)/cumsum(game_count))) %>% # winning %
        mutate(cover_pct_roll_season=cumsum(cover_count)/cumsum(game_count)) %>% # % covers the spreads 
        mutate(over_pct_roll_season=cumsum(over_count)/cumsum(game_count)) %>% # % overs 
        mutate(score_avg_pts_for_roll_season=cummean(score))%>% 
        mutate(score_avg_pts_against_roll_season=cummean(score_against))%>%
        arrange(team,schedule_date)


# team offense/defense avg pts scored/allowed + offense type
nflCalc$team_offense_type <- ifelse(is.na(nflCalc$score_avg_pts_for_roll_lag)==TRUE,"neutral",ifelse(nflCalc$score_avg_pts_for_roll_lag>24,"strong",ifelse(nflCalc$score_avg_pts_for_roll_lag<18,"weak","neutral")))
nflCalc$team_defense_type <- ifelse(is.na(nflCalc$score_avg_pts_against_roll_lag)==TRUE,"neutral",ifelse(nflCalc$score_avg_pts_against_roll_lag>24,"weak",ifelse(nflCalc$score_avg_pts_against_roll_lag<18,"strong","neutral")))

# table with W, L, T, Win %, Cover %, Over %
k=16
teamTable <- nflCalc %>%
        group_by(team, season) %>% 
        mutate(wins_roll_season=cumsum(ifelse(win_count==1,1,0))) %>% # wins
        mutate(losses_roll_season=cumsum(ifelse(win_count==0.5,0,ifelse(win_count==1,0,1)))) %>% # losses
        mutate(ties_roll_season=cumsum(ifelse(win_count==0.5,1,0))) %>% # ties
        mutate(cover_pct_roll_season=cumsum(cover_count)/cumsum(game_count)) %>% # % covers the spreads 
        mutate(over_pct_roll_season=cumsum(over_count)/cumsum(game_count)) %>% # % overs 
        mutate(score_avg_pts_for_roll_season=cummean(score))%>% 
        mutate(score_avg_pts_against_roll_season=cummean(score_against))%>%
        mutate(score_total_pts_for_roll_season=cumsum(score))%>% 
        mutate(score_total_pts_against_roll_season=cumsum(score_against))%>%
        slice(which.max(schedule_date)) %>%
        select(team,season, wins_roll_season,losses_roll_season,ties_roll_season,win_pct_roll_season,
               cover_pct_roll_season, over_pct_roll_season,
               score_avg_pts_for_roll_season,score_avg_pts_against_roll_season, 
               score_total_pts_for_roll_season,score_total_pts_against_roll_season) %>%
        arrange(team,season)

teamTable$win_pct_roll_season <- round(teamTable$win_pct_roll_season*100,digits=1)
teamTable$cover_pct_roll_season <- round(teamTable$cover_pct_roll_season*100,digits=1)
teamTable$over_pct_roll_season <- round(teamTable$over_pct_roll_season*100,digits=1)
teamTable$score_avg_pts_for_roll_season <- round(teamTable$score_avg_pts_for_roll_season,digits=1)
teamTable$score_avg_pts_against_roll_season <- round(teamTable$score_avg_pts_against_roll_season,digits=1)

teamTable <- subset(teamTable, teamTable$season>2017)
colnames(teamTable) <- c("Team","Season","W","L","T","Win %","Cover %","Over %","Off Pts/G","Def Pts/G", "Off Tot Pts","Def Tot Pts")
write.csv(teamTable,"teams.csv")

# elo for forecasting
eloForecast <- nflCalc %>%
        group_by(team) %>%
        slice(which.max(schedule_date)) %>%
        select(team,elo) 

# team offense/defense stats for forecasting
teamPointsForecast <- nflCalc %>%
        group_by(team)%>%
        slice(which.max(schedule_date)) %>%
        select(team,score_avg_pts_for_roll_lag,score_avg_pts_against_roll_lag,team_offense_type,team_defense_type) 

# bye week
teamByeWeeks <- nflCalc %>%
        group_by(team)%>%
        mutate(days_since_last_game= schedule_date-lag(schedule_date)) %>% # losses
        select(schedule_date,team,opponent, game_id,days_since_last_game) 

teamByeWeeks$schedule_bye <- ifelse(teamByeWeeks$days_since_last_game>13 & teamByeWeeks$days_since_last_game<21 ,"Bye Week",
                                    ifelse(teamByeWeeks$days_since_last_game<6 ,"Short Week",
                                           "Normal")
                                    )
#nflByeCalc$schedule_short_week <- FALSE # init with false value
#nflByeCalc$schedule_short_week <- ifelse(nflCalc$days_since_last_game<6,TRUE,FALSE)

# select variables needed
nflCalc <- nflCalc %>%
        select(game_id,schedule_date,season,schedule_week,team,opponent,venue,elo,
               score_avg_pts_for_roll_lag,score_avg_pts_against_roll_lag,team_offense_type,team_defense_type)

nflHome <- subset(nflCalc,nflCalc$venue %in% c("home"))
nflAway <- subset(nflCalc,nflCalc$venue %in% c("away"))

nflTemp <- merge(nflHome,nflAway,by=c("game_id","schedule_date","season","schedule_week"))
nflTemp <- nflTemp %>%
        select(game_id,schedule_date,score_avg_pts_for_roll_lag.x,score_avg_pts_against_roll_lag.x,
               score_avg_pts_for_roll_lag.y,score_avg_pts_against_roll_lag.y,team_offense_type.x,
               team_defense_type.x,team_offense_type.y,team_defense_type.y)
nfl <- merge(nfl,nflTemp,by=c("game_id","schedule_date"))

# weather variables   
nfl$weather_cold <- ifelse(is.na(nfl$weather_temperature),FALSE,ifelse(nfl$weather_temperature < 36,TRUE,FALSE))       
nfl$weather_wind_bad <- ifelse(is.na(nfl$weather_wind_mph),FALSE,ifelse(nfl$weather_wind_mph > 12,TRUE,FALSE))        
nfl$weather_rain <- grepl(c("Rain"),nfl$weather_detail, ignore.case=TRUE)    
nfl$weather_snow <- grepl(c("Snow"),nfl$weather_detail, ignore.case=TRUE)      
nfl$weather_fog <- grepl(c("Fog"),nfl$weather_detail, ignore.case=TRUE)      

nfl$team_offense_type.x <- as.factor(nfl$team_offense_type.x)
nfl$team_defense_type.x <- as.factor(nfl$team_defense_type.x) 
nfl$team_offense_type.y <- as.factor(nfl$team_offense_type.y)
nfl$team_defense_type.y <- as.factor(nfl$team_defense_type.y)
nfl$spread_favorite_cover_result <- as.factor(nfl$spread_favorite_cover_result)
nfl$spread_underdog_cover_result <- as.factor(nfl$spread_underdog_cover_result)

# models
train <- nfl[nfl$schedule_season>1979 & nfl$schedule_season<=2012,]
test <- nfl[nfl$schedule_season>2012,]

train <- subset(train, train$over_under_result %in% c("Over","Under")) # remove push
test <- subset(test, test$over_under_result %in% c("Over","Under")) # remove push

varsOver <- over_under_result ~ 
        team_home_elo_pre+team_away_elo_pre+
        score_avg_pts_for_roll_lag.x+score_avg_pts_against_roll_lag.x+
        score_avg_pts_for_roll_lag.y+score_avg_pts_against_roll_lag.y+
        team_offense_type.x+team_defense_type.x+
        team_offense_type.y+team_defense_type.y+
        weather_cold+weather_wind_bad+weather_rain+weather_snow+weather_fog

library(e1071)
library(rpart)
library(caret)
# classification over/under
fitOver <- rpart(varsOver, method="class",data=train)
plot(fitOver)
text(fitOver, cex=.5, use.n=TRUE, all=TRUE)
summary(fitOver)
confusionMatrix(predict(fitOver,test,type="class"),test$over_under_result)

# classification cover
#train <- subset(train, train$spread_favorite_cover_result %in% c("Cover","Did Not Cover")) # remove push
#test <- subset(test, test$spread_favorite_cover_result %in% c("Cover","Did Not Cover")) # remove push

varsSpread <- spread_favorite_cover_result ~ 
        division_matchup + team_home_favorite + schedule_week_1 + schedule_sunday + schedule_month +    
        team_home_elo_pre + team_away_elo_pre +
        score_avg_pts_for_roll_lag.x + score_avg_pts_against_roll_lag.x +
        score_avg_pts_for_roll_lag.y+ score_avg_pts_against_roll_lag.y +
#        team_offense_type.x+ team_defense_type.y +
#        team_offense_type.y+ team_defense_type.x +
        weather_cold+weather_wind_bad+weather_rain+weather_snow+weather_fog

fitSpread <- rpart(varsSpread, method="class",data=train)
plot(fitSpread)
text(fitSpread, cex=.5, use.n=TRUE, all=TRUE)
summary(fitSpread)
confusionMatrix(predict(fitSpread,test,type="class"),test$spread_favorite_cover_result)

fitSpreadPredict <- lm(spread_home_result ~ 
                               schedule_week_last + division_matchup +
                               team_home_elo_pre + team_away_elo_pre + 
                               team_offense_type.x + team_defense_type.y+
                               team_offense_type.y + team_defense_type.x+
                               team_home_favorite +
                               weather_wind_bad + weather_cold + weather_rain, data=train)
summary(fitSpreadPredict)

## for game predictions

# assign elo predicted scores

nflForecast$team_home_elo_predicted <- NA
nflForecast$team_away_elo_predicted <- NA

for (i in 1:nrow(nflForecast)) {
        for(j in 1:length(eloForecast$team)){
                if(nflForecast$team_home_id[i]==eloForecast$team[j]){
                        nflForecast$team_home_elo_predicted[i]<-eloForecast$elo[j]
                }
        }
}

for (i in 1:nrow(nflForecast)) {
        for(j in 1:length(eloForecast$team)){
                if(nflForecast$team_away_id[i]==eloForecast$team[j]){
                        nflForecast$team_away_elo_predicted[i]<-eloForecast$elo[j]
                }
        }
}

# assign offense/defense types and avg pts for/against by team
nflForecast$team_home_offense_type <- NA
nflForecast$team_home_defense_type <- NA
nflForecast$team_away_offense_type <- NA
nflForecast$team_away_defense_type <- NA

for (i in 1:nrow(nflForecast)) {
        for(j in 1:length(teamPointsForecast$team)){
                if(nflForecast$team_home_id[i]==teamPointsForecast$team[j]){
                        nflForecast$team_home_offense_type[i]<-teamPointsForecast$team_offense_type[j]
                        nflForecast$team_home_offense_avg_pts_for[i]<-teamPointsForecast$score_avg_pts_for_roll_lag[j]
                        nflForecast$team_home_defense_type[i]<-teamPointsForecast$team_defense_type[j]
                        nflForecast$team_home_defense_avg_pts_for[i]<-teamPointsForecast$score_avg_pts_against_roll_lag[j]
                        
                        
                }
        }
}

for (i in 1:nrow(nflForecast)) {
        for(j in 1:length(teamPointsForecast$team)){
                if(nflForecast$team_away_id[i]==teamPointsForecast$team[j]){
                        nflForecast$team_away_offense_type[i]<-teamPointsForecast$team_offense_type[j]
                        nflForecast$team_away_offense_avg_pts_for[i]<-teamPointsForecast$score_avg_pts_for_roll_lag[j]
                        nflForecast$team_away_defense_type[i]<-teamPointsForecast$team_defense_type[j]
                        nflForecast$team_away_defense_avg_pts_for[i]<-teamPointsForecast$score_avg_pts_against_roll_lag[j]
                        
                }
        }
}


# Winner predicted
nflForecast$team_home_win_prob <- winprob(nflForecast$team_home_elo_pre+55,nflForecast$team_away_elo_pre) # adj ELO for home team historically wins 58% games
nflForecast$team_away_win_prob <- 1-nflForecast$team_home_win_prob

nflForecast$team_winner_predicted <- ifelse(nflForecast$team_home_win_prob==nflForecast$team_away_win_prob,
                                   "PICK",ifelse(nflForecast$team_home_win_prob>nflForecast$team_away_win_prob,
                                                    paste0(as.character(nflForecast$team_home_id)," (",round(nflForecast$team_home_win_prob*100,digits=0),"%)"),
                                                    paste0(as.character(nflForecast$team_away_id)," (",round(nflForecast$team_away_win_prob*100,digits=0),"%)")))

nflForecast$team_winner_id_predicted <- ifelse(nflForecast$team_home_win_prob==nflForecast$team_away_win_prob,
                                            "PICK",ifelse(nflForecast$team_home_win_prob>nflForecast$team_away_win_prob,
                                                          nflForecast$team_home_id,
                                                          nflForecast$team_away_id))


nfl$team_winner_predicted <- ifelse(nfl$team_home_win_prob==nfl$team_away_win_prob,
                                            "PICK",ifelse(nfl$team_home_win_prob>nfl$team_away_win_prob,
                                                          paste0(as.character(nfl$team_home_id)," (",round(nfl$team_home_win_prob*100,digits=0),"%)"),
                                                          paste0(as.character(nfl$team_away_id)," (",round(nfl$team_away_win_prob*100,digits=0),"%)"))) 

nfl$team_winner_id_predicted <- ifelse(nfl$team_home_win_prob==nfl$team_away_win_prob,
                                    "PICK",ifelse(nfl$team_home_win_prob>nfl$team_away_win_prob,
                                                  nfl$team_home_id,nfl$team_away_id)) 


# Spreads 
nflForecast$spread_home_predicted <- -0.343262-0.023827*nflForecast$team_home_elo_predicted+0.021341*nflForecast$team_away_elo_predicted
nflForecast$spread_home_predicted <- ifelse(is.na(nflForecast$spread_home_predicted),-2.5,round((nflForecast$spread_home_predicted*2))/2)
nflForecast$spread_away_predicted <- -nflForecast$spread_home_predicted

nflForecast$team_favorite_id_predicted <- ifelse(nflForecast$spread_home_predicted==nflForecast$spread_home,"PICK",
                                                ifelse(nflForecast$spread_home_predicted-nflForecast$spread_home<0,
                                                       as.character(nflForecast$team_home_id),
                                                       as.character(nflForecast$team_away_id)))
nflForecast$team_winner_ats <- ifelse(nflForecast$spread_home_predicted==nflForecast$spread_home,
                                      paste0(nflForecast$team_favorite_id," (",nflForecast$spread_favorite,")"),
                                             ifelse(nflForecast$spread_home_predicted-nflForecast$spread_home<0,
                                                    paste0(nflForecast$team_home_id,ifelse(nflForecast$spread_home>0,c(" (+"),c(" (")),nflForecast$spread_home,c(")")),
                                                    paste0(nflForecast$team_away_id,ifelse(nflForecast$spread_away>0,c(" (+"),c(" (")),nflForecast$spread_away,c(")"))))


nfl$spread_home_predicted <- -0.343262-0.023827*nfl$team_home_elo_pre+0.021341*nfl$team_away_elo_pre
nfl$spread_home_predicted <- ifelse(is.na(nfl$spread_home_predicted),-2.5,round((nfl$spread_home_predicted*2))/2)
nfl$spread_away_predicted <- -nfl$spread_home_predicted
nfl$team_favorite_id_predicted <- ifelse(nfl$spread_home_predicted==nfl$spread_home,"PICK",
                                                 ifelse(nfl$spread_home_predicted-nfl$spread_home<0,
                                                        as.character(nfl$team_home_id),
                                                        as.character(nfl$team_away_id)))
nfl$team_winner_ats <- ifelse(nfl$spread_home_predicted==nfl$spread_home,
                              paste0(nfl$team_favorite_id," (",nfl$spread_favorite,")"),
                                      ifelse(nfl$spread_home_predicted-nfl$spread_home<0,
                                             paste0(nfl$team_home_id,ifelse(nfl$spread_home>0,c(" (+"),c(" (")),nfl$spread_home,c(")")),
                                             paste0(nfl$team_away_id,ifelse(nfl$spread_away>0,c(" (+"),c(" (")),nfl$spread_away,c(")"))))


# Over Under Predicted
nflForecast$weather_cold <- ifelse(is.na(nflForecast$weather_temperature),FALSE,ifelse(nflForecast$weather_temperature < 36,TRUE,FALSE))       
nflForecast$weather_wind_bad <- ifelse(is.na(nflForecast$weather_wind_mph),FALSE,ifelse(nflForecast$weather_wind_mph > 12,TRUE,FALSE))        
nflForecast$weather_rain <- grepl(c("Rain"),nflForecast$weather_detail, ignore.case=TRUE)    
nflForecast$weather_snow <- grepl(c("Snow"),nflForecast$weather_detail, ignore.case=TRUE)      
nflForecast$weather_fog <- grepl(c("Fog"),nflForecast$weather_detail, ignore.case=TRUE)      


nflForecast$score_predicted <- round(((nflForecast$team_home_offense_avg_pts_for+nflForecast$team_away_offense_avg_pts_for
                                      +nflForecast$team_home_defense_avg_pts_for+nflForecast$team_away_defense_avg_pts_for)/2),digits=1)

nflForecast$score_total_predicted <- round(34.7 +
                                                 0.001934*nflForecast$team_home_elo_predicted +
                                                 0.004540*nflForecast$team_away_elo_predicted +
                                                 ifelse(nflForecast$team_home_offense_type=="strong",3.495672,ifelse(nflForecast$team_home_offense_type=="weak",-1.387331,0))+
                                                 ifelse(nflForecast$team_away_defense_type=="strong",-1.880359,ifelse(nflForecast$team_away_defense_type=="weak",1.888973,0))+
                                                 ifelse(nflForecast$team_away_offense_type=="strong",2.691029,ifelse(nflForecast$team_away_offense_type=="weak",-1.176916,0))+
                                                 ifelse(nflForecast$team_home_defense_type=="strong",-1.867485,ifelse(nflForecast$team_home_defense_type=="weak",2.280479,0)),
                                         digits=0)

nflForecast$over_under_predicted <- ifelse(nflForecast$weather_wind_bad==TRUE,
                                      "Under",
                                      ifelse(nflForecast$score_total_predicted>nflForecast$over_under_line,
                                            "Over",
                                             "Under"))

nflForecast$over_under_pick <- ifelse(nflForecast$weather_wind_bad==TRUE,
                                      paste0("Under (",nflForecast$over_under_line,")"),
                                      ifelse(nflForecast$score_total_predicted>nflForecast$over_under_line,
                                                      paste0("Over (",nflForecast$over_under_line,")"),
                                                      paste0("Under (",nflForecast$over_under_line,")")))

nfl$team_home_offense_avg_pts_for <- nfl$score_avg_pts_for_roll_lag.x
nfl$team_away_offense_avg_pts_for <- nfl$score_avg_pts_for_roll_lag.y
nfl$team_home_defense_avg_pts_for <- nfl$score_avg_pts_against_roll_lag.x
nfl$team_away_defense_avg_pts_for <- nfl$score_avg_pts_against_roll_lag.y


nfl$score_predicted <- round(((nfl$team_home_offense_avg_pts_for+nfl$team_away_offense_avg_pts_for
                                       +nfl$team_home_defense_avg_pts_for+nfl$team_away_defense_avg_pts_for)/2),digits=1)

nfl$team_home_offense_type <- nfl$team_offense_type.x
nfl$team_away_offense_type <- nfl$team_offense_type.y
nfl$team_home_defense_type <- nfl$team_defense_type.x
nfl$team_away_defense_type <- nfl$team_defense_type.y

nfl$score_total_predicted <- round(34.7 +
                                                  0.001934*nfl$team_home_elo_pre +
                                                  0.004540*nfl$team_away_elo_pre +
                                                  ifelse(nfl$team_home_offense_type=="strong",3.495672,ifelse(nfl$team_home_offense_type=="weak",-1.387331,0))+
                                                  ifelse(nfl$team_away_defense_type=="strong",-1.880359,ifelse(nfl$team_away_defense_type=="weak",1.888973,0))+
                                                  ifelse(nfl$team_away_offense_type=="strong",2.691029,ifelse(nfl$team_away_offense_type=="weak",-1.176916,0))+
                                                  ifelse(nfl$team_home_defense_type=="strong",-1.867485,ifelse(nfl$team_home_defense_type=="weak",2.280479,0)),
                                          digits=1)

nfl$over_under_predicted <- ifelse(nfl$weather_wind_bad==TRUE,
                                           "Under",
                                           ifelse(nfl$score_total_predicted>nfl$over_under_line,
                                                  "Over",
                                                  "Under"))
nfl$over_under_predicted <- as.factor(nfl$over_under_predicted)

nfl$over_under_pick <- ifelse(nfl$weather_wind_bad==TRUE,
                                      paste0("Under (",nfl$over_under_line,")"),
                                      ifelse(nfl$score_total_predicted>nfl$over_under_line,
                                             paste0("Over (",nfl$over_under_line,")"),
                                             paste0("Under (",nfl$over_under_line,")")))

nfl2 <- merge(nfl,nflForecast,all.x=TRUE,all.y = TRUE)
nfl3 <- subset(nfl2, nfl2$schedule_season%in%2018)
nflGames <- nfl3[c("schedule_week","schedule_date","team_home_id","team_away_id",
                            "team_winner_predicted","team_winner_ats","over_under_pick")]
nflColumnNames <- c("schedule_week","Date","Home Team","Away Team","Winner Pick","Spread Pick","Over/Under Pick")
colnames(nflGames) <- nflColumnNames   
write.csv(nflGames, "games.csv")

# matrix
overUnderTable <- table(nfl$over_under_result,nfl$over_under_predicted)

# pick em file
#ifelse(nfl$team_home_favorite==TRUE&nfl$team_home_win_prob==0.5,0.5,
#       ifelse(nfl$team_home_favorite==TRUE&nfl$team_home_win_prob>.5,1,0))

# csv data files
nflPickem <- nfl2[c("schedule_week","schedule_date","team_home_id","team_away_id",
                    "team_winner_predicted","team_winner_ats","team_home_win_prob","team_away_win_prob","over_under_pick","score_total_predicted")]
write.csv(nflPickem,"nflpickem.csv")
nflScores <- nfl2[c("game_id","schedule_season","schedule_week","schedule_date","team_home_id","team_away_id","score_home","score_away","stadium_neutral","schedule_playoff")] # home/away team, scores
write.csv(nflScores, "scores.csv")
nflElo <- nfl2[c("game_id","schedule_season","schedule_week","schedule_date","team_home_id","team_away_id","team_home_elo_pre","team_away_elo_pre")] # elo rankings by game
write.csv(nflElo, "elo.csv")
nflSpreads <- nfl2[c("game_id","schedule_season","schedule_week","schedule_date","team_favorite_id","spread_favorite","over_under_line")] # spread, over under by game
write.csv(nflSpreads, "spreads.csv")
nflWeatherInfo <- nfl2[c("game_id","schedule_season","schedule_week","schedule_date","team_home_id","stadium","weather_temperature","weather_wind_mph","weather_humidity","weather_detail")] # weather info by game
write.csv(nflWeatherInfo, "weather.csv")
nflTeamScoring <- nfl2[c("game_id","schedule_season","schedule_week","schedule_date","team_home_id","team_away_id","score_avg_pts_for_roll_lag.x", "score_avg_pts_against_roll_lag.x", "score_avg_pts_for_roll_lag.y", "score_avg_pts_against_roll_lag.y")] # team avg points scored
write.csv(nflTeamScoring, "teamScoring.csv")

