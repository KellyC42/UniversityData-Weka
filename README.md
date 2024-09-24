The first data set is of World University Rankings from kaggle and consists of three ‘.csv’ files
from separate university ranking websites. These rankings are from Times Higher Education, Academic
Ranking of World Universities (also known as the Shanghai Ranking), and The Center for World
University Rankings (CWUR).
The second data set is also from kaggle and is of Salaries By College Type. These statistics are
from The Wall Street Journal.
This means a total of four ‘.csv’ files, one from each of the three ranking websites and one with
salary data. The salary data needs to be combined with each university ranking file, resulting in a total
of three ‘.arff’ files for analysis.

# b
The intended goal for analyzing this data set is to determine which aspects of a university are
most relevant or least relevant for determining the alumni’s future income. Each set of ranking data
uses their own factors and weights for determining the overall score and global rank so, the
methodology is highly debated. For example, the Shanghai Ranking places a higher importance on
Research Output than the other two. Therefore, the previous analysis will be extended to examine
salary data using their indicators and ignoring their final ranking.
By performing analysis on each data set separately, it will give more accurate information on
the most important aspects for predicting future alumni salary. Each analysis will be repeated for each
data set, and the results will be compared. CWUR, Shanghai, and Times may all give varying results
for which factors are the most important, so it is important to compare what they have in common (to
conclude important factors) or what is different (to conclude irrelevant factors).

# c
In order to combine the three university ranking datasets with the alumni salary data set, a
Python script was created. If information existed on alumni salaries and there was also university
ranking data, then the university was added to a new data set. From the salary data, the ‘Starting
Median Salary’, ‘Mid-Career Median Salary’, and ‘Mid-Career 10th’, ‘25th’, ‘27th’, and ‘90th Percentile
Salary’ was included.
From the ranking data, since each ranking source used different factors to calculate their rank,
there is different data for each university. For example, CWUR is the only ranking that uses a ‘High
Quality Publication Score’ which is measured by the number of research papers appearing in
prestigious journals. Times Higher Education has information on number of students and the student-
to-staff ratio, and Shanghai uses more detailed information on the number and types of published
papers. All of these had the alumni salary data added and irrelevant indicators were thrown out (such as
Country and Total Score). Then the results were simply converted into an ‘.arff’ format.
The Python script results in three ‘.arff’ files, combining CWUR, Shanghai, and Times with the
salary data to produce ‘cwurDataRaw.arff’, ‘shanDataRaw.arff’, and ‘timesDataRaw.arff’ respectively.
Then, using Weka, the University Name and Global Ranking was deleted as well as all salary data
except for ‘Mid-Career Median Salary’. The Mid-Career Salary was then moved to the bottom.
These Modified files can be used for examining the ‘Mid-Career Salary’ and the raw files will
later be re-modified to only have one of each “salary data” (such as ‘Starting Median Salary’ or ‘25th
Percentile Median Salary’). This way, the data shows if a certain indicator is more important for an
alumni’s salary immediately following graduation as well as which indicators are more important for
the top and bottom percentile earners.
A minor problem when combining the salary data was that university names would be recorded
differently, such as one data set would have “Massachusetts Institute of Technology” and the other
would have “Massachusets Institute of Technology (MIT)”. To fix this, their names were modified to
remove enclosed parenthesis, stripped of trailing/leading whitespace, and spaces were replaced with
underscores.

# d
By knowing which aspects a university needs to have so that the alumni are most likely to have
a larger salary, universities can then prioritize those aspects and put less importance on irrelevant
factors. For example, a university can put a higher budget on hiring more qualified instructors, or by
providing smaller class sizes to attain a smaller student-to-faculty ratio. They can also see if an
instructor having more published papers and/or prizes in their field will result in a higher student salary.
When high-school graduates are trying to decide on which university to attend, they can use the
results of this analysis to compare schools. In order to determine where they want to go, examining the
university’s data on published papers (for example) may be the deciding factor.

# e
Weka’s Regression analysis will be used to determine the which factors are most influential on
alumni salary. About 60% of the data will be put into a training set and the remaining will be in a test
set. This way, the impact on salary can be viewed and the most important factors can be determined.
After the most and least influential factors are found, universities can then prioritize the
important ones and put less priority on the irrelevant ones.