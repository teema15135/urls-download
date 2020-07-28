import os
import shutil
import requests
from threading import Thread

# Select directory
directory = str(input("Enter directory (default 'out'): "))
outputDirectory = 'out/'
if directory:
    outputDirectory = f'{directory}/'

# Input urls
urls = str(input("Enter url separate by semicolon(;): "))
urls = urls.split(';')

# Clear empty url in urls
temp_urls = []
for url in urls:
    if url:
        temp_urls.append(url)
urls = temp_urls

# Check directory existance
if not os.path.exists(os.path.dirname(outputDirectory)):
    try:
        os.makedirs(os.path.dirname(outputDirectory))
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
else:
    print(f"You already have {outputDirectory} directory, press Enter to continue or exit with CTRL-C")
    input()

# Counting of completed file and indicator
complete_count = 0
file_count = len(urls)
progress = ['-' for i in range(file_count)]

# Define get function
def get(url, filenum):
    global complete_count, progress
    c = filenum
    file_name = url[url.rindex('/') + 1:len(url)]
    img = requests.get(url, stream=True)
    outputPath = f'out/{str(filenum).zfill(3)}_{file_name}'
    localFile = open(outputPath, 'wb')
    img.raw.decode_content = True
    shutil.copyfileobj(img.raw, localFile)
    progress[c] = '*'
    complete_count += 1

# Start all thread
thread_list = []
number = 0

for url in urls:
    thread = Thread(target=get, args=(url, number))
    thread.start()
    thread_list.append(thread)
    number += 1

while complete_count < file_count:
    print('\r' + (''.join(progress)), end='')
print('\r' + (''.join(progress)))
print("Download complete...")
input()