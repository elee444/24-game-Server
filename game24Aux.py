##########################
<<<<<<< HEAD
#File Name:  game24aux.py
#Description: Classes - game and aBlob. An instance of  'game' class initilizes
#                the game, it also creates all the objects of aBlob.
#                
#Last Modified:  Enoch Lee (11/14/18) Rewrote the helper codes in OOP, Added
=======
# File Name:  game24aux.py
# Description: Classes - game and aBlob. An instance of  'game' class initilizes
#                the game, it also creates all the objects of aBlob.
#
# Last Modified:  Enoch Lee (11/14/18) Rewrote the helper codes in OOP, Added
>>>>>>> f2718d7865ebe578f935fec0fe47b4a3a475d2cd
#                'New", 'Restart','End', 'Back', and 'Hint'  buttons. Added
#                restoration capability so the new buttons (except 'Hint'
#                work).  Todo - determine and implement what
#                'Hint' button should do.
<<<<<<< HEAD
#Last Modified:  Enoch Lee (12/5/18) Fixed checkAttempt.
=======
# Last Modified:  Enoch Lee (12/5/18) Fixed checkAttempt.
>>>>>>> f2718d7865ebe578f935fec0fe47b4a3a475d2cd
##########################

import os
import cv2 as cv
import time
import numpy as np
import tensorflow as tf
import sys
import random
import math
from utils import label_map_util
from fractions import Fraction
from post24obj import checkTarget, doMath
from copy import deepcopy

<<<<<<< HEAD
tfont=cv.FONT_HERSHEY_SIMPLEX
color={'blue': (255, 0, 0, 255),'green': (0, 128, 0, 255), 'red': (0, 0, 255, 255), 'black':(0,0,0,0), 'white':(255,255,255,255), 'lime':(0,255,0,255), 'pink':(255,0,255,255)}
class game():
    #freq=0
    freq=cv.getTickFrequency()
    frame_w, frame_h, frame=0,0,None
    fps=0
    target=24
    num_boxes=4
    next_num_box=None
    max_num_boxes=2*(num_boxes-1)+1
    num_ops=4
    ops=['+','-','*','/']
    N=[None] *num_boxes #4 numbers
    #box_dim=0 #the square in a circle
    c_radius=0 #the radius of a blob/circle - compute in
    radius_scale=0.7
    EndGame=False
    #Blob stuffs
    activeBlobs=dict()#store the current active blob for this loop
    activeBlobLocs=dict()   #'Repeated': dict(), and ('Num':dict() or 'Op':dict())
    sessionHistory=[]  #TBD:a list of lists of the active blod idens of each loop
    repeatedBlobTypes=['End', 'Restart',  'New', 'Hint', 'Back']  #locations lsited below
    repeatedBlobTypeLocs=None #[(r2,r2),(int(w_2),r2),(int(w-r2),r2),(int(w-r2-r2),int(h-r2)),(r2+r2,h-r2)]
    #selector: call the repeatedBlob type function
    selector=dict()
    repeatedBlobs=[] #Blobs that are active in each loop - New Game, Restart, End, Hint, Back, etc.
    NumCircles=[] #holding all possible numBlobs
    OpCircles=[]#holding all possible opBlobs
    active_type=None #'Num', 'Op' - type of blobs that are active in the current loop
    BlobstobeOperated=[] # store the two NumBlobs and opBlob to be operated - [num1,num2,op] in postfix form
    displayTexts=[] # a list for display items for this loop/session
    #Messages
    mesgfontsize=2
    Mcorners=dict() #Lower left corners (locations) for Mesgs
    Mesgs={'No':'There is no solution!','Yes':'A solution exists.','Win':'You have won!',\
           'Lost':'You have lost!','Invalid':'Wrong Move!'}
    answers=[] #store all  sols in postfix form
    attempts=[] #store all sols that contains the attempts upto the current one
    #attempts=[answers left after 1st attempt, answers left after 2nd attempts, ...]
    ananswerlen=2*num_boxes-1    #len of an answer in postfix form
    def __init__(self,video):
        ###static data###
        self.frame_w = int(video.get(3))  # float
        self.frame_h = int(video.get(4)) # float
        #comp radius
        self.compRadius()
        ###repeatedBlobTypeLocs
        h,w,r2=self.frame_h,self.frame_w,self.c_radius*2
        w_2,h_2=w/2,h/2
        self.repeatedBlobTypeLocs=[(int(r2*1.5),r2),(int(w_2),r2),(int(w-r2*1.5),r2),(int(w-r2*2),int(h-r2)),(r2*2,h-r2)]
        for e in self.Mesgs:
            Msize=cv.getTextSize(self.Mesgs[e], tfont, self.mesgfontsize, 2)[0]
            self.Mcorners[e]=(int((self.frame_w-Msize[0])/2), int((self.frame_h-Msize[1])/2))
        #compute the locations where to display actiave blobs
        self.blobLocs()
        self.selector={'End': self.End,'Restart':self.Restart,  'New':self.New, 'Hint':self.Hint, 'Back':self.Back} 
        ###session data###
        self.active_type='Num'  #it begins with Num type
        self.next_num_box=self.num_boxes
        #generate  numbers for the game
        for i in range(self.num_boxes):
            self.N[i]=str(random.randint(1,10))
        self.N=['4','3','3','5']
        #pre-compute all possible answers in postfix form
        self.verifyTarget(self.N)
        #create all blobs
        self.createBlobs()
        #these blobs are always there
        self.activeBlobs['Repeated']=self.repeatedBlobs  
        
    #return frame width and frame height
    def getDim(self):
        return self.frame_w,self.frame_h
    
    #check if there are solutions
    def verifyTarget(self,N):
        self.answers=checkTarget(N,self.target)
        self.attempts=[deepcopy(self.answers)]
        print('An answer is - ')#,self.answers)
        for a in self.answers:
            print(a)
        
    #found sols that the attempts (upto now) will yield the target and store
    #it in 'attempts'
    #Note 'res' is the result after evaluating 'bloblist'
    def checkAttempt(self,bloblist,res):
        lenc=len(bloblist) #should be of length 3
        #get the actual 'number's and operator from bloblist
        blobvallist=[str(x.getVal()) for  x in bloblist]
        #prepare to replace the match substring with its resultant value
        replace=[str(res)]
        tmp=[]
        #tmp=set()
        for ans in self.attempts[-1]:
            #determine if blobvallist is a substrig of a valid solution
            tmpans=deepcopy(ans)
            for i in range(len(ans)-lenc+1):
                if (blobvallist==ans[i:i+lenc]): #a valid move
                    tmpans[i:i+lenc]=replace
                    print('Partial ans ',tmpans)
                    tmp.append(tmpans)
                    #tmp.add(tmpans)
                    tmpans=deepcopy(ans)
        self.attempts.append(tmp)
        if len(tmp)==0: return False
        return True
        
    def End(self):
        self.EndGame=True
    def getEndGame(self):
        return self.EndGame
    def Restart(self):
        print('in Restart ...')
        #return
        self.active_type='Num'  #it begins with Num type
        self.next_num_box=self.num_boxes
        self.activeBlobs=dict() #store the current active blob for this loop
        self.sessionHistory=[]  #a list of
        self.BlobstobeOperated=[] # store the two NumBlobs to be operated - [num1,num2,op]
        self.displayTexts=[] #
        self.NumCircles.clear()
        self.OpCircles.clear()
        self.repeatedBlobs.clear()
        self.attempts=[deepcopy(self.answers)]
        self.createBlobs()
        self.updateactiveBlobs()
    def New(self): #Start a new game, clean up all parameters
        print('in New ...')
        self.active_type='Num'  #it begins with Num type
        self.next_num_box=self.num_boxes
        self.activeBlobs=dict() #store the current active blob for this loop
        self.sessionHistory=[]  #a list of
        self.BlobstobeOperated=[] # store the two NumBlobs to be operated - [num1,num2,op]
        self.displayTexts=[] #
