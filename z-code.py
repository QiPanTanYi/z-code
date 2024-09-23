import os
import configparser
from pathlib import Path
from datetime import datetime


def read_blacklist(blacklist_file):
    if not os.path.exists(blacklist_file):
        print(f"Warning: Blacklist file '{blacklist_file}' not found. Using empty blacklist.")
        return {'folders': [], 'files': [], 'extensions': [], 'tree_folders_exclude': []}

    config = configparser.ConfigParser()
    config.read(blacklist_file)
    blacklist = {}
    if 'blacklist' in config:
        blacklist['folders'] = config['blacklist'].get('folders', '').split(',')
        blacklist['files'] = config['blacklist'].get('files', '').split(',')
        blacklist['extensions'] = config['blacklist'].get('extensions', '').split(',')
        blacklist['tree_folders_exclude'] = config['blacklist'].get('tree_folders_exclude', '').split(',')
    return blacklist



def is_blacklisted(file_path, blacklist):
    return (file_path.name in blacklist['files'] or
            file_path.suffix[1:] in blacklist['extensions'])


# 生成完整文件夹树（根据 blacklist.ini 中 tree_folders_exclude 来过滤文件夹）
def generate_full_tree(project_path, tree_folders_exclude):
    tree_lines = []
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in tree_folders_exclude]
        indent_level = Path(root).relative_to(project_path).parts
        if len(indent_level) == 0:
            tree_lines.append(f"├── {Path(root).name}/")  # 根文件夹
        else:
            tree_lines.append(f"{'│   ' * len(indent_level)}├── {Path(root).name}/")

        for file in files:
            file_indent = '│   ' * (len(indent_level) + 1)
            tree_lines.append(f"{file_indent}├── {file}")
    return '\n'.join(tree_lines)


def generate_markdown(project_path, output_file, blacklist):
    project_path = Path(project_path).resolve()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")  # 获取当前时间，精确到毫秒
    with open(output_file, 'w', encoding='utf-8') as md_file:
        md_file.write("# Project Documentation\n\n")

        # 写入项目结构树（根据 tree_folders_exclude 参数排除文件夹）
        md_file.write("## Project Structure\n\n")
        md_file.write("```\n")
        md_file.write(generate_full_tree(project_path, blacklist['tree_folders_exclude']))
        md_file.write("\n```\n\n")

        # 写入代码文件信息和生成时间
        md_file.write("## Code Files\n\n")
        md_file.write(f"**Generated on:** {current_time}\n\n")  # 增加生成时间

        # 继续写入所有代码文件内容（排除黑名单）
        for root, dirs, files in os.walk(project_path):
            # 根据黑名单排除文件夹（blacklist.ini）
            dirs[:] = [d for d in dirs if d not in blacklist['folders']]

            for file in files:
                file_path = Path(root) / file
                if not is_blacklisted(file_path, blacklist):
                    relative_path = file_path.relative_to(project_path)
                    md_file.write(f"### {relative_path}\n\n")
                    md_file.write(f"```\n")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as source_file:
                            md_file.write(source_file.read())
                    except UnicodeDecodeError:
                        md_file.write(f"Unable to read file: {relative_path}\n")
                    except Exception as e:
                        md_file.write(f"Error reading file {relative_path}: {str(e)}\n")
                    md_file.write("\n```\n\n")


if __name__ == "__main__":
    project_path = input("Enter the project path: ")
    output_file = input("Enter the output file name (default: z-code.md): ") or "z-code.md"
    blacklist_file = input("Enter the blacklist file path (default: blacklist.ini): ") or "blacklist.ini"

    # 提取文件名基础部分和扩展名
    base_name, ext = os.path.splitext(output_file)
    if not ext:  # 默认给 .md 后缀
        ext = '.md'

    blacklist = read_blacklist(blacklist_file)
    generate_markdown(project_path, output_file, blacklist)
    print(f"Markdown file created: {output_file}")

    # 新增：询问用户是否需要额外更新
    counter = 1  # 文件名计数器
    while True:
        update_more = input("Do you need an additional update? (y/n): ").strip().lower()
        if update_more == 'y':
            counter += 1
            # 使用用户的初始文件名基础生成后续文件名
            new_output_file = f"{base_name}{counter:02}{ext}"
            generate_markdown(project_path, new_output_file, blacklist)
            print(f"Markdown file created: {new_output_file}")
        elif update_more == 'n':
            print("No further updates. Process stopped.")
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
