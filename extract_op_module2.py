tf = r'C:\Users\Joaco\AppData\Roaming\Notion\Partitions\notion\Service Worker\CacheStorage\5381cb7d7f0d31a6afec904154068ba9f06028a5\28dc48d6-277e-469e-8ff4-6ad673ba27ca\34070e4cac3243af_0'

with open(tf, 'rb') as fp:
    raw = fp.read()
text = raw.decode('utf-8', errors='ignore')

idx = text.find('command:"listAfter')
start = idx
end = min(len(text), idx + 2500)
print(text[start:end])
