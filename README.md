# Permutation plotter

![Screenshot](_static/screenshot.png)

This tiny app was inspired by a [blog post by Andrew Gelman](https://statmodeling.stat.columbia.edu/2020/02/20/an-article-in-a-statistics-or-medical-journal-using-simulations-to-convince-people-of-the-importance-of-random-variation-when-interpreting-statistics/). It's intended to be mainly used as an educational tool.

The app takes a `csv` or an example dataset and let's the user decide which columns to plot against each other and then creates some subplots with permuted response.

Deployed on [Heroku](https://go.epfl.ch/permutationplotter).

## Todo: 
- Fit also some regression line 
- Let the use decide about the number of subplots (?)
- Automatically explore all columns (?)
- Add labels for sliders
- Drop all non-numeric columns
- Feedback for selected column (maybe show df below upload field and highlight column)
- Overflow of selection