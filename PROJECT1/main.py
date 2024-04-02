import os
import re

def process_text(text):
    # 删除字母，只保留中文和数字
    processed_text = re.sub(r'[^\u4e00-\u9fa5\d]+', '', text)
    return processed_text

def process_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        content = file.read()
        processed_content = process_text(content)
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(processed_content)

def process_directory(src_directory, dest_directory):
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)

    for root, _, files in os.walk(src_directory):
        for file_name in files:
            input_path = os.path.join(root, file_name)
            output_path = os.path.join(dest_directory, file_name)
            process_file(input_path, output_path)

if __name__ == "__main__":
    src_directory = "downloaded/cn"
    dest_directory = "processed_texts_chinese"
    process_directory(src_directory, dest_directory)
    print("Text processing completed.")

