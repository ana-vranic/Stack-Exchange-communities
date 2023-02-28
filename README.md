# StackExchange-communities

This code is used in paper: 

Vranić, A., Tomašević, A., Alorić, A. et al. [Sustainability of Stack Exchange Q&A communities: the role of trust](https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-023-00381-x). EPJ Data Sci. 12, 4 (2023). https://doi.org/10.1140/epjds/s13688-023-00381-x

## Data

Communities are categorized as:

-  closed or "Area 51" 
-  active or beta communities 

Area 51 community filenames have prefix denoting the date origin of the StackExchange archive file containing the data. For example: `050112astronomy` folder is related to Area 51 version of the astronomy community, while `astronomy` refers to the beta astronomy community.


### XML raw data
Beta Stack Exchange communities are available [here](https://archive.org/details/stackexchange).

Area 51 Stack Exchange communities can be downloaded from [Area51](https://area51.stackexchange.com/).

`data/raw_data/...`
From raw xml data we select questions, answers, comments, accepted_answers, users and votes for the first 180 days of each community. 

---

### Interactions

`data/interactions/...`

For each community we have several .csv files containing all recorded interactions of a given type. These CSV files are obtained by transforming raw XML data using code provided in `src/data_preparation`.

- `...interactions_post_questions.csv` Posted questions
- `...interactions_questions_answers.csv` Questions and answers
- `...interactions_comments.csv` All posted comments
- `...interactions_comments_questions.csv` Comments posted directly on a question
- `...interactions_comments_answers.csv` Comments posted on answers
- `...interactions_acc_answers.csv` Accepted answers
- `...interactions_votes.csv` Votes cast on questions, answers and comments

Detailed explanation of the columns of these .csv files are given [here](https://meta.stackexchange.com/questions/2677/database-schema-documentation-for-the-public-data-dump-and-sede).

---

### Reputations

`data/reputations/...`

Values of dynamic reputation for each user for each of 180 days in given communites are stored as CSV files. `eng` refers to engagement reputation and `pop` refers to popularity reputation.

Each row of CSV is unique user in a given community and each column is each day starting from 0 (first day).

---
## Code

- `src/data_preparation` holds several scripts needed to transform original XML StackExchange raw data into time-stamped record of interactions of a given type. [Data Preparation Pipeline](src/data_preparation/readme.md) explains the run order and the ouput of the scripts.

- `src/dynamical_reputation.py` is the main module for estimating dynamical reputation in StackExchange communities.
`src/calculate_dynamical_reputation.ipynb` shows usage of calculating dynamical reputation.

- `src/calculate_core_periphery.ipynb` is a notebook for calculating core-periphery structure (we use [Bayesian Core-Periphery Stochastic Block Models](https://github.com/ryanjgallagher/core_periphery_sbm), while `src/core_periphery_functions.py` contains  functions for transforming data into appropriate input and saving results into hdf5 format.

- `src/data_processing.ipynb` is script for calculating the evolution of dynamical reputation, network and core-periphery properties. The results are stored in `data/processed data`, so they can be directly used for plotting figures   
    
- `Figures.ipynb` is notebook for plotting results. Script `src/drawing_functions.py` holds different drawing functions.



