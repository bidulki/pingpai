from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from utils import FAQDB , RealTimeDB

faq_path = "./faq.tsv"
index_path = "./faq.index"
model_name = "jhgan/ko-sbert-nli"
document_path = "./document.tsv"
document_index_path = "./document.index"
history_path = "./qa_history.tsv"



faqdb = FAQDB(
    faq_path=faq_path, 
    index_path=index_path, 
    model_name=model_name
)

real_time_db = RealTimeDB(
    document_path=document_path, 
    index_path=document_index_path, 
    model_name=model_name,
    history_path = history_path
)


class FAQ(BaseModel):
    question: str
    answer: str

class RemoveIdx(BaseModel):
    idx: int

class FaqQuery(BaseModel):
    query: str
    topk: int
class RealQuery(BaseModel):
    query: str


app = FastAPI()

@app.post("/api/get-faq")
async def get_faq():
    res = faqdb.get_faq()
    return res

@app.post("/api/add-faq")
async def add_faq(faq: FAQ):
    res = faqdb.add_faq(faq.question, faq.answer)
    return res

@app.post("/api/delete-faq")
async def delete_faq(remove_idx : RemoveIdx):
    res = faqdb.delete_faq(remove_idx.idx)
    return res

@app.post("/api/search-faq")
async def search_faq(faq_query : FaqQuery):
    res = faqdb.search_faq(faq_query.query, faq_query.topk)
    return res

@app.post("/api/search-realtime")
async def search_realtime(real_query : RealQuery ):
    res = real_time_db.search_realtime(real_query.query)
    return res



uvicorn.run(app, host="127.0.0.1", port=8000)