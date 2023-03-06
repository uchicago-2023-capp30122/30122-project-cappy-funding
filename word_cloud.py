import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def funding_word_clouds():
    """
    Create word cloud graphs for each year between 2016 and 2020 based on 
    federal funding by NAICS category.
    """

    df = pd.read_csv('us_funding_time_series.csv')

    # load the funding image
    funding_mask = np.array(Image.open("Funding2.png"))

    # loop through the years
    for year in range(2016, 2021):
        # create a dictionary that contains the NAICS category as the key and the funding percentage for the current year as the value
        category_weight = {}
        for _, row in df.iterrows():
            category = row['NAICS Category']
            weight = row[str(year)]
            category_weight[category] = weight

        # sort the dictionary by value in descending order and select the top 10 categories
        top_categories = dict(sorted(category_weight.items(), key=lambda item: item[1], reverse=True)[:10])

        # create a word cloud object and generate the word cloud using the dictionary and the funding image as the mask
        wordcloud = WordCloud(width = 800, height = 800, 
                        background_color ='white', 
                        min_font_size = 7,
                        max_words = 50,
                        mask = funding_mask, # use the funding image as the mask
                        contour_width=1,
                        contour_color='lightgrey',
                        colormap='tab20',
                        scale=2
                    ).generate_from_frequencies(top_categories)

        # plot the word cloud using matplotlib
        plt.figure(figsize = (10, 10), facecolor = None) 
        plt.imshow(wordcloud, aspect='auto')
        plt.axis("off") 
        plt.tight_layout(pad = 0) 
        plt.title(f"Word Cloud of NAICS Category for {year}", fontsize=20)
        plt.show()