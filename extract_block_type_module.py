tf = r'C:\Users\Joaco\AppData\Roaming\Notion\Partitions\notion\Service Worker\CacheStorage\5381cb7d7f0d31a6afec904154068ba9f06028a5\28dc48d6-277e-469e-8ff4-6ad673ba27ca\34070e4cac3243af_0'

with open(tf, 'rb') as fp:
    raw = fp.read()
text = raw.decode('utf-8', errors='ignore')

start = 125500
end = 132000
print(text[start:end])
