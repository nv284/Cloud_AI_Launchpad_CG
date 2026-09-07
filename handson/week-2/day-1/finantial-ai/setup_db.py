import os
from qdrant_client import QdrantClient
from qdrant_client import models

# 1. Setup direct Python local folder tracking (No Docker required!)
DB_PATH = "./local_qdrant_db"
client = QdrantClient(path=DB_PATH)

collection_name = "financial_regulations"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# 2. Define the mock compliance text documents
documents = [
    "Global Systemically Important Banks (G-SIBs) must maintain an additional Common Equity Tier 1 (CET1) capital buffer of 1.5% to 3.5% depending on their systemic importance score. This buffer must be met entirely with CET1 capital and is calculated quarterly.",
    "Institutions with total consolidated assets exceeding $250 billion must submit stress testing evaluations using the severely adverse scenario by April 5th annually. Failure to comply results in immediate operational restrictions."
]

# 3. Define accompanying source metadata
metadata = [
    {"doc_ref": "Basel III Amendment, Sec 14.2 (2025)", "year": 2025},
    {"doc_ref": "SEC Dodd-Frank Rule 419-A (2023)", "year": 2023}
]

print("Initializing collection and generating embeddings...")

# 4. Explicitly track and build your collection framework schema
if not client.collection_exists(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=client.get_embedding_size(EMBEDDING_MODEL),
            distance=models.Distance.COSINE
        )
    )

# 5. Upload documents cleanly using the explicit Document model wrapper
client.upload_collection(
    collection_name=collection_name,
    vectors=[models.Document(text=doc, model=EMBEDDING_MODEL) for doc in documents],
    payload=[{"document": doc, **meta} for doc, meta in zip(documents, metadata)],
    ids=list(range(len(documents))) # Explicitly sets incremental integer IDs [0, 1]
)

print("Success! Documents are securely indexed in Qdrant.\n")

# =====================================================================
# Real-Time Query Validation Layer (The Hallucination Guardrail)
# =====================================================================
def query_regulations(user_prompt: str):
    print(f"User Query: '{user_prompt}'")
    
    # Standard fallback method for local clients to fetch matches
    search_results = client.query_points(
        collection_name=collection_name,
        query=models.Document(text=user_prompt, model=EMBEDDING_MODEL),
        limit=1,
        score_threshold=0.5  # Rule out low-scoring irrelevant text context
    )
    
    # Guardrail: Rejection response if no contextual data parameters clear the minimum threshold 
    if not search_results or not search_results.points:
        print("AI System Response: [GUARDRAIL TRIGGERED] I cannot find the answer in the provided regulatory documents.\n")
        return

    # Extract target information fields on a validated strong hit
    matched_hit = search_results.points[0]
    matched_text = matched_hit.payload["document"]
    matched_source = matched_hit.payload["doc_ref"]
    
    print(f"Found Regulatory Context: \"{matched_text}\"")
    print(f"Verified Source: {matched_source}")
    print("AI System Response: Pass this verified context safely to your local LLM.\n")

# --- Test Case 1: Valid Regulatory Match ---
query_regulations("What are the CET1 capital buffer requirements for G-SIBs?")

# --- Test Case 2: Out of Domain Inquiry (Triggers Guardrail Verification) ---
query_regulations("What is the standard dress code policy for internal office bank tellers?")
