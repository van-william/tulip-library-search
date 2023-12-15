import requests
import json
import pandas as pd
import openai
import os
import sys

def prepare_prompt(question):
    response = requests.get('https://api.library.tulipintra.net/v2/assets')
    body = response.content
    body_json = json.loads(body)        

    apps = body_json['apps']
    df_apps = pd.DataFrame(apps)
    apps = body_json['apps']
    # app_groups = body_json['appGroups']
    df_apps = pd.DataFrame(apps)
    # df_app_groups = pd.DataFrame(app_groups)

    df_union = df_apps #pd.concat([df_apps, df_app_groups])


    #df_apps.columns
    df_union_col = ['description','marketingHeadline', 'name', 'slug']
    df_union = df_union[df_union_col] 
    df_union['url'] = 'https://tulip.co/library/apps/'+df_union['slug']
    df_union = df_union.drop(columns='slug')

    df_union_json = df_union.to_json(orient='split')
    prompt = f"""please provide an answer to the question belowing use the DataFrame {df_union_json} as context. 
    You are an AI library assistant skilled in manufacturing and frontline operations. Based upon the question, please recommend some of the apps provided in the json dataframe. 
    Please provide some context on the recommendation, and the url for viewing. Please provide around 3-5 recommended app sorted by relevance. If there are fewer than 5 relevant apps, 
    only include apps which are relevant.
    For example, if there is only 1 app that is extremely relevant, only include that.
    Please output the format in markdown format for easy viewing. for output mimic the following format:
    Name of app(with hyperlink to url): Headline
    Description 
    
    Please include spacing between the recommended apps
    Question below:
    {question}
    """
    return prompt
