import logging

from langchain_text_splitters import RecursiveCharacterTextSplitter

class RecursiveChunker:
    def __init__(self, chunk_size: int, chunk_overlap: int) -> None:
        log = logging.getLogger(__name__)
        log.info(
            "Initializing recursive chunker with params: chunk_size = %d, chunk_overlap = %d"
            % (chunk_size, chunk_overlap)
        )
        self._splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    def split_text(self, text: str) -> list[str]:
        return self._splitter.split_text(text)