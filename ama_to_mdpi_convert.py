#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Set, Tuple


# Constants
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".pdf", ".eps", ".svg"}
BIB_EXTS = {".bib"}


@dataclass
class ConversionReport:
    """Conversion report data structure"""
    source_main_tex: Optional[str]
    mdpi_template_main_tex: Optional[str]
    extracted_body_lines: int
    copied_images: List[str]
    merged_bib: Optional[str]
    warnings: List[str]
    errors: List[str]

    def to_md(self) -> str:
        """Generate markdown report"""
        out: List[str] = []
        out.append("# AMA → MDPI LaTeX 迁移报告\n")

        out.append("## 1) 主文件识别")
        out.append(f"- AMA 主 tex：{self.source_main_tex or '（未找到）'}")
        out.append(f"- MDPI 模板主 tex：{self.mdpi_template_main_tex or '（未找到）'}")

        out.append("\n## 2) 正文抽取")
        out.append(f"- 抽取正文行数（粗略）：{self.extracted_body_lines}")

        out.append("\n## 3) 图片迁移")
        if self.copied_images:
            out.append(f"- 迁移图片数量：{len(self.copied_images)}")
            for p in self.copied_images[:40]:
                out.append(f"  - {p}")
            if len(self.copied_images) > 40:
                out.append("  - ...（剩余略）")
        else:
            out.append("- 未发现图片或未迁移")

        out.append("\n## 4) 参考文献迁移")
        out.append(f"- refs.bib：{self.merged_bib or '（未生成）'}")

        out.append("\n## 5) 警告（可能需要人工确认）")
        if self.warnings:
            for w in self.warnings:
                out.append(f"- ⚠️ {w}")
        else:
            out.append("- （无）")

        out.append("\n## 6) 错误（需要处理）")
        if self.errors:
            for e in self.errors:
                out.append(f"- ❌ {e}")
        else:
            out.append("- （无）")

        out.append("")
        return "\n".join(out)


class TeXParser:
    """Handle TeX file detection and parsing"""

    @staticmethod
    def read_text(p: Path) -> str:
        """Read text file with UTF-8 encoding"""
        return p.read_text(encoding="utf-8", errors="ignore")

    @staticmethod
    def find_main_tex(tex_files: List[Path]) -> Optional[Path]:
        """Find the main TeX file from a list of TeX files"""
        candidates: List[Path] = []
        for f in tex_files:
            t = TeXParser.read_text(f)
            if "\\documentclass" in t and "\\begin{document}" in t:
                candidates.append(f)

        if not candidates:
            return None

        # Priority names
        priority_names = ["main.tex", "manuscript.tex", "paper.tex", "submission.tex", "template.tex"]
        for name in priority_names:
            for c in candidates:
                if c.name.lower() == name:
                    return c

        # Fallback: shortest path depth then largest file size
        candidates.sort(key=lambda x: (len(x.parts), -x.stat().st_size))
        return candidates[0]

    @staticmethod
    def extract_document_body(tex_text: str) -> str:
        """Extract content between \\begin{document} and \\end{document}"""
        begin = tex_text.find("\\begin{document}")
        end = tex_text.rfind("\\end{document}")
        if begin == -1 or end == -1 or end <= begin:
            return ""
        body = tex_text[begin + len("\\begin{document}") : end]
        return body.strip()

    @staticmethod
    def collect_tex_files(folder: Path) -> List[Path]:
        """Collect all .tex files from a folder"""
        return [p for p in folder.rglob("*.tex") if p.is_file()]

    @staticmethod
    def extract_title(tex_text: str) -> Optional[str]:
        """Extract title from \\title{...} command"""
        match = re.search(r'\\title\{([^}]+)\}', tex_text)
        if match:
            return match.group(1).strip()
        return None

    @staticmethod
    def extract_abstract(body: str) -> Tuple[Optional[str], str]:
        """
        Extract abstract section content and return (abstract_text, body_without_abstract)
        Looks for \\section*{Abstract} or \\section{Abstract}
        """
        # Try to find abstract section
        pattern = r'\\section\*?\{Abstract\}\\label\{[^}]*\}\s*(.*?)(?=\\section|\Z)'
        match = re.search(pattern, body, re.DOTALL | re.IGNORECASE)

        if match:
            abstract_text = match.group(1).strip()
            # Remove the abstract section from body
            body_without_abstract = re.sub(
                r'\\section\*?\{Abstract\}\\label\{[^}]*\}.*?(?=\\section)',
                '',
                body,
                count=1,
                flags=re.DOTALL | re.IGNORECASE
            )
            return abstract_text, body_without_abstract.strip()

        return None, body


