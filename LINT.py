#!/usr/bin/python3

##    ___       ___  ________   _________      ##
##   |\  \     |\  \|\   ___  \|\___   ___\    ##
##   \ \  \    \ \  \ \  \\ \  \|___ \  \_|    ##
##    \ \  \    \ \  \ \  \\ \  \   \ \  \     ##
##     \ \  \____\ \  \ \  \\ \  \   \ \  \    ##
##      \ \_______\ \__\ \__\\ \__\   \ \__\   ##
##       \|_______|\|__|\|__| \|__|    \|__|   ##


__title__   = 'LINT: LIterature reference managemeNT'
__version__ = '3.1'
__author__  = 'christoph irrenfried'
__license__ = 'none'

# prepare environment
import time,os
import textwrap
import subprocess


### Set environment variables
if os.environ['LITERATURE'] != "":
   prefix=os.environ['LITERATURE'].strip("literature.bib")
else:
   prefix=""
PDFviewer="evince "
Editor="emacs "

### repr(
### entry=next(filter(lambda obj: obj.get('doi'), self.BibContent), None)


#======== Fancy terminal print ==================

color=["black","red","green","blue","pink","yellow","peru"]

class Texti:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

#================================================

            
#===== Main routine definition ==================
def main():
   print(Texti.GREEN+"Literature reference manager"+Texti.END)
   print(Texti.GREEN+"================================\n"+Texti.END)

      
   database,msg=ReadDatabase(prefix)
   # print(msg)

   # for val in database:
   #    print(val.BibName)
   #    print(val.file)
   #    print(val.keywords)
   #    print(val.bibtex)
   #    print()
   # for val in database:
   #    print(val.BibContent)

   cli(database,msg,prefix)


   # arguments={"database":database,
   #            "prefix":prefix,
   #            "searchString":""
   #            }
   
   #ListAuthors_all(database)
   #ListAuthors(arguments)
   #ListPublications(arguments)
   #Search(arguments)




#===== LitEntry class ==================
class LitEntry:
   """
   class for holding all relevent information of a literature entry
   """
   def __init__(self,doi,file,bibtex):
      self.doi=doi
      
      self.file=file
      self.bibtex=bibtex

      self.BibType=''
      self.BibName=''
      self.Title=''
      
      self.BibContent={}

      self.keywords=[]
      self.projects=[]
      
      # Array holding all data accessible in a serach
      self.searchString=[]

      self.BibAutors=[]
      
      self.abstract=''

   def SetupEntry(self):
      # process data stored in dict "BibContent"
      
      self.file=self.BibContent["file"]
      self.Title=self.BibContent["title"]

      if "projects" in self.BibContent.keys():
         for val in self.BibContent["projects"].split(","):
            self.projects.append(val.strip("\"").strip("{").strip("}"))
      
      for val in self.BibContent["keywords"].split(","):
         self.keywords.append(val.strip("\"").strip("{").strip("}"))

      for aut in self.BibContent["author"].split("and"):
         entry=aut.strip("{").strip("}").strip("\"").split(" ")
         format=len(list(filter(lambda x: "," in x, entry)))
         
         #print(repr(entry),len(entry),format)
         
         if(format == 0):
            if entry[-1] == "":
               self.BibAutors.append(entry[-2])
            else:
               self.BibAutors.append(entry[-1])
         else:
            if entry[-1] == "":
               self.BibAutors.append(entry[-3].strip(","))
            else:
               self.BibAutors.append(entry[-2].strip(","))
            
               
      # Array holding all data accessible in a serach
      self.searchString.append(self.Title.lower())
      for val in self.keywords:
         self.searchString.append(val.lower())
      for val in self.projects:
         self.searchString.append(val.lower())
      for val in self.BibAutors:
         self.searchString.append(val.lower())
      self.searchString.append(self.BibName.lower())
      self.searchString.append(self.abstract.lower())


      # print(self.searchString)

   def GenerateBibTex(self):
      # Generate a BibTex entry
      
      string=self.BibType+'{'+self.BibName+','
      for key,val in self.BibContent.items():
         string=string+'\n\t{:20} = {}'.format(key,val)
      string=string[:-1]+'\n}'
      
      #print(repr(string))
      
      self.bibtex=string

   def PrintBibTex(self):
      print(self.bibtex)
      
   def ReturnBibTex(self):
      return self.bibtex


