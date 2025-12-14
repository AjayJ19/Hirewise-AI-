from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def score_response(user_response, ideal_answer="A clear, confident and detailed answer."):
    user_embed = model.encode([user_response])
    ideal_embed = model.encode([ideal_answer])
    score = cosine_similarity(user_embed, ideal_embed)[0][0]
    return round(score * 100, 2)


