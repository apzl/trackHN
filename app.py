import streamlit as st

import time
import re
import requests 
from scipy.spatial.distance import cosine

from utils import word_embed, highlight


from transformers import BertTokenizer, BertModel



threshold = st.sidebar.slider(
    'similarity',
    0.1, 0.99, (0.6)
)
category = st.sidebar.radio('category',['new','top','best'])    




@st.cache
def load_model():
	tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
	model = BertModel.from_pretrained('bert-base-uncased',
                                  output_hidden_states = True,
                                  )
	return model,tokenizer




def main():
  st.markdown("<h1 style='text-align: center; color: rgb(246, 51, 102);'>trackHN</h1>", unsafe_allow_html=True)	
  st.markdown("<p style='text-align: center;'>track HackerNews, with sense</p>",unsafe_allow_html=True)
  keyword = st.text_input("search keyword")
  context = st.text_area("sample text")
  st.write("give text having keyword in the needed context")
  search = st.button("go")



  if search:
    #check if keyword in sample text
    if(re.search(r'\b'+keyword+r'\b',context,flags=re.IGNORECASE)):
      model,tokenizer = load_model()
      #gets embedding for the keyword
      context_embed = word_embed(context, keyword, model, tokenizer)
      
      
      with st.spinner('searching...'):
        base_url = 'https://hacker-news.firebaseio.com/v0/' 
        end_url = '.json?print=pretty'
        ids_url = ''.join([base_url,category,'stories',end_url])
        #gets ids of 500 posts             
        ids = requests.get(ids_url) 
        for id in ids.json():
          url = ''.join([base_url,'item/',str(id),end_url])
          r = requests.get(url).json()
          if (r):
            if 'url' in r.keys():
              link = r['url']
              title = r['title']
              match = (re.search(r'\b'+keyword+r'\b',title,flags=re.IGNORECASE))
              if match:
                index = match.start() 
                #gets embedding for keyword in search result                                          
                title_embed = word_embed(title,keyword,model, tokenizer)        
                similarity=(1-cosine(context_embed,title_embed))
                if (similarity>threshold):
                  before = title[:index]
                  key = title[index:index+len(keyword)]
                  after = title[index+len(keyword):]
                  #calculate the intensity of keyword highlighting
                  h,s,l=highlight(similarity)                                   
                  
                  
                  #formatting output text                                
                  st.markdown("<style>.before{background-color:0;margin:0; display:inline;}</style>",unsafe_allow_html=True)
                  st.markdown("<style>.after{background-color:0;margin:0; display:inline;}</style>",unsafe_allow_html=True)
                  first = "<div><p class=before>{}</p><a style = 'background-color:".format(before)
                  st.markdown(first+"hsl({},{}%,{}%);'>{}</a><p class=after>{}</p></div>".format(h,s,l,key,after), unsafe_allow_html=True)
                  st.markdown("<a href={}>read more</a>".format(link),unsafe_allow_html=True)
    
    
    else:
      st.write('keyword missing in text')


if __name__=='__main__':
  main()