#===== cli ==================
def cli(database,msg,prefix):
   # command line interface

   arguments={"database":database,
              "prefix":prefix,
              "msg":msg,
              "searchString":"",
              "export":[]
              }

   menuItems = [
      { "E(x)it": CLI_Exit },
      { "List all publications": CLI_ListPublications },
      { "List all authors": CLI_ListAuthors },
      { "Search": CLI_Search },
      { Texti.RED+"Modify database"+Texti.END: CLI_ModDatabase },
      { Texti.RED+"Reload database"+Texti.END: CLI_ReloadDatabase },
      { Texti.DARKCYAN+"Export"+Texti.END: CLI_Export }
   ]
   	
   while True:
      os.system('clear')

      Logo()
      
      print(arguments["msg"])
                                            
      
      for item in menuItems:
         print("[" + str(menuItems.index(item)) + "] "+ list(item.keys())[0])

      choice = input("# or search >> ")
      try:
         if len(choice) > 1:
            arguments["searchString"]=choice
            choice=3
         if choice == 'x': choice=0
         if int(choice) < 0 : raise ValueError
         list(menuItems[int(choice)].values())[0](arguments)
         arguments["searchString"]=""
      except (ValueError, IndexError):
         pass


#===== Utility functions for cli ==================
def Logo():
   """
   Routine for plotting the logo
   """
   print(Texti.GREEN+"  ___       ___  ________   _________    "+Texti.END)
   print(Texti.GREEN+" |\  \     |\  \|\   ___  \|\___   ___\  "+Texti.END)
   print(Texti.GREEN+" \ \  \    \ \  \ \  \\\ \  \|___ \  \_|   "+Texti.END)
   print(Texti.GREEN+"  \ \  \    \ \  \ \  \\\ \  \   \ \  \   "+Texti.END)
   print(Texti.GREEN+"   \ \  \____\ \  \ \  \\\ \  \   \ \  \  "+Texti.END)
   print(Texti.GREEN+"    \ \_______\ \__\ \__\\\ \__\   \ \__\ "+Texti.END)
   print(Texti.GREEN+"     \|_______|\|__|\|__| \|__|    \|__| "+Texti.END)
   print("       "+Texti.GREEN+"LI"+Texti.END+"terature reference manageme"+Texti.GREEN+"NT"+Texti.END)
   print("                    "+Texti.GREEN+"chi86"+Texti.END)
   print()


#===== literature database functions ==================
def CLI_ReloadDatabase(arguments):
   """
   Reload databese
   """
   prefix=arguments["prefix"]
   database,msg=ReadDatabase(prefix)
   arguments["database"]=database
   arguments["msg"]=msg
   
def CLI_ModDatabase(arguments):
   """
   Modify databese --> open the databases file in $Editor
   """
   subprocess.Popen([Editor+prefix+"literature.bib"],shell=True)


#===== general literature database stuff ==================
def OutputFormat(val):
   """
   helper: fancy output of literature entry
   """
   entry=Texti.BLUE+val.BibName+Texti.END+" "
   entry+=Texti.RED+val.BibContent['title'].replace('{','').replace('}','')+Texti.END+" "
   entry+=Texti.GREEN+val.BibContent['author'].replace('{','').replace('}','')+Texti.END+" "
   entry+=Texti.YELLOW+str(val.keywords)+Texti.END

   return entry
   
def Menu_SingeLitEntry(datapoint,arguments):   
   """
   helper: menu for a single literature entry
   """
   choice=""
   while( choice != "x"):
      # if int(choice) >= 0:
      print(datapoint.bibtex)

      print('open(SPACE) | export (e) | exit (x)')
      choice = input(">> ")
      
      if choice == "e":
         arguments["export"].append(datapoint)
      elif choice == " ":
         # print("open : "+datapoint.file.strip("{").strip("}"))
         # print(PDFviewer+prefix+datapoint.file.strip("{").strip("}"))
         
         #input("Press [Enter] to continue...")
   
         subprocess.Popen([PDFviewer+prefix+datapoint.file.strip("{").strip("}")],shell=True)


def CLI_Export(arguments):
   """
   CLI entry **Export**
   """
   for dat in arguments["export"]:
      print(dat.BibName)

   choice=""
   while( choice!= "x"):
      print("print bibtex (p) | export to file (f) | delete list (d) | exit (x)")
      choice=input(">> ")

      if(choice == "p"):
         for dat in arguments["export"]:
            print(dat.bibtex)
      elif(choice == "d"):
         arguments["export"]=[]
      elif(choice == "f"):
         print("work in progress ..")


def CLI_ListPublications(arguments):
   """
   CLI entry **ListPublications**
   """
   database=arguments["database"]
   prefix  =arguments["prefix"]
   
   datapoint=[]

   for idx,dat in enumerate(database):
      datapoint.append(dat)
      entry=OutputFormat(dat)

      msg=entry
      msg=msg.replace('}','')
      msg=(str(idx)+' : '+msg)
      msg=textwrap.wrap(msg, 72)
      
      print(msg[0])
      for i in msg[1:]:
         print('\t'+i)
      
   print('number / X')
   choiceDat = input(">> ")

   if( int(choiceDat) >= 0 ):
      Menu_SingeLitEntry(datapoint[int(choiceDat)],arguments)


