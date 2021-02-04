import streamlit as st
import random
keyword = 'apple'
sens = ["Apple shipped new computers featuring innovative graphical user interfaces, such as the original Macintosh in 1984",
        "Apple's worldwide annual revenue totaled $274.5 billion for the 2020 fiscal year.",
        "Tech giants Apple and Google have joined forces to develop an interoperable contact-tracing tool that will help individuals determine if they have come in contact with someone infected with COVID-19.",
        "Lawsuit claims Apple facilitates, benefits from illegal gambling on the App Store",
        "An apple is an edible fruit produced by an apple tree",
        "Apple trees are large if grown from seed",
        "Because apples do not breed true when planted as seeds, although cuttings can take root and breed true, and may live for a century, grafting is usually used",
        "Apples have been acclimatized in Ecuador at very high altitudes, where they can often, with the needed factors, provide crops twice per year because of constant temperate conditions year-round."]

def highlight(sim):
	r = 240
	g = (129*(sim-0.9)/-0.5)+4
	b = (82*(sim-0.9)/-0.5)+88
	return r,g,b

for title in sens:
	similarity = random.random()
	index = title.lower().find(keyword.lower())
	before = title[:index]
	key = title[index:index+len(keyword)]
	after = title[index+len(keyword):]
	r,g,b=highlight(similarity)
	st.markdown("<style>.before{background-color:0;margin:0; display:inline;}</style>",unsafe_allow_html=True)
	st.markdown("<style>.after{background-color:0;margin:0; display:inline;}</style>",unsafe_allow_html=True)
	first = "<div><p class=before>{}</p><a style = 'background-color:".format(before)
	st.markdown(first+"rgb({},{},{});'>{}</a><p class=after>{}</p></div>".format(r,g,b,keyword,after), unsafe_allow_html=True)
	st.markdown("<p> {}</p>".format(similarity),unsafe_allow_html=True)