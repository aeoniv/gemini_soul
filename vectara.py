import os
import streamlit as st
from dotenv import load_dotenv
from Vectara import Indexing, Searching  



class Searching:
    def __init__(self):
        self.customer_id = os.getenv('CUSTOMER_ID')
        self.api_key = os.getenv('API_KEY')

    def send_query(self, corpus_id, query_text, num_results, summarizer_prompt_name, response_lang, max_summarized_results):
        api_key_header = {
            "customer-id": self.customer_id,
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

        data_dict = {
            "query": [
                {
                    "query": query_text,
                    "num_results": num_results,
                    "corpus_key": [{"customer_id": self.customer_id, "corpus_id": corpus_id}],
                    'summary': [
                        {
                            'summarizerPromptName': summarizer_prompt_name,
                            'responseLang': response_lang,
                            'maxSummarizedResults': max_summarized_results
                        }
                    ]
                }
            ]
        }

        payload = json.dumps(data_dict)

        response = requests.post(
            "https://api.vectara.io/v1/query",
            data=payload,
            verify=True,
            headers=api_key_header
        )

        if response.status_code == 200:
            print("Request was successful!")
            data = response.json()
            texts = [item['text'] for item in data['responseSet'][0]['response'] if 'text' in item]
            return texts
        else:
            print("Request failed with status code:", response.status_code)
            print("Response:", response.text)
            return None