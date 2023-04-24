import pandas as pd
import numpy as np
import os
from tqdm import tqdm

'''
tools funtions
'''
class nlpUtil:
    def __init__(self):
        self.df_cat=pd.read_csv('../c7reviews/df_cat.csv')
        self.keywords=self.df_cat['keyword'].tolist()



if __name__ == "__main__":
    #read appid list
    path='../c7reviews/replyTag/'
    appList=os.listdir(path)
    #appList=appList
    #tool class
    nUtil=nlpUtil()

    appList=appList[0:1]

    for appid in tqdm(appList):
        df_app= pd.read_csv(path+appid,converters={"tags":eval,"replyTags":eval})
        #ignore empty file
        if len(df_app)==0: continue
        # function to combine the lists and remove duplicates
        def combine_lists(x):
            tags = set()
            for lst in [x['tags'], x['replyTags']]:
                for item in lst:
                    if isinstance(item, list):
                        tags.update(item)
                    elif item:
                        tags.add(item)
            return list(tags)


        df_app['mergeTags']=df_app.apply(combine_lists, axis=1)
        df_app.to_csv('../c7reviews/replyTag/'+appid)

    

