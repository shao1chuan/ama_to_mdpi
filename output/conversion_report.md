# AMA → MDPI LaTeX 迁移报告

## 1) 主文件识别
- AMA 主 tex：manuscript.tex
- MDPI 模板主 tex：template.tex

## 2) 正文抽取
- 抽取正文行数（粗略）：868

## 3) 图片迁移
- 迁移图片数量：3
  - figures\1.png
  - figures\2.png
  - figures\3.png

## 4) 参考文献迁移
- refs.bib：refs.bib

## 5) 警告（可能需要人工确认）
- ⚠️ 已从正文中提取 abstract 并注入到 MDPI 模板的 \abstract{} 命令。
- ⚠️ 已移除 \printbibliography 命令（MDPI 使用 natbib 而非 biblatex）。
- ⚠️ 未检测到 bibliography 指令，已在 \end{document} 前添加 \bibliography{refs}。
- ⚠️ bib key 重复跳过：ParkLeeKimSeoGoothers2020（来源 ref.bib）

## 6) 错误（需要处理）
- （无）
