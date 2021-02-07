import streamlit as st
import time
import requests 
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
  keyword = ' '+st.text_input("")
  context = st.text_area("sample text")
  search = st.button("go")
  if search:
    if(keyword.lower() in context.lower()):
      model,tokenizer = load_model()
      context_embed = word_embed(context, keyword, model, tokenizer)
      with st.spinner('searching...'):
        base_url = 'https://hacker-news.firebaseio.com/v0/' 
        end_url = '.json?print=pretty'
        ids_url = ''.join([base_url,category,'stories',end_url])
        ids = requests.get(ids_url)
        for id in ids.json():
          url = ''.join([base_url,'item/',str(id),end_url])
          r = requests.get(url).json()
          if 'url' in r.keys():
            link = r['url']
            title = r['title']
            if (keyword.lower() in title.lower()):
              title_embed = word_embed(title,keyword,model, tokenizer)
              similarity=(1-cosine(context_embed,title_embed))
              if (similarity>threshold):
                index = title.lower().find(keyword.lower())
                before = title[:index]
                key = title[index:index+len(keyword)]
                after = title[index+len(keyword):]
                r,g,b=highlight(similarity)              #calculate the intensity of keyword highlighting
                st.markdown("<style>.before{background-color:0;margin:0; display:inline;}</style>",unsafe_allow_html=True)
                st.markdown("<style>.after{background-color:0;margin:0; display:inline;}</style>",unsafe_allow_html=True)
                first = "<div><p class=before>{}</p><a style = 'background-color:".format(before)
                st.markdown(first+"hsl({},{}%,{}%);'>{}</a><p class=after>{}</p></div>".format(r,g,b,keyword,after), unsafe_allow_html=True)
                st.markdown("<a href={}>read more</a>".format(link),unsafe_allow_html=True)
    else:
      st.write('keyword missing in text')


if __name__=='__main__':
  main()

