import redshift_connector
import pandas as pd
import os
import requests
import json
import numpy as np


def query_top_installs():
    HOST = os.getenv('REDSHIFT_HOST')
    DATABASE = os.getenv('REDSHIFT_DB')
    USER = os.getenv('REDSHIFT_USER')
    PASSWORD = os.getenv('REDSHIFT_PASSWORD')

    conn = redshift_connector.connect(
        host=HOST,
        database=DATABASE,
        user=USER,
        password=PASSWORD
    )

    cursor = conn.cursor()

    query = """
    WITH top_installs AS (
    SELECT 
        asset_id,
        asset_type,
        count(*) AS install_count
    FROM "cds"."tbllibraryinstalls"
    WHERE created_at >= current_date - interval '30 days'
    and asset_id is not null
    GROUP BY asset_id, asset_type
    ORDER BY install_count DESC
    LIMIT 50
    )
    select
    t."name" ,
    i.asset_type,
    i.install_count,
    i.asset_id, 
    t.asset_page_url 
    FROM top_installs i
    join cds.tbllibraryasset t on t.asset_id = i.asset_id 
    """
    cursor.execute(query)
    df_installs = cursor.fetch_dataframe()
    cursor.close()
    conn.close()
    # pull marketing descriptions
    response = requests.get('https://api.library.tulipintra.net/v2/assets')
    body = response.content
    body_json = json.loads(body)  
    apps = body_json['apps']
    df_apps = pd.DataFrame(apps)

    app_groups = body_json['appGroups']
    df_app_groups = pd.DataFrame(app_groups)

    connectors = body_json['connectors']
    df_connectors = pd.DataFrame(connectors)

    df_union = pd.concat([df_apps, df_app_groups, df_connectors])
    df_union_col = ['description','marketingHeadline', 'assetId']
    df_union = df_union[df_union_col] 

    install_table = pd.merge(df_installs, df_union, left_on='asset_id', right_on='assetId')

    install_table = install_table.drop(columns=['asset_id', 'assetId', 'description'])

    install_table = install_table[['name','asset_type', 'marketingHeadline', 'install_count', 'asset_page_url']]

    install_table = install_table.rename(columns={
        'asset_type': 'content type',
        'install_count': 'installs',
        'marketingHeadline': 'summary',
        'asset_page_url':'link'
    })

    install_table = install_table.sort_values(by='installs', ascending=False)

    install_table = install_table.reset_index(drop=True)
    

    # Modify the index to start with 1 instead of 0
    install_table.index = install_table.index + 1

    install_table = install_table.drop(columns=['installs'])
    return install_table



def most_recent_content():
    HOST = os.getenv('REDSHIFT_HOST')
    DATABASE = os.getenv('REDSHIFT_DB')
    USER = os.getenv('REDSHIFT_USER')
    PASSWORD = os.getenv('REDSHIFT_PASSWORD')

    conn = redshift_connector.connect(
        host=HOST,
        database=DATABASE,
        user=USER,
        password=PASSWORD
    )

    cursor = conn.cursor()

    query = """
    SELECT asset_id, asset_page_url  FROM cds.tbllibraryasset
    """
    cursor.execute(query)
    library_assets = cursor.fetch_dataframe()
    cursor.close()
    conn.close()

# recently added content
    response = requests.get('https://api.library.tulipintra.net/v2/assets')
    body = response.content
    body_json = json.loads(body)  
    apps = body_json['apps']
    df_apps = pd.DataFrame(apps)

    app_groups = body_json['appGroups']
    df_app_groups = pd.DataFrame(app_groups)

    connectors = body_json['connectors']
    df_connectors = pd.DataFrame(connectors)

    df_union = pd.concat([df_apps, df_app_groups, df_connectors])
    df_union_col = ['assetId', 'assetType', 'created', 'lastModified', 'marketingHeadline', 'name']
    df_union = df_union[df_union_col] 

    recent_asset_table = pd.merge(library_assets, df_union, left_on='asset_id', right_on='assetId')

    recent_asset_table = recent_asset_table.drop(columns=['asset_id', 'assetId'])

    recent_asset_table['created'] = recent_asset_table['created'].apply(lambda x: x['at'] if 'at' in x else None)

    recent_asset_table = recent_asset_table[['name','assetType', 'marketingHeadline', 'created', 'asset_page_url']]

    recent_asset_table = recent_asset_table.rename(columns={
        'assetType': 'content type',
        'marketingHeadline': 'summary',
        'asset_page_url':'link',
        'created': 'date published'
    })

    recent_asset_table = recent_asset_table.sort_values(by='date published', ascending=False)

    recent_asset_table = recent_asset_table.reset_index(drop=True)
    

    # Modify the index to start with 1 instead of 0
    recent_asset_table.index = recent_asset_table.index + 1

    recent_asset_table = recent_asset_table.iloc[0:50]
    return recent_asset_table