class ContentProcessor:
    """Process and transform TeX content"""

    @staticmethod
    def normalize_citations(body: str) -> Tuple[str, List[str]]:
        """Convert natbib-like cite commands to MDPI friendly \\cite{}"""
        warnings: List[str] = []

        # \citep{A} \citet{A} -> \cite{A}
        body2 = re.sub(r"\\citep\s*\{", r"\\cite{", body)
        body2 = re.sub(r"\\citet\s*\{", r"\\cite{", body2)

        # Check for unsupported commands
        if "\\citeauthor" in body2:
            warnings.append("检测到 \\citeauthor，MDPI 模板可能不支持或需要 natbib 支持。")
        if "\\citeyear" in body2:
            warnings.append("检测到 \\citeyear，MDPI 模板可能不支持或需要 natbib 支持。")

        return body2, warnings

    @staticmethod
    def fix_includegraphics_paths(tex: str, figures_dir: str = "figures") -> str:
        """Rewrite includegraphics{...} to includegraphics{figures/<basename>}"""
        pattern = re.compile(r"(\\includegraphics(?:\[[^\]]*\])?\{)([^}]+)(\})")

        def repl(m: re.Match) -> str:
            prefix = m.group(1)
            path = m.group(2).strip()
            suffix = m.group(3)

            # Already points to figures/
            if path.startswith(figures_dir + "/") or path.startswith("./" + figures_dir + "/"):
                return m.group(0)

            basename = Path(path).name
            return f"{prefix}{figures_dir}/{basename}{suffix}"

        return pattern.sub(repl, tex)

    @staticmethod
    def strip_ama_artifacts(body: str) -> str:
        """Remove common AMA-specific commands"""
        body = re.sub(r"\\maketitle\s*", "", body)
        return body

    @staticmethod
    def remove_biblatex_commands(body: str) -> Tuple[str, List[str]]:
        """Remove biblatex-specific commands that conflict with MDPI natbib"""
        warnings: List[str] = []

        # Remove \printbibliography command
        if "\\printbibliography" in body:
            body = re.sub(r"\\printbibliography\s*(?:\[[^\]]*\])?\s*", "", body)
            warnings.append("已移除 \\printbibliography 命令（MDPI 使用 natbib 而非 biblatex）。")

        # Remove \addbibresource commands
        if "\\addbibresource" in body:
            body = re.sub(r"\\addbibresource\s*\{[^}]+\}\s*", "", body)
            warnings.append("已移除 \\addbibresource 命令（MDPI 使用 natbib 而非 biblatex）。")

        return body, warnings


