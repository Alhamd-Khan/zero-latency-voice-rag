from pypdf import PdfReader
import chromadb
from fastembed import TextEmbedding
import ollama
import threading

PDF_FILE = "manulpdf.pdf"

print("Reading PDF...")

reader = PdfReader(PDF_FILE)
text = ""

for page in reader.pages:
    t = page.extract_text()
    if t:
        text += t

print("Chunking...")

chunks = []
size = 400

for i in range(0, len(text), size):
    chunks.append(text[i:i + size])

print("Embedding...")

embedder = TextEmbedding()
vectors = list(embedder.embed(chunks))

client = chromadb.Client()
collection = client.create_collection("manual")

for i, v in enumerate(vectors):
    collection.add(
        ids=[str(i)],
        embeddings=[v.tolist()],
        documents=[chunks[i]],
    )

print("Vector DB ready.")

conversation = []

# ---------- Speculative RAG (Parallel) ----------

prefetched = []

def speculative_fetch(partial):
    global prefetched
    vec = list(embedder.embed([partial]))[0].tolist()
    res = collection.query(query_embeddings=[vec], n_results=5)
    prefetched = res["documents"][0]

print("\nSystem ready. Ask questions.\n")

while True:
    q = input("Ask: ")

    if q.lower() in ["exit", "quit"]:
        break

    # Query rewriting (simple)
    if "second" in q.lower() and conversation:
        q = conversation[-1] + " " + q

    conversation.append(q)

    # Start speculative retrieval
    t = threading.Thread(target=speculative_fetch, args=(q[:20],))
    t.start()

    t.join()

    # Hybrid search (vector + keyword)
    results = []
    for d in prefetched:
        if any(w in d.lower() for w in q.lower().split()):
            results.append(d)

    if not results:
        results = prefetched[:3]

    # Simple reranker = shortest chunks first
    results = sorted(results, key=len)[:3]

    # Filler (simulated latency hiding)
    print("Let me check that for you...")

    context = "\n".join(results)

    prompt = f"""
Answer ONLY from this context:

{context}

Question: {q}
"""

    response = ollama.generate(
        model="tinyllama",
        prompt=prompt,
    )

    answer = response["response"]

    # Voice optimization
    answer = answer.replace(".", ". ").replace("configuration", "config")

    print("\nAnswer:\n")
    print(answer)
    print()