=======
tfont = cv.FONT_HERSHEY_SIMPLEX
color = {'blue': (255, 0, 0, 255), 'green': (0, 128, 0, 255), 'red': (0, 0, 255, 255), 'black': (
    0, 0, 0, 0), 'white': (255, 255, 255, 255), 'lime': (0, 255, 0, 255), 'pink': (255, 0, 255, 255)}


class game():
    # freq=0
    freq = cv.getTickFrequency()
    frame_w, frame_h, frame = 0, 0, None
    fps = 0
    target = 24
    num_boxes = 4
    next_num_box = None
    max_num_boxes = 2 * (num_boxes - 1) + 1
    num_ops = 4
    ops = ['+', '-', '*', '/']
    N = [None] * num_boxes  # 4 numbers
    # box_dim=0 #the square in a circle
    c_radius = 0  # the radius of a blob/circle - compute in
    radius_scale = 0.7
    EndGame = False
    # Blob stuffs
    activeBlobs = dict()  # store the current active blob for this loop
    activeBlobLocs = dict()  # 'Repeated': dict(), and ('Num':dict() or 'Op':dict())
    sessionHistory = []  # TBD:a list of lists of the active blod idens of each loop
    repeatedBlobTypes = ['End', 'Restart',  'New',
                         'Hint', 'Back']  # locations lsited below
    # [(r2,r2),(int(w_2),r2),(int(w-r2),r2),(int(w-r2-r2),int(h-r2)),(r2+r2,h-r2)]
    repeatedBlobTypeLocs = None
    # selector: call the repeatedBlob type function
    selector = dict()
    # Blobs that are active in each loop - New Game, Restart, End, Hint, Back, etc.
    repeatedBlobs = []
    NumCircles = []  # holding all possible numBlobs
    OpCircles = []  # holding all possible opBlobs
    active_type = None  # 'Num', 'Op' - type of blobs that are active in the current loop
    # store the two NumBlobs and opBlob to be operated - [num1,num2,op] in postfix form
    BlobstobeOperated = []
    displayTexts = []  # a list for display items for this loop/session
    # Messages
    mesgfontsize = 2
    Mcorners = dict()  # Lower left corners (locations) for Mesgs
    Mesgs = {'No': 'There is no solution!', 'Yes': 'A solution exists.', 'Win': 'You have won!',
             'Lost': 'You have lost!', 'Invalid': 'Wrong Move!'}
    answers = []  # store all  sols in postfix form
    attempts = []  # store all sols that contains the attempts upto the current one
    # attempts=[answers left after 1st attempt, answers left after 2nd attempts, ...]
    ananswerlen = 2 * num_boxes - 1  # len of an answer in postfix form

    def __init__(self, video):
        ###static data###
        self.frame_w = int(video.get(3))  # float
        self.frame_h = int(video.get(4))  # float
        # comp radius
        self.compRadius()
        # repeatedBlobTypeLocs
        h, w, r2 = self.frame_h, self.frame_w, self.c_radius * 2
        w_2, h_2 = w / 2, h / 2
        self.repeatedBlobTypeLocs = [(int(r2 * 1.5), r2), (int(w_2), r2), (int(
            w - r2 * 1.5), r2), (int(w - r2 * 2), int(h - r2)), (r2 * 2, h - r2)]
        for e in self.Mesgs:
            Msize = cv.getTextSize(
                self.Mesgs[e], tfont, self.mesgfontsize, 2)[0]
            self.Mcorners[e] = (int((self.frame_w - Msize[0]) / 2),
                                int((self.frame_h - Msize[1]) / 2))
        # compute the locations where to display actiave blobs
        self.blobLocs()
        self.selector = {'End': self.End, 'Restart': self.Restart,
                         'New': self.New, 'Hint': self.Hint, 'Back': self.Back}
        ###session data###
        self.active_type = 'Num'  # it begins with Num type
        self.next_num_box = self.num_boxes
        # generate  numbers for the game
        for i in range(self.num_boxes):
            self.N[i] = str(random.randint(1, 10))
        self.N = ['4', '3', '3', '5']
        # pre-compute all possible answers in postfix form
        self.verifyTarget(self.N)
        # create all blobs
        self.createBlobs()
        # these blobs are always there
        self.activeBlobs['Repeated'] = self.repeatedBlobs

    # return frame width and frame height
    def getDim(self):
        return self.frame_w, self.frame_h

    # check if there are solutions
    def verifyTarget(self, N):
        self.answers = checkTarget(N, self.target)
        self.attempts = [deepcopy(self.answers)]
        print('An answer is - ')  # ,self.answers)
        for a in self.answers:
            print(a)

    # found sols that the attempts (upto now) will yield the target and store
    #it in 'attempts'
    # Note 'res' is the result after evaluating 'bloblist'
    def checkAttempt(self, bloblist, res):
        lenc = len(bloblist)  # should be of length 3
        # get the actual 'number's and operator from bloblist
        blobvallist = [str(x.getVal()) for x in bloblist]
        # prepare to replace the match substring with its resultant value
        replace = [str(res)]
        tmp = []
        # tmp=set()
        for ans in self.attempts[-1]:
            # determine if blobvallist is a substrig of a valid solution
            tmpans = deepcopy(ans)
            for i in range(len(ans) - lenc + 1):
                if (blobvallist == ans[i:i + lenc]):  # a valid move
                    tmpans[i:i + lenc] = replace
                    print('Partial ans ', tmpans)
                    tmp.append(tmpans)
                    # tmp.add(tmpans)
                    tmpans = deepcopy(ans)
        self.attempts.append(tmp)
        if len(tmp) == 0:
            return False
        return True

    def End(self):
        self.EndGame = True

    def getEndGame(self):
        return self.EndGame

    def Restart(self):
        print('in Restart ...')
        # return
        self.active_type = 'Num'  # it begins with Num type
        self.next_num_box = self.num_boxes
        self.activeBlobs = dict()  # store the current active blob for this loop
        self.sessionHistory = []  # a list of
        self.BlobstobeOperated = []  # store the two NumBlobs to be operated - [num1,num2,op]
        self.displayTexts = []
        self.NumCircles.clear()
        self.OpCircles.clear()
        self.repeatedBlobs.clear()
        self.attempts = [deepcopy(self.answers)]
        self.createBlobs()
        self.updateactiveBlobs()

    def New(self):  # Start a new game, clean up all parameters
        print('in New ...')
        self.active_type = 'Num'  # it begins with Num type
        self.next_num_box = self.num_boxes
        self.activeBlobs = dict()  # store the current active blob for this loop
        self.sessionHistory = []  # a list of
        self.BlobstobeOperated = []  # store the two NumBlobs to be operated - [num1,num2,op]
        self.displayTexts = []
