import boto3
import pandas as pd
from io import BytesIO
from datetime import datetime
from common.schema import PprCleanAll
from common.base import session
from sqlalchemy import text
import csv
from word2number import w2n



"""    
def _old_transform(df):    
rejectTitles = ['manager','consultant','vice president','vp','lead',
                'intern','senior','c++','c#','sr','sr.','director',
                'principal','architect']
cleanTitlesList = [df.iloc[i:i+1,:] 
                    for i in range(len(df.index)) 
                    if not(any(word in df.title[i].lower() 
                                for word in rejectTitles))]
df = pd.concat(cleanTitlesList,sort=False, ignore_index=True)

rejectDesc = ['2','3','4','5','6','7','8','9','10','12','15','two',
                'three','four','five','six','seven','eight','nine',
                'ten','fifteen']
cleanRecordIndices=[]
for i in range(df.shape[0]):
    #i use iloc '6' cuz that's the index of the 'description' colm.
    paraSplitted = df.iloc[i,8].replace(","," ").replace('+'," ")\
                .replace('/'," ").replace("'"," ").replace("-"," ")\
                .replace('('," ").replace(')'," ").lower().split()
    expIndices = [i for i in range(len(paraSplitted)) 
                    if 'experience' == paraSplitted[i]]

    switch = True
    for instIndex in expIndices:
        if any(x in paraSplitted[instIndex-10:instIndex+10] 
                for x in rejectDesc):
            switch = False
            break
    if switch is True:
        cleanRecordIndices.append(i)

cleanRecords = [ df.iloc[i:i+1,:] for i in cleanRecordIndices ]
df = pd.concat(cleanRecords,sort=False, ignore_index=False)
return df
"""

def load_data_from_s3(s3FileName):
    
    # Setup variables
    bucket = "linkedin-scraper-1"
    s3FileName = f'/linkedin/{s3FileName}' 

    # Initialize s3
    s3 = boto3.resource('s3')
    
    # Reading CSV into DF  
    obj = s3.Object(bucket, s3FileName)
    with BytesIO(obj.get()['Body'].read()) as bio:
        df = pd.read_csv(bio)

    return df


#! Never drop anything in transform. Only transform.
def transform(df):
    counter = 0
    
    years_to_colum = ['0','1','2','3','4','5','6','7','8','9','10','12','13','14','15']
    
    tag_filters = ['sql','python','airflow','etl','snowflake','aws','azure','gcp','bigquery','spark',
                        'hadoop','hive','lambda','dbt', 'google','amazon','microsoft','bi','tableau',
                   'power','looker', 'excel','javascript','react','vue']
    
    years = ['1','2','3','4','5','6','7','8','9','10','12','13','14','15',
             'one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve',
            'thirteen','fourteen','fifteen']
        
    for year in years_to_colum:
        df[year]=0
        
    for tag in tag_filters:
        df[tag]=0
    
    for i in range(df.shape[0]):
        paraSplitted = df.loc[i,'description'].replace(","," ").replace('+'," ").replace('/'," ").replace("'"," ").replace("-"," ").replace('('," ").replace(')'," ").lower().split()

        # Marking tags
        for word in paraSplitted:
            for tag in tag_filters:
                if tag == word:
                    df.loc[i,tag]=1
        
        
        # Marking years
        expIndices = [i for i in range(len(paraSplitted)) if 'experience' == paraSplitted[i]]
        counter = counter + len(expIndices)
        blank_exp = 0
        for instance_of_exp in expIndices:
            count = 0
            for year in years:
                
                # ex: " 2-5 of experience..."; no line will mention more than 2 numbers 
                if count == 2:
                    break
                
                # Marks years 1 -15
                if year in paraSplitted[instance_of_exp-10:instance_of_exp+10]:
                    
                    # Marks single digit years, 1 - 9
                    if len(year) == 1 or len(year)==2:
                        df.loc[i,str(year)]=1
                        count += 1
                        
                    # Marks years 10-15
                    else:
                        df.loc[i,str(w2n.word_to_num(year))]=1
                        count += 1
                
                # Marks jobs with no specific YoE req.
                else:
                    if year == years[-1]:
                        print('index : ' + str(i) + " lenIndices : " + str(len(expIndices)) + ", & expInstance : " + str(instance_of_exp))
                        blank_exp += 1
                        if blank_exp == len(expIndices):
                            df.loc[i,'0']= 1
                        
    return df




def push_data_to_snowflake(df):
    """
    Apply all transformations for each row in the .csv file before saving it 
    into database
    """
    
    # Initialize an empty list for our PprCleanAll objects
    ppr_clean_objects = []
    for i in range(df.shape[0]):
        
        # Apply transformations and save as PprCleanAll object
        for column in df.columns:
            ppr_clean_objects.append(
                PprCleanAll(
                    column = df.loc[i,column]
                )
            )

    # Save all new processed objects and commit
    session.bulk_save_objects(ppr_clean_objects)
    session.commit()

def main(s3FileName):
    df = load_data_from_s3(s3FileName)
    transformed = transform(df)
    df = transformed[0]
    columns = transformed[1]
    push_data_to_snowflake(df, columns)


if __name__ == '__main__':
    df = load_data_from_s3("linkedin/linkedin_2022-12-14T22-42-40.csv")
    transformed = transform(df)
    print(df)
    df = transformed
    push_data_to_snowflake(df)
