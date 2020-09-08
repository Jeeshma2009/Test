# Usage python my_program.py --input  Interview_sample_data.pdf  --output  sample_data.json

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
import json
import sys
import argparse

try:
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-inputfile", "--input", required=True,
      help="path to input dataset")
    ap.add_argument("-outputfile", "--output", required=True,
      help="path to output model")
    args = vars(ap.parse_args())
    d={}
    json_file={}
    content=''
    sh=''
    c=0

    def createPDFDoc(fpath):
        fp = open(fpath, 'rb')
        parser = PDFParser(fp)
        document = PDFDocument(parser, password='')
        # Check if the document allows text extraction. If not, abort.
        if not document.is_extractable:
            raise "Not extractable"
        else:
            return document


    def createDeviceInterpreter():
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        return device, interpreter


    def parse_obj(objs):
        for obj in objs:
            if isinstance(obj, pdfminer.layout.LTTextBox):
                for o in obj._objs:
                    if isinstance(o,pdfminer.layout.LTTextLine):
                        text=o.get_text()
                        if text.strip():
                            tmp=text.strip()
                            b='_'
                            for char in b:
                                 tmp= tmp.replace(char,"")
                                 tmp = (tmp.encode('ascii', 'ignore')).decode("utf-8")
                            for c in  o._objs:
                                if isinstance(c, pdfminer.layout.LTChar):
                                    d[tmp]=c.size

            elif isinstance(obj, pdfminer.layout.LTFigure):
                parse_obj(obj._objs)
            else:
                pass

    document=createPDFDoc("Interview_sample_data.pdf")
    device,interpreter=createDeviceInterpreter()
    pages=PDFPage.create_pages(document)
    interpreter.process_page(next(pages))
    layout = device.get_result()
    parse_obj(layout._objs)

    for i in d:
        if c==0:
            json_file["Name"]=i
            c+=1
        else:
            if int(d[i])!=12: #font size 12 is used for sub heading
                content =content+i+' '
            else:
                if c==1:

                    json_file["Address & Email"]=content
                    content=''
                    c+=1

                else:

                    json_file[sh]=content
                    content=''
                sh=i
    with open('data.json', 'w') as outfile:
        json.dump(json_file, outfile)
        print("Json file created please check your folder")

except Exception as e:
    print("Sorry unable to process")

    