>>>>>>> f2718d7865ebe578f935fec0fe47b4a3a475d2cd
        self.NumCircles.clear()
        self.OpCircles.clear()
        self.repeatedBlobs.clear()
        for i in range(self.num_boxes):
<<<<<<< HEAD
            self.N[i]=str(random.randint(1,10))
        self.verifyTarget(self.N)
        self.attempts=[deepcopy(self.answers)]
=======
            self.N[i] = str(random.randint(1, 10))
        self.verifyTarget(self.N)
        self.attempts = [deepcopy(self.answers)]
>>>>>>> f2718d7865ebe578f935fec0fe47b4a3a475d2cd
        self.createBlobs()
        self.updateactiveBlobs()

    def Hint(self):
        print('in Hint...')
<<<<<<< HEAD
        None #TBD

    def Back(self):
        print('in Back ...')
        self.active_type='Num'
        self.displayTexts=[]
        if 0<len(self.BlobstobeOperated)<3:
            for e in self.BlobstobeOperated:
                print('BlobstobeOperated=',len(self.BlobstobeOperated), e.getId())
                e.updateBlob({'isLocked':False})
                self.updateactiveBlobs()
            self.BlobstobeOperated=[]
            return
        if (self.next_num_box==self.num_boxes): return
        self.next_num_box=self.next_num_box-1
        ancestor=self.NumCircles[self.next_num_box].getParents()
        tparams={'isActive':False, 'isLocked':False,'blobType':'Num','value':None, \
                     'iden':self.next_num_box,'cradius':self.c_radius}
        #restore the blobs
        self.NumCircles[self.next_num_box].updateBlob(tparams) 
        self.NumCircles[ancestor[0].getId()]=ancestor[0]
        self.NumCircles[ancestor[2].getId()]=ancestor[2]
        self.attempts.pop(-1)
        
        
    def loadFrame(self, img):
        self.frame=img
    def getFreq(self):
        return self.freq
    def createBlobs(self):
        #Create the New Game Blob
        ###Static - new state changes ###
        for b in self.repeatedBlobTypes:
             tparams={'isActive':True, 'isLocked':False,'blobType':b,'value':b, \
                     'iden':0,'cradius':self.c_radius}
             self.repeatedBlobs.append(aBlob(tparams))
        ###Session###
        #Create all Op Blobs
        for i , op in enumerate(self.ops):
            tparams={'isActive':True, 'isLocked':False,'blobType':'Op','value':self.ops[i], \
                     'iden':i,'cradius':self.c_radius}
            self.OpCircles.append(aBlob(tparams)) #True, 'Op', self.ops[i], self.c_radius,i)
        #Create all the Num Blobs
        for i in range(self.num_boxes):
            tparams={'isActive':True, 'isLocked':False,'blobType':'Num','value':self.N[i], \
                     'iden':i,'cradius':self.c_radius}
            self.NumCircles.append(aBlob(tparams)) #True, 'Num', self.N[i], self.c_radius,i)
        for i in range(self.num_boxes,self.max_num_boxes):
            tparams={'isActive':False, 'isLocked':False,'blobType':'Num','value':None, \
                     'iden':i,'cradius':self.c_radius}
            self.NumCircles.append(aBlob(tparams)) #False, 'Num', None, self.c_radius,i)

    def blobLocs(self): #Compute the locations of all blobs
        tmp=[]
        #'Repeated' blobs such as 'Restart', ...
        for k,b in enumerate(self.repeatedBlobTypes):
            tmp.append(self.repeatedBlobTypeLocs[k])
        self.activeBlobLocs['Repeated']={len(self.repeatedBlobTypes):tmp}
        #session Blob locations
        #for 'Num': find the centers for .. , 4, 3 and 2 numbers
        tmp=dict()
        for i in range(1,self.num_boxes+1):
            tmp[i]=[(int((2*j+1)/(2*i+1)*(self.frame_w)+self.c_radius/2), \
                     int(self.frame_h*0.65)) for j in range(i)]
        self.activeBlobLocs['Num']=tmp
        #for 'Op': find the centers for 4 operaions
        self.activeBlobLocs['Op']={self.num_ops:[(int((2*i+1)/(2*self.num_ops+1)*\
                                                      (self.frame_w)+self.c_radius/2), int(self.frame_h*0.4)) \
                                                 for i in range(self.num_ops)]}

    def printBlobs(self):
        for e in self.OpCircles: 
            e.bPrint()
        for e in self.NumCircles:
            e.bPrint()
    def printActiveBlobs(self):  
        for e in self.activeBlobs:
            e.bPrint()
    def printToBeOperatedBlobs(self):
        for e in self.BlobstobeOperated:
            e.bPrint()
        
    #update activeBlob list of the loop
    ##First len(repeatedBlobs) are Repeated type, the rest are either Num or Op type
    def updateactiveBlobs(self):
        ##E.g. activeBlobs={'Repeated':[Some blobs ...],'Num':[....]}
        ###Static-repeated list###
        self.activeBlobs=dict()
        self.activeBlobs['Repeated']=self.repeatedBlobs     
        ###Session-Num or Op list###
        tmp=[]
        if self.active_type =='Num' :
            for n in self.NumCircles:
                if n.getActive() == True:
                    tmp.append(n)
            self.activeBlobs['Num']=tmp
        elif self.active_type =='Op':
            self.activeBlobs['Op']=self.OpCircles
        else:
            None
        
    #check if any activeBlob got locked
    #for now we use only the first hand
    def handlockedBlob(self, hand_centers, framerate):
        btype=None
        if len(hand_centers) ==0: return #no hands
        for atype,activeB in self.activeBlobs.items():
            lab=len(activeB)
            for j, b in enumerate(activeB):
                if b.getLock() == False and b.getActive() == True:
                    bcenter= self.activeBlobLocs[atype][lab][j]
                    t_lock=b.isHandLocked(bcenter,hand_centers[0],self.c_radius, framerate)
                    if t_lock == True:
                        btype=b.getType()
                        if (btype in self.repeatedBlobTypes): #for Repeated type - 'New','End', etc.
                            self.selector[btype]()   #call New(), End(), etc.
                            return #'Continue'
                        else:
                            self.BlobstobeOperated.append(b)
                        break
        lb=len(self.BlobstobeOperated)
        if lb==3:
            #self.compSelectedBlobs(self.BlobstobeOperated)
            self.checkSelectedBlobs(self.BlobstobeOperated)
            self.BlobstobeOperated=[]
            self.active_type ='Num'
        elif lb==2:
            self.active_type ='Op'                  
        return #'Continue'
    
