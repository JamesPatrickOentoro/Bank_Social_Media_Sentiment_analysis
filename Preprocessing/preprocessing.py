import pandas as pd
import re
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import torch
import emoji
from googletrans import Translator
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import nltk
nltk.download('stopwords')

def read_file(path):
    df = pd.read_excel(path)
    return df

def handle_missing_value(df_raw):
    # Erase baris dengan label atau komen kosong
    df_raw_p = df_raw[df_raw['Label (1,0,-1)'].notna()]
    df = df_raw_p[df_raw_p['comments'].notna()]
    return df

if __name__=="__main__":
    path = ''