def CLI_ListAuthors(arguments):
   """
   CLI entry **ListAuthors**
   """
   database=arguments["database"]
   prefix  =arguments["prefix"]
   
   datapoint0={}
   for idx,dat in enumerate(database):
      for author in dat.BibAutors:
         entry=author
         if(entry==None): continue
         if(not entry in datapoint0):
            datapoint0[entry]=[dat]
         else:
            datapoint0[entry].append(dat)

   #print(datapoint)

   datapoint={}
   for key, value in sorted(datapoint0.items()):
      datapoint[key]=value

   # for key,value in datapoint.items():
   #    print("{:3} : {}".format(key,value))

   for idx,dat in enumerate(datapoint):
      print("{:3} : {}".format(idx,dat))

   print('number / X')
   choice = input(">> ")


   if int(choice) >= 0:
      #print(datapoint.values()[int(choice)])
      for idx,val in enumerate(list(datapoint.values())[int(choice)]):
         entry=OutputFormat(val)
         
         msg=entry
         msg=(str(idx)+' : '+msg)
         msg=textwrap.wrap(msg, 72)
      
         print(msg[0])
         for i in msg[1:]:
            print('\t'+i)
         
         #print("{:3} : {}".format(idx,entry))
         
      print('open / SPC or number ')
      choiceDat = input(">> ")
      
      if( int(choiceDat) >= 0 ):
         Menu_SingeLitEntry(list(datapoint.values())[int(choice)][int(choiceDat)],arguments)
         
 
def CLI_Search(arguments):
   """
   CLI entry **Search**
   """
   database=arguments["database"]
   prefix  =arguments["prefix"]
   
   datapoint=[]

   if(arguments["searchString"] != ""):
      keyw=arguments["searchString"]
   else:
      keyw=input("keyword : ")
      
   idx=0
   for id,dat in enumerate(database):
      for dat_keyw in dat.searchString:
         if keyw in dat_keyw:

            datapoint.append(dat)
            entry=OutputFormat(dat)
            
            msg=entry
            msg=(str(idx)+' : '+msg)
            msg=textwrap.wrap(msg, 72)
      
            print(msg[0])
            for i in msg[1:]:
               print('\t'+i)
            idx+=1
            break

   print('select (number) | quick open (number#) | export all (e)')
   choiceDat = input(">> ")


   if choiceDat[-1] == "#":
      choiceDat=choiceDat[0:-1]
      print("open : "+datapoint[int(choiceDat)].file.strip("{").strip("}"))
      subprocess.Popen([PDFviewer+prefix+datapoint[int(choiceDat)].file.strip("{").strip("}")],shell=True)
   elif choiceDat == "e":
      arguments["export"].extend(datapoint[:])
   elif int(choiceDat) >= 0:
      Menu_SingeLitEntry(datapoint[int(choiceDat)],arguments)

   

def CLI_Exit(arguments):
   """
   CLI entry **Exit**
   """
   exit()


#===== Database related functions ==================
def ReadDatabase(prefix):
   """
   Read database given by prefix
   """
   msg=""
   database=[]
   
   try:
   #if(True):      
      fileH=open(prefix+"literature.bib",'r')
      fileH.readline()
      fileH.readline()

      dataField=0
      for line in fileH:
         if(line!="\n"):
            data=line.strip("\n").strip("\t")
            #print(dataField,repr(data))
         
            if(dataField==0):
               LE=LitEntry('NONE','NONE','NONE')
               LE.BibType=data.split('{')[0].strip("'")
               LE.BibName=data.split('{')[1].split(",")[0]
               dataField=1
            elif(data=="}"):
               dataField=0
               
               LE.SetupEntry()
               LE.GenerateBibTex()
               
               database.append(LE)
            elif(dataField==1):
               di_key=data.strip(",").split("=")[0].replace(" ","")
               di_val=data.strip(",").split("=")[1]

               if(di_val[0] == " "):
                  di_val=di_val[1:]
               
               #print(" \t 2 {:15} : {}".format(repr(di_key),repr(di_val)))

               LE.BibContent[di_key]=di_val
      
      fileH.close()
   except:
      msg=msg+"literature.bib "+Texti.YELLOW+'error reading database ... '+Texti.END+"\n"
      print(Texti.RED+"Error reading database"+Texti.END)


   msg+=" Number of literature entries: "+str(len(database))+"\n"
      
   return database,msg
         



#===== execute MAIN ==================
if __name__ == '__main__':
   #===== Main routine execute =============
   #start = time.time()
   main()
   #end = time.time()
   #print('\n\nTime:',end - start,'sec')
   #========================================