=======
        None  # TBD

    def Back(self):
        print('in Back ...')
        self.active_type = 'Num'
        self.displayTexts = []
        if 0 < len(self.BlobstobeOperated) < 3:
            for e in self.BlobstobeOperated:
                print('BlobstobeOperated=', len(
                    self.BlobstobeOperated), e.getId())
                e.updateBlob({'isLocked': False})
                self.updateactiveBlobs()
            self.BlobstobeOperated = []
            return
        if (self.next_num_box == self.num_boxes):
            return
        self.next_num_box = self.next_num_box - 1
        ancestor = self.NumCircles[self.next_num_box].getParents()
        tparams = {'isActive': False, 'isLocked': False, 'blobType': 'Num', 'value': None,
                   'iden': self.next_num_box, 'cradius': self.c_radius}
        # restore the blobs
        self.NumCircles[self.next_num_box].updateBlob(tparams)
        self.NumCircles[ancestor[0].getId()] = ancestor[0]
        self.NumCircles[ancestor[2].getId()] = ancestor[2]
        self.attempts.pop(-1)

    def loadFrame(self, img):
        self.frame = img

    def getFreq(self):
        return self.freq

    def createBlobs(self):
        # Create the New Game Blob
        ###Static - new state changes ###
        for b in self.repeatedBlobTypes:
            tparams = {'isActive': True, 'isLocked': False, 'blobType': b, 'value': b,
                       'iden': 0, 'cradius': self.c_radius}
            self.repeatedBlobs.append(aBlob(tparams))
        ###Session###
        # Create all Op Blobs
        for i, op in enumerate(self.ops):
            tparams = {'isActive': True, 'isLocked': False, 'blobType': 'Op', 'value': self.ops[i],
                       'iden': i, 'cradius': self.c_radius}
            # True, 'Op', self.ops[i], self.c_radius,i)
            self.OpCircles.append(aBlob(tparams))
        # Create all the Num Blobs
        for i in range(self.num_boxes):
            tparams = {'isActive': True, 'isLocked': False, 'blobType': 'Num', 'value': self.N[i],
                       'iden': i, 'cradius': self.c_radius}
            # True, 'Num', self.N[i], self.c_radius,i)
            self.NumCircles.append(aBlob(tparams))
        for i in range(self.num_boxes, self.max_num_boxes):
            tparams = {'isActive': False, 'isLocked': False, 'blobType': 'Num', 'value': None,
                       'iden': i, 'cradius': self.c_radius}
            # False, 'Num', None, self.c_radius,i)
            self.NumCircles.append(aBlob(tparams))

    def blobLocs(self):  # Compute the locations of all blobs
        tmp = []
        # 'Repeated' blobs such as 'Restart', ...
        for k, b in enumerate(self.repeatedBlobTypes):
            tmp.append(self.repeatedBlobTypeLocs[k])
        self.activeBlobLocs['Repeated'] = {len(self.repeatedBlobTypes): tmp}
        # session Blob locations
        # for 'Num': find the centers for .. , 4, 3 and 2 numbers
        tmp = dict()
        for i in range(1, self.num_boxes + 1):
            tmp[i] = [(int((2 * j + 1) / (2 * i + 1) * (self.frame_w) + self.c_radius / 2),
                       int(self.frame_h * 0.65)) for j in range(i)]
        self.activeBlobLocs['Num'] = tmp
        # for 'Op': find the centers for 4 operaions
        self.activeBlobLocs['Op'] = {self.num_ops: [(int((2 * i + 1) / (2 * self.num_ops + 1) *
                                                         (self.frame_w) + self.c_radius / 2), int(self.frame_h * 0.4))
                                                    for i in range(self.num_ops)]}

    def printBlobs(self):
        for e in self.OpCircles:
            e.bPrint()
        for e in self.NumCircles:
            e.bPrint()

    def printActiveBlobs(self):
        for e in self.activeBlobs:
            e.bPrint()

    def printToBeOperatedBlobs(self):
        for e in self.BlobstobeOperated:
            e.bPrint()

    # update activeBlob list of the loop
    # First len(repeatedBlobs) are Repeated type, the rest are either Num or Op type
    def updateactiveBlobs(self):
        # E.g. activeBlobs={'Repeated':[Some blobs ...],'Num':[....]}
        ###Static-repeated list###
        self.activeBlobs = dict()
        self.activeBlobs['Repeated'] = self.repeatedBlobs
        ###Session-Num or Op list###
        tmp = []
        if self.active_type == 'Num':
            for n in self.NumCircles:
                if n.getActive() == True:
                    tmp.append(n)
            self.activeBlobs['Num'] = tmp
        elif self.active_type == 'Op':
            self.activeBlobs['Op'] = self.OpCircles
        else:
            None

    # check if any activeBlob got locked
    # for now we use only the first hand
    def handlockedBlob(self, hand_centers, framerate):
        btype = None
        if len(hand_centers) == 0:
            return  # no hands
        for atype, activeB in self.activeBlobs.items():
            lab = len(activeB)
            for j, b in enumerate(activeB):
                if b.getLock() == False and b.getActive() == True:
                    bcenter = self.activeBlobLocs[atype][lab][j]
                    t_lock = b.isHandLocked(
                        bcenter, hand_centers[0], self.c_radius, framerate)
                    if t_lock == True:
                        btype = b.getType()
                        # for Repeated type - 'New','End', etc.
                        if (btype in self.repeatedBlobTypes):
                            self.selector[btype]()  # call New(), End(), etc.
                            return  # 'Continue'
                        else:
                            self.BlobstobeOperated.append(b)
                        break
        lb = len(self.BlobstobeOperated)
        if lb == 3:
            # self.compSelectedBlobs(self.BlobstobeOperated)
            self.checkSelectedBlobs(self.BlobstobeOperated)
            self.BlobstobeOperated = []
            self.active_type = 'Num'
        elif lb == 2:
            self.active_type = 'Op'
        return  # 'Continue'

