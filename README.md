# NBA Z-Score Generator

NBA Z-Score Generator is a function that returns a JSON object that contains the corresponding total z-score of every basketball player in the NBA. The purpose of a Z-Score is to calculate how many standard deviations each player is above or below the league average in every significant statistical category. This is more accurate in terms of evaluating players in comparison to just looking a raw statistics or per game statistics relative to the rest of the league.

## Getting Started

Just install the prerequiste technologies listed below and run scrape_bbr.py.

### Prerequisites

What things you need to install the software and how to install them

```
Requires Python 3 and above. 
Requires the following packages to be installed: BeautifulSoup (bs4), Boto3, requests, datetime, statistics
```

### Installing

Install Python 3.0 and above!

## Deployment

TBD

## Built With

* [Python](https://docs.python.org/3/) - Language used
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Web Scraper Library


## Authors

* **Sam Morehouse** - *Initial work* - [smorehouse](https://github.com/smorehouse)
* **Darren He** - *Extended functions* - [darrenche](https://github.com/darrenche)


## Acknowledgments

Thanks to Sam Morehouse (github: smorehouse) for writing the web scraper function to scrape the raw data from basketball reference (https://www.basketball-reference.com/leagues/NBA_2019_totals.html)
