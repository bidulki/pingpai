import os
import pickle
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import pandas as pd
from langchain.llms import OpenAI

class FAQDB:
    def __init__(self, faq_path, index_path, model_name):
        self.faq_path = faq_path
        self.index_path = index_path
        self.embedding_model = self.load_embedding_model(model_name)
        self.faq_list = self.load_faq()
        self.index = self.load_index()
    
    def load_faq(self):
        if os.path.exists(self.faq_path):
            df = pd.read_csv(self.faq_path, sep="\t")
            question_list = df['question'].to_list()
            answer_list = df['answer'].to_list()
            faq_list = list()
            for question, answer in zip(question_list, answer_list):
                faq={
                    'question': question,
                    'answer': answer
                }
                faq_list.append(faq)

        else:
            faq_list = list()
        return faq_list
    
    def save_faq(self):
        with open(self.faq_path, 'wb') as f:
            pickle.dump(self.faq_list, f)
        df = pd.DataFrame()
        question_list = []
        answer_list = []
        for faq in self.faq_list:
            question = faq['question']
            answer = faq['answer']
            question_list.append(question)
            answer_list.append(answer)
        df['question'] = question_list
        df['ansewr'] = answer_list
        df.to_csv("faq.tsv", index=False, sep="\t")

    def load_embedding_model(self, model_name):
        embedding_model = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device':'cuda:0'},
            encode_kwargs={'normalize_embeddings':True})
        return embedding_model
    
    def load_index(self):
        if os.path.exists(self.index_path):
            index = FAISS.load_local(self.index_path, self.embedding_model, allow_dangerous_deserialization=True)
        elif len(self.faq_list)>0:
            index = self.update_index()
        else:
            index = None
        return index
    
    def update_index(self):
        questions = [faq['question'] for faq in self.faq_list]
        index = FAISS.from_texts(questions, embedding=self.embedding_model)
        return index
    
    def save_index(self):
        self.index.save_local(self.index_path)

    def get_faq(self):
        res = dict()       
        for i, faq in enumerate(self.faq_list):
            res[i] = faq
        return res
    
    def add_faq(self, question, answer):
        faq={
            'question': question,
            'answer': answer
        }
        self.faq_list.append(faq)
        if self.index==None:
            self.index = self.load_index()
        else:
            self.index.add_texts([question])
        self.save_faq()
        self.save_index()
        return self.get_faq()
    
    def delete_faq(self, idx):
        self.faq_list.pop(idx)
        self.index = self.update_index()
        self.save_faq()
        self.save_index()
        return self.get_faq()
    
    def search_faq(self, query, topk):
        topk_question_list = self.index.similarity_search(query, topk)
        question_list = [faq['question'] for faq in self.faq_list]
        answer_list = []
        for question in topk_question_list:
            answer = self.faq_list[question_list.index(question.page_content)]['answer']
            answer_list.append(answer)
        res = dict()
        for i, answer in enumerate(answer_list):
            res[i] = answer
        return res



class RealTimeDB:
    def __init__(self, document_path, index_path, model_name, history_path):
        self.document_path = document_path
        self.index_path = index_path
        self.embedding_model = self.load_embedding_model(model_name)
        self.doc_dic = self.load_doc_dic()
        self.index = self.load_index()
        self.history_path = history_path

    
    def load_doc_dic(self):
        if os.path.exists(self.document_path):
            doc_dic={}
            df = pd.read_csv(self.document_path, delimiter="\t")
            url_list = df['did'].to_list()
            document_list = df['document'].to_list()
            for d_i, d in enumerate(document_list):
                doc_dic[d] = url_list[d_i] 
        else:
            doc_dic={}
        return doc_dic


    def load_embedding_model(self, model_name):
        embedding_model = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device':'cuda:0'},
            encode_kwargs={'normalize_embeddings':True})
        return embedding_model
    
    def load_index(self):
        if os.path.exists(self.index_path):
            index = FAISS.load_local(self.index_path, self.embedding_model, allow_dangerous_deserialization=True)
        else:
            index = FAISS.from_texts(self.document_list, embedding=self.embedding_model)
            index.save_local(self.index_path)
        return index
    
    def qa_prompt(self,query,documents,prompt_filename='config/SKKU.prompt'):
        with open(prompt_filename) as f:
            prompt_template = f.read().rstrip("\n")
        formatted_documents = []
        for document_index, document in enumerate(documents):
            formatted_documents.append(f"문서[{document_index+1}] {document}")
        return prompt_template.format(query=query, search_results="\n".join(formatted_documents))    
        
    def search_realtime(self, query, topk=1):
        api_key = os.getenv('OPENAI_API_KEY')
        topk_document_list = self.index.similarity_search(query, topk)
        prompt = self.qa_prompt(query,topk_document_list)
        url_list=[]
        if (len(topk_document_list)==0):
            responese='검색된 결과가 없습니다. faq 서비스를 이용해주세요'
            url_list=['']
        else:
            for d in topk_document_list:
                url_list.append(self.doc_dic[d.page_content])
            llm = OpenAI(api_key = api_key)
            responese = llm(prompt)
            with open(self.history_path, "a", encoding="utf-8") as file:
                file.write(f"{query}\t{responese}\n")
        
        
        return {'answer': responese, 'url_list': url_list}