>>>>>>> f2718d7865ebe578f935fec0fe47b4a3a475d2cd
    # #if two numbers are picked (two NumBlobs got handlocked),
    # #compute the result 'locally'
    # #bloblist=[left operand blob, right operand blob, operator blob]
    # def compSelectedBlobs(self,bloblist):
    #     #compute it
    #     result=doMath(bloblist[2].getVal(),int(bloblist[0].getVal()),int(bloblist[1].getVal()))
    #     #prepare to update the blobs
    #     tdata={'isActive':True,'isLocked':False,'value':str(result)}
    #     print(self.next_num_box, tdata['value'])
    #     self.NumCircles[self.next_num_box].updateBlob(tdata)
    #     #Time to update the 'parents' of this Blob to [bloblist[0],bloblist[2],bloblist[1]]
    #     tdata={'isLocked':False}
    #     bloblist[0].updateBlob(tdata)
<<<<<<< HEAD
    #     bloblist[1].updateBlob(tdata)   
=======
    #     bloblist[1].updateBlob(tdata)
>>>>>>> f2718d7865ebe578f935fec0fe47b4a3a475d2cd
    #     ancestor=[bloblist[0],bloblist[2],bloblist[1]]
    #     #active the new NumBlob
    #     self.NumCircles[self.next_num_box].updateParents(list(map(deepcopy,ancestor)))
    #     #deactivate the selected NumBlobs
    #     tdata={'isActive':False}
    #     bloblist[0].updateBlob(tdata)
    #     bloblist[1].updateBlob(tdata)
    #     #if the move is illegal, i.e. division by zero
    #     if (result==None): #invalid move
    #         print(self.Mesgs['Invalid'])
    #         tparams=['Repeated',(self.Mesgs['Invalid'], self.Mcorners['Invalid'], tfont, self.mesgfontsize, color['green'],  8)]
    #         self.displayTexts.append(tparams)
    #     #No more selection
    #     #Done selection sequence. Time to check if the end  result ==target
    #     if (self.next_num_box ==self.max_num_boxes -1):  ##
    #         print('%%%%% --- ',result)
    #         if result==self.target:
    #             print(self.Mesgs['Win']) #won
    #             tparams=['Repeated',(self.Mesgs['Win'], self.Mcorners['Win'], tfont, self.mesgfontsize, color['blue'],  8)]
    #         else:  #Lost
    #             print(self.Mesgs['Lost'])
    #             tparams=['Repeated',(self.Mesgs['Lost'], self.Mcorners['Lost'], tfont, self.mesgfontsize, color['red'],  8)]
    #         self.displayTexts.append(tparams)
    #     self.next_num_box=self.next_num_box+1

