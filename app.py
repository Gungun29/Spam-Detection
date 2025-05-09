import streamlit as st
import pickle
import nltk
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')

ps=PorterStemmer()

def transform_text(text):
  text=text.lower()
  text=nltk.word_tokenize(text)
  y=[]
  for i in text:
    if i.isalnum():
      y.append(i)

  text=y[:]
  y.clear()

  for i in text:
    if i not in stopwords.words('english') and i not in string.punctuation:
      y.append(i)

  text=y[:]
  y.clear()

  for i in text:
    y.append(ps.stem(i))

  return ' '.join(y)

tfidf=pickle.load(open('vectorizer.pkl','rb'))
model=pickle.load(open('model.pkl','rb'))

st.title("Email/SMS Classifier")

input_sms=st.text_area("Enter the message")

if st.button("Predict"):
  #Preprocess
  transformed_text=transform_text(input_sms)

  #Vectorize
  vector_input=tfidf.transform([transformed_text])

  #Predict
  result=model.predict(vector_input)[0]

  #Display
  if result==1:
    st.header("Spam")
  else:
    st.header("Not Spam")


