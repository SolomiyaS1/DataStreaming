# Data streaming project

## Team

## Service details

### NLP modules  
* **Language detection**  
    - FastText model is used to detect a language of input text (https://github.com/facebookresearch/fastText/blob/master/docs/language-identification.md)
    - Input: `raw text`
    - Output: language label (e.g. `en`, `es`)  
  **Note:** Please download a model https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin to the folder `Data`  
* **Name Entity Recognition**  
    - Spacy models are used to detect entities (https://spacy.io/usage/models)  
    - Input: `raw text`, `detected language`
    - Output: list of tuples (entity, entity_label) (e.g. `[('Thursday', 'DATE')]`, `[('Danny', 'PERSON'), ('NHL', 'ORG')]`)  
    **Note:** If there isn't a spacy model for a detected language the English model is applied.
* **Sentiment detection**  
    - NLTK Vader lexicon is used to detect a sentiment (https://www.nltk.org/_modules/nltk/sentiment/vader.html)  
    - Input: `raw text`, `detected language`
    - Output: dictionary with sentiments scores (e.g. `{'neg': 0.0, 'neu': 0.727, 'pos': 0.273, 'compound': 0.4588}`)  
    **Note:** NLTK Vader lexicon is in English, that's why to detect sentiments for non-English texts the translator is used. As a translator the pre-trained transformers model was chosen (https://huggingface.co/transformers/model_doc/m2m_100.html)  
      