<<<<<<< HEAD
    #Same as above but it compare the current bloblist with all pre-computed answers
    def checkSelectedBlobs(self,bloblist):
        #compute it
        valid=False
        #result=None
        result=doMath(bloblist[2].getVal(),int(bloblist[0].getVal()), int(bloblist[1].getVal()), exact=True)
        if (self.checkAttempt(bloblist,result) == True):
            valid=True  #attempts[-1] has len >0, i.e. a valid  move
        
        #prepare to update the blobs    
        tdata={'isActive':True,'isLocked':False,'value':str(result)}
        print(self.next_num_box, tdata['value'])
        self.NumCircles[self.next_num_box].updateBlob(tdata)
        #Time to update the 'parents' of this Blob to [bloblist[0],bloblist[2],bloblist[1]]
        tdata={'isLocked':False}
        bloblist[0].updateBlob(tdata)
        bloblist[1].updateBlob(tdata)   
        ancestor=[bloblist[0],bloblist[2],bloblist[1]]
        #active the new NumBlob
        self.NumCircles[self.next_num_box].updateParents(list(map(deepcopy,ancestor)))
        #deactivate the selected NumBlobs
        tdata={'isActive':False}
        bloblist[0].updateBlob(tdata)
        bloblist[1].updateBlob(tdata)
        #if the move is illegal, i.e. division by zero
        if (result ==None or valid==False): #invalid or illegal move
            print(self.Mesgs['Invalid'])
            tparams=['Repeated',(self.Mesgs['Invalid'], self.Mcorners['Invalid'], tfont, self.mesgfontsize, color['blue'],  8)]
            self.displayTexts.append(tparams)
        #No more selection
        #Done selection sequence. Time to check if the end  result ==target
        if (valid==True and self.next_num_box ==self.max_num_boxes -1):  ##
            print('%%%%% --- ',result)
            if result==self.target:
                print(self.Mesgs['Win']) #won
                tparams=['Repeated',(self.Mesgs['Win'], self.Mcorners['Win'], tfont, self.mesgfontsize, color['blue'],  8)]
            else:  #Lost
                print(self.Mesgs['Lost'])
                tparams=['Repeated',(self.Mesgs['Lost'], self.Mcorners['Lost'], tfont, self.mesgfontsize, color['red'],  8)]
            self.displayTexts.append(tparams)
        self.next_num_box=self.next_num_box+1




        
    #draw active Blobs for display, and prepare their and others texts
    def processactiveBlobs(self):
        for atype,activeB in self.activeBlobs.items():  #activeB=[some blobs ....]
            lab=len(activeB)
            for j, b in enumerate(activeB):
                tmp=b.draw(self.activeBlobLocs[atype][lab][j],self.frame)
                self.displayTexts.extend(tmp)
        tokeep=[]
        for i, d in enumerate(self.displayTexts):
            cv.putText(self.frame,*(d[1]))
            if d[0]=='Repeated': tokeep.append(d)
        self.displayTexts=tokeep


    def box_normal_to_pixel(self, box, dim):
        height, width = dim[0], dim[1]
        box_pixel = [int(box[0]*height), int(box[1]*width), int(box[2]*height), int(box[3]*width)]
        return np.array(box_pixel)     
    def compRadius(self):
        box_dim=int(max(self.frame_h,self.frame_w)/(2*self.num_boxes+1)) 
        self.c_radius= math.ceil(self.radius_scale*box_dim/math.sqrt(2))

