import os

pages_folder = 'pages'
print(f"Does pages folder exist? {os.path.exists(pages_folder)}")
print(f"Contents of pages folder: {os.listdir(pages_folder)}")