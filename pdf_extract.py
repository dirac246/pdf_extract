#
# python pdf_extract.py [input pdf] [start page] [end page] -o [output pdf]

import argparse
import os
from pypdf import PdfReader, PdfWriter


def extract_pages(input_pdf, start_page, end_page, output_pdf=None):
    # 1. 入力ファイルの存在確認
    if not os.path.exists(input_pdf):
        print(f"エラー: 指定されたファイルが見つかりません: {input_pdf}")
        return

    # 2. 出力ファイル名が指定されていない場合は自動生成
    if not output_pdf:
        base, ext = os.path.splitext(input_pdf)
        output_pdf = f"{base}_extracted_{start_page}_{end_page}{ext}"

    # 3. PDFの読み込みとページ抽出
    try:
        reader = PdfReader(input_pdf)
        writer = PdfWriter()
        total_pages = len(reader.pages)

        # ページ番号のバリデーション
        if start_page < 1 or end_page > total_pages or start_page > end_page:
            print(
                f"エラー: ページ指定が不正です。このPDFの総ページ数は {total_pages} です。"
            )
            return

        # pypdfは0始まりのインデックスのため、1を引いて調整
        for page_num in range(start_page - 1, end_page):
            writer.add_page(reader.pages[page_num])

        # 4. 新しいPDFファイルへの書き出し
        with open(output_pdf, "wb") as output_file:
            writer.write(output_file)

        print(f"成功: {start_page}ページから{end_page}ページを抽出しました。")
        print(f"保存先: {output_pdf}")

    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    # コマンドライン引数の設定
    parser = argparse.ArgumentParser(
        description="PDFファイルから指定したページ範囲を別ファイルとして抽出します。"
    )
    # 必須の引数
    parser.add_argument(
        "input_pdf", type=str, help="入力するPDFファイルのパス"
    )
    parser.add_argument(
        "start_page", type=int, help="開始ページ番号 (1始まり)"
    )
    parser.add_argument(
        "end_page", type=int, help="終了ページ番号 (1始まり)"
    )

    # 任意の引数（出力パスの指定）
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="出力するPDFファイルのパス (省略時は自動生成されます)",
    )

    args = parser.parse_args()

    # 抽出処理の実行
    extract_pages(args.input_pdf, args.start_page, args.end_page, args.output)
