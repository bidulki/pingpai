import requests
import json

url = "http://127.0.0.1:7000"

def get_faq():
    res =requests.post(url + '/api/get-faq')
    return res.content

def add_faq(question, answer):
    param = {
        "question": question,
        "answer": answer
    }
    res = requests.post(url + "/api/add-faq", json=param)
    return res.content

def delete_faq(idx):
    param = {
        "idx": idx
    }
    res = requests.post(url + '/api/delete-faq', json=param)
    return res.content

def search_faq(query, topk):
    param = {
        "query": query,
        "topk": topk
    }
    res = requests.post(url + "/api/search-faq", json=param)
    return res.content

def search_realtime(query):
    param = {
        "query": query
    }
    res = requests.post(url + "/api/search-realtime", json=param)
    return res.content

def print_faq_list(res):
    for i in res.keys():
        print(f"index: {i}")
        print(f"Q: {res[i]['question']}")
        print(f"A: {res[i]['answer']}")
        print()

while(True):
    print("Select Options")
    print("1: get faq list")
    print("2: add faq in faq list")
    print("3: delete faq in faq list")
    print("4: search in faq list by query")
    print("5: get realtime generated answer by llm")
    print("6: Exit")
    print("")
    option = input("Option: ")
    
    if option=="1":
        res = json.loads(get_faq())
        print_faq_list(res)
    
    elif option=="2":
        question = input("Q: ")
        answer = input("A: ")
        res = json.loads(add_faq(question, answer))
        print_faq_list(res)
    
    elif option=="3":
        idx = int(input("idx: "))
        res = json.loads(delete_faq(idx))
        print_faq_list(res)

    elif option=="4":
        query = input("Q: ")
        topk = input("topk: ")
        res = json.loads(search_faq(query, topk))
        for i in res.keys():
            print(f"{i}: {res[i]['question']}")
            print(f"{res[i]['answer']}")

    elif option=="5":
        query = input("Q: ")
        res = json.loads(search_realtime(query))
        print(query)
        print(res)
        answer = res['answer']
        print(f'A: {answer}')
    
    else:
        break
    print("#######################################")