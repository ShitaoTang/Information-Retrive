import os
import re
import zhconv

def get_character_cn(src_text):
    dest_text = re.sub(r"[^\u4e00-\u9fa5]+", '', src_text)
    # convert zh-tw/zh-hk/zh-hant to zh-cn
    dest_text = zhconv.convert(dest_text, "zh-cn")
    return dest_text

def get_character_en(src_text):
    dest_text = re.sub(r"[^A-Za-z]+", ' ', src_text)
    dest_text = dest_text.lower()
    return dest_text

def get_characterized_file(src_file, dest_file, get_character):
    with open(src_file, 'r', encoding = "utf-8") as f:
        dest_text = get_character(f.read())
    with open(dest_file, 'w', encoding = "utf-8") as f:
        f.write(dest_text)

dict_get_character = {
    "en": get_character_en,
    "cn": get_character_cn
}

def characterize(src_dir, dest_dir, type):
    os.makedirs(dest_dir, exist_ok = True)
    
    files = os.listdir(src_dir)
    index = 1
    for file in files:
        src_file = os.path.join(src_dir, file)
        dest_file = os.path.join(dest_dir, f"{index}.txt")
        # using dictionary to call function instead of "if...else..."
        get_characterized_file(src_file, dest_file, dict_get_character[type])
        index += 1


# cn
src_dir_cn = "downloaded/cn"
dest_dir_cn = "res/cn"
characterize(src_dir_cn, dest_dir_cn, "cn")

#en
src_dir_en = "downloaded/en"
dest_dir_en = "res/en"
characterize(src_dir_en, dest_dir_en, "en")

