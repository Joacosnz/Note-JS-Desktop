import os

roaming = r'C:\Users\Joaco\AppData\Roaming\Notion'
for root, dirs, files in os.walk(roaming):
    for f in files:
        full = os.path.join(root, f)
        size = os.path.getsize(full)
        if size > 500000: # > 500 KB
            print(f"{full} ({size / (1024*1024):.2f} MB)")
