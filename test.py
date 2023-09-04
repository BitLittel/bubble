from xml2xlsx import xml2xlsx

template = '<sheet title="test"></sheet>'
t = open('test.xml', 'rb').read()
print(t)

f = open('test.xlsx', 'wb')

convert = xml2xlsx(t)
print(convert.decode('WIN-1255'))
f.write(convert)
f.close()
