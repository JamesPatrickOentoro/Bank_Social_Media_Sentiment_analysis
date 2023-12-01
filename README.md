# Social Media Sentiment Analysis Bahasa Indonesia on Banking Industry
NLP BASED Indonesian Sentiment Analysis
============================================================

# Install transformers library.
!pip install -q git+https://github.com/huggingface/transformers.git
# Install helper functions.
!pip install -q git+https://github.com/gmihaila/ml_things.git


Requirements :
Python				3.11.4
session_info        1.0.0
IPython             8.14.0
jupyter_client      7.4.9
jupyter_core        5.3.1
notebook            6.5.4
accelerate			0.22.0
emoji				2.7.0
googletrans			3.1.0a0
huggingface-hub		0.16.4
keras				2.13.1
keras-preprocessing	1.1.2
matplotlib			3.7.2
nltk				3.8.1
numba				0.57.1
numpy				1.25.0
openpyxl			3.1.2
pandas				1.5.3
pytorch-cuda		11.8
sastrawi			1.0.1
scikit-learn		1.3.0
seaborn				0.12.2
tensorflow			2.13.0
tokenizers			0.13.3
tqdm				4.65.0
transformers		4.32.0
wordcloud			1.9.2


How to use:
1. Data Scrapping and Data set Generation:
	Buka file Scraping
	Pilih platform media sosial yang diinginkan
	Ubah akun bank sesuai yang dinginkan pada file
	Ubah tanggal sesuai yang dinginkan

2. Data Preprocessing:
	Buka file preprocessing
	Buka preprocessing.ipynb 
	Install library yang dibutuhkan
	Ubah file sesuai yang diinginkan
	Run Preprocessing
	Save File Train & Test

3. Sentiment Analysis Model:
	Buka nama file sesuai model yang diinginkan
	Install library yang dibutuhkan

Hope that this is useful.


Regards,
James Patrick Oentoro


References:
https://github.com/sivi-shahab/FTDS-HACKTIV8-Batch006/blob/main/P2M1M2/h8dsft_Milestone2P2.ipynb <br>
https://huggingface.co/ayameRushia/bert-base-indonesian-1.5G-sentiment-analysis-smsa<br>
https://huggingface.co/ayameRushia/roberta-base-indonesian-1.5G-sentiment-analysis-smsa <br>
https://huggingface.co/indonesian-nlp/gpt2<br>
https://huggingface.co/docs/transformers/training<br>
