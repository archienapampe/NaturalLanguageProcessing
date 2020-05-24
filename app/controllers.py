import pandas as pd
import spacy

from flask import render_template, make_response

nlp = spacy.load('en_core_web_lg')


class BaseController:
    def __init__(self):
        pass
    
    def call(self, *args, **kwargs):
        try:
            return self._call(*args, **kwargs)
        except Exception as e:
            return make_response(str(e), 500)
        
    def _call(self, *args, **kwargs):
        raise NotImplementedError('_call')
    

class RawDataInput(BaseController):
    def _call(self):
        return render_template('index.html')
    

class StartProcess(BaseController):
    def _call(self, rawdata):
        doc = nlp(rawdata)
  
        label2cat = {
            'PERSON': [],
            'ORG': [],
            'LOC': [], 
            'GPE': [], 
            'DATE': []
            }
        
        for entity in doc.ents:
            if entity.label_ in label2cat:
                label2cat[entity.label_].append(entity.text)      
                    
        df = pd.DataFrame.from_dict({
            'PLAYERS': label2cat['PERSON'], 
            'FOOTBALL CLUB': label2cat['ORG'], 
            'AREA': label2cat['LOC'], 
            'CITY': label2cat['GPE'], 
            'DATE': label2cat['DATE']
        }, orient='index')

        df = df.transpose()
        df.fillna(value='', inplace=True)
        df_html = df.to_html(index=False)  
        
        return render_template("result.html", data=df_html, title='Result NLP')