import os
import zhconv

def convert(directory):
    for filename in os.listdir(directory):
        new_filename = zhconv.convert(filename, 'zh-hans')
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
        print(f'{filename} -> {new_filename}')

if __name__ == '__main__':
    convert('downloaded/cn')
