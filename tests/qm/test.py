import os
import re


# 递归遍历定目录所有文件，获取含 TMP 的文件名
def get_tmp_files(path):
    tmp_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if "TMP" in file:
                tmp_files.append(os.path.join(root, file))
    return tmp_files


def extract_context_tags(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = r"<TS(.*?)>(.*?)</TS>"
    matches = re.findall(pattern, content, flags=re.DOTALL)[0][1]
    return matches


def process_ts_file_inplace(input_file):
    print(input_file)
    context = extract_context_tags(input_file)
    with open(input_file, "r+", encoding="utf-8") as f:
        content = f.read()

        content = content.replace(context, "")

        # 将修改后的内容写入文件
        f.seek(0)
        f.truncate()
        f.write(content)


files = get_tmp_files("./tests")
print(files)
firstfile = ""
content = ""
firstcontext = ""
with open(files[0], "r", encoding="utf-8") as f:
    firstfile = f.read()
    firstcontext = extract_context_tags(files[0])

for file in files:
    content = content + extract_context_tags(file)

result = firstfile.replace(firstcontext, content)
with open("./tests/qm/result.ts", "w", encoding="utf-8") as f:
    f.write(result)

# process_ts_file_inplace(files[0])
# print(extract_context_tags(file[0]))
