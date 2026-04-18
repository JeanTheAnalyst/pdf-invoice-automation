import pdfplumber
import pandas as pd
import re,os
from pathlib import Path
from collections import defaultdict

path = Path(__file__).parent

out_path = path / "output"

if not out_path.exists():
    out_path.mkdir()

pattern = r"\d{2}-\d{5}"

def adjust_length(text):
    # 查找 Length 后的小数点数字并调整格式
    return re.sub(r"(Length\s)(\d+\.\d{2})(\sIN)", lambda m: f"{m.group(1)}{float(m.group(2)):.3f}{m.group(3)}", text)

def invoice(file):

    pdf = pdfplumber.open(file)

    des = []
    pos = []
    subtotal = []


    for page in pdf.pages:
        extracted_table = page.extract_table()
        po = page.extract_text().split("\n")[3].split(" ")[2]

        count = 0
        if extracted_table:
            for item in extracted_table:
            
                if item and item[1] and any(["Coil" in item[1],'Sheet' in item[1]]):
                    count += 1
                    des.append(adjust_length(re.sub(r", HS Code: \d+","",re.findall(r"Alloy.*\n.*",item[1])[0].replace("\n"," ")).replace(","," ").replace(":"," ")))
                    if item[-1]:
                        subtotal.extend(float(value.replace('USD', '').replace(',', '').strip()) for value in re.findall('USD .*',item[-1]))
        
            pos.extend([po] * count)  
    df = pd.DataFrame({"PO #" : pos,"Description": des,"Subtotal" : subtotal})
    return df
               

 



def ps(file):
        
    pdf = pdfplumber.open(file)

    POS = []
    Des = []
    Qty = []
    Heat = []
    Skid = []
    PCS = []
    
    text = ""
    for page in pdf.pages:
        extracted_table = page.extract_table()
        po = page.extract_text().split("\n")[2].split(" ")[3]
        
        
        if extracted_table:
        
        
            for item in extracted_table:
    
        
                
                if item.count(None) != 2 and item[0] != 'ITEM':
                    if item[2]:
                        item.insert(2,"")

                    skid = re.findall(r'(\d{7})',item[3])
                    Skid.extend(skid)
                    
                    if len(item[3]) > 2:
                        if item[7]:
                            qty = [round(int(i)*2.20462,0) for i in item[7].replace(',','').split('\n')]
                            Qty.extend(qty)

                        
                        if not 'Total' in item[3]:

                            pcs = [int(i) for i in item[4].split("\n") if i.isdigit()]
                            
                            
                            PCS.extend(pcs)

                    
                    if item[1]:
                        
                        text += ("\n" + item[1])
                    
                        POS.extend([po]*item[1].count('SRC:'))

    

    for item in text.split("Total For Item"):
        if re.findall(r"(\d+) SRC",item) and re.findall(r"Alloy.*\n.*",item) :
            Heat.extend(re.findall(r"(\d+) SRC",item))
            l = len(re.findall(r"(\d+) SRC",item))
            Des.extend([re.sub(r", HS Code: \d+","",re.findall(r"Alloy.*\n.*",item)[0].replace("\n"," ")).replace(","," ").replace(":"," ")]*l)
            
    PL =  pd.DataFrame(columns=["Company","PO #", "Item #","Vendor Item#",	"Description","Qty",	"Unit Cost",	"Extd. Cost",	"UOfM",	"Location",	"lot", "qty pcs", "ship#", "Heat#","SKID#"])
    
    PL['PO #'] = POS
    PL['Company'] = 'SRLLC'
    PL['Description'] = Des
    PL['Qty'] = Qty
    PL['UOfM'] = 'LBS'
    PL['Location'] = 'B2B'
    PL['qty pcs'] = PCS
    # PL['ship#'] = sr
    PL['Heat#'] = Heat
    PL['SKID#'] = Skid
    PL['Grouped_qty'] = PL.groupby(["PO #", "Description"])["Qty"].transform("sum")   
    # PL['Grouped_qty'] = PL.groupby(["PO #", "Description"])["Qty"].cumsum()

    return PL

if __name__ == '__main__':

    files = []

# Collect all PDF filenames in the folder
    for file in path.glob("*.pdf"):
        files.append(file.name)
    groups = defaultdict(list)

# Traverse files to group them by pattern match
for file in files:
    match = re.search(pattern, file)

    if match:
        group_key = match.group(0)  # Extract matched PO number (e.g., IP-PO123456)
        groups[group_key].append(file)

for group, file_list in groups.items():
        for file in file_list:
            file_path = path / file
            if "ci" in file.lower():
                inv = invoice(file_path)  # Open Commercial invoice PDF
            elif "pl" in file.lower():
                pl = ps(file_path)  #
        
        if inv is None or pl is None:
            continue

        master = pd.merge(inv,pl,how='right',on=['PO #','Description'])
        master['Unit Cost'] = (master['Subtotal'] / master['Grouped_qty']).astype(float).round(4)
        master['Extd. Cost'] = (master['Unit Cost'] * master['Qty']).astype(float).round(2)
        master['ship#'] = group

        receiving =  master[["Company","PO #", "Item #","Vendor Item#",	"Description","Qty",	"Unit Cost",	"Extd. Cost",	"UOfM",	"Location",	"lot", "qty pcs", "ship#", "Heat#","SKID#"]]
    

        receiving.to_excel(out_path / f"{group} receiving.xlsx",index=False )

     
