#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Jon Zhang 
@contact: zj.fly100@gmail.com
@site: 
@version: 1.0
@license: 
@file: shopping_mark.py
@time: 2017/3/11 18:46
Shopping
    1.show the commodities：id,name,price
    2.choose one commodity ,update your list
    3.payment,if not too much money,you can minus the commodities
"""

def calcTheTotalPrices(shoppingList):
    """
    calculation the prices of the shopping-list
    :param shoppingList:
    :return theTotalPrices:
    :return shoppingList:
    """
    theTotalPrices = 0
    print("This is your shopping list")
    copyShoppingList = shoppingList.copy()  # Python RuntimeError: dictionary changed size during iteration,so use copy
    for i in copyShoppingList.keys():
        if copyShoppingList[i][2] == 0:
            del shoppingList[i]
        else:
            print("ID",i,"\t","NEME:", shoppingList[i][0],"\t","Cost:", shoppingList[i][1],"\t","Num:", shoppingList[i][2],"\t","Total:", int(shoppingList[i][1]) * shoppingList[i][2])
            theTotalPrices += int(shoppingList[i][1]) * shoppingList[i][2]
    print("You must pay for %s(RMB)" % theTotalPrices)
    return (theTotalPrices,shoppingList)

def toMinusCommodity(shoppingDictList):
    """
    minus the commodity from the shopping list
    :param shoppingDictList:
    :return newTotalPrices:
    :return newShoppingDictList:
    """
    calcTheTotalPrices(shoppingDictList)
    while True:
        chooseOneID = input("Please choose one to minus:").strip()
        # if len(minus_id) == 0:
        #     continue
        if chooseOneID in shoppingDictList.keys():
            shoppingDictList[chooseOneID][2] -= 1
            newTotalPrices, newShoppingDictList = calcTheTotalPrices(shoppingDictList)
            return (newTotalPrices, newShoppingDictList)

def rewriteAccountFile(theAccountFile,theAccountList):
    """
    update the account file
    :param theAccountFile:
    :param theAccountList:
    :return:
    """
    writeAccountFile = open(theAccountFile, 'w')
    for i in range(len(theAccountList)):
        a, b, c, d = theAccountList[i]
        line = a + "\t" + b + "\t" + str(c) + "\t" + str(d) + "\n"
        # print(line)
        writeAccountFile.write(line)
    writeAccountFile.close()

def paymentSystem(accountFile,accountList,theTotalPrices, shoppingList):
    """
    the payment system , check the account、password and enough money ,then pay for
    If the account's password has been wrong for three time,the account is locking
    :param accountFile:
    :param accountList:
    :param theTotalPrices:
    :param shoppingList:
    :return 0 or 1 or None:
    """
    while True:
        theInputCardNum = input("Please input your card_num:").strip()
        if len(theInputCardNum) == 0:
            continue
        theSignForPassword = 1
        while theSignForPassword:
            theInputPassword = input("Please input your password:").strip()
            if len(theInputPassword) != 0:
                theSignForPassword = 0
        for i in range(len(accountList)):
            if theInputCardNum == accountList[i][0]:
                if accountList[i][2] == "3":
                    # sys.exit("Your account %s is locked,please unlock!"% input_name)
                    print("Your Card %s is locked,please unlock!" % theInputCardNum)
                    return 0
                if accountList[i][1] == theInputPassword:
                    accountList[i][2] = 0
                    rewriteAccountFile(accountFile,accountList)
                    if theTotalPrices > int(accountList[i][3]):
                        chooseWhatToDo = input("Sorry,you have not too much money!Please change one card[1] or minus the commodity[2]!")
                        if chooseWhatToDo == '2':
                            newTotalprices, newShoppingList = toMinusCommodity(shoppingList)
                            return paymentSystem(accountFile,accountList,newTotalprices,newShoppingList)
                        else:break
                    else:
                        accountList[i][3] = str(int(accountList[i][3]) - theTotalPrices)
                        rewriteAccountFile(accountFile,accountList)
                        print("Thank you for shopping again!")
                        return 1
                else:
                    accountList[i][2] = str(int(accountList[i][2]) + 1)
                    #print("Your CardNum or password is wrong! Please try again!")
                    rewriteAccountFile(accountFile,accountList)
                    #break
        else:
            print("Your CardNum or password is wrong! Please try again!")

def mainShopping(shoppingDictList,accountListList,accountFile):
    """
    go into the shopping mark and shopping
    :param shoppingDictList:
    :param accountListList:
    :param accountFile:
    :return:
    """
    yourShoppingList = {}
    print("-------------------------------------------------")
    print("+            +")
    print("+   Welcome shopping   +")
    print("+            +")
    print("-------------------------------------------------")
    theSignOfShopping = 1
    while theSignOfShopping:
        for i in shoppingDictList.keys():
            print(i,'\t\t',shoppingDictList[i][0],'\t\t',shoppingDictList[i][1])
        print("\n-------------------------------------------------")
        oneChoiceId = input("Please choose one commodity's id to buy([1-4]):").strip()
        if (len(oneChoiceId) == 0) or (not oneChoiceId.isdigit()):
            continue
        if oneChoiceId in shoppingDictList.keys():
            if oneChoiceId not in yourShoppingList.keys():
                yourShoppingList[oneChoiceId] = [shoppingDictList[oneChoiceId][0], shoppingDictList[oneChoiceId][1], 1]
            else:
                yourShoppingList[oneChoiceId][2] += 1
                print(yourShoppingList)
            whetherContinueShopping = input("Whether to continue!?('y' or 'n',default [y])").strip()
            if whetherContinueShopping == 'n':
                theSignOfShopping -= 1
    theTotalPrices,yourShoppingList = calcTheTotalPrices(yourShoppingList)
    paymentSystem(accountFile,accountListList,theTotalPrices, yourShoppingList)

if __name__ == "__main__":
    commodityFile = "all_shopping.txt"
    readCommodityFile = open(commodityFile)
    makeCommodityFileAsDict = dict([i.split()[0], [i.split()[1], i.split()[2]]] for i in readCommodityFile)
    readCommodityFile.close()

    accountFile = "card_account.txt"
    readAccountFile = open(accountFile)
    makeAccountFileAsList = [[i.split()[0], i.split()[1], i.split()[2], i.split()[3]] for i in readAccountFile]
    readAccountFile.close()

    mainShopping(makeCommodityFileAsDict,makeAccountFileAsList,accountFile)





