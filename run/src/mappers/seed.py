import sqlite3
import json
from pprint import pprint


def load_dictionary(filename):
    """imports json file as a dictionary"""
    with open(filename, 'r') as json_file:
        return json.load(json_file)

def price_premium(retail,average):
    if retail == '--' or average == '--':
        return None
    else:
        intRetail = retail.strip('$')
        new_intRetail = intRetail.replace(',','')
        final_intRetail = float(new_intRetail)
        intAverage = average.strip('$')
        new_intAverage = intAverage.replace(',','')
        final_intAverage = float(new_intAverage)
        
        difference = final_intAverage - final_intRetail
        percentageOf = float(difference/final_intRetail)
        premium = '{:.2f}'.format(percentageOf*100)

        return premium

full_file = "/Users/ahn.ch/Projects/shoe_data/run/src/json/total190130.json"

def run(dbname="shoebox.db"):
    conn = sqlite3.connect(dbname)
    cur  = conn.cursor()

    PARENT_SQL = """INSERT INTO sneakers (
                brand,
                type,
                name,
                colorway,
                image,
                image_placeholder,
                release_date,
                retail_price,
                ticker,
                total_sales,
                url,
                year_high,
                year_low,
                avg_sale_price,
                premium
            ) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?); """


    # importing the raw data json file created through a scrape of TFB html
    dcty = load_dictionary(full_file)

    for key in dcty.keys():

        name = key

        brand = dcty[key]['brand']

        image = dcty[key]['image']

        if 'Harden' in name.split(' ') and brand != 'Nike':
            type = 'Harden'
        elif 'Curry' in name.split(' ') and brand != 'Nike':
            type = 'Curry'
        elif 'PG' in name.split(' '):
            type = 'PG'
        elif 'Westbrook' in name.split(' '):
            type = 'Westbrook'
        elif 'Kyrie' in name.split(' '):
            type = 'Kyrie'
        elif 'Dame' in name.split(' '):
            type = 'Dame'
        elif 'React' in name.split(' '):
            type = 'React'
        else:
            type = dcty[key]['type']

        if 'Placeholder' in image.split('-'):
            image_placeholder = 'YES'
        else:
            image_placeholder = 'NO'

        total_sales = dcty[key]['total_sales'].replace(',','')
        
        retailPrice = dcty[key]['retail_price'].strip('$')
        new_retailPrice = retailPrice.replace(',','')

        avgSalePrice = dcty[key]['avg_sale_price'].strip('$')
        new_avgSalePrice = avgSalePrice.replace(',','')

        yearHigh = dcty[key]['year_high'].strip('$')
        new_yearHigh = yearHigh.replace(',','')

        yearLow = dcty[key]['year_low'].strip('$')
        new_yearLow = yearLow.replace(',','')

        premium = price_premium(dcty[key]['retail_price'],dcty[key]['avg_sale_price'])

        # populate all values in table
        par_sql_values = (brand, type, name, dcty[key]['colorway'], dcty[key]['image'], image_placeholder, 
            dcty[key]['release_date'], new_retailPrice, dcty[key]['ticker'], total_sales, 
            dcty[key]['url'], new_yearHigh, new_yearLow, new_avgSalePrice, premium)
        cur.execute(PARENT_SQL, par_sql_values)


    conn.commit()
    conn.close()

if __name__ == "__main__":
    run()