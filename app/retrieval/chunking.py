from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=120,
    separators=["\n\n", "\n", ". ", " "]
)

def chunk_article(text: str, metadata: dict) -> list[dict]:
    pieces = splitter.split_text(text)
    return [
        {**metadata, "content": piece, "chunk_id": f"{metadata['url']}_{i}"}
        for i, piece in enumerate(pieces)
    ]
