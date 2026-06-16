"""Quick test script for Vector DB RAG search quality."""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rag.vector_store import RAGVectorStore

def main():
    print("=" * 60)
    print("  VECTOR DB RAG - Search Quality Test")
    print("=" * 60)

    store = RAGVectorStore()

    # Load and index
    start = time.time()
    result = store.load_and_index()
    load_time = time.time() - start
    print(f"\n[INDEX] {result}")
    print(f"[TIME] Load + index: {load_time:.2f}s")

    # Stats
    stats = store.get_stats()
    print(f"[STATS] {stats}")

    # Test queries
    test_queries = [
        ("high CPU ETL batch deadlock process stuck", None),
        ("kill process remediation safety", "tool_knowledge"),
        ("billing-api critical tier SLA", "service_catalog"),
        ("data-transform batch service dependencies", None),
        ("connection pool exhausted timeout", "incident_history"),
    ]

    for query, filter_type in test_queries:
        print(f"\n{'─' * 60}")
        print(f"Query: \"{query}\"")
        if filter_type:
            print(f"Filter: {filter_type}")

        start = time.time()
        if filter_type:
            results = store.search(query, top_k=3, filter_type=filter_type)
        else:
            results = store.search(query, top_k=3)
        search_time = time.time() - start

        print(f"Results ({len(results)}) in {search_time*1000:.0f}ms:")
        for r in results:
            score = r["similarity_score"]
            doc_type = r["metadata"]["doc_type"]
            title = r["metadata"].get("title", "")[:50]
            text_preview = r["text"][:80].replace("\n", " ")
            print(f"  [{r['rank']}] score={score:.3f} | {doc_type:18s} | {title}")
            print(f"      {text_preview}...")

    print(f"\n{'=' * 60}")
    print(f"  ALL TESTS COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
