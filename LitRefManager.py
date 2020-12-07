#!/usr/bin/python3

import time,os
import textwrap
import subprocess


### Set environment variables
if os.environ['LITERATURE'] is not "":
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
   #ListPublications(database,prefix)
   #Search(database)




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
      
      # Array holding all data accessible in a serach
      self.searchString=[]

      self.BibAutors=[]
      
      self.abstract=''

   def SetupEntry(self):
      # process data stored in dict "BibContent"
      
      self.file=self.BibContent["file"]
      self.Title=self.BibContent["title"]

      
      for val in self.BibContent["keywords"].split(","):
         self.keywords.append(val.strip("\"").strip("{").strip("}"))

      for aut in self.BibContent["author"].split("and"):
         entry=aut.strip("{").strip("}").strip("\"").split(" ")
         format=len(list(filter(lambda x: "," in x, entry)))
         print(repr(entry),len(entry),format)
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













def cli(database,msg,prefix):
   # command line interface

   arguments={"database":database,
              "prefix":prefix,
              "searchString":""
              }

   ### cli
   menuItems = [
      { "E(x)it": Exit },
      { "List all publications": ListPublications },
      { "List all authors": ListAuthors },
      { "List all authors all": ListAuthors_all },
      { "Modify database": Mod_Database },
      { "Search": Search },
   ]
   	
   while True:
      os.system('clear')
      print(Texti.GREEN+"Literature reference manager"+Texti.END)
      print(Texti.GREEN+"============================\n"+Texti.END)
      print(msg)
      
      # Print some badass ascii art header here !
      for item in menuItems:
         print("[" + str(menuItems.index(item)) + "] "+ list(item.keys())[0])

      choice = input("# or search >> ")
      try:
         if len(choice) > 1:
            arguments["searchString"]=choice
            choice=4
         if choice is 'x': choice=0
         if int(choice) < 0 : raise ValueError
         list(menuItems[int(choice)].values())[0](arguments)
         arguments["searchString"]=""
      except (ValueError, IndexError):
         pass


def Mod_Database(arguments):
   subprocess.Popen([Editor+prefix+"literature.bib"],shell=True)

def OutputFormat(val):
   entry=Texti.BLUE+val.BibName+Texti.END+" "
   entry+=Texti.RED+val.BibContent['title'].replace('{','').replace('}','')+Texti.END+" "
   entry+=Texti.GREEN+val.BibContent['author'].replace('{','').replace('}','')+Texti.END+" "
   entry+=Texti.YELLOW+str(val.keywords)+Texti.END

   return entry

def ListPublications(arguments):
   database=arguments["database"]
   prefix  =arguments["prefix"]
   
   datapoint=[]

   for idx,dat in enumerate(database):
      # #entry=next(filter(lambda obj: obj.get('title'), dat.BibContent), None)
      # entry=dat.BibContent["title"]

      # if(entry==None): continue
      # datapoint.append(dat)
      # #print(idx,entry['title'].strip('{').strip('}'))

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
   choice = input(">> ")

   if int(choice) >= 0:
      print(datapoint[int(choice)].bibtex)

      print('open / SPACE')
      choice2 = input(">> ")
      
      if choice2 is " ":
         # print("open : "+datapoint[int(choice)].file.strip("{").strip("}"))
         # print(PDFviewer+prefix+datapoint[int(choice)].file.strip("{").strip("}"))
         
         #input("Press [Enter] to continue...")
   
         subprocess.Popen([PDFviewer+prefix+datapoint[int(choice)].file.strip("{").strip("}")],shell=True)
   
   
   input("Press [Enter] to continue...")

def ListAuthors_all(arguments):
   database=arguments["database"]
   prefix  =arguments["prefix"]
   
   datapoint=[]

   for idx,dat in enumerate(database):
      entry=dat.BibContent['author']
      if(entry==None): continue
      datapoint.append(dat)
      #print(idx,entry['author'].strip('{').strip('}'))
      
      msg=entry.replace('{','')
      msg=msg.replace('}','')
      msg=(str(idx)+' : '+msg)
      msg=textwrap.wrap(msg, 72)
      
      print(msg[0])
      for i in msg[1:]:
         print('\t'+i)

   print('number / X')
   choice = input(">> ")

   if int(choice) >= 0:
      print(datapoint[int(choice)].bibtex)
      
      print('open / SPACE')
      choice2 = input(">> ")
      
      if choice2 is " ":
         print("open : "+datapoint[int(choice)].file.strip("{").strip("}"))
         subprocess.Popen([PDFviewer+prefix+datapoint[int(choice)].file.strip("{").strip("}")],shell=True)

 

def ListAuthors(arguments):
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
      choice2 = input(">> ")
      
      if choice2 is not "":
         # for val in list(datapoint.values())[int(choice)]:
         #    print("open : "+val.file.strip("{").strip("}"))
         #    subprocess.Popen([PDFviewer+val.file.strip("{").strip("}")],shell=True)
         if choice2 is " ": choice2=0
         val=list(datapoint.values())[int(choice)][int(choice2)]
         print(val.file)
         print("open : "+val.file.strip("{").strip("}"))
         subprocess.Popen([PDFviewer+prefix+val.file.strip("{").strip("}")],shell=True)
   
    
   #input("Press [Enter] to continue...")
 
def Search(arguments):
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

   print('number / X')
   choice = input(">> ")

   if int(choice) >= 0:
      print(datapoint[int(choice)].bibtex)
      
      print('open / SPACE')
      choice2 = input(">> ")
      
      if choice2 is " ":
         print("open : "+datapoint[int(choice)].file.strip("{").strip("}"))
         subprocess.Popen([PDFviewer+prefix+datapoint[int(choice)].file.strip("{").strip("}")],shell=True)

 
def Exit(arguments):
   exit()



   
def ReadDatabase(prefix):
   msg=""
   database=[]
   
   try:
   # if(True):      
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
               di={data.strip(",").split("=")[0][:-1]:data.strip(",").split("=")[1][1:]}
               # print(2,data)
               # print(3,di)
               
               LE.BibContent[data.strip(",").split("=")[0][:-1].strip(" ")]=data.strip(",").split("=")[1][1:]
      
      fileH.close()
   except:
      msg=msg+"literature.bib "+Texti.YELLOW+'error reading database ... '+Texti.END+"\n"
      print(Texti.RED+"Error reading database"+Texti.END)


   msg+=" Number of literature entries: "+str(len(database))+"\n"
      
   return database,msg
         





if __name__ == '__main__':
   #===== Main routine execute =============
   #start = time.time()
   main()
   #end = time.time()
   #print('\n\nTime:',end - start,'sec')
   #========================================
