from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering
from nltk.tokenize import sent_tokenize

qa_model_name = "deepset/roberta-large-squad2"
tokenizer = AutoTokenizer.from_pretrained(qa_model_name)
qa_model = AutoModelForQuestionAnswering.from_pretrained(qa_model_name)
qa_pipeline = pipeline("question-answering", model=qa_model, tokenizer=tokenizer)

def refine_context(query, context):
    sentences = sent_tokenize(context)
    keyword = query.split()[-1].lower()
    relevant_sentences = [s for s in sentences if keyword in s.lower()]
    return " ".join(relevant_sentences) if relevant_sentences else context

def query_pdf_with_better_context(query, chunks):
    from models.embedder import find_most_relevant_chunks
    relevant_chunks = find_most_relevant_chunks(query, chunks, top_k=3)
    combined_context = " ".join(relevant_chunks)
    refined_context = refine_context(query, combined_context)
    result = qa_pipeline(question=query, context=refined_context)
    return result['answer'] if result['score'] > 0.2 else "No accurate answer found."
