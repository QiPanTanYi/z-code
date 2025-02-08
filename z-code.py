import os
import configparser
from pathlib import Path
from datetime import datetime


def read_blacklist(blacklist_file):
    if not os.path.exists(blacklist_file):
        print(f"Warning: Blacklist file '{blacklist_file}' not found. Using empty blacklist.")
        return {'folders': [], 'files': [], 'extensions': [], 'tree_folders_exclude': []}

    config = configparser.ConfigParser()
    try:
        with open(blacklist_file, 'r', encoding='utf-8') as f:
            config.read_file(f)
    except UnicodeDecodeError:
        print(f"Error: Unable to read '{blacklist_file}' due to encoding issues.")
        return {'folders': [], 'files': [], 'extensions': [], 'tree_folders_exclude': []}

    blacklist = {}
    if 'blacklist' in config:
        blacklist['folders'] = config['blacklist'].get('folders', '').split(',')
        blacklist['files'] = config['blacklist'].get('files', '').split(',')
        blacklist['extensions'] = config['blacklist'].get('extensions', '').split(',')
        blacklist['tree_folders_exclude'] = config['blacklist'].get('tree_folders_exclude', '').split(',')
    return blacklist


def read_config(config_file):
    if not os.path.exists(config_file):
        print(f"Error: Config file '{config_file}' not found.")
        return None

    config = configparser.ConfigParser()
    try:
        with open(config_file, 'r', encoding='utf-8') as f:  # 强制使用 UTF-8 读取
            config.read_file(f)
    except UnicodeDecodeError:
        print(f"Error: Unable to read '{config_file}' due to encoding issues.")
        return None

    if 'config' not in config:
        print(f"Error: Invalid config file format.")
        return None

    return {
        'project_path': config['config'].get('project_path', '').strip(),
        'output_file': config['config'].get('output_file', 'project-doc.md').strip(),
        'blacklist_file': config['config'].get('blacklist_file', 'blacklist.ini').strip(),
        'output_path': config['config'].get('output_path', '.').strip()
    }


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


def generate_markdown(project_path, output_file, blacklist, output_path):
    project_path = Path(project_path).resolve()
    output_dir = Path(output_path).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file_path = output_dir / output_file

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")  # 获取当前时间，精确到毫秒
    with open(output_file_path, 'w', encoding='utf-8') as md_file:
        # 写入项目结构树（根据 tree_folders_exclude 参数排除文件夹）
        md_file.write("# Project Documentation\n\n")
        md_file.write("## Project Structure\n\n")
        md_file.write("````\n")
        md_file.write(generate_full_tree(project_path, blacklist['tree_folders_exclude']))
        md_file.write("\n````\n\n")
        # 写入代码文件信息和生成时间
        md_file.write("## Code Files\n\n")
        md_file.write(f"**Generated on:** {current_time}\n\n")

        # 继续写入所有代码文件内容（排除黑名单）
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if d not in blacklist['folders']]
            for file in files:
                file_path = Path(root) / file
                if not is_blacklisted(file_path, blacklist):
                    relative_path = file_path.relative_to(project_path)
                    md_file.write(f"### {relative_path}\n\n")
                    md_file.write("````\n")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as source_file:
                            md_file.write(source_file.read())
                    except UnicodeDecodeError:
                        md_file.write(f"Unable to read file: {relative_path}\n")
                    except Exception as e:
                        md_file.write(f"Error reading file {relative_path}: {str(e)}\n")
                    md_file.write("\n````\n\n")


if __name__ == "__main__":
    config = read_config("config.ini")
    if not config:
        print("Failed to load config.ini. Exiting.")
        exit(1)

    project_path = config['project_path']
    output_file = config['output_file']
    blacklist_file = config['blacklist_file']
    output_path = config['output_path']

    if not project_path:
        print("Error: project_path is not specified in config.ini")
        exit(1)

    blacklist = read_blacklist(blacklist_file)
    output_base, output_ext = os.path.splitext(output_file)
    output_ext = output_ext if output_ext else '.md'

    output_file_path = Path(output_path) / output_file
    counter = 1  # 文件名计数器，若该文件名存在，计数累增
    while output_file_path.exists():
        output_file_path = Path(output_path) / f"{output_base}{counter:02}{output_ext}"
        counter += 1

    generate_markdown(project_path, output_file_path.name, blacklist, output_path)
    print(f"Markdown file created: {output_file_path}")
