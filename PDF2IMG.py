from os import listdir
import concurrent.futures
import Converter

#===================== Convert PDFs to images and straighten =================================
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(Converter.Convert, PDF_file): PDF_file for PDF_file in listdir("RawFiles")}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            err = ""
            print('%r generated an exception: %s' % (url, exc))

#===================== Convert PDFs to images and straighten =================================
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(Converter.Convert, PDF_file): PDF_file for PDF_file in listdir("RawFiles")}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            err = ""
            print('%r generated an exception: %s' % (url, exc))

