# written for chrome version 84.0.4147.105 (Official Build) (64-bit)
from selenium import webdriver
import random
import time

driver = webdriver.Chrome('./chromedriver')
driver.get('https://web.whatsapp.com/')
input("Scan the QR and hit enter")

def replyWith(message,name):
    user= driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
    user.click()
    msg_box= driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
    msg_box.send_keys(message)
    btn= driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')
    btn.click()
    driver.execute_script("document.querySelector('"+chr(35)+"pane-side').scrollTop=0")
    driver.find_element_by_xpath('//span[@title = "Notes"]').click()
    time.sleep(1)
def fetchLastText(name):
    user= driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
    user.click()
    try:
        user= driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
        user.click()
        lastMsg= driver.find_elements_by_class_name('message-in')
        lastMsg=lastMsg[-1]
        lastMsg= lastMsg.find_element_by_xpath('.//div/div/div/div[1]/div/span[1]/span')
        return(lastMsg.get_attribute('innerHTML').split('<')[0])  
    except:
        return(None)

elems= driver.find_elements_by_xpath('//*[@id="pane-side"]/div[1]/div/div/div')
turn=0

# default greeting message
defaultTxt="This is YOUR-BOT-NAME, YOURNAME's faithful Bot. YOURNAME is busy(probably sleeping!) and will get back to you. Meanwhile, do you want to play a game??"
# defaultTxt=input("Enter your default text")

# Name of whatsapp contacts or groups that you dont want to reply to
noreplies=["abcd","efgh", "ijkl"]
# noreplies = input("Enter comma separated blacklist names").split(',')


print("\nNames of people that the bot replies to, will apeear below, for future reference")
people=[]
maps={}
flag=True
while True:
    turn=(turn+1)%2
    for iters in elems:
        try:
            marks=iters.find_elements_by_xpath('.//div/div/div[2]/div[2]/div[2]/span')
            N = iters.find_element_by_xpath('.//div/div/div[2]/div[1]/div[1]/span')
            try:
                name=N.find_element_by_xpath('.//span')
                name=name.get_attribute('title')
            except:
                name=N.get_attribute('title')
            for i in noreplies:
                if i in name:
                    flag=False
                    break
            if flag:
                marks=marks[0].find_elements_by_xpath('.//div')
                unread=marks[-1].find_element_by_xpath('.//span')
                notif=unread.get_attribute('aria-label')
                if "unread" in notif and name not in people:
                    people.append(name)
                    maps[name]=[random.randint(0,500),1,True]
                    print("Assigned the random number",maps[name][0],"to",name)
                    replyWith(defaultTxt,name)
                    turn =0
                elif "unread" in notif and name in people and maps[name][1]==1:
                    response= fetchLastText(name)
                    
                    if response== None:
                        replyWith("I am dumb!! Give me Yes/No answers :/ -_-",name)
                        turn = 0
                    else:
                        response=response.lower()
                        out=""
                        for i in response:
                            if i not in '".,;!':
                                out += i
                        response= out
                        response=response.split(' ')
                        F=0
                        for i in ["done","haa","haaa","yes","ya","yea","yeah","yep","cool","ok","okay","definitely","sure","ha","hmm","possibly","maybe"]:
                            if i in response:
                                maps[name][1]=2
                                replyWith("So, I will pick a counting number in my mind(less than or equal to 500). You are supposed to guess a number, and I will tell if my Number is higher or lower.",name)
                                replyWith("I CAN LIE ANY NUMBER OF TIMES... BUT I WILL NEVER LIE CONSECUTIVELY! COOL?",name)
                                replyWith("I am done picking a number. You start guessing. I am waiting.",name)
                                replyWith("*Lets see, if you have a good strategy*",name)
                                turn =0
                                F=1
                        for  i in ["no","nope","nah","na","naaa"]: 
                            if i in response:
                                replyWith("Cool, Mriganka will get back to you. :) If you text again, I will be right here to reply!",name)
                                turn =0 
                                people.remove(name)
                                F=2
                        
                        if F==0:
                            replyWith("Thats a complicated answer, thats beyond my intelligence. Could you be less insulting to me? :(" ,name)
                            turn = 0
                        
                        
                elif "unread" in notif and maps[name][1]==2:
                    response=fetchLastText(name)
                    try:
                        response= int(response)
                        target=maps[name][0]
                        if maps[name][2]==True:
                            intent=random.randint(0,1)
                            if intent==1:
                                if response < target:
                                    replyWith("It is larger",name)
                                    turn =0
                                elif response > target:
                                    replyWith("It is smaller",name)
                                    turn =0
                                else:
                                    replyWith("Its Equal... Bravo there Johny!",name)
                                    replyWith("You take some rest, and Mriganka will get back to you.",name)
                                    turn =0
                                    people.remove(name)
                            else:
                                maps[name][2]=False
                                if response < target:
                                    replyWith("It is smaller",name)
                                    turn =0
                                elif response > target:
                                    replyWith("It is greater",name)
                                    turn =0
                                else:
                                    replyWith("Its Equal... Bravo there Johny!",name)
                                    replyWith("You take some rest, and Mriganka will get back to you.",name)
                                    turn =0
                                    people.remove(name)
                        else:
                            maps[name][2]=True
                            if response < target:
                                replyWith("It is greater",name)
                                turn =0
                            elif response > target:
                                replyWith("It is smaller",name)
                                turn =0
                            else:
                                replyWith("Its Equal... Bravo there Johny!",name)
                                replyWith("You take some rest, and Mriganka will get back to you.",name)
                                turn =0
                                people.remove(name)
                    except:
                        replyWith("Are you sure you understand the rules of the game?",name)
                        turn =0
    
        except:
            pass
        flag=True
    driver.execute_script("document.querySelector('"+chr(35)+"pane-side').scrollTop="+str(504*turn))