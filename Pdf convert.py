import fitz
import re
doc = fitz.open(r'C:\Users\user\Desktop\Test.pdf')

page1 = doc[0]
words1 = page1.get_text('words')
content1 = ' '.join([word[4] for word in words1])
#print(content1)

date = re.findall('[0-9]*/[0-9]*/[0-9]*', content1)[0]
print('Date:', date)
print('INV NO:', content1.split()[content1.split().index(date)+1])
quantity = re.findall('[0-9]*\,[0-9]*\.[0-9]*', content1)
print('Units:', quantity[0])
print('Amount: $' + quantity[1])

'''#print(content1)
#print('================')

page3 = doc[2]
words2 = page3.get_text('words')
content2 = ' '.join([word[4] for word in words2]).split()
#print(content2)

#matchContent = ' '.join([word for word in content1 if word in content2])
#print(matchContent)
'''