#Blobs -- number circles, operator circles, etc.
class aBlob():
    cdata={'isActive':None, 'isLocked':None,'blobType':None,\
           'value':None, 'iden':None,'cradius':None}
    textsize = None
    valCorner=None
    handCount=0
    t1=0
    t2=0
    lockscale=1.8  #hand lock senitivity > 1
    #This parents  is None if it is the original blob containing one of the numbers
    #ANd the 'isActive' is True.
    fontsize=1
    parents=None #history - [numBlob1, opBlob, numBlob2]
    def __init__(self, params): #sactive, blobtype, val, radius,iden):
        self.handCount=0
        self.t1=0
        self.t2=0
        self.updateBlob(params)
        self.textsize = cv.getTextSize(self.cdata['value'], tfont, self.fontsize, 2)[0]
    def updateParents(self, ancestor):
        self.parents=ancestor
    def updateBlob(self,params):  #params dict of data
        t=deepcopy(self.cdata)
        t.update(params)
        self.cdata=t
        if 'value' in params:
            self.textsize = cv.getTextSize(str(self.cdata['value']), tfont, self.fontsize, 2)[0]
    def getParents(self):
        return self.parents
    def getLock(self):
        return self.cdata['isLocked']
    def getVal(self):
        return self.cdata['value']
    def getData(self):
        return self.cdata
    def getId(self):
        return self.cdata['iden']
    def getActive(self):
        return self.cdata['isActive']
    def getRadius(self):
        return self.cdata['cradius']
    def getType(self):
        return self.cdata['blobType']

    #Check if this blob is locked on by a hand
    def isHandLocked(self, c_center,h_center,rad,framerate): 
        if ((c_center[0]-h_center[0])**2)+((c_center[1]-h_center[1])**2)<(rad**2):
            self.handCount=self.handCount+1
            if (self.handCount >=self.lockscale*framerate):
                if (self.getType()=='Num'):  #Don't update this for 'Op' or any 'Repeated' types
                    self.cdata['isLocked']=True
                self.handCount=0
                return True
        return False
        
    def draw(self, location,img):
        cFull=2
        if (self.getLock() == True):
            cFull=-1
        cv.circle(img,location,self.getRadius(),color['lime'],cFull)
        valCorner=(location[0]-self.textsize[0]//2, location[1]+self.textsize[1]//2)
        #cv.putText(img, self.getVal(), valCorner, tfont,1.5, color['black'],  5)
        sv=self.getVal()
        tparams1=['Once',(sv, valCorner, tfont,self.fontsize, color['black'],  5)]
        tparams2=['Once',(sv, valCorner, tfont,self.fontsize, color['white'],  1)]
        return [tparams1,tparams2]
        #return tparams2

    def bPrint(self):
        print(self.cdata)


    
=======
    # Same as above but it compare the current bloblist with all pre-computed answers
    def checkSelectedBlobs(self, bloblist):
        # compute it
        valid = False
        # result=None
        result = doMath(bloblist[2].getVal(), int(
            bloblist[0].getVal()), int(bloblist[1].getVal()), exact=True)
        if (self.checkAttempt(bloblist, result) == True):
            valid = True  # attempts[-1] has len >0, i.e. a valid  move

        # prepare to update the blobs
        tdata = {'isActive': True, 'isLocked': False, 'value': str(result)}
        print(self.next_num_box, tdata['value'])
        self.NumCircles[self.next_num_box].updateBlob(tdata)
        # Time to update the 'parents' of this Blob to [bloblist[0],bloblist[2],bloblist[1]]
        tdata = {'isLocked': False}
        bloblist[0].updateBlob(tdata)
        bloblist[1].updateBlob(tdata)
        ancestor = [bloblist[0], bloblist[2], bloblist[1]]
        # active the new NumBlob
        self.NumCircles[self.next_num_box].updateParents(
            list(map(deepcopy, ancestor)))
        # deactivate the selected NumBlobs
        tdata = {'isActive': False}
        bloblist[0].updateBlob(tdata)
        bloblist[1].updateBlob(tdata)
        # if the move is illegal, i.e. division by zero
        if (result == None or valid == False):  # invalid or illegal move
            print(self.Mesgs['Invalid'])
            tparams = ['Repeated', (self.Mesgs['Invalid'], self.Mcorners['Invalid'],
                                    tfont, self.mesgfontsize, color['blue'],  8)]
            self.displayTexts.append(tparams)
        # No more selection
        # Done selection sequence. Time to check if the end  result ==target
        if (valid == True and self.next_num_box == self.max_num_boxes - 1):
            print('%%%%% --- ', result)
            if result == self.target:
                print(self.Mesgs['Win'])  # won
                tparams = ['Repeated', (self.Mesgs['Win'], self.Mcorners['Win'],
                                        tfont, self.mesgfontsize, color['blue'],  8)]
            else:  # Lost
                print(self.Mesgs['Lost'])
                tparams = ['Repeated', (self.Mesgs['Lost'], self.Mcorners['Lost'],
                                        tfont, self.mesgfontsize, color['red'],  8)]
            self.displayTexts.append(tparams)
        self.next_num_box = self.next_num_box + 1

    # draw active Blobs for display, and prepare their and others texts

    def processactiveBlobs(self):
        # activeB=[some blobs ....]
        for atype, activeB in self.activeBlobs.items():
            lab = len(activeB)
            for j, b in enumerate(activeB):
                tmp = b.draw(self.activeBlobLocs[atype][lab][j], self.frame)
                self.displayTexts.extend(tmp)
        tokeep = []
        for i, d in enumerate(self.displayTexts):
            cv.putText(self.frame, *(d[1]))
            if d[0] == 'Repeated':
                tokeep.append(d)
        self.displayTexts = tokeep

    def box_normal_to_pixel(self, box, dim):
        height, width = dim[0], dim[1]
        box_pixel = [int(box[0] * height), int(box[1] * width),
                     int(box[2] * height), int(box[3] * width)]
        return np.array(box_pixel)

    def compRadius(self):
        box_dim = int(max(self.frame_h, self.frame_w)
                      / (2 * self.num_boxes + 1))
        self.c_radius = math.ceil(self.radius_scale * box_dim / math.sqrt(2))

# Blobs -- number circles, operator circles, etc.


class aBlob():
    cdata = {'isActive': None, 'isLocked': None, 'blobType': None,
             'value': None, 'iden': None, 'cradius': None}
    textsize = None
    valCorner = None
    handCount = 0
    t1 = 0
    t2 = 0
    lockscale = 1.8  # hand lock senitivity > 1
    # This parents  is None if it is the original blob containing one of the numbers
    # ANd the 'isActive' is True.
    fontsize = 1
    parents = None  # history - [numBlob1, opBlob, numBlob2]

    def __init__(self, params):  # sactive, blobtype, val, radius,iden):
        self.handCount = 0
        self.t1 = 0
        self.t2 = 0
        self.updateBlob(params)
        self.textsize = cv.getTextSize(
            self.cdata['value'], tfont, self.fontsize, 2)[0]

    def updateParents(self, ancestor):
        self.parents = ancestor

    def updateBlob(self, params):  # params dict of data
        t = deepcopy(self.cdata)
        t.update(params)
        self.cdata = t
        if 'value' in params:
            self.textsize = cv.getTextSize(
                str(self.cdata['value']), tfont, self.fontsize, 2)[0]

    def getParents(self):
        return self.parents

    def getLock(self):
        return self.cdata['isLocked']

    def getVal(self):
        return self.cdata['value']

    def getData(self):
        return self.cdata

    def getId(self):
        return self.cdata['iden']

    def getActive(self):
        return self.cdata['isActive']

    def getRadius(self):
        return self.cdata['cradius']

    def getType(self):
        return self.cdata['blobType']

    # Check if this blob is locked on by a hand
    def isHandLocked(self, c_center, h_center, rad, framerate):
        if ((c_center[0] - h_center[0])**2) + ((c_center[1] - h_center[1])**2) < (rad**2):
            self.handCount = self.handCount + 1
            if (self.handCount >= self.lockscale * framerate):
                if (self.getType() == 'Num'):  # Don't update this for 'Op' or any 'Repeated' types
                    self.cdata['isLocked'] = True
                self.handCount = 0
                return True
        return False

    def draw(self, location, img):
        cFull = 2
        if (self.getLock() == True):
            cFull = -1
        cv.circle(img, location, self.getRadius(), color['lime'], cFull)
        valCorner = (location[0] - self.textsize[0] // 2,
                     location[1] + self.textsize[1] // 2)
        #cv.putText(img, self.getVal(), valCorner, tfont,1.5, color['black'],  5)
        sv = self.getVal()
        tparams1 = ['Once', (sv, valCorner, tfont,
                             self.fontsize, color['black'],  5)]
        tparams2 = ['Once', (sv, valCorner, tfont,
                             self.fontsize, color['white'],  1)]
        return [tparams1, tparams2]
        # return tparams2

    def bPrint(self):
        print(self.cdata)
>>>>>>> f2718d7865ebe578f935fec0fe47b4a3a475d2cd