class FileHandler:
    """Handle file operations: copying images, merging bib files"""

    @staticmethod
    def collect_files_by_ext(folder: Path, exts: Set[str]) -> List[Path]:
        """Collect files with specific extensions"""
        return [p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in exts]

    @staticmethod
    def safe_copy(src: Path, dst: Path) -> None:
        """Safely copy file, creating parent directories if needed"""
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    @staticmethod
    def copy_images(source_dir: Path, out_dir: Path, figures_dir: str) -> Tuple[List[str], List[str]]:
        """Copy all images from source to output figures directory"""
        images = FileHandler.collect_files_by_ext(source_dir, IMAGE_EXTS)
        fig_dir = out_dir / figures_dir
        fig_dir.mkdir(parents=True, exist_ok=True)

        copied: List[str] = []
        warnings: List[str] = []

        for img in images:
            dst = fig_dir / img.name
            try:
                FileHandler.safe_copy(img, dst)
                copied.append(str(dst.relative_to(out_dir)))
            except Exception as e:
                warnings.append(f"复制图片失败：{img} -> {dst}，原因：{e}")

        return copied, warnings

    @staticmethod
    def merge_bib_files(bibs: List[Path], out_bib: Path) -> Tuple[bool, List[str]]:
        """Merge multiple .bib files into one, detecting duplicates"""
        warnings: List[str] = []
        seen_keys: Set[str] = set()
        merged_entries: List[str] = []

        key_pattern = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,", re.IGNORECASE)

        for bib in bibs:
            txt = TeXParser.read_text(bib)
            parts = re.split(r"\n(?=@\w+\s*\{)", txt, flags=re.IGNORECASE)
            for part in parts:
                s = part.strip()
                if not s.startswith("@"):
                    continue
                m = key_pattern.search(s)
                if not m:
                    warnings.append(f"bib 条目 key 解析失败（跳过）：{bib.name}")
                    continue
                k = m.group(1).strip()
                if k in seen_keys:
                    warnings.append(f"bib key 重复跳过：{k}（来源 {bib.name}）")
                    continue
                seen_keys.add(k)
                merged_entries.append(s + "\n")

        if not merged_entries:
            return False, warnings

        out_bib.parent.mkdir(parents=True, exist_ok=True)
        out_bib.write_text("\n\n".join(merged_entries), encoding="utf-8")
        return True, warnings

    @staticmethod
    def copy_template_structure(mdpi_dir: Path, out_dir: Path) -> None:
        """Copy entire MDPI template structure to output directory"""
        for p in mdpi_dir.rglob("*"):
            if p.is_dir():
                continue
            rel = p.relative_to(mdpi_dir)
            dst = out_dir / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dst)


