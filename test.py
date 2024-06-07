from utils import FAQDB , RealTimeDB
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

faq_path = "./faq.tsv"
index_path = "./faq.index"
model_name = "jhgan/ko-sbert-nli"
document_path = "./document.tsv"
document_index_path = "./document.index"
history_path = "qa_history.tsv"





real_time_db = RealTimeDB(
    document_path=document_path, 
    index_path=document_index_path, 
    model_name=model_name,
    history_path = history_path
)
query ="안녕하세요. 저는 성균관대학교 학생입니다. "
res = real_time_db.search_realtime(query)
print(res)