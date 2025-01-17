
llm_context_query_template = """You are an AI Assistant. Based on the given context, answer the given query. 
If you feel context is is not sufficient, use your own knowledge. context: {context}, query: {query}"""


htr_correction_template = """I have a text read from ocr (performed on handwritten text) regarding machine learning notes taken in class. 
                                    But it is not very accurate. Give me the corrected version of the text without any explanations or assumptions.
                                    Make sure to use your own knowledge on the subject as well when making corrections.
                       ocr text: "{final_text}"
                       """