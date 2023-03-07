# **PROJECT CAPPY FUNDING**

## Project Overview

The main purpose of this project, Cappy Funding, is to visualize the allocation of federal fundings in the US so that to help audiences have better sense of where the money is going. Target audience are federal foundation managers, funding seekers, and anyone who’s interested in the funding distribution of the public sector. The complete data set is going to contain the federal fundings that goes to a certain industry (e.g. education, healthcare) in every state in the US. 


Our project is expected to perform data visualization and analysis from the following four ways:
1. Interactive Funding Heat Map of the US: see how much of the grant amount has flown to a certain industry in a certain state, and get its weight in this state's total federal fundings to see if the federal foundation has funded much in this industry.
2. Interactive Scatter Graph on expenditure per capita of every state.
3. Time-series Stacked Charts: time series analysis to see the change in the categories that federal funding has focus on. 
4. Interactive Time-series Change in Relation between expenditure per capita and fundings per capita: to see the correlation between expenditure and funding amounts.  
5. Top 10 Categories Word Cloud: find the top 10 industries that receive most fundings separately for five years, and make it a word cloud depending on the ranking

Done by: Yujie Jiang, Ziyang Chen, Gongzi Chen, Bryan Foo


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
