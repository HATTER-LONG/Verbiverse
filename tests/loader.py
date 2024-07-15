from langchain_community.document_loaders import PyPDFLoader

# from langchain_core.documents import Document
path = "~/Desktop/资料/文档/Magic Tree House 神奇树屋01-55（MOBI+PDF+MP3）/01 Dinosaurs Before Dark - Mary Pope Osborne[www.oiabc.com]/01 Dinosaurs Before Dark - Mary Pope Osborne.pdf"
ret = PyPDFLoader(path)
# print(len(ret.load()))
print(len(ret.load_and_split()))
print(ret.load_and_split())
