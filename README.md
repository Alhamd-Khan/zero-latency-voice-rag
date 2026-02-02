# Zero-Latency Voice Knowledge Base (RAG Prototype)

This project implements a Retrieval-Augmented Generation system for large technical manuals, designed to support Voice AI agents with sub-second response latency.

The system allows natural-language questions over PDF manuals and returns grounded answers using vector search + LLM generation.

This prototype demonstrates:

- Document ingestion and chunking  
- Vector embeddings + similarity search  
- Context-aware answering  
- Low-latency architecture concepts  

---

## Project Structure

rag.py  
Main executable RAG pipeline.

architecture.md  
System design covering Parallel RAG, Hybrid Search, Reranking, and Voice Optimization.

manulpdf.pdf  
Sample technical manual used for indexing.

README.md  
Project overview and usage.

---

## Stack Used

PDF Parsing: PyPDF  
Embeddings: FastEmbed  
Vector Store: ChromaDB  
LLM: TinyLlama (Ollama local runtime)  
Language: Python  

Optional HuggingFace fallback supported.

---

## How It Works

1. PDF is loaded and split into small chunks.
2. Chunks are embedded into vectors.
3. Vectors are stored in ChromaDB.
4. User queries are embedded and matched.
5. Top results are injected into prompt.
6. LLM generates grounded response.

---

## Running the Project

Activate environment:

venv\Scripts\activate

Run:

python rag.py

Ask questions interactively.

Type `exit` to quit.

---

## Architecture Highlights

- Speculative retrieval design  
- Hybrid ranking strategy  
- Voice-optimized output concept  
- Latency hiding via filler responses  

Full explanation in architecture.md.

---

## Notes

This is a local prototype focused on architectural concepts for Voice RAG systems.  
Production systems would integrate streaming ASR + TTS and GPU reranking.

---

Built for Articence SDE Internship Technical Evaluation.
