# Data streaming project

## Team  
* Solomiya Synytsia  
* Bohdan Yarychevskyi   
* Khrystyna Hranishak  

## How to run  
#### Requirements  
* Linux OS
* Python3.6  

#### Steps
* Start Kafka service by executing `docker-compose up`  
* Create an environment and install all dependencies (`pip install -r requirements.txt`)
* Execute `./run_app.sh`  
* See the visualization here https://app.powerbi.com/groups/me/dashboards/4ba98332-4a17-466b-b29c-fb17a80bc45d (please ask the access credentials in private)

## Service details

### Data preparation and kafka communicator services  
* **source_data_handler**  
    - Input: .tsv file  
    - Ouput: messages one by one
* **kafka_publisher**      
    - Input: message, topic
    - Output: 1 - if message was published. 0 -- if message was empty and it wasn't published
* **generator**
    - calls source_data_handler to get next message and publish it with kafka_publisher      
* **kafka_reader**
    - Input: topic
    - Output: messages from the topic 

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
      
