import gym
from queue import PriorityQueue
import pixelate_arena
import time
import pybullet as p
import pybullet_data
import cv2
import math
import cv2.aruco as aruco
import numpy as np
import os

import time
start_time = time.time()

co_mat=[]
spider=[]
villain=[]
antidote=[]
sand_anti=[]
sandman=[]
goblin_anti=[]
goblin=[]
electro_anti=[]
electro=[]
pa={}
m=13
n=13
inf=100
colmat=np.zeros((n,m))
cosmat=np.zeros((n,m))
graph={}
angle=0
vel=11

cellval=0
cellvaly=0

def fillcomat(img):
    global cellval
    global cellvaly

    height= img.shape[0]
    width= int(img.shape[1])
    for i in range(0,200,1):
        if img[height//2,i][0]>10 or img[height//2,i][1]>10 or img[height//2,i][2]>10:
            print("one",i,img[height//2,i])
            dis1=i
            break

    for i in range(width-1,width-200,-1):  
        if img[height//2,i][0]>10 or img[height//2,i][1]>10 or img[height//2,i][2]>10:
            print("two",width-i,img[height//2,i])
            dis2=width-i
            break
         
    left = min(dis1,dis2)
    #cellval = round((width-left-left)/13)
    # cellval = round((width-left-left+12)/13)
    # start_x_odd = left - 6 + cellval
    # start_x_even = left - 6 +(cellval//2)
    # cellvaly=round(cellval*math.cos(0.523599))
    # cellvaly+=1
    # start_y = (height//2) - (6*cellvaly)
    cellval=40
    cellvaly=45
    addx=45
    addy=39
    start_x_odd=55
    start_x_even=32
    start_y=66
    print("height",height)
    print("width",width)
    print("left",left)
    print("cellval",cellval)
    print("star_x_odd",start_x_odd)
    print("star_x_even",start_x_even)
    print("star_y",start_y)
    print("cellvaly",cellvaly)

    for k in range(13):
        co=[]
        if(k%2==0):
            value=start_x_even
        else:
            value=start_x_odd
        for i in range(13):
            co.append([value,start_y])
            value+=addx
        start_y+=addy
        co_mat.append(co)
    print(co_mat)


def predict_col(im):
    ii=im.shape[0]//2
    jj=im.shape[1]//2
   # b,g,r=im[jj-1,ii-1]
    b,g,r=im[ii-1,jj-1]

    if(b>=200 and g>=200 and r>=200):
        return 4#white
    elif(b>=150 and g>=70 and r>=200):
        return 0#pink
    elif(b<=50 and g>=110 and r<=50):
        return 1#green
    elif(b<=5 and g<=5 and r<=5):
        return -1#black
    elif(b<=10 and g>=160 and r>=200):
        return 2#yellow
    elif(b>=140 and g<=80 and r<=10):
        return 3#blue
    elif(b<=10 and g<=30 and r>=100):
        return 5#red
    elif(b>=60 and g<=40 and r>=50):
        return 6#purple
    else:
        return(10)

def cornercolor(box):
    
    # cv2.imshow("my", box)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    ii=(box.shape[0]//2)
    jj=(box.shape[1]//2)-30
    #b,g,r=box[ii,jj]
    b,g,r=box[ii,10]
    #b,g,r=box[43,5]

    if(b>=200 and g>=200 and r>=200):
        return 4#white
    elif(b>=150 and g>=70 and r>=200):
        return 0#pink
    elif(b<=50 and g>=110 and r<=50):
        return 1#green
    elif(b<=5 and g<=5 and r<=5):
        return -1#black
    elif(b<=10 and g>=160 and r>=200):
        return 2#yellow
    elif(b>=140 and g<=80 and r<=10):
        return 3#blue
    elif(b<=10 and g<=30 and r>=100):
        return 5#red
    elif(b>=60 and g<=40 and r>=50):
        return 6#purple
    else:
        return(10)


def predictshape(mask):
    kernel=np.ones((5,5),np.uint8)
    mask=cv2.erode(mask, kernel,iterations=1)
    mask=cv2.dilate(mask, kernel,iterations=1)
    mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN, kernel)
    mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE, kernel)
    #cv2.imshow("mask",mask)
    #cv2.imwrite(r"C:\Users\jaiss\Downloads\mask1.JPG",mask)
    #cv2.waitKey(0)
    contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cntr in contours:
        area=cv2.contourArea(cntr)
        if area>=300:
            per=cv2.arcLength(cntr, closed=True)
            approx=cv2.approxPolyDP(cntr, epsilon=0.036*per, closed=True)
            #print(len(approx))
            return(approx)


def fill_colmat(img):
    global cellvaly
    global cellval
    for i in range(n):
        for j in range(m):
            
            ii=co_mat[i][j][0]
            jj=co_mat[i][j][1]
            #print("cellval",cellval)
            c=round((cellval-6)/2)
            c=round(c/math.cos(0.523599))
            # c=c*86
            # c=round(c/100)
            #ne=int(((cellval+2)/2)*86/100)
            #print("c",c)
            #box=img[jj-(c+2):jj+(c+2),ii-(round(cellval/2)+2):ii+(round(cellval/2)+2)]
            box=img[jj-26:jj+26,ii-22:ii+22]
           # box=img[ii-((cellval//2)+2):ii+((cellval//2)+2),jj-((cellvaly//2)+2):jj+((cellvaly//2)+2)]
            #print("bpx",box.shape)
            #t=cellval*2
            #box=cv2.resize(box,(120,104))
            box=cv2.resize(box,(box.shape[1]*2,box.shape[0]*2))
            #print((i*13)+j,"shape",box.shape)
            # cv2.imshow("box",box)
            # cv2.waitKey(100)
            col=predict_col(box)
            #print(col)
            if(col==5 and (i!=6 or j!=6)):
                spider.append((i,j))
            if (col==3):
                #kb=box
                #kb=cv2.cvtColor(box,cv2.COLOR_BGR2HSV)
                lowerb=np.array([130,40,0])
                upperb=np.array([255,80,10])
                mask=cv2.inRange(box, lowerb, upperb)
                approx=predictshape(mask)
                #print(len(approx))
                approx=approx.reshape(-1,2)
                #print(approx)
                cornercol=cornercolor(box)
                # print("corner",cornercol)
                # print(box.shape)
                if(len(approx) is 3):  #blue colour in mid and triangle
                    #print("this")
                    if(cornercol==0):
                        colmat[i][j]=51 #sandman antidote
                        antidote.append((i,j))
                        sand_anti.append((i,j))
                    elif(cornercol==6):
                        colmat[i][j]=21 #sandman
                        villain.append((i,j))
                        sandman.append((i,j))
                elif(len(approx) is 4):
                    if(cornercol==0):
                        colmat[i][j]=61 #goblin antidote
                        antidote.append((i,j))
                        goblin_anti.append((i,j))
                    elif(cornercol==1):
                        colmat[i][j]=31 #goblin
                        villain.append((i,j))
                        goblin.append((i,j))
                else:
                    if(cornercol==0):
                        colmat[i][j]=71 #electro antidote
                        antidote.append((i,j))
                        electro_anti.append((i,j))
                    elif(cornercol==2):
                        colmat[i][j]=41 #eectro
                        villain.append((i,j))
                        electro.append((i,j))
            
            else:
                colmat[i][j]=col



def fill_cosmat():
    
    for i in range(n):
        for j in range(m):
            if colmat[i][j]==-1:   #black
                cosmat[i][j]=inf
            elif colmat[i][j]==0:  #pink
                cosmat[i][j]=1
            elif colmat[i][j]==4:  #white
                cosmat[i][j]=1
            elif colmat[i][j]==1:  #green
                cosmat[i][j]=4
            elif colmat[i][j]==5:  #red
                cosmat[i][j]=1
            elif colmat[i][j]==2:  #yellow
                cosmat[i][j]=2
            elif colmat[i][j]==6:  #purple
                cosmat[i][j]=3
            else :
                if colmat[i][j]==21:  #sandman
                    cosmat[i][j]=50
                elif colmat[i][j]==31:  #goblin
                    cosmat[i][j]=50
                elif colmat[i][j]==41: #electro
                    cosmat[i][j]=50
                elif colmat[i][j]==51:  #sandman antidote
                    cosmat[i][j]=1
                elif colmat[i][j]==61:  #goblin antidote
                    cosmat[i][j]=1
                elif colmat[i][j]==71:  #electro antidote
                    cosmat[i][j]=1
                else:
                    cosmat[i][j]=1


def create_graph():
    for i in range(n):
        for j in range(m):
            val=i*n+j
            graph[val]=[]
            # if(colmat[i][j]==-1):  will think later to keep or not:/
            #     continue
            if(i%2==0):  #even rows
                if(j-1>=0 and colmat[i][j-1]!=-1):
                    graph[val].append(i*n+j-1)
                if(j+1<n and colmat[i][j+1]!=-1):
                    graph[val].append(i*n+j+1)
                if(i-1>=0 and j-1>=0 and colmat[i-1][j-1]!=-1):
                    graph[val].append((i-1)*n+j-1)
                if(i-1>=0 and colmat[i-1][j]!=-1):
                    graph[val].append((i-1)*n+j)
                if(i+1<n and j-1>=0 and colmat[i+1][j-1]!=-1):
                    graph[val].append((i+1)*n+j-1)
                if(i+1<n and colmat[i+1][j]!=-1):
                    graph[val].append((i+1)*n+j)
            else:
                if(j-1>=0 and colmat[i][j-1]!=-1):
                    graph[val].append(i*n+j-1)
                if(j+1<n and colmat[i][j+1]!=-1):
                    graph[val].append(i*n+j+1)
                if(i-1>=0 and colmat[i-1][j]!=-1):
                    graph[val].append((i-1)*n+j)
                if(i-1>=0 and j+1<n and colmat[i-1][j+1]!=-1):
                    graph[val].append((i-1)*n+j+1)
                if(i+1<n and colmat[i+1][j]!=-1):
                    graph[val].append((i+1)*n+j)
                if(i+1<n and j+1<n and colmat[i+1][j+1]!=-1):
                    graph[val].append((i+1)*n+j+1)




def dijktras(src,dest,cos_mat):
	q=PriorityQueue()
	par={}
	par[src]=src
	(srcx,srcy)=src
	dist=np.zeros((n,m))
	for i in range(n):
		for j in range(m):
			dist[i][j]=inf
	dist[srcx][srcy]=0
	destx,desty=dest
	q.put((0,src))
	d=[1,-1,0]
	while not q.empty():
		wt,(x,y)=q.get()
		for i in range(len(graph[x*n+y])):
			v=graph[x*n+y][i]
			dx=v//n
			dy=v%n
			if(dist[dx][dy]>dist[x][y]+cos_mat[dx][dy]):
				dist[dx][dy]=dist[x][y]+cos_mat[dx][dy]
				par[(dx,dy)]=(x,y)
				q.put((dist[dx][dy],(dx,dy)))


	path=[]
	(destx,desty)=dest
	path.append(dest)
	#print(dest)
	while destx!=srcx or desty!=srcy:
		(destx,desty)=par[(destx,desty)]
		#print((destx,desty))
		path.append((destx,desty))

	path.reverse()
	return path
            



def dist(img,dest):
    corner=posdetect(img)
    if(len(corner)==0):
        return -1
    x=(corner[0][0]+corner[2][0])//2
    y=(corner[0][1]+corner[2][1])//2
    return(np.sqrt((x-dest[0])**2+(y-dest[1])**2))

def posdetect(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ARUCO_PARAMETERS = aruco.DetectorParameters_create()
    ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, ARUCO_DICT, parameters=ARUCO_PARAMETERS)
    # img = aruco.drawDetectedMarkers(img, corners, borderColor=(0, 0, 255))
    if ids is None:
        return([])
    corners=np.array(corners)
    corner=corners[0]
    corner=corner.reshape((corner.shape[1],corner.shape[2]))
    # print(corner)
    return(corner)




def movement(corner,dest):
    global angle
    x=(corner[0][0]+corner[2][0])//2
    y=(corner[0][1]+corner[2][1])//2
    #print(x,y)
    vxreq=(dest[0]-x)
    vyreq=(dest[1]-y)
    modv=np.sqrt(vxreq**2+vyreq**2)
    vxreq=vxreq/modv
    vyreq=vyreq/modv
    botvx=(corner[0][0]-corner[3][0])
    botvy=(corner[0][1]-corner[3][1])
    mod=np.sqrt(botvx**2+botvy**2)
    botvx=botvx/mod
    botvy=botvy/mod
    botvec=complex(botvx,botvy)
    vec=complex(vxreq,vyreq)
    angle=np.angle(botvec/vec,deg=True)
    #print("angle :",angle)
    if(-7.5<=angle and angle<=7.5):
        #print("straight")
        return("straight")
    elif(angle>=60):
        #print("left60")
        return("left60")
    elif(angle>=30):
        #print("left30")
        return("left30")
    elif(angle>=7.2):
        #print("left")
        return("left")
    elif(angle<=-60):
        #print("right60")
        return("right60")
    elif(angle<=-30):
        #print("right30")
        return("right30")
    else:
        #print("right")
        return("right")

def stop():
    g=0
    while g<20:
        g+=1
        p.stepSimulation()
        env.move_husky(0.0,0.0,0.0,0.0)


def moveforward():
    cnt=0
    while cnt<=100:
        p.stepSimulation()
        # if cnt%600==0:
        #     img=env.camera_feed()
        #     cv2.imshow("im",img)
        #     cv2.waitKey(1)
        cnt+=1
        env.move_husky(vel,vel,vel,vel)
        #env.move_husky(12,12,12,12)
        #cv2.waitKey(5)

def moveright():
    cnt=0
    while(cnt<=25):
        # if cnt%150==0:
        #     img=env.camera_feed()
        #     cv2.imshow("im",img)
        #     cv2.waitKey(1)
        p.stepSimulation()
        env.move_husky(vel,-vel,vel,-vel)
        cnt+=1

def moveright30():
    cnt=0
    while(cnt<=75):
        # if cnt%400==0:
        #     img=env.camera_feed()
        #     cv2.imshow("im",img)
        #     cv2.waitKey(1)
        p.stepSimulation()
        env.move_husky(vel,-vel,vel,-vel)
        cnt+=1

def moveright60():
    cnt=0
    while(cnt<=130):
        # if cnt%700==0:
        #     img=env.camera_feed()
        #     cv2.imshow("im",img)
        #     cv2.waitKey(1)
        p.stepSimulation()
        env.move_husky(vel,-vel,vel,-vel)
        cnt+=1

def moveleft():
    cnt=0
    while(cnt<=25):
        # if(cnt%200==0):
        #     img=env.camera_feed()
        #     cv2.imshow("im",img)
        #     cv2.waitKey(1)
        p.stepSimulation()
        env.move_husky(-vel,vel,-vel,vel)
        cnt+=1

def moveleft30():
    cnt=0
    while(cnt<=75):
        # if(cnt%400==0):
        #     img=env.camera_feed()
        #     cv2.imshow("im",img)
        #     cv2.waitKey(1)
        p.stepSimulation()
        env.move_husky(-vel,vel,-vel,vel)
        cnt+=1

def moveleft60():
    cnt=0
    while(cnt<=130):
        # if cnt%700==0:
        #     img=env.camera_feed()
        #     cv2.imshow("im",img)
        #     cv2.waitKey(1)
        p.stepSimulation()
        env.move_husky(-vel,vel,-vel,vel)
        cnt+=1

def adjust():
    cnt=0

    if(angle>0):
        a=7
    else:
        a=-7
    while(cnt<=10):
        # if(cnt%100==0):
        #     img=env.camera_feed()
        #     cv2.imshow("im",img)
        #     cv2.waitKey(1)
        p.stepSimulation()
        # if(cnt%2==0):
        #     env.move_husky(a,a,a,a)
        # else:
        env.move_husky(-a,a,-a,a)

        #env.move_husky(0,0,0,0)
        cnt+=1

def go(dest):
    while True:
        img=env.camera_feed()
        distance=dist(img,dest)
        #print(distance)
        if(distance==-1):
            print("adjust distance",angle)

            adjust()
            stop()
            continue
        if(distance<15.0):
            break
        corner=posdetect(img)
        if(len(corner)==0):
            print("adjust corner",angle)
            adjust()
            stop()
            continue
        move=movement(corner, dest)
        #print("move",move)
        if(move=="right"):
            moveright()
            stop()
        elif(move=="right30"):
            moveright30()
            stop()
        elif(move=="right60"):
            moveright60()
            stop()  
        elif(move=="left"):
            moveleft()
            stop()
        elif(move=="left30"):
            moveleft30()
            stop()
        elif(move=="left60"):
            moveleft60()
            stop()
        else:
            moveforward()
            stop()


if __name__=="__main__":
    env = gym.make("pixelate_arena-v0")

    env.remove_car()
    x=0
    img =env.camera_feed()
    # img=cv2.imread(r"C:\Users\jaiss\Downloads\Pixelate-22-Sample-Arena\media\sample_image.png")
    # img=cv2.resize(img,(720,720))
    # print(img.shape)
    #img=cv2.imread(r"C:\Users\jaiss\Downloads\tttt.jpeg")
    #cv2.imshow("begin",img)
    #cv2.imwrite(r"C:\Users\jaiss\Downloads\newnew.JPG",img)
    #cv2.waitKey(0)
    print(img.shape)
    fillcomat(img)
    fill_colmat(img)
    #print(colmat)
    # env.unlock_antidotes()
    # img =env.camera_feed()
    # cv2.imshow("begin",img)
    # cv2.waitKey(0)
    # fill_colmat(img)
    # print(colmat)

    fill_cosmat()  #will update later
    #print(cosmat)
    create_graph()
    

    # print(spider)
    # print(villain)

    env.respawn_car()
    begin=(6,6)
    p1=dijktras(begin,spider[0],cosmat)
    p2=dijktras(begin,spider[1],cosmat)
    sp=[]

    if(len(p1)<=len(p2)):
        sp.append(spider[0])
        sp.append(spider[1])
    else:
        sp.append(spider[1])
        sp.append(spider[0])
    for i in range(len(sp)):
        path=dijktras(begin,sp[i],cosmat)
        j=1
        print(i,len(path))
        while j<len(path):
            x=path[j][0]
            y=path[j][1]
           # print(x,y)
            go(co_mat[x][y])
            j=j+1
        begin=sp[i]
        print("Successfully met second spiderman")
    print("Succesfully met third spiderman")
    #env.remove_car()
    env.unlock_antidotes()
    img =env.camera_feed()
    #env.respawn_car()
    fill_colmat(img)
    colmat[6][6]=5
    #print(colmat)

    fill_cosmat() #update later
    #print(cosmat)

    # # create_graph()
    # # printgraph()

    
    
    pa[0]=[sand_anti[0],goblin_anti[0],electro_anti[0],sandman[0],goblin[0],electro[0]]
    pa[1]=[sand_anti[0],electro_anti[0],goblin_anti[0],sandman[0],electro[0],goblin[0]]
    pa[2]=[goblin_anti[0],sand_anti[0],electro_anti[0],goblin[0],sandman[0],electro[0]]
    pa[3]=[goblin_anti[0],electro_anti[0],sand_anti[0],goblin[0],electro[0],sandman[0]]
    pa[4]=[electro_anti[0],sand_anti[0],goblin_anti[0],electro[0],sandman[0],goblin[0]]
    pa[5]=[electro_anti[0],goblin_anti[0],sand_anti[0],electro[0],goblin[0],sandman[0]]

    # pa[6]=[s2,s1,sandman[0],goblin[0],electro[0],sand_anti[0],goblin_anti[0],electro_anti[0]]
    # pa[7]=[s2,s1,sandman[0],electro[0],goblin[0],sand_anti[0],electro_anti[0],goblin_anti[0]]
    # pa[8]=[s2,s1,goblin[0],sandman[0],electro[0],goblin_anti[0],sand_anti[0],electro_anti[0]]
    # pa[9]=[s2,s1,goblin[0],electro[0],sandman[0],goblin_anti[0],electro_anti[0],sand_anti[0]]
    # pa[10]=[s2,s1,electro[0],sandman[0],goblin[0],electro_anti[0],sand_anti[0],goblin_anti[0]]
    # pa[11]=[s2,s1,electro[0],goblin[0],sandman[0],electro_anti[0],goblin_anti[0],sand_anti[0]]
    
    # print(graph[3])
    # print(pa[0])
    
    minimum_path=[]
    minstep=10000
    for i in range(6):
        beg=begin
        tot=0
        for j in range(6):
            path=dijktras(beg,pa[i][j],cosmat)
            tot+=len(path)
            beg=pa[i][j]
        print(i,j,tot)
        if(tot<minstep):
            minstep=tot
            minimum_path=pa[i]
    print("min", minstep)
    #print(minimum_path)
    
    for i in range(len(minimum_path)):
        path=dijktras(begin,minimum_path[i],cosmat)
        j=1
        if(i==3):
            print("Successfully aquired all antidotes")
        while j<len(path):
            x=path[j][0]
            y=path[j][1]
            #print(x,y)
            go(co_mat[x][y])
            j=j+1
            begin=minimum_path[i]
        if(minimum_path[i]==sand_anti[0]):
            print("Sand Man AntiDote aquired")
        elif(minimum_path[i]==sandman[0]):
            print("Sand Man cured")
        elif(minimum_path[i]==goblin_anti[0]):
            print("Goblin AntiDote aquired")
        elif(minimum_path[i]==goblin[0]):
            print("Goblin cured")
        elif(minimum_path[i]==electro_anti[0]):
            print("Electro AntiDote aquired")
        elif(minimum_path[i]==electro[0]):
            print("Electro cured")    

    print("Successfully defeated villains")
    #print("--- %s seconds ---" % (time.time() - start_time))
    
    print("TASK COMPLETED IN",(time.time() - start_time),"SECONDS")
    print("-------------------------------------------")




