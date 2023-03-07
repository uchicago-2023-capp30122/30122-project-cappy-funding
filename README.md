# **PROJECT CAPPY FUNDING**

## Project Overview

The main purpose of this project, Cappy Funding, is to visualize the allocation of federal fundings in the US to allow the audience to have a better sense of how funds at the federal level are spent on different industries and categories. Our expected target audience include federal foundation managers, funding seekers, and others who are interested in the way federal funds are spent. The complete data set contains a breakdown of federal funding by industry (using the NAICS categorisation) as well as by state.


Our project performs data visualization and analysis for federal funding expenditure from 2016-2020 in the following five ways:
1. Interactive Funding Heat Map of the US: illustrates how funding grants are distributed geographically to different states for each NAICS sector.
2. Interactive Scatter Plot on expenditure per capita of every state: illustrates how state expenditure per capita is correlated with population size.
3. Time-series Stacked Charts: illustrates how federal funding for each sector changes over time.
4. Interactive Scatter Plot for Expenditure per Capita and Funding per Capita: illustrates how state expenditure per capita is correlated with funding per capita in a given year and how the relationship changes over time.
5. Top 10 Categories Word Cloud: illustrates the top ten NAICS industries that have received the greatest amount of federal funds over the last five years.

Created by: Yujie Jiang, Ziyang Chen, Gongzi Chen, Bryan Foo


## Instructions to run the project in your local directory:

1. Clone the project repository to your local directory:
```
git clone git@github.com:uchicago-capp122-spring23/30122-project-cappy-funding.git
```

2. Go to the cloned repository:
```
cd 30122-project-cappy-funding/
```

3. Install Poetry
```
poetry install
```

4. Run the program:
```
poetry run python3 -m cappy_funding
```
