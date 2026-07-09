from langchain_text_splitters import RecursiveCharacterTextSplitter

text = ""
with open("notes.txt") as f:
    text = f.read()

print(text)

text_splitter = RecursiveCharacterTextSplitter(
    separators=[" ", ".", "\n"],
    chunk_size=200,
    chunk_overlap=50,
    keep_separator=True,
)

chunks = text_splitter.split_text(text)

for chunk in chunks:
    print(len(chunk))
    print(chunk)
