# AMA to MDPI LaTeX Converter

自动将 AMA 格式的 LaTeX 论文转换为 MDPI 模板格式，并生成最终 PDF。

## 快速开始

### Windows 用户

双击运行批处理文件：
```
convert_and_compile.bat
```

或在命令行中运行：
```cmd
convert_and_compile.bat
```

### Linux/Mac 用户

在终端中运行：
```bash
chmod +x convert_and_compile.sh
./convert_and_compile.sh
```

## 功能特点

✅ **自动转换**：从 AMA 格式转换到 MDPI 格式
✅ **标题提取**：自动提取并注入论文标题
✅ **摘要处理**：提取摘要并避免重复
✅ **引用转换**：将 biblatex 引用转换为 natbib 格式
✅ **图片迁移**：自动复制所有图片文件
✅ **参考文献**：合并并处理参考文献数据库
✅ **完整编译**：自动运行完整的 LaTeX 编译流程（pdflatex + bibtex + pdflatex × 2）

## 目录结构

```
paper/
├── ama_source/              # AMA 格式源文件
│   ├── manuscript.tex       # 主 TeX 文件
│   ├── ref.bib              # 参考文献
│   └── *.png                # 图片文件
├── mdpi_template/           # MDPI 模板
│   ├── template.tex         # 模板主文件
│   └── Definitions/         # 样式文件
├── output/                  # 输出目录（自动生成）
│   ├── main.tex             # 转换后的主文件
│   ├── main.pdf             # 最终 PDF
│   ├── refs.bib             # 合并的参考文献
│   ├── figures/             # 图片文件夹
│   └── conversion_report.md # 转换报告
├── ama_to_mdpi_convert.py   # 转换程序
└── convert_and_compile.bat   # 一键转换和编译脚本
```

## 运行流程

脚本执行以下步骤：

1. **[1/5] 运行转换程序**：将 AMA 格式转换为 MDPI 格式
2. **[2/5] 第一次编译**：生成 .aux 文件
3. **[3/5] 运行 BibTeX**：处理参考文献数据库
4. **[4/5] 第二次编译**：包含参考文献
5. **[5/5] 最终编译**：解析所有交叉引用

## 输出文件

- **main.pdf**：最终生成的 PDF 文档（包含完整的参考文献）
- **conversion_report.md**：详细的转换报告，包含：
  - 识别的主文件
  - 提取的正文行数
  - 迁移的图片数量
  - 合并的参考文献信息
  - 警告和错误信息

## 手动运行（可选）

如果需要单独运行某个步骤：

### 仅转换（不编译）
```bash
python ama_to_mdpi_convert.py --source_dir ./ama_source --mdpi_template_dir ./mdpi_template --out_dir ./output
```

### 仅编译（已转换）
```bash
cd output
compile.bat         # Windows
./compile.sh        # Linux/Mac
```

## 常见问题

### Q: 转换失败怎么办？
A: 检查 `output/conversion_report.md` 中的错误信息，确保：
- ama_source 目录包含有效的 .tex 文件
- mdpi_template 目录包含完整的模板文件

### Q: PDF 中没有参考文献？
A: 确保运行了完整的编译流程（包含 bibtex 步骤）。使用提供的批处理脚本会自动完成。

### Q: 编译时出现错误？
A: 检查 `output/main.log` 文件查看详细的编译错误信息。

### Q: 图片没有显示？
A: 确保：
- 图片文件在 ama_source 目录中
- 图片格式为支持的类型（.png, .jpg, .jpeg, .pdf, .eps, .svg）

## 系统要求

- Python 3.7+
- LaTeX 发行版（如 MiKTeX 或 TeX Live）
- BibTeX

## 技术细节

### 转换特性

- **引用格式转换**：`\citep{}` → `\cite{}`，`\citet{}` → `\cite{}`
- **移除 biblatex 命令**：自动移除 `\printbibliography` 和 `\addbibresource`
- **图片路径标准化**：所有图片路径统一为 `figures/<filename>`
- **重复检测**：检测并警告重复的参考文献条目

### 面向对象架构

- `TeXParser`：TeX 文件解析
- `ContentProcessor`：内容处理和转换
- `FileHandler`：文件操作
- `AMAToMDPIConverter`：主控制器

## 许可证

本项目用于学术论文格式转换。
