import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from tqdm import tqdm

'''
tools funtions
'''
class nlpUtil:

    def __init__(self):
        self.df_cat=pd.read_csv('../c7reviews/df_cat.csv')
        self.keywords=self.df_cat['keyword'].tolist()
        self.keywords = [self.stemmer.stem(word) for word in self.keywords]
        
    
    #function to remove stopwords and tokenize a text
    stop_words = stopwords.words("english")
    stop_words.extend(['.',',','!','?','(',')'])
    stemmer = PorterStemmer()
    def rmStopWd(self,text):
        tokens=nltk.word_tokenize(str(text).lower())
        tokens = [word for word in tokens if word not in self.stop_words]
        tokens = [self.stemmer.stem(word) for word in tokens]
        return tokens
    
    def tag(self,tokens):
        tags = [kword for kword in self.keywords if kword in tokens]
        return tags
        
    
    #category dictionary
    #@staticmethod
    def get_catDict(self):
        return self.df_cat
    def get_catList(self):
        return self.list_cat


if __name__ == "__main__":
    #path of app list
    df_temp=pd.read_csv('../c7reviews/free7p4.csv')
    appList=df_temp['appId'].tolist()

    #tool class
    nUtil=nlpUtil()


    for appid in tqdm(appList):
        #read reviews 
        df_app=pd.read_csv('../c7reviews/raw/'+appid+'.csv')
        df_app.drop(labels =['Unnamed: 0'],axis=1,inplace=True)

        #remove stopwords and tokenize
        df_tmpTokens=df_app['content'].apply(nUtil.rmStopWd)
        df_tmpTokensReply=df_app['replyContent'].apply(nUtil.rmStopWd)

        #tag on
        df_app['tags']=df_tmpTokens.apply(nUtil.tag)
        df_app['replyTags']=df_tmpTokensReply.apply(nUtil.tag)
        df_taged = df_app[df_app.tags.astype(bool) | df_app.replyTags.astype(bool)]
        df_taged.to_csv('../c7reviews/replyTag/'+appid+'.csv')