class AMAToMDPIConverter:
    """Main converter class orchestrating the conversion process"""

    def __init__(
        self,
        source_dir: Path,
        mdpi_template_dir: Path,
        out_dir: Path,
        out_main_tex: str = "main.tex",
        figures_dir: str = "figures",
        bib_name: str = "refs.bib"
    ):
        self.source_dir = source_dir.resolve()
        self.mdpi_dir = mdpi_template_dir.resolve()
        self.out_dir = out_dir.resolve()
        self.out_main_tex = out_main_tex
        self.figures_dir = figures_dir
        self.bib_name = bib_name

        self.report = ConversionReport(
            source_main_tex=None,
            mdpi_template_main_tex=None,
            extracted_body_lines=0,
            copied_images=[],
            merged_bib=None,
            warnings=[],
            errors=[],
        )

        # Extracted metadata from source
        self.title: Optional[str] = None
        self.abstract: Optional[str] = None

    def validate_inputs(self) -> bool:
        """Validate input directories exist"""
        if not self.source_dir.exists():
            self.report.errors.append(f"source_dir 不存在：{self.source_dir}")
        if not self.mdpi_dir.exists():
            self.report.errors.append(f"mdpi_template_dir 不存在：{self.mdpi_dir}")

        return len(self.report.errors) == 0

    def find_main_files(self) -> Tuple[Optional[Path], Optional[Path]]:
        """Find main TeX files in both source and template"""
        tex_source_files = TeXParser.collect_tex_files(self.source_dir)
        tex_mdpi_files = TeXParser.collect_tex_files(self.mdpi_dir)

        src_main = TeXParser.find_main_tex(tex_source_files)
        mdpi_main = TeXParser.find_main_tex(tex_mdpi_files)

        if not src_main:
            self.report.errors.append("未找到 AMA 主 tex（缺少 \\documentclass 或 \\begin{document}）。")
        else:
            self.report.source_main_tex = str(src_main.relative_to(self.source_dir))

        if not mdpi_main:
            self.report.errors.append("未找到 MDPI 模板主 tex（缺少 \\documentclass 或 \\begin{document}）。")
        else:
            self.report.mdpi_template_main_tex = str(mdpi_main.relative_to(self.mdpi_dir))

        return src_main, mdpi_main

    def extract_and_process_body(self, src_main: Path) -> str:
        """Extract and process AMA document body"""
        src_text = TeXParser.read_text(src_main)
        body = TeXParser.extract_document_body(src_text)

        if not body:
            self.report.errors.append("AMA 主文件无法抽取正文块（找不到 begin/end document）。")
            return ""

        # Extract title from preamble
        self.title = TeXParser.extract_title(src_text)
        if not self.title:
            self.report.warnings.append("未找到 \\title{} 命令，MDPI 标题将使用默认值。")

        # Extract abstract from body
        self.abstract, body = TeXParser.extract_abstract(body)
        if self.abstract:
            self.report.warnings.append("已从正文中提取 abstract 并注入到 MDPI 模板的 \\abstract{} 命令。")
        else:
            self.report.warnings.append("未找到 abstract section，MDPI abstract 将使用默认值。")

        # Process citations
        body, cite_warns = ContentProcessor.normalize_citations(body)
        self.report.warnings.extend(cite_warns)

        # Remove biblatex commands
        body, biblatex_warns = ContentProcessor.remove_biblatex_commands(body)
        self.report.warnings.extend(biblatex_warns)

        # Strip AMA artifacts
        body = ContentProcessor.strip_ama_artifacts(body)

        # Fix graphics paths
        body = ContentProcessor.fix_includegraphics_paths(body, figures_dir=self.figures_dir)

        self.report.extracted_body_lines = len(body.splitlines())

        return body

    def inject_body_into_template(self, mdpi_main: Path, body: str) -> str:
        """Inject processed body into MDPI template"""
        mdpi_template_path = self.out_dir / mdpi_main.relative_to(self.mdpi_dir)
        mdpi_template_text = TeXParser.read_text(mdpi_template_path)

        # Find \begin{document} and \end{document} at start of line (not in comments)
        begin_match = re.search(r'^\\begin\{document\}', mdpi_template_text, re.MULTILINE)
        end_match = re.search(r'^\\end\{document\}', mdpi_template_text, re.MULTILINE)

        if not begin_match or not end_match:
            self.report.errors.append("MDPI 模板主文件结构异常，无法定位 begin/end document。")
            return ""

        mdpi_begin = begin_match.end()
        mdpi_end = end_match.start()

        if mdpi_end <= mdpi_begin:
            self.report.errors.append("MDPI 模板主文件结构异常，end document 在 begin document 之前。")
            return ""

        pre = mdpi_template_text[:mdpi_begin]
        post = mdpi_template_text[mdpi_end:]

        # Replace title in preamble if extracted
        if self.title:
            pre = re.sub(r'\\Title\{[^}]*\}', f'\\\\Title{{{self.title}}}', pre)

        # Replace abstract in preamble if extracted
        if self.abstract:
            # Escape special regex characters in abstract
            abstract_escaped = self.abstract.replace('\\', '\\\\')
            pre = re.sub(
                r'\\abstract\{[^}]*?\}',
                f'\\\\abstract{{{self.abstract}}}',
                pre,
                flags=re.DOTALL
            )

        # Combine body with template
        final_main = pre + "\n\n" + body + "\n\n" + post

        # Ensure bibliography command exists (check if not already in body or template)
        # Check the entire document body section
        if "\\bibliography{" not in body and "\\begin{thebibliography}" not in body:
            # Insert bibliography before \end{document}
            end_doc_pos = final_main.rfind("\\end{document}")
            if end_doc_pos != -1:
                final_main = final_main[:end_doc_pos] + "\\bibliography{refs}\n\n" + final_main[end_doc_pos:]
                self.report.warnings.append("未检测到 bibliography 指令，已在 \\end{document} 前添加 \\bibliography{refs}。")

        return final_main

    def process_images(self) -> None:
        """Copy images from source to output"""
        copied, warnings = FileHandler.copy_images(
            self.source_dir,
            self.out_dir,
            self.figures_dir
        )
        self.report.copied_images = copied
        self.report.warnings.extend(warnings)

    def process_bibliography(self) -> None:
        """Merge bibliography files"""
        bibs = FileHandler.collect_files_by_ext(self.source_dir, BIB_EXTS)
        out_bib = self.out_dir / self.bib_name

        if bibs:
            ok, bib_warns = FileHandler.merge_bib_files(bibs, out_bib)
            self.report.warnings.extend(bib_warns)
            if ok:
                self.report.merged_bib = str(out_bib.relative_to(self.out_dir))
            else:
                self.report.warnings.append("bib 合并失败：未生成 refs.bib（可能源 bib 为空）。")
        else:
            self.report.warnings.append("未找到任何 .bib 文件，引用可能无法编译。")

    def convert(self) -> bool:
        """Execute the complete conversion process"""
        # Create output directory
        self.out_dir.mkdir(parents=True, exist_ok=True)

        # Validate inputs
        if not self.validate_inputs():
            self.save_report()
            return False

        # Find main files
        src_main, mdpi_main = self.find_main_files()
        if self.report.errors:
            self.save_report()
            return False

        # Copy MDPI template structure
        FileHandler.copy_template_structure(self.mdpi_dir, self.out_dir)

        # Extract and process body
        body = self.extract_and_process_body(src_main)
        if self.report.errors:
            self.save_report()
            return False

        # Inject body into template
        final_main = self.inject_body_into_template(mdpi_main, body)
        if self.report.errors:
            self.save_report()
            return False

        # Process images
        self.process_images()

        # Process bibliography
        self.process_bibliography()

        # Write output main TeX file
        (self.out_dir / self.out_main_tex).write_text(final_main, encoding="utf-8")

        # Save report
        self.save_report()

        return True

    def save_report(self) -> None:
        """Save conversion report to output directory"""
        (self.out_dir / "conversion_report.md").write_text(
            self.report.to_md(),
            encoding="utf-8"
        )

    def print_summary(self) -> None:
        """Print conversion summary"""
        if self.report.errors:
            print(f"[ERROR] Conversion failed. Check report: {self.out_dir / 'conversion_report.md'}")
            for err in self.report.errors:
                print(f"  - {err}")
        else:
            print(f"[OK] Converted project generated at: {self.out_dir}")
            print(f"[OK] Main TeX: {self.out_dir / self.out_main_tex}")
            print(f"[OK] Report: {self.out_dir / 'conversion_report.md'}")


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Convert AMA format LaTeX paper to MDPI template format"
    )
    ap.add_argument("--source_dir", required=True, help="AMA source directory")
    ap.add_argument("--mdpi_template_dir", required=True, help="MDPI template directory")
    ap.add_argument("--out_dir", required=True, help="Output directory")
    ap.add_argument("--out_main_tex", default="main.tex", help="Output main TeX filename")
    ap.add_argument("--figures_dir", default="figures", help="Figures directory name")
    ap.add_argument("--bib_name", default="refs.bib", help="Output bibliography filename")
    args = ap.parse_args()

    converter = AMAToMDPIConverter(
        source_dir=Path(args.source_dir),
        mdpi_template_dir=Path(args.mdpi_template_dir),
        out_dir=Path(args.out_dir),
        out_main_tex=args.out_main_tex,
        figures_dir=args.figures_dir,
        bib_name=args.bib_name
    )

    success = converter.convert()
    converter.print_summary()

    if not success:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
