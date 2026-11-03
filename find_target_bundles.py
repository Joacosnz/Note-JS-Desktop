import os

cache_dir = r'C:\Users\Joaco\AppData\Roaming\Notion\Partitions\notion\Service Worker\CacheStorage'
target_names = ['44dd6ef580e46afc_0', 'ef0ca39f9c8a3890_0', '8cbceebc64912dc2_1']
found = {}
for root, dirs, files in os.walk(cache_dir):
    for f in files:
        if f in target_names:
            found[f] = os.path.join(root, f)

for name, path in found.items():
    print(f"{name} -> {path}")
