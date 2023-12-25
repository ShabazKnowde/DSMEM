from flask import Flask, render_template, Response
import time

import json
app = Flask(__name__)

def simulate_long_running_task():
    # Simulate a long-running task
    for i in range(1, 11):
        # time.sleep(1)  # Simulate work

        
        dat = json.dumps({"msg":"hi", "dat":i * 10})
        yield f"data: {dat}\n\n"  # Yield the progress
        # yield f"data: {i * 10}%\n\n"  # Yield the progress



@app.route('/')
def progress():
    return Response(scrape_website("https://plasticsfinder.com/products/mat"), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)



from playwright.sync_api import sync_playwright
def scrape_website(url):
    with sync_playwright() as p:
        f = []
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(url)

        # tot = int(page.locator('div[class="col-xs-12 col-sm-8 tags-search wrap"] span').first.text_content().split("(")[-1].split(")")[0])
        # tt = tot
        cond =True
        coun = 0 
        mem =[]
        try:
            while cond:
                coun +=1
                page.wait_for_selector('h4[class="clickable flex-wrap cross-center"]')
                page.wait_for_selector('div[class="col-xs-12 col-sm-8 tags-search wrap"] span')
                time.sleep(2)
                tt = int(page.locator('div[class="col-xs-12 col-sm-8 tags-search wrap"] span').first.text_content().split("(")[-1].split(")")[0])
                nm = page.locator('div[class="tile shadow-md"]')
                base = "https://plasticsfinder.com/datasheet/"
                fst =nm.first.get_attribute("id")
                if fst not in mem:
                    mem.append(fst)
                
                    all_eles = nm.all()
                    lis = [{"Name":j.locator('h4').text_content(),"Link": base + j.locator('h4').text_content().replace(" ","%20")+"/" +j.get_attribute("id")} for j in all_eles]
                
                    f +=lis
                    cmp = len(f)
                    print("cmp",cmp)
                    print("tt",tt)
                    i = cmp/tt
                    if (i== 1):
                        dat = json.dumps({"msg":f, "dat":i*100, "cond":1})
                        yield f"data: {dat}\n\n"
                    else:
                        dat = json.dumps({"msg":"hi", "dat":i*100, "cond":0})
                        yield f"data: {dat}\n\n"

                next = page.is_visible('a[aria-label="Next"]')
                cond = next
                if next: 
                    np = page.locator('a[aria-label="Next"]').first
                    np.click()
                    
                # else:
                    
                    # cond =False
                   
        except BaseException as exception:
            print(type(exception).__name__)
    
        browser.close()
        # convert(f)
    

    




