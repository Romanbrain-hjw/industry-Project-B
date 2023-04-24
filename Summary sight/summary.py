import os
import pandas as pd


'''
tools funtions
'''
class nlpUtil:
    def __init__(self):
        self.df_cat=pd.read_csv('../c7reviews/df_cat.csv')
        self.keywords=self.df_cat['keyword'].tolist()
        

    #category dictionary
    #@staticmethod
    def get_catDict(self):
        return self.df_cat
    def get_catList(self):
        return self.list_cat


if __name__ == "__main__":
    #filter reviews file larger than 100KB
    #because summary for an app with too few reviews is not convincible
    path="E:\\Cyber security\\2022S2T3\\project A\\NLP\\c7reviews\\taged"
    applist=os.listdir(path)
    for app in applist.copy():
        reviewSize=os.path.getsize(os.path.join(path, app))/1024
        if reviewSize<99: applist.remove(app)
        
    # tool class
    nUtil=nlpUtil()

    
    #Processbar vars
    listSize=len(applist)
    PBcount=0
    PBstep=10
    PBcanprint=PBstep
    print('start. data size: '+str(listSize))
    for appfile in applist:
        df_app= pd.read_csv('../c7reviews/taged/'+appfile,usecols=['tags'],converters={"tags":eval})
        df_tmp= df_app.explode('tags')        
        
        # issues statistics
        statistics=pd.DataFrame(df_tmp['tags'].value_counts())
        statistics.columns=['counts']
        statistics['i']=range(len(statistics))
        statistics['tags']=statistics.index
        statistics.set_index('i',inplace=True)
        statistics['category']=''
        
        #tag category 
        categoryDict={'spam':['spam', 'scam', 'phish', 'advertisement', 'adware']}
        categoryDict['malware']=['malicious', 'malware', 'virus', 'trojan', 'hack']
        categoryDict['privacy']=['permission', 'spy', 'spyware', 'location', 'breach', 'leak']
        categoryDict['abnormal behaviour']=['secretly', 'bloatware', 'battery', 'bug', 'crash']
        for category in categoryDict.keys():
            statistics.loc[statistics['tags'].isin(categoryDict[category]),'category']=category
        statistics.to_csv('statistics/'+appfile)
        
        #summary
        summary=pd.DataFrame(statistics.groupby(['category'])['counts'].sum())
        summary.sort_values(by=['counts'],ascending=False,inplace=True)
        detail=statistics.groupby(['category','tags'])['counts'].sum()
        with open('E:\\Cyber security\\2022S2T3\\project A\\NLP\\summary\\summary\\'+appfile.removesuffix('.csv')+'.txt', 'w' ) as f:
            rsum=int(summary.sum())
            text_Summary=f'{rsum} security related reviews counted\n\n'
            percList=[]
            for category in summary.index:
                tmpPerc='{:.0f}%'.format(summary.loc[category]['counts'] / rsum *100)
                percList.append(tmpPerc)
                if category=='':
                    continue
                text_Summary+=f"{summary.loc[category]['counts']} comments related to {category} accounted for {tmpPerc} of the total."
            #risk 
                if category=='spam':
                    text_Summary+='This part of the reviews may be mainly reporting the problem of inappropriate ads and unnecessary notification. Excessive ads or notifications can affect user experience. Some advertisements may induce users to download other bloatwares, or link to phishing or fake websites, which could further include risks of memory redundancy, privacy leaks and  financial fraud.\n'
                elif category=='malware':
                    text_Summary+='This part of reviews reports there are malicious activities happening while using the app. It is not ruled out that the users downloaded a modified version from an unofficial platform, or maybe they are just complaining emotionally.\n'
                elif category=='privacy':
                    text_Summary+='This part of the comments might reflect the problem of excessive permission request. Unreasonable requests for permissions of location, clipboard or camera could directly violate users\' privacy and portrait rights. Furthermore, excessive permissions may create vulnerabilities that malicious applications can exploit. \n'
                elif category=='abnormal behaviour':
                    text_Summary+='This part of reviews primarily reflects about the app\'s functional failure or abnormal background behaviours.Bugs that cause application or system crashes are at risk of being exploited in denial of service attacks.On the other side, battery drain could be a signal triggered by malicious activities.\n'

                text_Summary+='The following is the statistics of reporting keywords or '+str(detail[category])+'\n\n'
            summary['percentage']=percList
            f.write(text_Summary)

            

