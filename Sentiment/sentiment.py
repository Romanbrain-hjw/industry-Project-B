import pandas as pd
import sys
from nltk.stem.porter import PorterStemmer
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import tokenize
import emoji
from tqdm import tqdm

'''
tools funtions
'''
class nlpUtil:

    stemmer = PorterStemmer()
    def __init__(self):
        self.df_cat=pd.read_csv('../c7reviews/df_cat.csv')
        self.keywords=self.df_cat['keyword'].tolist()
        self.keywords = [self.stemmer.stem(word) for word in self.keywords]
        
    
    
    def tag(self,tokens):
        tags = [kword for kword in self.keywords if kword in tokens]
        return tags
    
    #analyze review compound sentiment
    sid = SentimentIntensityAnalyzer()
    def sentiment(self,review):
        review = emoji.demojize(review)
        sentences = tokenize.sent_tokenize(review)
        scores = [self.sid.polarity_scores(sentence)['compound'] for sentence in sentences]
        return sum(scores)/len(scores)



if __name__ == "__main__":
    #path of app list
    df_temp=pd.read_csv('../c7reviews/free7.csv')
    appList=df_temp['appId'].tolist()

    appList=appList[0:10]
    #tool class
    nUtil=nlpUtil()

    for appid in tqdm(appList):
        #read reviews 
        try:
            df_app=pd.read_csv('../c7reviews/replyTag/'+appid+'.csv',usecols=['reviewId','content','score','mergeTags'],index_col=False)
            df_app['sentiment']=df_app['content'].apply(nUtil.sentiment)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            continue
        #sentiment analysis

        df_app.to_csv('../c7reviews/sentiment/'+appid+'.csv')
        
