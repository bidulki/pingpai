import os
import pickle
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

class FAQDB:
    def __init__(self, faq_path, index_path, model_name):
        self.faq_path = faq_path
        self.index_path = index_path
        self.embedding_model = self.load_embedding_model(model_name)
        self.faq_list = self.load_faq()
        self.index = self.load_index()
    
    def load_faq(self):
        if os.path.exists(self.faq_path):
            with open(self.faq_path, 'rb') as f:
                faq_list = pickle.load(f)
        else:
            faq_list = list()
        return faq_list
    
    def save_faq(self):
        with open(self.faq_path, 'wb') as f:
            pickle.dump(self.faq_list, f)

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







    

