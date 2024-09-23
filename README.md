# z-code

**z-code** 是一个用于生成 Markdown 格式的项目文档的工具，专门为 AI 项目输入提供简化的项目结构和代码内容展示。它通过读取项目目录中的文件和文件夹结构，并根据用户自定义的黑名单文件 `blacklist.ini` 进行过滤，生成包含项目结构和代码内容的 `.md` 文件。

开发该程序的意义在于，每次向AI聊天类平台输送纯文本过于麻烦，且这些平台对于md文档的支持效果较好，所以就想着：将小型项目的内容直接汇总到一个md文档中，作为投喂物进行提交，这样对于AI对话的效率是显著提高的。（主要是懒得复制粘贴那么多。。。）

![LOGO](image/favicon-192x192.png)

## 功能简介

- **自动生成 Markdown 文档**：从指定的项目目录中提取项目结构和代码文件，并生成 Markdown 格式的文档。
- **黑名单支持**：可以根据配置文件 `blacklist.ini` 排除特定的文件、文件夹和文件扩展名。
- **可选多次更新**：在生成完文档后，支持多次生成新文档，自动添加递增的编号文件名（如 `z-code01.md`, `z-code02.md` 等）。

![LOGO](image/test.gif)



## 使用方法

### 1. 基本运行

在项目的根目录下，运行 `z-code.py`(需要自带python环境)，并按照提示输入项目路径和输出文件名：

```bash
python z-code.py
```

或者直接使用下载已打包好的二进制文件[[仅支持Windows，点击即可下载]](https://github.com/QiPanTanYi/z-code/releases/tag/z-code)，解压整个z-code文件夹存放在自己喜欢的路径（推荐-桌面），使用`cmd`打开文件夹z-code，运行 `z-code.exe`，并按照提示输入项目路径和输出文件名：

```cmd
./z-code.exe
```

你需要按照提示提供以下信息：

- **项目路径**：要生成文档的项目文件夹路径（推荐使用绝对路径）。
- **输出文件名**：生成的 Markdown 文件名，可直接回车，默认命名为 `z-code.md`。
- **黑名单文件路径**：过滤文件/文件夹的黑名单配置文件路径，可直接回车，默认值为 `blacklist.ini`。
- **是否需要再次生成**：如下👇。<br />

### 2. 循环生成更新

生成完初始文档后，程序会询问你是否需要生成额外更新。如果选择 `y`，程序将生成下一个带编号的文件（如 `z-code01.md`，`z-code02.md`），直到你输入 `n` 停止。

### 3. 示例

```bash
Enter the project path: C:/path/to/project   # 文件夹绝对路径
Enter the output file name (default: z-code.md): project-doc.md	# 可自定义md文件名称
Enter the blacklist file path (default: blacklist.ini): 	# 默认回车则会选择blacklist.ini
Markdown file created: project-doc.md
Do you need an additional update? (y/n): y
Markdown file created: project-doc01.md
Do you need an additional update? (y/n): n
No further updates. Process stopped.
```

## blacklist.ini 配置文件说明

`blacklist.ini` 是 z-code 的黑名单配置文件，用于排除特定的文件、文件夹或文件扩展名。以下是 `blacklist.ini` 文件中的各个参数的说明：

```ini
[blacklist]
folders = node_modules,dist,build,.git,win-proxy,Docker,ssl,src\assets\json,.idea,.vscode
files = README.md,package-lock.json,nest-cli.json,package.json,postcss.config.js,tailwind.config.js,vite.config.js,.prettierrc,.gitignore,.eslintrc.js,.log,.editorconfig,.eslintignore,.eslintrc.cjs,.prettierignore,.prettierrc.json,deploy.sh,dev.bat,jquery.min.js
extensions = jpg,jpeg,png,gif,bmp,svg,mp4,avi,mov,wmv,flv,mkv,ttf,TTF,txt,mjs,ico,md
tree_folders_exclude = node_modules,dist,.idea,.vscode,.git
```

- **folders**: 该参数用于指定在生成<u>项目文档时要排除的文件夹</u>。这些文件夹通常包含编译后的代码、依赖项、配置等，不需要纳入文档生成。例如，`node_modules`, `.git`, `dist` 等。

- **files**: 该参数列出了在生成文档时<u>要排除的具体文件名称</u>。这些文件一般是项目中的配置文件或不需要展示的文件，如 `README.md`, `package.json` 等。

- **extensions**: 用于<u>指定要排除的文件扩展名</u>，所有带有这些扩展名的文件都不会纳入文档中。常见的有图片、视频、字体等文件格式，如 `jpg`, `png`, `svg`, `mp4`, `ico`，以及 `.md`，避免重复生成文档自身。

- **tree_folders_exclude**: 该参数指定在生成<u>项目文件夹树结构时要排除的文件夹</u>。和 `folders` 参数类似，目的是使文档更加简洁，排除不必要的构建文件夹、依赖文件夹等。

  



## 项目结构

```bash
├── image		   # 图の存放点
├── blacklist.ini  # 黑名单配置文件
├── README.md      # 当前文件
└── z-code.py      # 主程序文件
```



## 其他内容

- **生成时间戳**：在生成的 Markdown 文档中，`## Code Files` 部分将包括文件生成的具体时间（精确到毫秒），方便记录和追踪。
- **异常处理**：如果无法读取某些文件（如非 UTF-8 编码），程序会跳过这些文件（但会留白），而不会中断整个生成过程，所以最好确定好`blacklist.init`中的参数。

- **打包**：若你想二次开发后打包成exe文件，建议使用`pyinstaller`：

  ```bash
  pyinstaller -F  -i C:\Users\ASUS\Desktop\z-code\image\favicon-192x192.png C:\Users\ASUS\Desktop\z-code\z-code.py
  ```


- 最后的最后，祝你生活愉快！😄👍