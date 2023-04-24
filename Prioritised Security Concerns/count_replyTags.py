import pandas as pd
import numpy as np
import os

'''
tools funtions
'''
class nlpUtil:
    def __init__(self):
        self.df_cat=pd.read_csv('../c7reviews/df_cat.csv')
        self.keywords=self.df_cat['keyword'].tolist()



    # category dictionary
    # @staticmethod
    def get_catDict(self):
        return self.df_cat
    def get_catList(self):
        return self.list_cat


if __name__ == "__main__":
    #read appid list
    path='../c7reviews/replyTag/'
    appList=os.listdir(path)
    #appList=appList
    #tool class
    nUtil=nlpUtil()
    #init statistics
    freq=pd.Series(index=nUtil.keywords,data=0)
    count_rtags=0
    
    #Processbar vars
    listSize=len(appList)
    PBcount=0
    PBstep=10
    PBcanprint=PBstep
    print('start. data size: '+str(listSize))
    for appid in appList:
        df_app= pd.read_csv(path+appid,usecols=['tags','replyTags'],converters={"tags":eval,"replyTags":eval})
        #ignore empty file
        if len(df_app)==0: continue
        # function to combine the lists and remove duplicates
        def combine_lists(x):
            combined = []
            for i in x['tags']:
                for j in x['replyTags']:
                    if isinstance(i, list):
                        combined.extend([item for item in i if item not in combined])
                    else:
                        if i not in combined:
                            combined.append(i)
                    if isinstance(j, list):
                        combined.extend([item for item in j if item not in combined])
                    else:
                        if j not in combined:
                            combined.append(j)
            return combined
        df_app['mergeTags']=df_app.apply(combine_lists, axis=1)
        df_tmp= df_app.explode('mergeTags')
        freq=freq.add(df_tmp['mergeTags'].value_counts(),fill_value=0)
        count_rtags+=len(df_app)
    
        
        PBcount+=1
        if PBcount/listSize>=PBcanprint/100: #process feedback
            print("has done %d%%"%(PBcanprint))
            PBcanprint=PBcanprint+PBstep
            
    print(freq)
