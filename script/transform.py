import pandas as pd
import os
import boto3


key = "%(name)s/%(name)s_%(time)s.jsonl"

def parseV2(filePath):
    #description col moved to a diff index with the new scraper changes, so i changed index 6 to 8
    AWS_S3_BUCKET = os.getenv("linkedin-scraper-1")
    AWS_ACCESS_KEY_ID = os.getenv("AKIAYUJWZRTZRRGQ3JVV")
    AWS_SECRET_ACCESS_KEY = os.getenv("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")



    s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    
    
    df = pd.read_json(
    f"s3://{AWS_S3_BUCKET}/{filePath}",
    storage_options={
        "key": AWS_ACCESS_KEY_ID,
        "secret": AWS_SECRET_ACCESS_KEY,
        "token": AWS_SESSION_TOKEN,
        },)
    
    #df = pd.read_json(file)

    rejectTitles = ['manager','consultant','vice president','vp','lead','intern','senior','c++','c#','sr','sr.','director','principal','architect']

    cleanTitlesList = [df.iloc[i:i+1,:] for i in range(len(df.index)) if not(any(word in df.title[i].lower() for word in rejectTitles))]
    df = pd.concat(cleanTitlesList,sort=False, ignore_index=True)
    rejectDesc = ['2','3','4','5','6','7','8','9','10','12','15','two','three','four','five','six','seven','eight','nine','ten','fifteen']

    cleanRecordIndices=[]

    for i in range(df.shape[0]):
        #i use iloc '6' cuz that's the index of the 'description' colm.
        paraSplitted = df.iloc[i,8].replace(","," ").replace('+'," ").replace('/'," ").replace("'"," ").replace("-"," ").replace('('," ").replace(')'," ").lower().split()
        expIndices = [i for i in range(len(paraSplitted)) if 'experience' == paraSplitted[i]]

        switch = True
        for instIndex in expIndices:
            if any(x in paraSplitted[instIndex-10:instIndex+10] for x in rejectDesc):
                switch = False
                break
        if switch is True:
            cleanRecordIndices.append(i)
    cleanRecords = [ df.iloc[i:i+1,:] for i in cleanRecordIndices ]
    df = pd.concat(cleanRecords,sort=False, ignore_index=False)
    return df

