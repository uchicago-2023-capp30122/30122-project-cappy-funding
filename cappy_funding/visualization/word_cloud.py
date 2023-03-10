import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# Author: Ziyang Chen

def funding_word_clouds(filepath):
    """
    Create word cloud graphs for each year between 2016 and 2020 based on 
    federal funding by NAICS category.
    """

    # load the data
    df = pd.read_csv(filepath + 'us_funding_time_series.csv')

    # define a custom color map
    meranti_colors = ['#FC766AFF', '#5B84B1FF', '#D8BFD8FF', '#DC143CFF', '#3C3C3CFF']
    meranti_colors_rgb = [mcolors.hex2color(color) for color in meranti_colors]
    meranti_cmap = mcolors.LinearSegmentedColormap.from_list('meranti', meranti_colors_rgb)

    # define a custom word cloud shape
    x, y = np.ogrid[:300, :300]
    mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
    mask = 255 * mask.astype(int)

    # iterate over the years and get the top 10 categories for each year
    for year in range(2016, 2021):
        # select rows where funding for the given year is not null
        not_null_rows = df.loc[df[f"{year}"].notnull()]

        # sort the not-null rows by funding percentage in descending order and select the top 5 categories
        top_5_categories = not_null_rows.sort_values(by=f"{year}", ascending=False).head(5)

        # extract the category names as a list, filter out any category containing "service", and join them with double quotes to ensure they stay as a whole
        category_list = [f'"{name}"' for name in top_5_categories["NAICS Category"].tolist()]

        # combine the category names into a single string
        text = ' '.join(category_list)
        text = text.replace("Services", " ")

        # create a word cloud object with custom color map and mask
        wordcloud = WordCloud(background_color="white", colormap=meranti_cmap, mask=mask).generate(text)

        # plot the word cloud
        plt.figure(figsize=(8, 8))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title(f"Word Cloud of NAICS Category for {year}", fontsize=20, fontweight='bold')
        plt.tight_layout(pad=0)

        # Save word clouds to file
        plt.savefig(f'./cappy_funding/visualization/word_cloud_{year}.png', bbox_inches='tight')