import os
from telegram import Update
from telegram.ext import (
    Application, 
    CommandHandler, 
    ConversationHandler,
    MessageHandler, 
    filters, 
    ContextTypes)
import gspread
from dotenv import load_dotenv
from datetime import datetime

#To retrieve telegram and excel api key from .env
load_dotenv()
Telegram_API_Key = os.getenv('Telegram_API_Key')
Excel_link = os.getenv('Excel_link')
gc = gspread.service_account(filename=
                             "###")
sh = gc.open("###").sheet1


#states for telegram commands
MENU, DEDUCT, DEPOSIT = range(3)


#Command Functions:

#Deduct function, used to deduct money from excel (-)
#gets receipt from user via telegram bot
async def Deduct_function(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = update.message.text                                                           #receipt sent by user is kept as message
    s_arr = Split_Message(message)                                                          #convert string into organised array
    Update_Sheet(Convert_array(s_arr,"-"))
    reply = Balance_function()                                                              #Send the balance after updating to excel sheet
    await update.message.reply_text(reply)
    return MENU                                                                             #return to menu

#Deposit function, used to add money into excel (+), similar to Deduct function
async def Deposit_function(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = update.message.text
    s_arr = Split_Message(message)
    Update_Sheet(Convert_array(s_arr,"+"))
    reply = Balance_function()
    await update.message.reply_text(reply)
    return MENU

#Balance function, to tell user the amount of money in excel
def Balance_function():
    names_row = sh.row_values(2)                                                            #retrieve the values from rows 2 and 3 of excel
    values_row = sh.row_values(3)

    reply_string = "Balance\n"                                                              #Reply string will look like:
    n = len(values_row)                                                                     #Balance
    for i in range(2,n-1):                                                                  #Person 1 : "Amount"
        reply_string = reply_string + names_row[i] + " : " + values_row[i] + "\n"           #Person x : "Amount"
                                                                                            #
    reply_string = reply_string + "\n" + names_row[n-1] + " : " + values_row[n-1]           #Total : "Amount"

    return reply_string


#Misc functions:

#Convert_array function is used to convert the amount("$$$") from receipt to int and either "+" or "-"
def Convert_array(array,sign):
    n = len(array)
    total = 0
    if sign == "+":
        j = 1
    else:
        j = -1

    for i in range(2,n-1):                              #starts from 2 as the first 2 index of array is date and event
        array[i] = int(array[i]) * j
        total += array[i]

    array[n-1] = total                                  #array[n-1] is the total amount

    return array


#Split_Message function is used to convert the receipt string from telebot to an organised array
def Split_Message(message):
    s_arr = message.split("\n")                                                 #Split string into array with "new line" as delimiter
    row_to_sheet= []
    date = datetime.today().strftime('%d/%m/%Y')

    row_to_sheet.append(date)                                                   #sets date and Title of receipt to 1st and 2nd index of array
    row_to_sheet.append(s_arr[0])

    for i in range(1,len(s_arr)-2):                                             #Receipt comes in the form of Person 1 : $$$
        row_to_sheet.append(s_arr[i].split(" : ", 1)[1])                        #Remove person 1 from string and store $$$ into array in order of person 1 to x

    row_to_sheet.append(s_arr[-1].split(" : ",1)[1])                            #Last index of s_arr is the total amount, stores only the $$$

    return row_to_sheet

#Update_Sheet function is used to update the excel via adding new rows with values from sorted array.
def Update_Sheet(update_array):
    sh.append_row(update_array)                                                 #Append to the lowest row, signifying latest event
    last_row = sh.row_count
    pre_row = last_row - 1

    #Check if date is different from last entry, change cell colour if different
    #to easily differentiate days
    if (sh.cell(last_row, 1).value) != (sh.cell(pre_row, 1).value):
        sh.format('A'+ str(last_row),{"backgroundColor":{"red":0/255, "blue":255/255, "green":255/255}})
    else:
        sh.format('A'+ str(last_row),{"backgroundColor":{"red":255/255, "blue":255/255, "green":255/255}})


    #To add borders to newly appended cell in excel
    sh.format(str(last_row),{"borders":{
        "top": {"style" : "SOLID"},
        "bottom": {"style" : "SOLID"},
        "left": {"style" : "SOLID"},
        "right": {"style" : "SOLID"},
    }})


#Commands:

#Start command, when user enters "/start", bot will send the menu message
async def Start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
                    "Menu:\n"
                    "/Deduct - Deduct from wallet\n\n"
                    "/Deposit - Deposit to wallet\n\n"
                    "/Balance - Check wallet balance\n\n"
                    "/Excel - Open Excel\n\n"
                    "/End - End session")
    return MENU                                                                 #return back to menu state

#Deduct command, when user enters /Deduct, bot will ask for receipt
async def Deduct(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Please send the receipt")
    return DEDUCT                                                               #receive receipt from user and go to DEDUCT state

#Deposit command, when user enters /Deposit, bot will ask for receipt
async def Deposit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Please send the receipt")
    return DEPOSIT                                                              #receive receipt and go to DEPOSIT state

#Balance command, when user enters /Balance, bot will run Balance_function
async def Balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply = Balance_function()
    await update.message.reply_text(str(reply))
    return MENU                                                                 #bot replies with balance of excel and return to MENU state

#Excel command, when user enters /Excel, bot will reply with excel link
async def Excel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(Excel_link)
    return MENU                                                                 #return to MENU state             

#End command, when user enters/ End, bot will reply end
async def End(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("End")
    return ConversationHandler.END                                              #ends conversation handler

#Main function, conducts polling and setting of states
def main():
    app = Application.builder().token(Telegram_API_Key). build()                #creation of telegram bot
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start",Start)],                           #telegrambot starts with /start
        states={
            MENU: [CommandHandler("start", Start),CommandHandler("Deduct", Deduct), CommandHandler("Deposit", Deposit),     #MENU state, determine which command user input
                   CommandHandler("Balance", Balance),CommandHandler("Excel", Excel),CommandHandler("End", End)],           #User send to appropriate state via CommandHandler
            DEDUCT: [MessageHandler(filters.TEXT,Deduct_function)],                                                         #DEDUCT state, retrieve user's receipt and send to Deduct_function
            DEPOSIT: [MessageHandler(filters.TEXT,Deposit_function)],                                                       #DEPOSIT function, similar to DEDUCT state
        },
        fallbacks=[CommandHandler("End",End)]                                                                               #END state, quits ConversationHandler
    )

    app.add_handler(conv_handler)

    app.run_polling()                                                           #Polling of telegram bot

if __name__ == '__main__':
    main()
