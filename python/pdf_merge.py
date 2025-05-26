import os
import PyPDF2
import argparse
 
def merge_pdfs(paths, output):
    pdf_writer = PyPDF2.PdfWriter()
 
    for path in paths:
        pdf_reader = PyPDF2.PdfReader(path)
        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])
 
    with open(output, 'wb') as out:
        pdf_writer.write(out)
 
def main(data_dir):
    names = os.listdir(data_dir)
    print("names:", names)
 
    file_paths = []
    for name in names:
        file_paths.append(os.path.join(data_dir, name))
 
    output = os.path.join(data_dir, "合并后的PDF/merge_%02d.pdf" % len(names))  # 合并后的PDF文件路径
    os.makedirs("./合并后的PDF", exist_ok=True)
 
    merge_pdfs(file_paths, output)
    print("合并后文件：", output)
 
def argv_parse():
    parser = argparse.ArgumentParser(usage="it's usage PyPDF2.", description="pdf merge.")
    parser.add_argument("--data_dir", type=str, help="pdf file dir.")
    return parser.parse_args()
 
if __name__ == "__main__":
    argv = argv_parse()
    print("argv:", argv)
    main(argv.data_dir)