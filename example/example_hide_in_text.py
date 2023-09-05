from hide_info import hide_in_text

bytes_data = "待嵌入的句子".encode('utf-8')

text = '一段文本，下面的代码中，这段文本会被嵌入隐藏信息' * 50

text_new = hide_in_text.encode(bytes_data, text)

text_extract = hide_in_text.decode(text_new)

print(text_extract.decode('utf-8'))
