from __future__ import print_function
import csv
from collections import defaultdict
import operator
import sys

def main(intputFilePath):
    traders = {}

    with open(intputFilePath, 'r') as inputFile:
        reader = csv.reader(inputFile, delimiter='\t')
        next(reader)
        for line in reader:
            trader = line[1]
            stkCode = line[2]
            price = float(line[4])
            tradeType = line[5]
            fee = float(line[6])

            if tradeType == 'Buy':
                quantity = int(line[3])
            else:
                quantity = int(line[3]) * (-1)

            if trader not in traders:
                traders[trader] = {
                    "cash": 0.0,
                    "stocks": {}
                }
            # Calculate the accumulated amount of money spent so far
            traders[trader]['cash'] -= price * float(quantity) + fee

            # Update the amount that the trader owns for each stock
            if stkCode not in traders[trader]['stocks']:
                traders[trader]['stocks'][stkCode] = {
                    "quantity": quantity,
                    "price": price
                }
            else:
                traders[trader]['stocks'][stkCode]["quantity"] += quantity
                traders[trader]['stocks'][stkCode]["price"] = price

    finalResult = defaultdict()

    for trader, history in traders.items():
        cash = history['cash']
        stocks = history['stocks']

        # The profit is calculated based on the accummulated money spent and the value of stocks owned
        # Note:
        # 1. The value of the stock is calculated based on the latest purchasing price
        for stkCode, detail in stocks.items():
            cash += detail['quantity'] * detail['price']
        finalResult[trader] = round(cash,2)

    finalResult = sorted(finalResult.items(), key=operator.itemgetter(1), reverse=True)

    with open("output.tsv", "w") as outputFile:
        for line in finalResult:
            outputFile.write("{}\t{}\n".format(line[0],line[1]))

    print("Success. The output file named 'output.tsv' is generated.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the path of the input file.")
        exit(0)

    try:
        filePath = sys.argv[1]
        main(filePath)
    except Exception as e:
        print(str(e))
        exit(0)
