import pandas as pd
import spacy
from afinn import Afinn
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask import render_template, make_response

from app import app

nlp = spacy.load('en_core_web_lg')
analyzer = SentimentIntensityAnalyzer()
af = Afinn()

                                                                                        
class BaseController:
    def __init__(self):
        pass
    
    def call(self, *args, **kwargs):
        try:
            app.logger.info(f'Started {self.__class__.__name__}')
            return self._call(*args, **kwargs)
        except Exception as e:
            app.logger.exception(f'Error: {e=}')
            return make_response(str(e), 500)
        
    def _call(self, *args, **kwargs):
        raise NotImplementedError('_call')
    

class RawDataInput(BaseController):
    def _call(self):
        return render_template('index.html')
    

class StartProcess(BaseController):
    def _call(self, rawdata):
        ner_dataframe = self._prepare_dataframe(self._named_entity_recognition_dataframe(rawdata))
        sentiment_dataframe = self._prepare_dataframe(self._sentiment_dataframe(rawdata))
        
        return render_template('result.html',
                                data={'ner_df': ner_dataframe, 'sentiment_df': sentiment_dataframe},
                                title='Result NLP'
                                )
                                                    
    def _sentiment_category(self, sentiment_scores, low=0, high=0):
        sentiment_category = []

        for score in sentiment_scores:
            if score > high:
                sentiment_category.append('positive') 
            elif score < low:
                sentiment_category.append('negative') 
            else:
                sentiment_category.append('neutral')

        return sentiment_category
        
    def _prepare_dataframe(self, df):
        df = df.transpose()
        df.fillna(value='', inplace=True)
        df_html = df.to_html(index=False, justify='left')  
        
        return df_html
    
    def _named_entity_recognition_dataframe(self, rawdata):
        doc = nlp(rawdata)
         
        label2cat = {
            'PERSON': set(),
            'ORG': set(),
            'LOC': set(), 
            'GPE': set(), 
            'DATE': set()
            }
        
        for entity in doc.ents:
            if entity.label_ in label2cat:
                label2cat[entity.label_].add(entity.text) 
                
        df = pd.DataFrame.from_dict({
            'PLAYERS': label2cat['PERSON'], 
            'FOOTBALL CLUB': label2cat['ORG'], 
            'AREA': label2cat['LOC'], 
            'CITY': label2cat['GPE'], 
            'DATE': label2cat['DATE']
        }, orient='index')
        
        return df
    
    def _sentiment_dataframe(self, rawdata):
        articles = [article for article in rawdata.replace('\r', '').split('\n\n') if article]
        
        sentiment_scores_afinn = [af.score(article) for article in articles]
        app.logger.info(f'{sentiment_scores_afinn=}')
        sentiment_scores_blob = [TextBlob(article).correct().sentiment.polarity for article in articles]
        app.logger.info(f'{sentiment_scores_blob=}')
        sentiment_scores_vader = [analyzer.polarity_scores(article)['compound'] for article in articles]
        app.logger.info(f'{sentiment_scores_vader=}')
        
        df = pd.DataFrame.from_dict({
            'SENTIMENT SCORES AFINN': sentiment_scores_afinn, 
            'SENTIMENT CATEGORY AFINN': self._sentiment_category(sentiment_scores_afinn), 
            'SENTIMENT SCORES BLOB': sentiment_scores_blob, 
            'SENTIMENT CATEGORY BLOB': self._sentiment_category(sentiment_scores_blob), 
            'SENTIMENT SCORES VADER': sentiment_scores_vader,
            'SENTIMENT CATEGORY VADER': self._sentiment_category(sentiment_scores_vader, low=-0.05, high=0.05)
        }, orient='index')
        
        return df