import platform
import os


print("""Welcome using System Drone. 
This would help you do some deployment job on your Windows OS.
Please make sure this program has privilege to write your hosts and to run pip-install.""")

if input("[yes|NO]") == "yes" and platform.system() == "Windows":
    print("installing dependencies...")
    if any((os.system("pip install bs4"), os.system("pip install lxml"), os.system("pip install requests"))):
        print('Sorry, something just didn\'t go right. You may use your cmd.exe run "pip install bs4 && pip install lxml && pip install requests" to install dependencies by yourself.')
        input("press enter to exit...")
        exit()
    try:
        with open('C:\Windows\System32\drivers\etc\hosts', mode='r') as f:
            text = f.read()
        if text.find('104.26.11.39 danbooru.donmai.us') != -1:
                pass
        else:
            if os.system('echo 104.26.11.39 danbooru.donmai.us >> C:\Windows\System32\drivers\etc\hosts') != 0:
                raise Exception
    except:
        print("Something went wrong, possibly because you didn't run me with privilege of Admin.")
        print("Now try to open hosts, you can add \"104.26.11.39 danbooru.donmai.us\" to the end of the text by yourself.")
        os.system("notepad C:\Windows\System32\drivers\etc\hosts")
else:
    print("""It seems that you are not using Windows OS.
There's not much that I can help, but I guess being able to choose other OS means you are able to solve deployment yourself.
Go check dependencies.txt will gives you a start.""")


input("press enter to exit...")        
