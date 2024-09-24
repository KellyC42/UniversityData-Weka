# Filename:    csvToArff.py
# Description: Reads data from the csv files and
#              outputs relevant data into an arff file.
#              Ran using Python 3.8
import csv
import re

salary_c  = 'csv/salary_by_college.csv'
rank_cwur = 'csv/ranking_cwur.csv'
rank_shan = 'csv/ranking_shanghai.csv'
rank_time = 'csv/ranking_times.csv'

schoolNames = [] # school names that have salary data


# Function: getSchoolNames
# Description: gets all school names which have data for
#              alumni salaries and stores in 'schoolNames'
def getSchoolNames():
    with open(salary_c, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # remove school name abreviation in parenthesis (ie (MIT))
            name = re.sub(r'\([^()]*\)', '', row['School Name'])
            schoolNames.append(name.strip())

            
# Function: getRankingNames
# Description: gets names of schools where salary data exists for given ranking file
def getRankingNames(filename, rowName):
    schools = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = re.sub(r'\([^()]*\)', '', row[rowName])
            if row['year'] == '2015' and name in schoolNames:
                schools.append(name)
    return schools


# Function: getSalaryData
# Description: gets salary data for the specified school
def getSalaryData(school):
    with open(salary_c, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sName = re.sub(r'\([^()]*\)', '', row['School Name']).strip()
            if(sName == school):
                data = [row['School Type'].replace(' ', '_'),
                        row['Starting Median Salary'][1::].replace(',',''), 
                        row['Mid-Career Median Salary'][1::].replace(',',''), 
                        row['Mid-Career 10th Percentile Salary'][1::].replace(',',''),
                        row['Mid-Career 25th Percentile Salary'][1::].replace(',',''),
                        row['Mid-Career 75th Percentile Salary'][1::].replace(',',''),
                        row['Mid-Career 90th Percentile Salary'][1::].replace(',',''),
                ]
                for i in range(0, len(data)):
                    if data[i] == '/A' or data[i] == 'N/A': # fix missing data
                        data[i] = '?'
                return data
    print('Error: Could not find', school)
    exit(-1)


# Function: getCwurData
# Description: gets data from CWUR rankings
def getCwurData(schools):
    data = []
    data.append(['University', 'GlobalRank', 'PrizeWinningAlumni',
                 'AlumniCEOPositions', 'FacultyPrizeScore', 'PublicationScore',
                 'HQPublicationScore', 'InfluenceScore', 'PatentScore',
                 'SchoolType', 'StartingMedian', 'MidMedian',
                 'Mid10th', 'Mid25th', 'Mid75th', 'Mid90th', 
    ])
    with open(rank_cwur, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['year'] == '2015' and row['institution'] in schools:
                salary = getSalaryData(row['institution'])
                data.append([row['institution'],
                             row['world_rank'],
                             row['quality_of_education'],
                             row['alumni_employment'],
                             row['quality_of_faculty'],
                             row['publications'],
                             row['influence'],
                             row['citations'],
                             row['patents'],
                             salary[0], salary[1], salary[2], salary[3],
                             salary[4], salary[5], salary[6],
                ])
    return data


# Function: getShanData
# Description: gets data from Shanghai rankings
def getShanData(schools):
    data = []
    data.append(['University', 'GlobalRank', 'PrizeWinningAlumni',
                 'FacultyPrizeScore', 'HighlyCitedResearchers',
                 'NatureSciencePaperScore', 'SocialSciencePaperScore',
                 'PerCapitaPerformance',
                 'SchoolType', 'StartingMedian', 'MidMedian',
                 'Mid10th', 'Mid25th', 'Mid75th', 'Mid90th', 
    ])
    with open(rank_shan, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['year'] == '2015' and row['university_name'] in schools:
                salary = getSalaryData(row['university_name'])
                world_rank = row['world_rank']
                # rank has range sometimes, get average
                if '-' in world_rank:
                    index = world_rank.find('-')
                    one = world_rank[0:index]
                    two = world_rank[index+1::]
                    world_rank = str((int(one)+int(two)) / 2)

                data.append([row['university_name'],
                             world_rank,
                             row['alumni'],
                             row['award'],
                             row['hici'],
                             row['ns'],
                             row['pub'],
                             row['pcp'],
                             salary[0], salary[1], salary[2], salary[3],
                             salary[4], salary[5], salary[6],
                ])
    return data


# Function: getTimesData
# Description: gets data from Times rankings
def getTimesData(schools):
    data = []
    data.append(['University', 'GlobalRank', 'TeachingScore',
                 'ResearchScore', 'CitationScore',
                 'NumStudents', 'StudentStaffRatio', 
                 'SchoolType', 'StartingMedian', 'MidMedian',
                 'Mid10th', 'Mid25th', 'Mid75th', 'Mid90th', 
    ])
    with open(rank_time, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['year'] == '2015' and row['university_name'] in schools:
                salary = getSalaryData(row['university_name'])
                world_rank = row['world_rank']
                # rank has range sometimes, get average
                if '-' in world_rank:
                    index = world_rank.find('-')
                    one = world_rank[0:index]
                    two = world_rank[index+1::]
                    world_rank = str((int(one)+int(two)) / 2)
                data.append([row['university_name'],
                            world_rank,
                            row['teaching'],
                            row['research'],
                            row['citations'],
                            row['num_students'],
                            row['student_staff_ratio'],
                            salary[0], salary[1], salary[2],
                            salary[3], salary[4], salary[5], salary[6],
                ])
    return data


# Function: cleanBlanks
# Description: replaces missing data with '?'
def cleanBlanks(dataset):
    for i in range(0, len(dataset)):
        dataset[i][0] = dataset[i][0].replace("-", "")
        dataset[i][0] = dataset[i][0].replace(",", "")
        dataset[i][0] = dataset[i][0].replace(" ", "_")

        for j in range(1, len(dataset[i])):
            data = dataset[i][j]
            if (data == '' or data == ' ' or
                data == '-' or data == 'N/A' or data == '/A'):
                dataset[i][j] = '?'
    return dataset


# Function: writeToArff
# Description: converts dataset to arff format and writes to file
def writeToArff(dataset, filename):
    f = open(filename + '.arff', 'w')
    f.write('@relation ')
    f.write(filename)
    f.write('\n\n@attribute University string\n@attribute GlobalRank numeric\n')
    attributes = dataset[0]
    for i in range(2, len(attributes)):
        if attributes[i] == 'SchoolType':
            f.write('@attribute ' + attributes[i] +
                    ' {Engineering,Party,Liberal_Arts,Ivy_League,State}\n')
        else:
            f.write('@attribute ' + attributes[i] + ' numeric\n')

    f.write('@data\n')
    for i in range(1, len(dataset)):
        for j in range(0, len(dataset[i])):
            f.write(dataset[i][j])
            if j != len(dataset[i])-1:
                f.write(',')
        f.write('\n')

    f.write('\n\n')
    f.close()


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    getSchoolNames()

    cwurSchools = getRankingNames(rank_cwur, 'institution')
    shanSchools = getRankingNames(rank_shan, 'university_name')
    timesSchools = getRankingNames(rank_time, 'university_name')

    cwurData = getCwurData(cwurSchools)
    shanData = getShanData(shanSchools)
    timesData = getTimesData(timesSchools)

    cwurData = cleanBlanks(cwurData)
    timesData = cleanBlanks(timesData)
    shanData = cleanBlanks(shanData)

    writeToArff(cwurData, 'cwurDataRaw')
    writeToArff(timesData, 'timesDataRaw')
    writeToArff(shanData, 'shanDataRaw')
    
    '''
    print('Salary #:', len(schoolNames))
    print('CWUR #:', len(cwurSchools))
    print('Shan #:', len(shanSchools))
    print('Time #:', len(timesSchools))
    '''
