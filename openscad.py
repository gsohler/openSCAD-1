from numpy import *
import matplotlib.pyplot as plt
import time
from scipy.spatial import cKDTree
import pandas as pd


def arc(radius=0,start_angle=0,end_angle=0,cp=[0,0],s=20):
    '''
    function for calculating 2d arc
    'cp': center point of the arc
    's': number of segments in the arc
    refer file "example of various functions" for application example
    '''
    cp=array(cp)
    r=linspace(start_angle,end_angle,s+1)
    x=radius*cos(pi/180*r)
    y=radius*sin(pi/180*r)
    c=(cp+array([x,y]).swapaxes(0,1))
    return c.tolist()        

def pts(p):
    '''
    calculates the cumulative sum of 2d list of points 'p'
    e.g.
    pts([[0,0],[4,0],[2,3],[5,-8]]) will produce following output
    [[0, 0], [4, 0], [6, 3], [11, -5]]
    '''
    return array(p)[:,0:2].cumsum(axis=0).tolist()




def pts1(p):
    
    p=[[a[0],a[1],0] if len(a)==2 else a for a in p]
    b=array(p)[:,0:2].cumsum(axis=0)
    c=array([array(p)[:,2].tolist()])
    return concatenate((b,c.T),1).tolist()

def cw(p):
    '''
    function to identify whether the section is clockwise or counter clockwise. 
    cw(sec)==1 means clockwise and -1 means counterclockwise. 
    e.g.
    cw([[0,0],[4,0],[0,4],[-4,0]]) => -1
    '''
    p=array(p)[:,0:2]
    q=p[1:].tolist()+[p[0].tolist()]
    r=[p[len(p)-1].tolist()]+p[0:len(p)-1].tolist()
    a=array(q)-p
    b=p-array(r)
    c=where(cross(b,a)>0,1,0).sum()
    d=where(cross(b,a)<0,1,0).sum()
    e=1 if c<d else -1
    return e    

# def cwv(p):
#     p=sec
#     p0=[p[len(p)-1]]+p[:-1]
#     p1=p
#     p2=p[1:]+[p[0]]
#     p0,p1,p2=array([p0,p1,p2])
#     p=array([p0,p1,p2]).transpose(1,0,2).tolist()
#     return [cw(p1) for p1 in p]


def ang(x,y):
    '''
function to calculate angle of a 2d vector starting from origin and end point with x and y co-ordinates
 example:
 p1,p2=array([[3,4],[-3,2]])
 v=p2-p1
 ang= ang(v[0],v[1])
 
    '''
    if x>=0 and y>=0:
        return arctan(y/(0.000001 if x==0 else x))*180/pi
    elif x<0 and y>=0:
        return 180-abs(arctan(y/x))*180/pi
    elif  x<0 and y<0:
        return 180+abs(arctan(y/x))*180/pi
    else:
        return 360-abs(arctan(y/(0.000001 if x==0 else x)))*180/pi



def q(vector=[1,0,0],point=[0,5,0],theta=0):
    '''
    function to rotate a point around a vector(axis) with angle theta
    example:
    q(vector=[1,0,0],point=[0,5,0],theta=90)
    output: [0,0,5]
    '''

    t=theta
    v=vector/(linalg.norm(vector)+.00001)
    a=t/2*pi/180
    p=[cos(a),multiply(v,sin(a))]
    p1=[p[0],-p[1]]
    q=[0,[point[0],point[1],0] if len(point)==2 else point]
    pq=[p[0]*q[0]-p[1]@q[1],multiply(p[0],q[1])+p[1]*q[0]+cross(p[1],q[1])]
    pqp1=[pq[0]*p1[0]-pq[1]@p1[1],pq[0]*p1[1]+pq[1]*p1[0]+cross(pq[1],p1[1])]
    transformation=pqp1[1].tolist()
    return transformation

def uv(v):
    v=array(v)
    return (v/linalg.norm(v)).tolist()

def norm(v):
    return linalg.norm(v)

def fillet2d(pl,rl,s):
    p0=array(array(pl)[len(pl)-2:len(pl)].tolist()+array(pl)[0:len(pl)-2].tolist())
    p1=array([array(pl)[len(pl)-1].tolist()]+array(pl)[0:len(pl)-1].tolist())
    p2=array(pl)
    p3=array(array(pl)[1:len(pl)].tolist()+[array(pl)[0].tolist()])
    p4=array(array(pl)[2:len(pl)].tolist()+array(pl)[0:2].tolist())
    r0=array([array(rl)[len(rl)-1].tolist()]+array(rl)[0:len(rl)-1].tolist())
    r1=array(rl)
    r2=array(array(rl)[1:len(rl)].tolist()+[array(rl)[0].tolist()])
    u0=(p0-p1)/linalg.norm(p0-p1,axis=1).reshape(-1,1)
    u1=(p2-p1)/linalg.norm(p2-p1,axis=1).reshape(-1,1)
    u2=(p1-p2)/linalg.norm(p1-p2,axis=1).reshape(-1,1)
    u3=(p3-p2)/linalg.norm(p3-p2,axis=1).reshape(-1,1)
    u4=(p2-p3)/linalg.norm(p2-p3,axis=1).reshape(-1,1)
    u5=(p4-p3)/linalg.norm(p4-p3,axis=1).reshape(-1,1)
    theta0= (180-arccos(einsum('ij,ij->i',u0,u1))*180/pi)/2
    theta1= (180-arccos(einsum('ij,ij->i',u2,u3))*180/pi)/2
    theta2= (180-arccos(einsum('ij,ij->i',u4,u5))*180/pi)/2
    return f2d(p1,p2,p3,r0,r1,r2,theta0,theta1,theta2,u2,u3,s)
    


def each(a):
    c=[]
    for p in a:
        for p1 in p:
            c.append(p1)
    return c

def cr1(pl,s=20):
    pl1=array(pl)[:,0:2].tolist()
    rl=[0 if len(p)==2 else p[2] for p in pl]
    return fillet2d(pl1,rl,s)

def cr(pl,s=20):
    '''
    function to create section with corner radiuses. e.g. 
    following code has 3 points at [0,0],[10,0] and [7,15] and radiuses of 0.5,2 and 1 respectively,
    s=5 represent the number of segments at each corner radius.
    sec=cr(pl=[[0,0,.5],[10,0,2],[7,15,1]],s=5)
    
    refer file "example of various functions" for application
    '''
    sec=array(cr1(pl,s)).round(8)
    s1=sec[sort(unique(sec,axis=0,return_index=True)[1])].tolist()
    return s1

def cr_c(pl,s=20):
    sec=array(cr1(pl,s)).round(8)
    s1=sec[sort(unique(sec,axis=0,return_index=True)[1])].tolist()
    p0,p1=array([s1[len(s1)-1],s1[0]])
    v=p1-p0
    p=(p0+v*.999).tolist()
    
    return s1+[p]

def f2d(p1,p2,p3,r0,r1,r2,theta0,theta1,theta2,u2,u3,s):
    l1=linalg.norm(p1-p2,axis=1)
    l2=r0*tan(theta0*pi/180)+r1*tan(theta1*pi/180)
    l3=linalg.norm(p3-p2,axis=1)
    l4=r1*tan(theta1*pi/180)+r2*tan(theta2*pi/180)
    rf1=[r1[i] if l1[i]>l2[i] else 0 if l2[i]==0 else l1[i]/l2[i]*r1[i] for i in range(len(l1))]
    rf2=[r1[i] if l3[i]>l4[i] else 0 if l4[i]==0 else l3[i]/l4[i]*r1[i] for i in range(len(l3))]
    rf=swapaxes([rf1,rf2],0,1).min(axis=1)
    p=p2+u2*(rf*tan(theta1*pi/180)).reshape(-1,1)
    q=swapaxes([p1,p2,p3],0,1)
    r=[]
    for i in range(len(q)):
        r.append(cw(q[i]))
    r=array(r)
    n=r==-1
    n1=p-u2@array(rm(90))*rf.reshape(-1,1)
    n2=p-u2@array(rm(-90))*rf.reshape(-1,1)
    cp=[]
    for i in range(len(n)):
        if n[i]==True:
            cp.append(n1[i])
        else:
            cp.append(n2[i])

    cp=array(cp)
    a1=[]
#     alpha=(p-cp)/linalg.norm(p-cp,axis=1).reshape(-1,1)
    alpha=[ [0,0] if linalg.norm(p[i]-cp[i])==0 else (p[i]-cp[i])/linalg.norm(p[i]-cp[i]) for i in range(len(p))]
    for i in range(len(alpha)):
        a1.append(ang(alpha[i][0],alpha[i][1]))
    a1=array(a1)
    boo=[]
    for i in range(len(p1)):
        boo.append(cw([p1[i],p2[i],p3[i]]))
    boo=array(boo)   
    a2=where(boo==-1,a1+2*theta1,a1-2*theta1)
    ar=[]
    for i in range(len(rf)):
        ar.append(arc(rf[i],a1[i],a2[i],cp[i],s))
    ar=array(ar)
    c1=r1==0
    c2=linalg.norm(u2-u3,axis=1)<.2
    d=[]
    for i in range(len(c1)):
        if c1[i] or c2[i]:
            d.append([p2[i].tolist()])
        else:
            d.append(ar[i].tolist())
    return concatenate(d).tolist()


def flip(sec): 
    return sec[::-1]
    

def r_3p(p1,p2,p3):
    p4=add(p1,divide(subtract(p2,p1),2)).tolist()
    p5=add(p2,divide(subtract(p3,p2),2)).tolist()
    u1=uv(subtract(p2,p4))
    u2=uv(subtract(p3,p5))
    p6=add(p4,dot(u1,rm(90))).tolist()
    p7=add(p5,dot(u2,rm(90))).tolist()
    cp=i_p2d([p4,p6],[p5,p7])
    r=norm(subtract(p1,cp))
    return r


def max_r(sec):
    c=[]
    for i in range(len(sec)):
        i_2minus=len(sec)-2 if i==0 else len(sec)-1 if i==1 else i-2
        i_minus=len(sec)-1 if i==0 else i-1
        i_plus=i+1 if i<len(sec)-1 else 0
        i_2plus=i+2 if i<len(sec)-2 else 0 if i<len(sec)-1 else 1
        pi_2minus=sec[i_2minus]
        pi_minus=sec[i_minus]
        pi=sec[i]
        pi_plus=sec[i_plus]
        pi_2plus=sec[i_2plus]
        v1=subtract(pi_minus,pi_2minus)
        v2=subtract(pi,pi_minus)
        v3=subtract(pi_plus,pi)
        v4=subtract(pi_2plus,pi_plus)
        l1=norm(v1).round(3)
        l2=norm(v2).round(3)
        l3=norm(v3).round(3)
        l4=norm(v4).round(3)
        r1=r_3p([pi_2minus,pi_minus,pi]).round(3)
        r2=r_3p([pi_minus,pi,pi_plus]).round(3)
        r3=r_3p([pi,pi_plus,pi_2plus]).round(3)
        c.append(0 if l2!=l3 and (r1!=r2 or r2!=r3) else r2)
    return max(c)
        

def offset_l(l,d):
    u=uv(subtract(l[1],l[0]))
    p0=add(l[0],dot(u,multiply(d,rm(-90)))).tolist()
    p1=add(l[1],dot(u,multiply(d,rm(-90)))).tolist()
    return [p0,p1]

def seg(sec):
    c=[]
    for i in range(len(sec)):
        i_plus=i+1 if i<len(sec)-1 else 0
        p0=sec[i]
        p1=sec[i_plus]
        l=[p0,p1]
        c.append(l)
    return c

def offset_seg(sec,r):
    s=seg(sec)
    c=[]
    for p in s:
        c.append(offset_l(p,r))
    return c

def offset_segv(sec,d):
    s=sec
    s1=s[1:]+[s[0]]
    x=(array(s1)-array(s))
    y=linalg.norm(x,axis=1)
    u=x/y.reshape(-1,1)
    p0=array(s)+u@array(rm(-90))*d
    p1=array(s1)+u@array(rm(-90))*d
    return swapaxes([p0,p1],0,1).tolist()

def offset_points(sec,r):
    s=seg(sec)
    c=[]
    for p in s:
        c.append(offset_l(p,r)[0])
    return array(c).tolist()

def offset_pointsv(sec,r):
    return array(offset_segv(sec,r))[:,0].tolist()

def offset_seg_cw(sec,r):
    c=[]
    for i in range(len(sec)):
        i_minus=len(sec)-1 if i==0 else i-1
        i_plus=i+1 if i<len(sec)-1 else 0
        p0=sec[i_minus]
        p1=sec[i]
        p2=sec[i_plus]
        clock=cw([p0,p1,p2])
        if clock==1:
            c.append(offset_l([p1,p2],r))
    d=[]
    for a in c:
        for b in a:
            d.append(b)
    return d

def lim(t,s,e):
    return t>=s and t<=e

def remove_extra_points(points_list):
    return array(points_list)[sort(unique(points_list,axis=0,return_index=True)[1])].tolist()

def convert_secv(sec,d):
    pi_2minus=sec[-2:]+sec[:-2]
    pi_minus=[sec[-1]]+sec[:-1]
    p_i=sec
    pi_plus=sec[1:]+[sec[0]]
    pi_2plus=sec[2:]+sec[:2]

    v1=array(pi_minus)-array(pi_2minus)
    v2=array(p_i)-array(pi_minus)
    v3=array(pi_plus)-array(p_i)
    v4=array(pi_2plus)-array(pi_plus)

    l1=linalg.norm(v1,axis=1).round(3)
    l2=linalg.norm(v2,axis=1).round(3)
    l3=linalg.norm(v3,axis=1).round(3)
    l4=linalg.norm(v4,axis=1).round(3)

    p4=array(pi_2minus)+(array(pi_minus)-array(pi_2minus))/2
    p5=array(pi_minus)+(array(p_i)-array(pi_minus))/2

    u1=(array(pi_minus)-p4)/linalg.norm(array(pi_minus)-p4,axis=1).reshape(-1,1)
    u2=(array(p_i)-p5)/linalg.norm(array(p_i)-p5).reshape(-1,1)

    v5=array(pi_minus)-p4
    v6=(v5/linalg.norm(v5,axis=1).reshape(-1,1))
    r1=r_3pv(array(pi_2minus),array(pi_minus),array(p_i)).round(3)
    r2=r_3pv(array(pi_minus),array(p_i),array(pi_plus)).round(3)
    r3=r_3pv(array(p_i),array(pi_plus),array(pi_2plus)).round(3)
    r=where((l2!=l3) & ((r1!=r2) | (r2!=r3)),0,r2)
    arr=swapaxes([pi_minus,p_i,pi_plus],0,1)
    clock=array(list(map(cw,arr)))
    c1=where(r==0,True,False)
    c2=where(r>=d,True,False)
    c3=where(clock==1,True,False)
    p=array(sec)[c1 | c2 | c3].round(6)
    p=p[sort(unique(p,axis=0,return_index=True)[1])]
    p1=cKDTree(array(sec)).query(p)[1].tolist()
    p2=[p1[len(p1)-1]]+p1[0:len(p1)-1]
    p3=p1[1:len(p1)]+[p1[0]]
    p4=p1[2:len(p1)]+p1[0:2]
    a=i_p2dv(array(sec)[p2],array(sec)[p1],array(sec)[p3],array(sec)[p4])
    b=array(sec)[p1]
    c=array(p3)-array(p1)>1
    d=[]
    for i in range(len(c)):
        if c[i]==True:
            d.append(a[i].tolist())
        else:
            d.append(b[i].tolist())
    d_minus=[d[len(d)-1]]+d[0:len(d)-1]
    d_plus=d[1:len(d)]+[d[0]]
    va=array(d)-array(d_minus)
    vb=array(d_plus)-array(d_minus)
    normva=1/linalg.norm(va,axis=1)
    normvb=1/linalg.norm(vb,axis=1)
    ua=einsum('ij,i->ij',va,normva)
    ub=einsum('ij,i->ij',vb,normvb)
    return array(d)[(ua!=ub).all(axis=1)].tolist()           


def convert_secv1(sec,d):
    pi_2minus=sec[-2:]+sec[:-2]
    pi_minus=[sec[-1]]+sec[:-1]
    p_i=sec
    pi_plus=sec[1:]+[sec[0]]
    pi_2plus=sec[2:]+sec[:2]

    v1=array(pi_minus)-array(pi_2minus)
    v2=array(p_i)-array(pi_minus)
    v3=array(pi_plus)-array(p_i)
    v4=array(pi_2plus)-array(pi_plus)

    l1=linalg.norm(v1,axis=1).round(3)
    l2=linalg.norm(v2,axis=1).round(3)
    l3=linalg.norm(v3,axis=1).round(3)
    l4=linalg.norm(v4,axis=1).round(3)

    p4=array(pi_2minus)+(array(pi_minus)-array(pi_2minus))/2
    p5=array(pi_minus)+(array(p_i)-array(pi_minus))/2

    u1=(array(pi_minus)-p4)/linalg.norm(array(pi_minus)-p4,axis=1).reshape(-1,1)
    u2=(array(p_i)-p5)/linalg.norm(array(p_i)-p5).reshape(-1,1)

    v5=array(pi_minus)-p4
    v6=(v5/linalg.norm(v5,axis=1).reshape(-1,1))
    r1=r_3pv(array(pi_2minus),array(pi_minus),array(p_i)).round(3)
    r2=r_3pv(array(pi_minus),array(p_i),array(pi_plus)).round(3)
    r3=r_3pv(array(p_i),array(pi_plus),array(pi_2plus)).round(3)
    r=where((l2!=l3) & ((r1!=r2) | (r2!=r3)),0,r2)
    arr=swapaxes([pi_minus,p_i,pi_plus],0,1)
    clock=array(list(map(cw,arr)))
    c1=where(r==0,True,False)
    c2=where(r>=d,True,False)
    c3=where(clock==-1,True,False)
    p=array(sec)[c1 | c2 | c3]
    p1=cKDTree(array(sec)).query(p)[1].tolist()
    p2=[p1[len(p1)-1]]+p1[0:len(p1)-1]
    p3=p1[1:len(p1)]+[p1[0]]
    p4=p1[2:len(p1)]+p1[0:2]
    a=i_p2dv(array(sec)[p2],array(sec)[p1],array(sec)[p3],array(sec)[p4])
    b=array(sec)[p1]
    c=array(p3)-array(p1)>1
    d=[]
    for i in range(len(c)):
        if c[i]==True:
            d.append(a[i].tolist())
        else:
            d.append(b[i].tolist())
    d_minus=[d[len(d)-1]]+d[0:len(d)-1]
    d_plus=d[1:len(d)]+[d[0]]
    va=array(d)-array(d_minus)
    vb=array(d_plus)-array(d_minus)
    normva=1/linalg.norm(va,axis=1)
    normvb=1/linalg.norm(vb,axis=1)
    ua=einsum('ij,i->ij',va,normva)
    ub=einsum('ij,i->ij',vb,normvb)
    return array(d)[(ua!=ub).all(axis=1)].tolist()           


def list_r(sec):
    pi_2minus=sec[-2:]+sec[:-2]
    pi_minus=[sec[-1]]+sec[:-1]
    p_i=sec
    pi_plus=sec[1:]+[sec[0]]
    pi_2plus=sec[2:]+sec[:2]

    v1=array(pi_minus)-array(pi_2minus)
    v2=array(p_i)-array(pi_minus)
    v3=array(pi_plus)-array(p_i)
    v4=array(pi_2plus)-array(pi_plus)

    l1=linalg.norm(v1,axis=1).round(3)
    l2=linalg.norm(v2,axis=1).round(3)
    l3=linalg.norm(v3,axis=1).round(3)
    l4=linalg.norm(v4,axis=1).round(3)

    p4=array(pi_2minus)+(array(pi_minus)-array(pi_2minus))/2
    p5=array(pi_minus)+(array(p_i)-array(pi_minus))/2

    u1=(array(pi_minus)-p4)/linalg.norm(array(pi_minus)-p4,axis=1).reshape(-1,1)
    u2=(array(p_i)-p5)/linalg.norm(array(p_i)-p5).reshape(-1,1)

    v5=array(pi_minus)-p4
    v6=(v5/linalg.norm(v5,axis=1).reshape(-1,1))
    r1=r_3pv(array(pi_2minus),array(pi_minus),array(p_i)).round(3)
    r2=r_3pv(array(pi_minus),array(p_i),array(pi_plus)).round(3)
    r3=r_3pv(array(p_i),array(pi_plus),array(pi_2plus)).round(3)
    r=where((l2!=l3) & ((r1!=r2) | (r2!=r3)),0,r2)
    return r

def list_ra(sec):
    pi_2minus=sec[-2:]+sec[:-2]
    pi_minus=[sec[-1]]+sec[:-1]
    p_i=sec
    pi_plus=sec[1:]+[sec[0]]
    pi_2plus=sec[2:]+sec[:2]

    v1=array(pi_minus)-array(pi_2minus)
    v2=array(p_i)-array(pi_minus)
    v3=array(pi_plus)-array(p_i)
    v4=array(pi_2plus)-array(pi_plus)

    l1=linalg.norm(v1,axis=1).round(3)
    l2=linalg.norm(v2,axis=1).round(3)
    l3=linalg.norm(v3,axis=1).round(3)
    l4=linalg.norm(v4,axis=1).round(3)

    p4=array(pi_2minus)+(array(pi_minus)-array(pi_2minus))/2
    p5=array(pi_minus)+(array(p_i)-array(pi_minus))/2

    u1=(array(pi_minus)-p4)/linalg.norm(array(pi_minus)-p4,axis=1).reshape(-1,1)
    u2=(array(p_i)-p5)/linalg.norm(array(p_i)-p5).reshape(-1,1)

    v5=array(pi_minus)-p4
    v6=(v5/linalg.norm(v5,axis=1).reshape(-1,1))
    r1=r_3pv(array(pi_2minus),array(pi_minus),array(p_i)).round(3)
    r2=r_3pv(array(pi_minus),array(p_i),array(pi_plus)).round(3)
    r3=r_3pv(array(p_i),array(pi_plus),array(pi_2plus)).round(3)
    r=where((l2!=l3) & ((r1!=r2) | (r2!=r3)),0,r2)
    return r2




def rnd_v(v,n):
    b=[]
    for i in v:
        b.append(round(i,n))
    return b

def i_m2d(m):
    return linalg.pinv(transpose(m)).tolist()

def rm(theta):
    '''
    function to rotate a vector by "theta" degrees e.g. try following code:
    line=[[0,0],[5,3]]
    line1=array(line)@rm(30)
    line1=line1.tolist()

    refer file "examples of various functions" for application
    '''
    pi=3.141592653589793
    return [[cos(theta * pi/180),sin(theta * pi/180)],[-sin(theta * pi/180),cos(theta * pi/180)]]

def max_rv(sec):
    pi_2minus=sec[-2:]+sec[:-2]
    pi_minus=[sec[-1]]+sec[:-1]
    p_i=sec
    pi_plus=sec[1:]+[sec[0]]
    pi_2plus=sec[2:]+sec[:2]

    v1=array(pi_minus)-array(pi_2minus)
    v2=array(p_i)-array(pi_minus)
    v3=array(pi_plus)-array(p_i)
    v4=array(pi_2plus)-array(pi_plus)

    l1=linalg.norm(v1,axis=1).round(3)
    l2=linalg.norm(v2,axis=1).round(3)
    l3=linalg.norm(v3,axis=1).round(3)
    l4=linalg.norm(v4,axis=1).round(3)

    p4=array(pi_2minus)+(array(pi_minus)-array(pi_2minus))/2
    p5=array(pi_minus)+(array(p_i)-array(pi_minus))/2

    u1=(array(pi_minus)-p4)/linalg.norm(array(pi_minus)-p4,axis=1).reshape(-1,1)
    u2=(array(p_i)-p5)/linalg.norm(array(p_i)-p5).reshape(-1,1)

    v5=array(pi_minus)-p4
    v6=(v5/linalg.norm(v5,axis=1).reshape(-1,1))
    r1=r_3pv(array(pi_2minus),array(pi_minus),array(p_i)).round(3)
    r2=r_3pv(array(pi_minus),array(p_i),array(pi_plus)).round(3)
    r3=r_3pv(array(p_i),array(pi_plus),array(pi_2plus)).round(3)
    return max(where((l2!=l3) & ((r1!=r2) | (r2!=r3)),0,r2))

def r_3p(p):
    p4=add(p[0],divide(subtract(p[1],p[0]),2)).tolist()
    p5=add(p[1],divide(subtract(p[2],p[1]),2)).tolist()
    u1=uv(subtract(p[1],p4))
    u2=uv(subtract(p[2],p5))
    p6=add(p4,dot(u1,rm(90))).tolist()
    p7=add(p5,dot(u2,rm(90))).tolist()
    cp=i_p2d([p4,p6],[p5,p7])
    r=norm(subtract(p[0],cp))
    return r


def i_p2d(l1,l2):
    '''
    function to calculate the intersection point between 2 lines in 2d space
    e.g. i_p2d(l1=[[0,0],[1,4]],l2=[[10,0],[7,2]]) =>  [1.42857, 5.71429]
    '''
    p0,p1,p2,p3=l1[0],l1[1],l2[0],l2[1]
    p0,p1,p2,p3=array([p0,p1,p2,p3])
    v1=p1-p0
    v2=p3-p2
    im=linalg.pinv(array([v1,-v2]).T)
    t1=(im@(p2-p0))[0]
    ip=p0+v1*t1
    
    return ip.tolist()


def offset_seg_cwv(sec,r):
    pi_minus=[sec[-1]]+sec[:-1]
    p_i=sec
    pi_plus=sec[1:]+[sec[0]]
    c=array(list(map(cw,swapaxes([pi_minus,p_i,pi_plus],0,1))))
    return array(offset_segv(sec,r))[c==1].reshape(-1,2)                    
            


def s_intv(s):
    c=[]
    for i in range(len(s)):
        p0=array([s[i]]*len(s))[:,0]
        p1=array([s[i]]*len(s))[:,1]
        v1=p1-p0
        p2=array(s)[:,0]
        p3=array(s)[:,1]
        v2=p3-p2
        m=swapaxes([swapaxes([v1.T[0],-v2.T[0]],0,1),swapaxes([v1.T[1],-v2.T[1]],0,1)],0,1)
        n=m[where(linalg.det(m)!=0)]
        pa=p0[where(linalg.det(m)!=0)]
        pb=p2[where(linalg.det(m)!=0)]
        v=v1[where(linalg.det(m)!=0)]
        A=linalg.inv(n)
        B=pb-pa
        def mul(a,b):
            return a@b
        t=einsum('ijk,ik->ij',A,B)[:,0].round(4)
        u=einsum('ijk,ik->ij',A,B)[:,1].round(4)
        t1=where(t>=0,where(t<=1,True,False),False)
        u1=where(u>=0,where(u<=1,True,False),False)
        d=(pa+v*t.reshape(-1,1))[where(t1&u1==True)].tolist()
        if d!=[]:
            c=c+d
    return c

def s_intv1(s):
    c=[]
    for i in range(len(s)):
        p0=array([s[i]]*len(s))[:,0]
        p1=array([s[i]]*len(s))[:,1]
        v1=p1-p0
        p2=array(s)[:,0]
        p3=array(s)[:,1]
        v2=p3-p2
        m=swapaxes([swapaxes([v1.T[0],-v2.T[0]],0,1),swapaxes([v1.T[1],-v2.T[1]],0,1)],0,1)
        n=m[where(linalg.det(m)!=0)]
        pa=p0[where(linalg.det(m)!=0)]
        pb=p2[where(linalg.det(m)!=0)]
        v=v1[where(linalg.det(m)!=0)]
        A=linalg.inv(n)
        B=pb-pa
        def mul(a,b):
            return a@b
        t=einsum('ijk,ik->ij',A,B)[:,0].round(4)
        u=einsum('ijk,ik->ij',A,B)[:,1].round(4)
        t1=where(t>0,where(t<1,True,False),False)
        u1=where(u>0,where(u<1,True,False),False)
        d=(pa+v*t.reshape(-1,1))[where(t1&u1==True)].tolist()
        if d!=[]:
            c=c+d
    return c


def r_3pv(p1,p2,p3):
    p4=p1+(p2-p1)/2
    p5=p2+(p3-p2)/2
    u1=(p2-p4)/linalg.norm(p2-p4,axis=1).reshape(-1,1)
    u2=(p3-p5)/linalg.norm(p3-p5,axis=1).reshape(-1,1)
    p6=p4+u1@array([[0,1],[-1,0]])
    p7=p5+u2@array([[0,1],[-1,0]])
    cp=i_p2dv(p4,p6,p5,p7)
    r=linalg.norm(p1-cp,axis=1)
    return r

def i_p2dv(p0,p1,p2,p3):
    v1=p1-p0
    v2=p3-p2
    a=linalg.pinv(swapaxes(transpose(array([v1,-v2])),0,1))
    b=p2-p0
    t=einsum('ijk,ik->ij',a,b)[:,0]
    return p0+einsum('ij,i->ij',v1,t)

def sort_points(sec,list):
    if list!=[]:
        b=[]
        for p in sec:
            a=[]
            for i in range(len(list)):
                a.append(norm(subtract(list[i],p)))
            for i,x in enumerate(a):
                if x==min(a):
                    b.append(list[i])
            
        return b
            
def sort_pointsv(sec,sec1):
    a=array(sec)
    b=array(sec1)
    c=[]
    for p in a:
        d=linalg.norm(b-p,axis=1)
        c.append(b[where(d==min(d))][0])
    return array(c).tolist()



def m_points(sec,sl=20):# multiple points within straight lines of a closed section 'sec' with equal segment length 'sl' in the straight line segments
    p0=array(sec)
    p1=array(sec)[1:].tolist()+[sec[0]]
    lnth=linalg.norm(array(p1)-array(p0),axis=1)
    sec1=concatenate([array(l([p0[i],p1[i]],lnth[i]/sl)) if lnth[i]>=sl*2 else [p0[i]] for i in range(len(p0))])
    return sec1.tolist()

def m_points_o(sec,sl=20):# multiple points within straight lines of an open section 'sec' with equal segment length 'sl' in the straight line segments
    p0=array(sec)
    p1=array(sec)[1:].tolist()+[sec[0]]
    lnth=linalg.norm(array(p1)-array(p0),axis=1)
    sec1=concatenate([array(l([p0[i],p1[i]],lnth[i]/sl)) if lnth[i]>=sl*2 else [p0[i]] for i in range(len(p0)-1)])
    return sec1.tolist()


def l(l,s=20):# line 'l' with number of segments 's'
    p0,p1=array(l[0]),array(l[1])
    v=p1-p0
    u=[v/linalg.norm(v)]
    length=linalg.norm(v)
    r=arange(0,length,length/s)
    return (p0+einsum('ij,k->kj',u,r)).tolist()

def l_len(l):# length of a line 'l'
    p0,p1=array(l[0]),array(l[1])
    v=p1-p0
    u=[v/(linalg.norm(v)+.00001)]
    length=linalg.norm(v)
    return length.tolist()

def arc_2p(p1,p2,r,cw=1,s=20):#arc with 2 points 'p1,p2' with radius 'r' and with orientation clockwise (1) or counterclock wise(-1)
    p1,p2=array([p1,p2])
    p3=p1+(p2-p1)/2
    d=linalg.norm(p3-p1)
    l=sqrt(abs(r**2-d**2))
    v=p1-p3
    u=v/linalg.norm(v)
    cp=p3+(u*l)@rm(-90 if cw==-1 else 90)
    v1,v2=p1-cp,p2-cp
    a1,a2=ang(v1[0],v1[1]),ang(v2[0],v2[1])
    a3= (a2+360 if a2<a1 else a2) if cw==-1 else (a2 if a2<a1 else a2-360)
    return arc(r,a1,a3,cp,s)

def arc_long_2p(p1,p2,r,cw=1,s=20):#long arc with 2 points 'p1,p2' with radius 'r' and with orientation clockwise (1) or counterclock wise(-1)
    p1,p2=array([p1,p2])
    p3=p1+(p2-p1)/2
    d=linalg.norm(p3-p1)
    l=sqrt(abs(r**2-d**2))
    v=p1-p3
    u=v/linalg.norm(v)
    cp=p3+(u*l)@rm(90 if cw==-1 else -90)
    v1,v2=p1-cp,p2-cp
    a1,a2=ang(v1[0],v1[1]),ang(v2[0],v2[1])
    a3=(a2+360 if a2<a1 else a2) if cw==-1 else (a2 if a2<a1 else a2-360)
    return arc(r,a1,a3,cp,s)

def arc_2p_cp(p1,p2,r,cw=-1):# center point of an arc with 2 points 'p1,p2' with radius 'r' and with orientation clockwise (1) or counterclock wise(-1)
    p1,p2=array([p1,p2])
    p3=p1+(p2-p1)/2
    d=linalg.norm(p3-p1)
    l=sqrt(abs(r**2-d**2))
    v=p1-p3
    u=v/linalg.norm(v)
    cp=p3+(u*l)@rm(-90 if cw==-1 else 90)
    return cp

def offset(sec,r):# offset for a section 'sec' by amount 'r'
#     return io(sec,r) if r<0 else sec if r==0 else oo_convex(sec,r) if convex(sec)==True else outer_offset(sec,r)
    return inner_offset(sec,r) if r<0 else sec if r==0 else oo_convex(sec,r) if convex(sec)==True else out_offset(sec,r)


def prism(sec,path):
    '''
function to make a prism with combination of 2d section and 2d path
Example:
sec=circle(10)
path=cr(pts1([[2,0],[-2,0,2],[0,10,3],[-3,0]]),5)
prism=prism(sec,path)

    '''
    s1=flip(sec) if cw(sec)==1 else sec
    return [array(trns([0,0,y],offset(s1,round(x,3)))).tolist() for (x,y) in path]

def trns(p,sec):#translates a prism or section by [x,y,z] distance
    '''
    function to translate a group of points "sec" by "p" distance defined in [x,y,z].e.g. try following code:
    sec=cr([[0,0,.5],[10,0,2],[7,15,1]],5)
    sec1=trns(p=[2,5,3],sec=sec)
    
    refer to file "example of various functions " for application
    '''
    return [ (array([p1[0],p1[1],0])+array(p)).tolist() if len(p1)==2 else (array(p1)+array(p)).tolist() for p1 in sec]

def prism1(sec,path,n):
        a=m_points(sec,n)
        return [ trns([0,0,y], array(m_points(offset(sec,x),n))[cKDTree(m_points(offset(sec,x),n)).query(a)[1]]) for (x,y) in path ]

def offset_points_cw(sec,r):
    s=seg(sec)
    c=[]
    for i in range(len(sec)):
        i_minus=len(sec)-1 if i==0 else i-1
        i_plus=i+1 if i<len(sec)-1 else 0
        p0=sec[i_minus]
        p1=sec[i]
        p2=sec[i_plus]
        if cw([p0,p1,p2])==1:
            c.append(offset_l([p1,p2],r)[0])
    return c


def cytz(path):# converts 'y' points to 'z' points in a 2d list of points
    '''
    function to convert the y co-ordinates to z co-ordinates e.g.[x,y]=>[x,0,y]. 2d to 3d coordinate system
    '''
    return [[p[0],0,p[1]] for p in path]

def surf_extrude(sec,path):# extrudes an open section 'sec' to a 'path' to create surface
    '''
    function to make surface with a polyline 2d sketch and a 3d path
    (there is no render here but points can be visualised with following command:
    for(p=surf_extrude(sec,path))points(p,.2);)
    example:
    sec2=cr(pts1([[-25,0],[10,5,5],[10,-3,10],[10,5,5],[10,-8,7],[10,1]]),10)  
    path2=cytz(cr(pts1([[-35,5,0],[10,8,20],[20,-5,10],[20,8,20],[10,-9,20],[10,1,0]]),10))
    surf2=surf_extrude(sec2,path2)
    
    refer file "example of various functions"
    '''
    p0=path
    p1=p0[1:]+[p0[0]]
    p0,p1=array(p0),array(p1)
    v=p1-p0
    a1=vectorize(ang)(v[:,0],v[:,1])
    b=sqrt(v[:,0]**2+v[:,1]**2)
    a2=vectorize(ang)(b,v[:,2])
    c=[]
    for i in range(len(path)-1):
        sec1=trns(p0[i],q_rot(['x90','z-90',f'y{-a2[i]}',f'z{a1[i]}'],sec))
        sec2=trns(p1[i],q_rot(['x90','z-90',f'y{-a2[i]}',f'z{a1[i]}'],sec))
        if i<len(path)-2:
            c.append([sec1])
        else:
            c.append([sec1,sec2])
    return concatenate(c).tolist()

def cpo(prism): # changes the orientation of points of a prism
    return swapaxes(array(prism),0,1).tolist()

def c2t3(p):# converts 2d list to 3d
    if len(array(p).shape)>2:
        return [trns([0,0,0],p) for p in p]
    else:
        return trns([0,0,0],p)

def c3t2(a): # converts 3d list to 2d list 
    '''
    function to convert 3d to 2d, it just removes the z-coordinate from the points list 
    example:
    list=c3t2([[1,2,3],[3,4,5],[6,7,8]])
    output=> [[1, 2], [3, 4], [6, 7]]
    '''
    if len(array(a).shape)==3:
        return array([ swapaxes([p[:,0],p[:,1]],0,1) for p in array(a)]).tolist()
    else:
        p=array(a)
        return swapaxes([p[:,0],p[:,1]],0,1).tolist()

def nv(p):# normal vector to the plane 'p' with atleast 3 known points
    p0,p1,p2=array(trns([0,0,0],[p[0],p[1],p[2]]))
    nv=cross(p0-p1,p2-p1)
    m=1/linalg.norm(nv) if linalg.norm(nv)>0 else 1e5
    return (nv*m).tolist()

def fillet_3p_3d(p0,p1,p2,r,s):# fillet with 3 known points 'p0,p1,p2' in 3d space. 'r' is the radius of fillet and 's' is the number of segments in the fillet
    p0,p1,p2=array(trns([0,0,0],[p0,p1,p2]))
    n=array(nv([p0,p1,p2]))
    u1=(p0-p1)/(linalg.norm(p0-p1)+.00001)
    u2=(p2-p1)/(linalg.norm(p2-p1)+.00001)
    theta=(180-arccos(u1@u2)*180/pi)/2
    alpha=arccos(u1@u2)*180/pi
    l=r*tan(theta*pi/180)
    cp=p1+q(n,u1*r/cos(theta*pi/180),alpha/2)
    pa=p1+u1*l
    arc=[ cp+q(n,pa-cp,-i) for i in linspace(0,theta*2,s)]
    a,b,c=arc[0],arc[1:s-1],arc[s-1]
    return concatenate([[p1],arc]).tolist()

def fillet_3p_3d_cp(p0,p1,p2,r):# center point 'cp' of the fillet with 3 known points 'p0,p1,p2' in 3d space. 'r' is the radius of fillet
    p0,p1,p2=array(trns([0,0,0],[p0,p1,p2]))
    n=array(nv([p0,p1,p2]))
    u1=(p0-p1)/(linalg.norm(p0-p1)+.00001)
    u2=(p2-p1)/(linalg.norm(p2-p1)+.00001)
    theta=(180-arccos(u1@u2)*180/pi)/2
    alpha=arccos(u1@u2)*180/pi
    l=r*tan(theta*pi/180)
    cp=p1+q(n,u1*r/cos(theta*pi/180),alpha/2)
    return cp.tolist()

def i_p3d(l1,l2): # intersection point between 2 lines 'l1' and 'l2' in 3d space where both the lines are in the same plane
    '''
    function to calculate intersection point between 2 lines in 3d space 
    (only if these lines lie on the same plane)
    function is similar to i_p2d
    '''
    l1,l2=array(l1),array(l2)
    v1=l1[1]-l1[0]
    v2=l2[1]-l2[0]
    u1=v1/(linalg.norm(v1)+.00001)
    u2=v2/(linalg.norm(v2)+.00001)
    v3=l2[0]-l1[0]
    t1= (linalg.pinv(array([v1,-v2,[1,1,1]]).T)@array(v3))[0]
    ip=l1[0]+v1*t1
    return ip.tolist()

def arc_3p_3d(points,s): # arc with 3 known list of 'points' in 3d space where 's' is the number of segments in the arc
    points=array(points)
    v1=points[0]-points[1]
    v2=points[2]-points[1]
    u1=v1/linalg.norm(v1)
    u2=v2/linalg.norm(v2)
    n=cross(u1,u2)
    alpha=arccos(u1@u2)*180/pi
    pa=v1/2
    pb=v2/2
    pap=pa+q(n,u1,90)
    pbp=pb+q(n,u2,-90)
    l1=[pa,pap]
    l2=[pb,pbp]
    cp=i_p3d(l1,l2)
    v3=points[0]-(points[1]+cp)
    u3=v3/linalg.norm(v3)
    v4=points[2]-(points[1]+cp)
    u4=v4/linalg.norm(v4)
    theta= 360-arccos(u3@u4)*180/pi if alpha<90 else arccos(u3@u4)*180/pi
    radius=linalg.norm(pa-cp)
    arc=trns(points[1]+cp,[ q(n,points[0]-(points[1]+cp),-i)  for i in linspace(0,theta,s) ])
    return array(arc).tolist()

def r_3p_3d(points):# radius of the circle with 3 known list of 'points' in 3d space
    points=array(points)
    v1=points[0]-points[1]
    v2=points[2]-points[1]
    u1=v1/(linalg.norm(v1)+.00001)
    u2=v2/(linalg.norm(v2)+.00001)
    n=cross(u1,u2)
    alpha=arccos(u1@u2)*180/pi
    pa=v1/2
    pb=v2/2
    pap=pa+q(n,u1,90)
    pbp=pb+q(n,u2,-90)
    l1=[pa,pap]
    l2=[pb,pbp]
    cp=i_p3d(l1,l2)
    v3=points[0]-(points[1]+cp)
    u3=v3/(linalg.norm(v3)+.00001)
    v4=points[2]-(points[1]+cp)
    u4=v4/(linalg.norm(v4)+.00001)
    theta= 360-arccos(u3@u4)*180/pi if alpha<90 else arccos(u3@u4)*180/pi
    radius=linalg.norm(pa-cp)
    return radius

def cir_3p_3d(points,s):#circle with 3 known list of 'points' in 3d space where 's' is the number of segments in the circle 
    points=array(points)
    v1=points[0]-points[1]
    v2=points[2]-points[1]
    u1=v1/linalg.norm(v1)
    u2=v2/linalg.norm(v2)
    n=cross(u1,u2)
    alpha=arccos(u1@u2)*180/pi
    pa=v1/2
    pb=v2/2
    pap=pa+q(n,u1,90)
    pbp=pb+q(n,u2,-90)
    l1=[pa,pap]
    l2=[pb,pbp]
    cp=i_p3d(l1,l2)
    v3=points[0]-(points[1]+cp)
    u3=v3/linalg.norm(v3)
    v4=points[2]-(points[1]+cp)
    u4=v4/linalg.norm(v4)
    theta= 360-arccos(u3@u4)*180/pi if alpha<90 else arccos(u3@u4)*180/pi
    radius=linalg.norm(pa-cp)
    arc=trns(points[1]+cp,[ q(n,points[0]-(points[1]+cp),-i)  for i in linspace(0,360,s) ])
    return array(arc).tolist()

def scl2d(sec,sl):# scale the 2d section 'sec' by a scaling factor 'sl'. this places the scaled section in the bottom center of the original section
    '''
    function to scale a 2d section by an amount "sl" which has to be >0 (keeps the y-coordinates same). 
    e.g.following code scales the section by 0.7 (70% of the original shape)
    sec=cr([[0,0,.5],[10,0,2],[7,15,1]],5)
    sec1=scl2d(sec,.7)
    
    refer file "example of various functions" for application
    '''
    s1=array(trns([0,0,0],sec))
    cp=array(s1).mean(axis=0)
    rev=array(s1).mean(axis=0)+(array(s1)-array(s1).mean(axis=0))*sl
    y1=cp-array([0,array(s1)[:,1].min(),0])
    y2=cp-array([0,rev[:,1].min(),0])
    d=y2-y1
    return c3t2(trns(d,rev))

def scl2d_c(sec,sl):# scale the 2d section 'sec' with scaling factor 'sl'. this places the scaled section in the center of original section or the center of both original and scaled section remains the same.
    '''
    function to scale a 2d section by an amount "sl" which has to be >0 (keeps the revised section in center). 
    e.g.following code scales the section by 0.7 (70% of the original shape)
    sec=cr([[0,0,.5],[10,0,2],[7,15,1]],5)
    sec1=scl2d_c(sec,.7)
    
    refer file "example of various functions" for application
    '''
    s1=array(trns([0,0,0],sec))
    cp=array(s1).mean(axis=0)
    rev=array(s1).mean(axis=0)+(array(s1)-array(s1).mean(axis=0))*sl
    return c3t2(rev)

def scl3d(p,s):# scale 3d prism 'p' with scaling factor 's'. This places the scaled prism at the same bottom of the original prism
    '''
    function to scale a 3d prism keeping the base z-coordinate same. 
    takes 2 arguments "p" to scale and the scaling factor "s". 
    scale factor can take any real number negative values will scale the prism and turn the prism upside down.
    try the following code to understand better:
    sec=circle(10);
    path=cr(pts1([[2,0],[-2,0,2],[0,10,3],[-3,0]]),5)
    sol=prism(sec,path)
    sol1=scl3d(sol,.7)

    refer file "example of various functions" for application
    '''
    p=array(p)
    cp=p.reshape(-1,3).mean(axis=0)
    rev=cp+(p-cp)*s
    z1=p.reshape(-1,3)[:,2].min()
    z2=rev.reshape(-1,3)[:,2].min()
    d=z1-z2
    return trns([0,0,d],rev)

def scl3dc(p,s):# scale a 3d prism 'p' with scaling factor 's'. This places the scaled prism in the center of the original prism or the center of both the prism is same
    '''
     function to scale a 3d prism keeping the prism centered. takes 2 arguments "p" to scale and 
     the scaling factor "s". 
     scale factor can take any real number negative values will scale the prism and turn the prism upside down.
     try the following code to understand better:
     sec=circle(10)
     path=cr(pts1([[2,0],[-2,0,2],[0,10,3],[-3,0]]),5)
     sol=prism(sec,path)
     sol1=scl3dc(p,.7)
     
    refer file "example of various functions" for application
    '''
    p=array(p)
    cp=p.reshape(-1,3).mean(axis=0)
    rev=cp+(p-cp)*s
    return rev.tolist()


def io(sec,r):# used for inner offset in offset function
    if r<0:
        s=flip(sec) if cw(sec)==1 else sec
        s1=s
#         s1=convert_secv(s,max_r(s)+1 if abs(r)>=max_r(s) else abs(r))
        s2=offset_seg(s1,r)
        s3=offset_seg_cw(s1,r)
        s4=s_int(s2)
        s5=sec_clean(s1,s4+s3,abs(r))
        s6=array(s5)[cKDTree(s5).query(s)[1]]
        return s6.tolist()


    
def outer_offset(sec,r):# used for offset function
    s1=flip(sec) if cw(sec)==1 else sec
    p0=[sec[len(sec)-1]]+sec[:len(sec)-1]
    p1=sec
    p2=sec[1:]+[sec[0]]
    p0,p1,p2=array([p0,p1,p2])
    v1=p0-p1
    u1=v1/linalg.norm(v1,axis=1).reshape(-1,1)
    v2=p2-p1
    u2=v2/linalg.norm(v2,axis=1).reshape(-1,1)
    theta=arccos(einsum('ij,ij->i',u1,u2))*180/pi
    alpha=180-theta
    pa=p1+einsum('ij,i->ij',(u1*r),tan(alpha/2*pi/180))
    pb=p1+einsum('ij,i->ij',(u2*r),tan(alpha/2*pi/180))
    cp=array([ arc_2p_cp(pa[i],pb[i],r,1) for i in range(len(p1))])
    pc=p1+(u1@rm(90))*r
    pd=p1+(u2@rm(-90))*r
    op=[ array(arc_2p(pc[i],pd[i],r,-1,0 if linalg.norm(pc[i]-pd[i])<1 else 5)) if cw([p0[i],p1[i],p2[i]])==-1 else [cp[i]] for i in range(len(p1))]
    radius=r_3pv(p0,p1,p2)
    op01=concatenate([op[i] for i in range(len(sec)) if (cw([p0[i],p1[i],p2[i]])==-1) | (radius[i]>=r)]).tolist()
    p0=op01
    p1=op01[1:]+[op01[0]]
    p2=op01[len(op01)-2:len(op01)]+op01[:len(op01)-2]
    p3=[op01[len(op01)-1]]+op01[:len(op01)-1]
    p4=op01[2:]+op01[0:2]
    p5=op01[3:]+op01[0:3]

    p0,p1,p2,p3,p4,p5=array([p0,p1,p2,p3,p4,p5])
    v1=p1-p0
    u1=v1/linalg.norm(v1,axis=1).reshape(-1,1)
    ip=swapaxes(array([i_p2dv(p0,p1,p2,p3),i_p2dv(p0,p1,p4,p5)]),0,1)
    l1=linalg.norm(p1-p0,axis=1)
    a=ip-p0[:,None]
    b=1/sqrt(einsum('ijk,ijk->ij',a,a))
    c=sqrt(einsum('ijk,ijk->ij',a,a))
    u2=einsum('ijk,ij->ijk',a,b)
    c1=c<l1[:,None]
    c2=((u2<0)==(u1<0)[:,None]).all(axis=1)
    op02=[ ip[i][0].tolist() if (c1&c2)[i][0]==True else (ip[i][1].tolist() if (c1&c2)[i][1]==True else op01[i]) for i in range(len(ip))]
    p=array(op02)
    p1=array(m_points1(s1,10))
    p.shape,p1.shape
    p2=p[:,None]-p1
    p3=sqrt(einsum('ijk,ijk->ij',p2,p2)).min(axis=1)
    p4=p[(p3>=r-.02)]

    return p4[cKDTree(p4).query(s1)[1]].tolist()

def m_points1(sec,s):# multiple points with in the straight lines in the closed section 'sec'. 's' is the number of segments between each straight line
    s1=sec
    s2=sec[1:]+[sec[0]]
    s1,s2=array([s1,s2])
    u=(s2-s1)/linalg.norm(s2-s1,axis=1).reshape(-1,1)
    l=linalg.norm(s2-s1,axis=1)
    n=(l/s).round(0)+1
    p=linspace(zeros(len(l)),l,s,axis=1)
    q=einsum('ij,ik->ikj',u,p)
    s1.shape,q.shape
    return (s1[:,None]+q).reshape(-1,2).tolist()

def ibsap(sec,pnt):# intersection between section and a point. used to find whether the poin is inside the section or outside the section
    p0=array(pnt)
    p2=sec
    p3=sec[1:]+[sec[0]]
    p2,p3=array([p2,p3])
    v1=[1,0]
    v2=(p3-p2)+[0,.00001]
    im=linalg.pinv(array([[v1]*len(v2),-v2]).transpose(1,0,2).transpose(0,2,1))
    p=p2-p0
    t1=einsum('ijk,ik->ij',im,p)[:,0]
    t2=einsum('ijk,ik->ij',im,p)[:,1]
    c1=(t2>=0)&(t2<=1)
    c2=t1>=0
    t=t1[c1&c2]
    p4=p0[None,:]+array(v1)*t.reshape(-1,1)
    return p4.tolist()

def sec_clean(sec,sec1,r):
    sec1=array([p for p in sec1 if len(ibsap(sec,p))%2==1])
    p0=sec
    p1=sec[1:]+[sec[0]]
    sec6=swapaxes(array([p0,p1]),0,1)
    p0,p1=array([p0,p1])
    v1=p1-p0
    v2=sec1[:,None]-p0
    v3=sec1[:,None]-p1
    u1=v1/linalg.norm(v1,axis=1).reshape(-1,1)
    n=1/linalg.norm(v1,axis=1)
    u1.shape,v2.shape
    d=einsum('jk,ijk->ij',u1,v2)
    t=einsum('ij,j->ij',d,n).round(3)
    u1.shape,d.shape
    n1=einsum('jk,ij->ijk',u1,d)
    p1=p0+n1
    sec1.shape,p1.shape
    n2=sec1[:,None]-p1
    n3=sqrt(einsum('ijk,ijk->ij',n2,n2)).round(3)
    n4=where((t>=0)&(t<=1),n3,1e5).min(axis=1)
    m=sec1[(n4>=abs(r)-.02)&(n4<=abs(r)+.02)].tolist()
    return array(m)[cKDTree(m).query(sec)[1]].tolist()


def sec_clean1(sec,sec1,r):
#     sec1=array([p for p in sec1 if len(ibsap(sec,p))%2==1])
    p0=sec
    p1=sec[1:]+[sec[0]]
    sec6=swapaxes(array([p0,p1]),0,1)
    p0,p1=array([p0,p1])
    v1=p1-p0
    v2=sec1[:,None]-p0
    v3=sec1[:,None]-p1
    u1=v1/linalg.norm(v1,axis=1).reshape(-1,1)
    n=1/linalg.norm(v1,axis=1)
    u1.shape,v2.shape
    d=einsum('jk,ijk->ij',u1,v2)
    t=einsum('ij,j->ij',d,n).round(3)
    u1.shape,d.shape
    n1=einsum('jk,ij->ijk',u1,d)
    p1=p0+n1
    sec1.shape,p1.shape
    n2=sec1[:,None]-p1
    n3=sqrt(einsum('ijk,ijk->ij',n2,n2)).round(3)
    n4=where((t>=0)&(t<=1),n3,1e5).min(axis=1)
    m=sec1[(n4>=abs(r)-.02)&(n4<=abs(r)+.02)].tolist()
    return array(m)[cKDTree(m).query(sec)[1]].tolist()



def fillet_2cir(r1,r2,c1,c2,r): # fillet between 2 circles with radius 'r1' and 'r2' and center points 'c1' and 'c2' and 'r' is the radius of the fillet
    '''
    function to create 2d fillet between 2 circles, where r1,r2 and c1,c2 are radiuses and enter points of the 2 circles respectively. r-> fillet radius
    example:
    fillet=fillet_2cir(r1=5,r2=3,c1=[0,0],c2=[7,0],r=1)
    
    refer to file "examples of various functions"
   
    '''
    
    c1,c2=array([c1,c2])
    l1=linalg.norm(c2-c1)
    l2=r1+r
    l3=r2+r
    t=(l1**2+l2**2-l3**2)/(2*l1)
    h=sqrt(l2**2-t**2)
    v=c2-c1
    u=v/linalg.norm(v)
    p1=c1+u*t+(u@rm(90))*h
    a1=ang((c1-p1)[0],(c1-p1)[1])
    a2=ang((c2-p1)[0],(c2-p1)[1])
    p2=c1+u*t+u@rm(-90)*h
    a3=ang((c2-p2)[0],(c2-p2)[1])
    a4=ang((c1-p2)[0],(c1-p2)[1])
    a5=ang((p1-c1)[0],(p1-c1)[1])
    a6=ang((p2-c1)[0] ,(p2-c1)[1])
    a7=ang((p1-c2)[0] ,(p1-c2)[1])
    a8=ang((p2-c2)[0] ,(p2-c2)[1])

    arc1=arc(r,360+a2 if a2<a1 else a2,a1,p1)
    arc2=arc(r,360+a4 if a4<a3 else a4,a3,p2)
    arc3=arc(r2,360+a7 if a7<a8 else a7,a8,c2)
    arc4=arc(r1,a5,360+a6 if a6<a5 else a6,c1)

    return arc2+arc1

def filleto_2cir(r1,r2,c1,c2,r): # fillet between 2 circles with radius 'r1' and 'r2' and center points 'c1' and 'c2' and 'r' is the radius of the fillet. This is an open fillet where first or the second fillet can be called based on requirement
    '''
    function to draw the fillet radius "r" between the 2 circle with radiuses "r1" and "r2" centered at "c1" and "c2" respectively.
    This function gives an additional flexibility for drawing fillet only one side. e.g 
    fillet=filleto_2cir(r1=10,r2=10,c1=[0,0],c2=[20,0],r=10)
    fillet[0] will calculate fillet on one side
    refer to the file "example of various functions" to see the application
    '''
    
    c1,c2=array([c1,c2])
    l1=linalg.norm(c2-c1)
    l2=r1+r
    l3=r2+r
    t=(l1**2+l2**2-l3**2)/(2*l1)
    h=sqrt(l2**2-t**2)
    v=c2-c1
    u=v/linalg.norm(v)
    p1=c1+u*t+(u@rm(90))*h
    a1=ang((c1-p1)[0],(c1-p1)[1])
    a2=ang((c2-p1)[0],(c2-p1)[1])
    p2=c1+u*t+u@rm(-90)*h
    a3=ang((c2-p2)[0],(c2-p2)[1])
    a4=ang((c1-p2)[0],(c1-p2)[1])
    a5=ang((p1-c1)[0],(p1-c1)[1])
    a6=ang((p2-c1)[0] ,(p2-c1)[1])
    a7=ang((p1-c2)[0] ,(p1-c2)[1])
    a8=ang((p2-c2)[0] ,(p2-c2)[1])

    arc1=arc(r,360+a2 if a2<a1 else a2,a1,p1)
    arc2=arc(r,360+a4 if a4<a3 else a4,a3,p2)
    arc3=arc(r2,360+a7 if a7<a8 else a7,a8,c2)
    arc4=arc(r1,a5,360+a6 if a6<a5 else a6,c1)

    return [arc2,arc1]

def tctp(r1,r2,cp1,cp2): # 2 circle tangent points (one side) r1 and r2 are the radius of 2 circles and cp1 and cp2 are the center points
    '''
    function to draw tangent line joining 2 circles with radiuses "r1" and "r2" with center points "cp1" and "cp2" respectively. 
    This function draws tangent line on only one side
     e.g. try this code below:
     sec=tctp(r1=10,r2=5,cp1=[0,0],cp2=[15,6]);
     
     refer to file "example of various functions" for application
 
    '''
    cp1,cp2=array([cp1,cp2])
    v1=cp2-cp1,
    u1=v1/linalg.norm(v1)
    ang1=arcsin((r2-r1)/linalg.norm(cp2-cp1))*180/pi

    t1=cp1+u1@rm(90+ang1)*r1
    t2=cp2+u1@rm(90+ang1)*r2

    t3=cp1+u1@rm(-90-ang1)*r1
    t4=cp2+u1@rm(-90-ang1)*r2
    return [t1[0].tolist(),t2[0].tolist()]

def tctpf(r1,r2,cp1,cp2): #2 circle tangent point full (both the sides)
    '''
    function to draw tangent line joining 2 circles with radiuses "r1" and "r2" with center points "cp1" and "cp2" respectively. 
    This function draws tangent line on both the sides
    example:
    cir1=circle(10)
    cir2=circle(5,[15,6])
    sec=tctpf(r1=10,r2=5,cp1=[0,0],cp2=[15,6])
    
    refer file "example of various functions" for application
    '''
    cp1,cp2=array([cp1,cp2])
    v1=cp2-cp1,
    u1=v1/linalg.norm(v1)
    ang1=arcsin((r2-r1)/linalg.norm(cp2-cp1))*180/pi

    t1=cp1+u1@rm(90+ang1)*r1
    t2=cp2+u1@rm(90+ang1)*r2

    t3=cp1+u1@rm(-90-ang1)*r1
    t4=cp2+u1@rm(-90-ang1)*r2
    return [t1[0].tolist(),t2[0].tolist(),t4[0].tolist(),t3[0].tolist()]

def circle(r,cp=[0,0],s=50): # circle with radius r and center point cp, s is the number of segments in the circle
    '''
    function for creating points in circle with radius "r", center point "cp" and number of segments "s" 
    '''
    return array([ [cp[0]+r*cos(i*pi/180),cp[1]+r*sin(i*pi/180)] for i in linspace(0,360,s)][0:-1]).tolist()

def circle_c(r,cp=[0,0],s=50):
    c=array([ [cp[0]+r*cos(i*pi/180),cp[1]+r*sin(i*pi/180)] for i in linspace(0,360,s)][0:-1]).tolist()
    p0,p1=array([c[len(c)-1],c[0]])
    v=p1-p0
    p=(p0+v*.999).tolist()
    return c+[p]

def qmr1(s,r,pl):
    for i in range(len(s)):
        a=[1,0,0] if s[i]=='x' else [0,1,0] if s[i]=='y' else [0,0,1]
        b=r[i]
        pl=[q(a,p,b) for p in pl]
    return pl

def qmr2(s,r,pl):
    for i in range(len(s)):
        a=[1,0,0] if s[i]=='x' else [0,1,0] if s[i]=='y' else [0,0,1]
        b=r[i]
        pl=[[q(a,p1,b) for p1 in p]for p in pl]
    return pl

def q_rot(s,pl):
    '''
    function to rotate a group of points "pl" around a series of axis with defined angles 
    example:
    q_rot(s=["z20","x40","y80"],pl=[[2,0],[10,2]])
    => 
    will rotate the line first around z axis by 20 deg then around x axis by 40 degrees and then around y axis by 80 degrees.
    '''
    if len(array(pl).shape)==2:
        return qmr1([p[0] for p in s],[0 if len(p)==1 else float(p[1:]) for p in s],pl)
    else:
        return qmr2([p[0] for p in s],[0 if len(p)==1 else float(p[1:]) for p in s],pl)
    
def l_extrude(sec,h=1,a=0,steps=1):
    s=2 if a==0 else steps
    return [trns([0,0,h*i if a==0 else h/a*i],q_rot([f"z{0 if a==0 else i}"],sec)) for i in linspace(0,1 if a==0 else a,s)]

def cylinder(r1=1,r2=1,h=1,cp=[0,0],s=50,r=0,d=0,d1=0,d2=0,center=False):
    '''
    function for making a cylinder
    r1 or r: radius of circle at the bottom
    r2 or r: radius of circle at the top
    d1 or d: diameter of circle at the bottom
    d2 or d: diameter of circle at the top
    h: height of the cylinder
    '''
    ra=r if r>0 else d/2 if d>0 else d1/2 if d1>0 else r1
    rb=r if r>0 else d/2 if d>0 else d2/2 if d2>0 else r2
    sec=circle(ra,cp,s)
    
    path=pts([[-ra+.1,0],[ra-.1,0],[rb-ra,h],[-rb+.1,0]])
    p= trns([0,0,-h/2],prism(sec,path)) if center==True else prism(sec,path)
    return p

def square(s=0,center=False):
    m= s if type(s)==int or type(s)==float else s[0]
    n= s if type(s)==int or type(s)==float else s[1]
    sec=cr(pts1([[0,0,.001],[m,0,.001],[0,n,.001],[-m,0,.001]]),10)
    sec1= [[p[0]-m/2,p[1]-n/2] for p in sec] if center==True else sec
    return sec1

def rsz3d(prism,rsz):
    prism1=array(prism).reshape(-1,3)
    max_x=prism1[:,0].max()
    max_y=prism1[:,1].max()
    max_z=prism1[:,2].max()
    min_x=prism1[:,0].min()
    min_y=prism1[:,1].min()
    min_z=prism1[:,2].min()
    avg=prism1.mean(axis=0)
    
    r_x=rsz[0]/(max_x-min_x)
    r_y=rsz[1]/(max_y-min_y)
    r_z=rsz[2]/(max_z-min_z)
    
    rev_prism=[[[avg[0]+r_x*(p[0]-avg[0]),avg[1]+r_y*(p[1]-avg[1]),avg[2]+r_z*(p[2]-avg[2])] for p in prism[i]] 
               for i in range(len(prism))]
    t=((array(bb(rev_prism))-array(bb(prism)))/2).tolist()
    return trns(t,rev_prism)

def rsz3dc(prism,rsz):
    prism1=array(prism).reshape(-1,3)
    max_x=prism1[:,0].max()
    max_y=prism1[:,1].max()
    max_z=prism1[:,2].max()
    min_x=prism1[:,0].min()
    min_y=prism1[:,1].min()
    min_z=prism1[:,2].min()
    avg=prism1.mean(axis=0)
    
    r_x=rsz[0]/(max_x-min_x)
    r_y=rsz[1]/(max_y-min_y)
    r_z=rsz[2]/(max_z-min_z)
    
    rev_prism=[[[avg[0]+r_x*(p[0]-avg[0]),avg[1]+r_y*(p[1]-avg[1]),avg[2]+r_z*(p[2]-avg[2])] for p in prism[i]] 
               for i in range(len(prism))]
    return rev_prism


def bb(prism):
    prism1=array(prism).reshape(-1,3)
    max_x=prism1[:,0].max()
    max_y=prism1[:,1].max()
    max_z=prism1[:,2].max()
    min_x=prism1[:,0].min()
    min_y=prism1[:,1].min()
    min_z=prism1[:,2].min()
    return [max_x-min_x,max_y-min_y,max_z-min_z]

# def cube(s,center=False):
#     m=s if type(s)==int or type(s)==float else s[0]
#     n=s if type(s)==int or type(s)==float else s[1]
#     o=s if type(s)==int or type(s)==float else s[2]
#     path=cr(pts1([[-m/2,0],[m/2,0],[0,o],[-m/2,0]]),1)
#     p=trns([-m/2,-n/2,-o/2],rsz3d(prism(square(m),path),[m,n,o])) if center==True else rsz3d(prism(square(m),path),[m,n,o])
#     return array(p).tolist()

def cube(s,center=False):
    if center==False:
        return l_extrude(square([s[0],s[1]]),s[2])
    elif center==True:
        return trns([0,0,-s[2]/2],l_extrude(square([s[0],s[1]],True),s[2]))


def sphere(r=0,cp=[0,0,0],s=50):
    path=arc(r,-90,90,s=s)
    p=[ trns([cp[0],cp[1],p[1]+cp[2]],circle(p[0],s=s)) for p in path]
    return array(p).tolist()

def rsz2d(sec,rsz):
    avg=array(sec).mean(axis=0)
    max_x=array(sec)[:,0].max()
    min_x=array(sec)[:,0].min()
    max_y=array(sec)[:,1].max()
    min_y=array(sec)[:,1].min()
    r_x=rsz[0]/(max_x-min_x)
    r_y=rsz[1]/(max_y-min_y)
    s=array([ avg+array([r_x*(sec[i][0]-avg[0]),r_y*(sec[i][1]-avg[1])-((min_y-avg[1])*r_y-(min_y-avg[1]))]) for i in range(len(sec))]).round(4)
    return s[sort(unique(s,axis=0,return_index=True)[1])].tolist()
    
def rsz2dc(sec,rsz):
    avg=array(sec).mean(axis=0)
    max_x=array(sec)[:,0].max()
    min_x=array(sec)[:,0].min()
    max_y=array(sec)[:,1].max()
    min_y=array(sec)[:,1].min()
    r_x=rsz[0]/(max_x-min_x)
    r_y=rsz[1]/(max_y-min_y)
    s=array([ avg+array([r_x*(sec[i][0]-avg[0]),r_y*(sec[i][1]-avg[1])]) for i in range(len(sec))]).round(4)
    return s[sort(unique(s,axis=0,return_index=True)[1])].tolist()

def ip(prism,prism1):
    '''
    function to calculate intersection point between two 3d prisms. 
     "prism" is the 3d object which is intersected with "prism1".
     try below code for better understanding:
    sec=circle(10)
    path=cr(pts1([[2,0],[-2,0,2],[0,10,3],[-9.9,0]]),5)
    p=prism(sec,path)
    p1=cylinder(r=3,h=15,s=30)
    ip1=ip(p,p1)
    
    refer to file "example of various functions" for application
    '''
    pa=prism
    pb=prism1
    p1=array([[ [[pa[i][j],pa[i][j+1],pa[i+1][j]],[pa[i+1][j+1],pa[i+1][j],pa[i][j+1]]] if j<len(pa[i])-1 
     else [[pa[i][j],pa[i][0],pa[i+1][j]],[pa[i+1][0],pa[i+1][j],pa[i][0]]] 
     for j in range(len(pa[i]))] 
              for i in range(len(pa)-1)]).reshape(-1,3,3)
    p2=array([[[pb[i][j],pb[i+1][j]] for j in range(len(pb[i]))] for i in range(len(pb)-1)]).reshape(-1,2,3)
    pm=p1[:,0]
    pn=p1[:,1]
    po=p1[:,2]
    px=p2[:,0]
    py=p2[:,1]
    v1,v2,v3=py-px,pn-pm,po-pm
    t1=einsum('ijk,jk->ij',px[:,None]-pm,cross(v2,v3))/einsum('ik,jk->ij',-v1,cross(v2,v3)+[.00001,.00001,.00001])
    t2=einsum('ijk,ijk->ij',px[:,None]-pm,cross(v3,-v1[:,None]))/einsum('ik,jk->ij',-v1,cross(v2,v3)+[.00001,.00001,.00001])
    t3=einsum('ijk,ijk->ij',px[:,None]-pm,cross(-v1[:,None],v2))/einsum('ik,jk->ij',-v1,cross(v2,v3)+[.00001,.00001,.00001])
    p=px[:,None]+einsum('ik,ij->ijk',v1,t1)
    condition=(t1>=0)&(t1<=1)&(t2>=0)&(t2<=1)&(t3>=0)&(t3<=1)&((t2+t3)>=0)&((t2+t3)<=1)
    p=p[condition]
#     p=p[unique(p,return_index=True)[1]]
    return p.tolist()

def ipf(prism,prism1,r,s,o=0):
    '''
    function to calculate fillet at the intersection point of 2 solids
    'prism': solid 1 or surface 1
    'prism1': solid 2
    'r': radius of the fillet
    's': number of segments in the fillet, more number of segments will give finer finish
    'o': option '0' produces fillet in outer side of the intersection and '1' in the inner side of the intersections
    refer to the file "example of various functions" for application
    '''
    pa=prism
    pb=prism1
    p1=array([[ [[pa[i][j],pa[i][j+1],pa[i+1][j]],[pa[i+1][j+1],pa[i+1][j],pa[i][j+1]]] if j<len(pa[i])-1 
     else [[pa[i][j],pa[i][0],pa[i+1][j]],[pa[i+1][0],pa[i+1][j],pa[i][0]]] 
     for j in range(len(pa[i])-1)] 
              for i in range(len(pa)-1)]).reshape(-1,3,3)
    p2=array([[[pb[i][j],pb[i+1][j]] for j in range(len(pb[i]))] for i in range(len(pb)-1)]).reshape(-1,2,3)
    pm=p1[:,0]
    pn=p1[:,1]
    po=p1[:,2]
    px=p2[:,0]
    py=p2[:,1]
    v1,v2,v3=py-px,pn-pm,po-pm
#     px+v1*t1=pm+v2*t2+v3*t3
#     v1*t1-v2*t2-v3*t3=pm-px
    u1=v1/(linalg.norm(v1,axis=1).reshape(-1,1)+.0001)
    t1=einsum('ijk,jk->ij',px[:,None]-pm,cross(v2,v3))/(einsum('ik,jk->ij',-v1,cross(v2,v3))+.0001)
    t2=einsum('ijk,ijk->ij',px[:,None]-pm,cross(v3,-v1[:,None]))/(einsum('ik,jk->ij',-v1,cross(v2,v3))+.0001)
    t3=einsum('ijk,ijk->ij',px[:,None]-pm,cross(-v1[:,None],v2))/(einsum('ik,jk->ij',-v1,cross(v2,v3))+.0001)
    p=px[:,None]+einsum('ik,ij->ijk',v1,t1)
    pq=p+(u1*r)[:,None]
    p.shape,pq.shape
    condition=(t1>=0)&(t1<=1)&(t2>=0)&(t2<=1)&(t3>=0)&(t3<=1)&((t2+t3)>=0)&((t2+t3)<=1)
    p=p[condition].tolist()
    pp=p[1:]+[p[0]]
    pq=pq[condition].tolist()
    v4=array(pp)-array(p)
    pnt=array(pq)-array(p)
    n=cross(v4,pnt)
    n=n/(linalg.norm(n,axis=1).reshape(-1,1)+.0001)*r
    pnt=n
    cir=[[(p[i]+array(q(v4[i],pnt[i],t))).tolist() for t in linspace(-90,90,10)]for i in range(len(v4))] if o==0 else \
    [[(p[i]+array(q(v4[i],pnt[i],-t))).tolist() for t in linspace(90,270,10)]for i in range(len(v4))] 
    p2=[[ [cir[i][j],cir[i][j+1]] for j in range(len(cir[i])-1)] for i in range(len(cir))]
    p2=array(p2).reshape(-1,2,3)
    px=p2[:,0]
    py=p2[:,1]
    v1,v2,v3=py-px,pn-pm,po-pm
    u1=v1/(linalg.norm(v1,axis=1).reshape(-1,1)+.0001)
    t1=einsum('ijk,jk->ij',px[:,None]-pm,cross(v2,v3))/(einsum('ik,jk->ij',-v1,cross(v2,v3))+.0001)
    t2=einsum('ijk,ijk->ij',px[:,None]-pm,cross(v3,-v1[:,None]))/(einsum('ik,jk->ij',-v1,cross(v2,v3))+.0001)
    t3=einsum('ijk,ijk->ij',px[:,None]-pm,cross(-v1[:,None],v2))/(einsum('ik,jk->ij',-v1,cross(v2,v3))+.0001)
    m=px[:,None]+einsum('ik,ij->ijk',v1,t1)
    condition=(t1>=0)&(t1<=1)&(t2>=0)&(t2<=1)&(t3>=0)&(t3<=1)&((t2+t3)>=0)&((t2+t3)<=1)
    m=m[condition]
    m=unique(m,axis=0)[:-1]
    m=m[cKDTree(m).query(p)[1]].tolist()
    p=swapaxes(array([m,p,pq]),0,1)
    p=[[fillet_3p_3d(p2,p1,p0,r_3p_3d([p0,p1,p2])*1.9,s)]for (p0,p1,p2) in p]
    p=array(p).reshape(-1,s+1,3).tolist()
    return p+[p[0]]

def ipf1(p,p1,r,s,o=0):
    pa=[[[[p[i][j],p[i][j+1],p[i+1][j]],[p[i+1][j+1],p[i+1][j],p[i][j+1]]] if j<len(p[0])-1 else \
         [[p[i][j],p[i][0],p[i+1][j]],[p[i+1][0],p[i+1][j],p[i][0]]] \
         for j in range(len(p[0]))] for i in range(len(p)-1)]
    pa=array(pa).reshape(-1,3,3)

    pb=[[[p1[i][j],p1[i+1][j]] for j in range(len(p1[0]))] for i in range(len(p1)-1)]
    pb=array(pb).reshape(-1,2,3)
    
    pm=pa[:,0]
    pn=pa[:,1]
    po=pa[:,2]
    px=pb[:,0]
    py=pb[:,1]
    v1,v2,v3=py-px,pn-pm,po-pm
    v5=array([cross(v2,v3).tolist()]*len(v1))
#     px+v1*t1=pm+v2*t2+v3*t3
#     v1*t1-v2*t2-v3*t3=pm-px
    u1=v1/(linalg.norm(v1,axis=1).reshape(-1,1)+.0001)
    t1=einsum('ijk,jk->ij',px[:,None]-pm,cross(v2,v3))/(einsum('ik,jk->ij',-v1,cross(v2,v3))+.0001)
    t2=einsum('ijk,ijk->ij',px[:,None]-pm,cross(v3,-v1[:,None]))/(einsum('ik,jk->ij',-v1,cross(v2,v3))+.0001)
    t3=einsum('ijk,ijk->ij',px[:,None]-pm,cross(-v1[:,None],v2))/(einsum('ik,jk->ij',-v1,cross(v2,v3))+.0001)
    p=px[:,None]+einsum('ik,ij->ijk',v1,t1)
    pq=p+(u1*r)[:,None]
    p.shape,pq.shape
    condition=(t1>=0)&(t1<=1)&(t2>=0)&(t2<=1)&(t3>=0)&(t3<=1)&((t2+t3)>=0)&((t2+t3)<=1)
    p=p[condition].tolist()
    pp=p[1:]+[p[0]]
    pq=pq[condition].tolist()
    v4=array(pp)-array(p)
#     pnt=array(pq)-array(p)
#     n=cross(v4,pnt)
#     n=n/(linalg.norm(n,axis=1).reshape(-1,1)+.0001)*r
#     pnt=n
    pnt=v5[condition]
    
    cir=[[(p[i]+array(q(v4[i],pnt[i],t))).tolist() for t in linspace(-90,90,10)]for i in range(len(v4))] if o==0 else \
    [[(p[i]+array(q(v4[i],pnt[i],-t))).tolist() for t in linspace(90,270,10)]for i in range(len(v4))] 
    p2=[[ [cir[i][j],cir[i][j+1]] for j in range(len(cir[i])-1)] for i in range(len(cir))]
    p2=array(p2).reshape(-1,2,3)
    px=p2[:,0]
    py=p2[:,1]
    v1,v2,v3=py-px,pn-pm,po-pm
    u1=v1/(linalg.norm(v1,axis=1).reshape(-1,1)+.0001)
    t1=einsum('ijk,jk->ij',px[:,None]-pm,cross(v2,v3))/(einsum('ik,jk->ij',-v1,cross(v2,v3))+.0001)
    t2=einsum('ijk,ijk->ij',px[:,None]-pm,cross(v3,-v1[:,None]))/(einsum('ik,jk->ij',-v1,cross(v2,v3))+.0001)
    t3=einsum('ijk,ijk->ij',px[:,None]-pm,cross(-v1[:,None],v2))/(einsum('ik,jk->ij',-v1,cross(v2,v3))+.0001)
    m=px[:,None]+einsum('ik,ij->ijk',v1,t1)
    condition=(t1>=0)&(t1<=1)&(t2>=0)&(t2<=1)&(t3>=0)&(t3<=1)&((t2+t3)>=0)&((t2+t3)<=1)
    m=m[condition]
    m=unique(m,axis=0)[:-1]
    m=m[cKDTree(m).query(p)[1]].tolist()
    p=swapaxes(array([m,p,pq]),0,1)
    p=[[fillet_3p_3d(p2,p1,p0,r_3p_3d([p0,p1,p2]),s)]for (p0,p1,p2) in p]
    p=array(p).reshape(-1,s+1,3).tolist()
    return p+[p[0]]


def ipe(prism,prism1,r,s,o):
    '''
    function to change the orientation of a fillet to create a solid
    prism: solid
    prism1: is another 3d solid which intersects 'prism' to create fillet
    r: radius of the fillet
    s: number of segments in the fillet
    o: options '0' and '1' (refer to the explanation of options in function fillet_sol2sol())
    
    refer to the file "explanation of various functions" for application example
    '''
    a=cpo(ipf(prism,prism1,2,10,0))[1:]
    return a


def s_int(s): #creates intersection between all the segments of a section
    p0=array([array(s)[:,0]]*len(s)).transpose(1,0,2)
    p1=array([array(s)[:,1]]*len(s)).transpose(1,0,2)
    v1=p1-p0
    p2=array([array(s)[:,0]]*len(s))
    p3=array([array(s)[:,1]]*len(s))
    v2=p3-p2
    v1.shape,v2.shape
    A=linalg.pinv(array([v1,-v2]).transpose(1,0,2,3).transpose(0,2,1,3).transpose(0,1,3,2))
    B=p2-p0
    t=einsum('ijkl,ijl->ijk',A,B)[:,:,0].round(4)
    u=einsum('ijkl,ijl->ijk',A,B)[:,:,1].round(4)
    condition=(t>=0)&(t<=1)&(u>=0)&(u<=1)
    d=(p0+einsum('ijk,ij->ijk',v1,t))[condition].tolist()
    return d

def comb(n,i): 
    '''
    calculates number of possible combinations for "n" items with "i" selected items
    comb(8,2) => 28
    '''
    return int(math.factorial(n)/(math.factorial(i)*math.factorial(n-i)))

def bezier(p,s=10):
    '''
    bezier curve defined by points 'p' and number of segments 's'
    refer file "example of various functions" for application
    '''
    return array([array([ comb((len(p)-1),i)*(1-t)**((len(p)-1)-i)*t**i*array(p[i])  for i in range(len(p))]).sum(0) for t in linspace(0,1,s)]).tolist()

def arc_3d(v=[0,0,1],r=1,theta1=0,theta2=360,cw=-1,s=50):
    '''
    3d arc defined by normal vector 'v', radius 'r1', start angle 'theta1', 
    end angle 'theta2' , clockwise(1) or counter clockwise(-1) and number of segments 's'
    
    refer file "example of various functions" for application example
    '''
#     theta=0 if v[:2]==[0,0] else ang(v[0],v[1])
#     v=q([0,0,1],v,-theta)
#     alpha=ang(v[0],v[2])
#     arc1=arc(r,theta1,theta2,[0,0],s=s) if cw==-1 else flip(arc(r,theta1,theta2,[0,0],s=s))
#     arc2=q_rot(['x90','z90'],arc1)
#     return array(q_rot([f'z{theta}',f'y{-alpha}'],arc2)).tolist()
    sec=arc(r,theta1,theta2,[0,0],s) if cw==-1 else flip(arc(r,theta1,theta2,[0,0],s))
    s=q_rot(['x90','z-90'],sec)
    v1=array(v)+array([0,0,0.00001])
    va=[v1[0],v1[1],0]
    u1=array(uv(v1))
    ua=array(uv(va))
    v2=cross(va,v1)
    a1=arccos(u1@ua)*180/pi
    a2=ang(v1[0],v1[1])
    s1=q_rot([f'z{a2}'],s)
    sec1=[q(v2,p,a1) for p in s1]
    return sec1

def plane(nv,radius):
    '''
    plane defined by normal 'nv' and 'radius'
    
    refer file "example of various functions" for application example
    '''
    sec1=arc_3d(nv,.0001,0,360,-1)
    sec2=arc_3d(nv,radius,0,360,-1)
    plane=[sec1,sec2]
    return plane

def l_cir_ip(line,cir):
    '''
    line circle intersection point
    '''
    p0,p1=array(line)
    p2=array(cir)
    p3=array(cir[1:]+[cir[0]])
    v1=p1-p0
    v2=p3-p2
    im=linalg.pinv(array([[v1]*len(v2),-v2]).transpose(1,0,2).transpose(0,2,1))
    pnt=p2-p0
    t=einsum('ijk,ik->ij',im,pnt)
    condition=((t>=0)&(t<=1)).all(1)
    ip=p2+v2*t[:,1].reshape(-1,1)
    return ip[condition].tolist()

def s_pnt(pnt): # starting point for calculating convex hull (bottom left point)
    pnt=array(pnt)
    c1=pnt[:,1]==pnt[:,1].min()
    s1=pnt[c1]
    c2=s1[:,0]==s1[:,0].min()
    return s1[c2][0].tolist()

def n_pnt(pnt,sp,an):
    pnt,sp=array(pnt),array(sp)
    pnt=pnt[(pnt!=sp).all(1)]
    a=pnt-sp
    a1=vectorize(ang)(a[:,0],a[:,1])
    n_pnt=pnt[a1==a1[a1>=an].min()][0].tolist()
    return [n_pnt,a1[a1>=an].min().tolist()]

def c_hull(pnt): # convex hull for an array of points
    '''
    function to calculate convex hull for a list of points 'pnt'
    
    refer file "example of various functions" for application example
    '''
    c=[]
    np=n_pnt(pnt,s_pnt(pnt),0)
    for i in range(len(pnt)):
        c.append(np[0])
        np=n_pnt(pnt,np[0],np[1])
        if np[0]==s_pnt(pnt):
            break
    return [s_pnt(pnt)]+c

def convex(sec): # to check whether a closed section is convex
    '''
    function to check whether a section is convex or not
    example:
    sec1=cr_c(pts1([[0,0,.2],[8,3,3],[5,7,1],[-8,0,2],[-5,20,1]]),20)
    sec2=cr_c(pts1([[0,0,.1],[7,5,2],[5,7,3],[-5,7,5],[-7,5,5]]),20)
    convex(sec1),convex(sec2) => (False, True)
    
    refer file "example of various functions" for application example
    '''
    s=flip(sec) if cw(sec)==1 else sec
    return True if offset_points_cw(s,-1)==[] else False

def oo_convex(sec,r): #outer offset of a convex section
    s=flip(sec) if cw(sec)==1 else sec
    return offset_points(sec,r)

def cir_p_t(cir,pnt):
    '''
    circle to point tangent line (point should be outside the circle)
    refer file "example of various functions" for application example
    '''
    p0=cir
    p1=cir[1:]+[cir[0]]
    p0,p1=array([p0,p1])
    v=p1-p0
    a1=vectorize(ang)(v[:,0],v[:,1])
    v1=array(pnt)-p0
    a2=vectorize(ang)(v1[:,0],v1[:,1])
    an=abs(a1-a2).round(4)
    a=360/len(cir)/2
    cond=abs(a1-a2)<a
    an1=abs(a1-a2)[cond].round(4)
    return array(cir)[an==an1][0].tolist()

def p_cir_t(pnt,cir): # point to circle tangent line (point should be outside the circle)
    p0=cir
    p1=cir[1:]+[cir[0]]
    p0,p1=array([p0,p1])
    v=p1-p0
    a1=vectorize(ang)(v[:,0],v[:,1])
    v1=p0-array(pnt)
    a2=vectorize(ang)(v1[:,0],v1[:,1])
    an=abs(a1-a2).round(4)
    a=360/len(cir)/2
    cond=abs(a1-a2)<a
    an1=abs(a1-a2)[cond].round(4)
    return array(cir)[an==an1][0].tolist()

def p_extrude(sec,path): # section extrude through a path
    p0=path
    p1=p0[1:]+[p0[0]]
    p0,p1=array(p0),array(p1)
    v=p1-p0
    a1=vectorize(ang)(v[:,0],v[:,1])
    b=sqrt(v[:,0]**2+v[:,1]**2)
    a2=vectorize(ang)(b,v[:,2])
    c=[]
    for i in range(len(path)-1):
        sec1=trns(p0[i],q_rot(['x90','z-90',f'y{-a2[i]}',f'z{a1[i]}'],sec))
        sec2=trns(p1[i],q_rot(['x90','z-90',f'y{-a2[i]}',f'z{a1[i]}'],sec))
        if i<len(path)-2:
            c.append([sec1])
        else:
            c.append([sec1,sec2])
    return flip(concatenate(c).tolist())

def p_extrudec(sec,path): # section extrude through a path (closed path)
    p0=path
    p1=p0[1:]+[p0[0]]
    p0,p1=array(p0),array(p1)
    v=p1-p0
    a1=vectorize(ang)(v[:,0],v[:,1])
    b=sqrt(v[:,0]**2+v[:,1]**2)
    a2=vectorize(ang)(b,v[:,2])
    c=[]
    for i in range(len(path)-1):
        sec1=trns(p0[i],q_rot(['x90','z-90',f'y{-a2[i]}',f'z{a1[i]}'],sec))
        sec2=trns(p1[i],q_rot(['x90','z-90',f'y{-a2[i]}',f'z{a1[i]}'],sec))
        if i<len(path)-2:
            c.append([sec1])
        else:
            c.append([sec1,sec2])
    a=concatenate(c).tolist()
    return flip(a+[a[0]])

def v_sec_extrude(sec,path,o): #variable section extrude through a given path
    sec=[offset(sec,i) for i in linspace(0,o,len(path))]
    p0=path
    p1=p0[1:]+[p0[0]]
    p0,p1=array(p0),array(p1)
    v=p1-p0
    a1=vectorize(ang)(v[:,0],v[:,1])
    b=sqrt(v[:,0]**2+v[:,1]**2)
    a2=vectorize(ang)(b,v[:,2])
    c=[]
    for i in range(len(path)-1):
        sec1=trns(p0[i],q_rot(['x90','z-90',f'y{-a2[i]}',f'z{a1[i]}'],sec[i]))
        sec2=trns(p1[i],q_rot(['x90','z-90',f'y{-a2[i]}',f'z{a1[i]}'],sec[i]))
        if i<len(path)-2:
            c.append([sec1])
        else:
            c.append([sec1,sec2])
    return concatenate(c).tolist()

def t_cir_tarc(r1,r2,cp1,cp2,r,s=50): #two circle tangent arc
    cp1,cp2=array([cp1,cp2])
    l1=linalg.norm(cp2-cp1)
    l2=r-r1
    l3=r-r2
    x=(l2**2-l3**2+l1**2)/(2*l1)
    h=sqrt(l2**2-x**2)
    v1=cp2-cp1
    u1=v1/linalg.norm(v1)
    p0=cp1+u1*x
    cp3=p0-(u1@rm(90))*h
    v2=cp2-cp3
    u2=v2/linalg.norm(v2)
    v3=cp1-cp3
    u3=v3/linalg.norm(v3)
    ang1=ang(u2[0],u2[1])
    ang2=ang(u3[0],u3[1])
    return array(arc(r,ang1,ang2,cp3,s)).tolist()

def tcct(r1,r2,cp1,cp2,cw=-1): # two circle cross tangent
    v1=[1,1]
    v2=[-r2,r1]
    cp1,cp2=array([cp1,cp2])
    d=linalg.norm(cp2-cp1)
    d1=(linalg.inv(array([v1,v2]).T)@array([d,0]))[0]
    d2=(linalg.inv(array([v1,v2]).T)@array([d,0]))[1]
    a=arcsin(r1/d1)*180/pi
    v3=cp2-cp1
    u3=v3/linalg.norm(v3)
    b=arccos(u3@array([1,0]))*180/pi
    if cw==-1:
        if v3[0]>0 and v3[1]<=0:
            theta1=270+a-b
            theta2=90+a-b
        elif v3[0]>=0 and v3[1]>0:
            theta1=270+a+b
            theta2=90+a+b
        elif v3[0]<0 and v3[1]>=0:
            theta1=270+a+b
            theta2=90+a+b
        else:
            theta1=270+a-b
            theta2=90+a-b
    else:
        if v3[0]>0 and v3[1]<=0:
            theta2=270-a-b
            theta1=90-a-b
        elif v3[0]>=0 and v3[1]>0:
            theta2=270-a+b
            theta1=90-a+b
        elif v3[0]<0 and v3[1]>=0:
            theta2=270-a+b
            theta1=90-a+b
        else:
            theta2=270-a-b
            theta1=90-a-b
        
    p0=(cp1+array([r1*cos(theta1*pi/180),r1*sin(theta1*pi/180)])).tolist()
    p1=(cp2+array([r2*cos(theta2*pi/180),r2*sin(theta2*pi/180)])).tolist()
    return [p0,p1]

def arc_3p(p1,p2,p3,s=30):
    p1,p2,p3=array([p1,p2,p3])
    p4=p1+(p2-p1)/2
    p5=p2+(p3-p2)/2
    v1=p2-p4
    u1=v1/linalg.norm(v1)
    v2=p3-p5
    u2=v2/linalg.norm(v2)
    p6=p4+u1@rm(90)
    p7=p5+u2@rm(90)
    cp=i_p2d([p4,p6],[p5,p7])
    r=linalg.norm(p1-cp)
    v3=p1-cp
    v4=p2-cp
    v5=p3-cp
    a1=ang(v3[0],v3[1])
    a2=ang(v4[0],v4[1])
    a3=ang(v5[0],v5[1])
    a4=(a3+360 if a3<a1 else a3) if cw([p1,p2,p3])==-1 else (a3 if a3<a1 else a3-360)
    return arc(r,a1,a4,cp,s)

def cir_3p(p1,p2,p3,s=30):
    p1,p2,p3=array([p1,p2,p3])
    p4=p1+(p2-p1)/2
    p5=p2+(p3-p2)/2
    v1=p2-p4
    u1=v1/linalg.norm(v1)
    v2=p3-p5
    u2=v2/linalg.norm(v2)
    p6=p4+u1@rm(90)
    p7=p5+u2@rm(90)
    cp=i_p2d([p4,p6],[p5,p7])
    r=linalg.norm(p1-cp)
#     v3=p1-cp
#     v4=p2-cp
#     v5=p3-cp
#     a1=ang(v3[0],v3[1])
#     a2=ang(v4[0],v4[1])
#     a3=ang(v5[0],v5[1])
#     a4=(a3+360 if a3<a1 else a3) if cw([p1,p2,p3])==-1 else (a3 if a3<a1 else a3-360)
    return circle(r,cp,s)

def cp_3p(p1,p2,p3):
    p1,p2,p3=array([p1,p2,p3])
    p4=p1+(p2-p1)/2
    p5=p2+(p3-p2)/2
    v1=p2-p4
    u1=v1/linalg.norm(v1)
    v2=p3-p5
    u2=v2/linalg.norm(v2)
    p6=p4+u1@rm(90)
    p7=p5+u2@rm(90)
    cp=i_p2d([p4,p6],[p5,p7])
    return array(cp).tolist()



def ip_surf(surf2,surf1):
    '''
     function to calculate intersection point between two 3d prisms or between surface and solid. 
     "surf2" is the 3d object which is intersected with "surf1".
 try below code for better understanding:
 sec=circle(10);
 path=cr(pts1([[2,0],[-2,0,2],[0,10,3],[-9.9,0]]),5);
 prism=prism(sec,path);
 prism1=q_rot(["y40"],cylinder(r=3,h=15,s=30));

 %swp(prism);
 %swp(prism1);
 ip=ip_surf(prism,prism1);
 points(ip,.2);
    '''
    i,j,_=array(surf2).shape
    a=surf2
    b=surf1
    p1=array([[[[a[i][j],a[i+1][j],a[i][j+1]],[a[i+1][j+1],a[i][j+1],a[i+1][j]]] 
            for j in range(j-1)]  for i in range(i-1)]).reshape(-1,3,3)
    p2=array([[[b[i][j],b[i+1][j]] for j in range(len(b[i]))] for i in range(len(b)-1)]).reshape(-1,2,3)
    pm=p1[:,0]
    pn=p1[:,1]
    po=p1[:,2]
    px=p2[:,0]
    py=p2[:,1]
    v1,v2,v3=py-px,pn-pm,po-pm
    t1=einsum('ijk,jk->ij',px[:,None]-pm,cross(v2,v3))/(einsum('ik,jk->ij',-v1,cross(v2,v3))+.00001)
    t2=einsum('ijk,ijk->ij',px[:,None]-pm,cross(v3,-v1[:,None]))/(einsum('ik,jk->ij',-v1,cross(v2,v3))+.00001)
    t3=einsum('ijk,ijk->ij',px[:,None]-pm,cross(-v1[:,None],v2))/(einsum('ik,jk->ij',-v1,cross(v2,v3))+.00001)
    p=px[:,None]+einsum('ik,ij->ijk',v1,t1)
    condition=(t1>=0)&(t1<=1)&(t2>=0)&(t2<=1)&(t3>=0)&(t3<=1)&((t2+t3)>=0)&((t2+t3)<=1)
    return p[condition].tolist()

def perp(sec,point,radius):
    sec=array(seg(sec))
    p0=sec[:,0]
    p1=sec[:,1]
    v1=p1-p0
    u1=v1/(linalg.norm(v1,axis=1).reshape(-1,1)+.00001)
    v2=array(point)-p0
    v1norm=linalg.norm(v1,axis=1)
    v2norm=linalg.norm(v2,axis=1)
    v2cost=einsum('ij,ij->i',u1,v2)
    cond1=v2cost>=0
    cond2=v2cost<=v1norm
    d=sqrt(v2norm**2-v2cost**2)
    d=min(d[(cond1)&(cond2)]).round(4)
    cond3=d==round(abs(radius),3)
    return point if cond3 else []

def perp_point(line,point,distance):
    p0=line[0]
    p1=line[1]
    p0,p1=array([p0,p1])
    v1=p1-p0
    u1=v1/(linalg.norm(v1)+.00001)
    v2=array(point)-p0
    v1norm=linalg.norm(v1)
    v2norm=linalg.norm(v2)
    v2cost=u1@v2
    cond1=v2cost>=0
    cond2=v2cost<=v1norm
    d=sqrt(v2norm**2-v2cost**2)
    cond3=d<=distance
    return point if cond1 & cond2 & cond3  else []

def perp_dist(line,point):
    p0=line[0]
    p1=line[1]
    p0,p1=array([p0,p1])
    v1=p1-p0
    u1=v1/(linalg.norm(v1)+.00001)
    v2=array(point)-p0
    v1norm=linalg.norm(v1)
    v2norm=linalg.norm(v2)
    v2cost=u1@v2
    d=sqrt(v2norm**2-v2cost**2)
    return d


def pies(sec,pnt):
    sec1=array([p for p in pnt if len(ibsap(sec,p))%2==1])
    return sec1.tolist()

def sq(d,cp=[0,0]):
    cp=array(cp)-d/2
    cp=[cp[0],cp[1],0]
    return c3t2(trns(cp,[[0,0],[d,0],[d,d],[0,d]]))

def near_points(points,s_p,n):
    l=array([ linalg.norm(array(p)-array(s_p)) for p in points])
    l1=sort(l)[0:n+1]
    index=array([[i for i in range(len(l)) if p==l[i]]for p in l1]).reshape(-1)
    p1=array(points)[index].tolist()
    return p1[1:]

def next_point(points,s_p):
    a1=[270+(360-ang((array(p)-array(s_p))[0],(array(p)-array(s_p))[1]))
        if ang((array(p)-array(s_p))[0],(array(p)-array(s_p))[1])>270 else
        270-ang((array(p)-array(s_p))[0],(array(p)-array(s_p))[1])
        for p in points]
    n_p=array(points)[a1==max(a1)][0].tolist()
    return n_p

def exclude_points(points,pnts):
    return [p for p in points if p not in pnts]

def i_p2dw(l1,l):
    p0,p1=array(l1)
    p2,p3=array(l)
    v1=p1-p0
    v2=p3-p2
#                     p0+v1*t1=p2+v2*t2
#                     v1*t1-v2*t2=p2-p0
    im=linalg.inv(array([v1,-v2]).transpose(1,0)
                  +array([[.000001,.000002],[.000002,.000003]]))
    t=(im@(p2-p0))[0]
    u=(im@(p2-p0))[1]
    return  (p0+v1*t).tolist() if (0<t<1)& (0<u<1) else []


def pies1(s8,s4):
    p0=array(s4)
    p2=s8
    p3=s8[1:]+[s8[0]]
    p2,p3=array([p2,p3])
    v1=array([[[1,0]]*len(p2)]*len(p0))
    v2=array([((p3-p2)+[0,.00001]).tolist()]*len(p0))
    # im=linalg.pinv(array([[v1]*len(v2),-v2]).transpose(1,0,2).transpose(0,2,1))
    # im=array([im.tolist()]*len(p0))
    p=p2-p0[:,None]
    # t=einsum('ijkl,ijl->ijl',im,p)
    # s10=[p0[i].tolist() for i in range(len(p0)) if \
    #     t[i][(t[i][:,0]>=0)&(t[i][:,1]>=0)&(t[i][:,1]<=1)].shape[0]%2 \
    #  ==1]

    im=linalg.pinv(array([v1,-v2]).transpose(1,0,2,3).transpose(0,2,1,3))
    im.shape,p.shape
    t=einsum('ijkl,ijk->ijl',im,p)
    s10=[p0[i].tolist() for i in range(len(p0)) if \
        t[i][(t[i][:,0]>=0)&(t[i][:,1]>=0)&(t[i][:,1]<=1)].shape[0]%2 \
     ==1]
    return s10

def rsec(line,radius):
    p0=line[0]
    p1=line[1]
    p0,p1=array([p0,p1])
    v=p1-p0
    a=ang(v[0],v[1])
    return arc(radius,a+90,a+270,p0,int(round(10+log10(radius+1)**6,0)))+arc(radius,a-90,a+90,p1,int(round(10+log10(radius+1)**6,0)))



def cleaning_seg(sec):
    r=-max_r(sec)-1
    s=seg(sec)
    s1=offset_points(sec,r)
    s2=seg(s1)
    u=array([(array(p[1])-array(p[0]))/linalg.norm(array(p[1])-array(p[0])) for p in s])
    u1=array([(array(p[1])-array(p[0]))/linalg.norm(array(p[1])-array(p[0])) for p in s2])
    s3=array(s)[linalg.norm(u-u1,axis=1)<1].tolist()
    return s3

def cleaning_sec_inner(sec,r):
    s=cleaning_seg(sec)
    s1=[rsec(p,abs(r)-.01) for p in s]
    return s1

def cleaning_sec_outer(sec,r):
    s=cleaning_seg(sec)
    s1=[rsec(p,abs(r)-.1) for p in s]
    return s1

# def inner_offset(sec,r):
#     sec=flip(sec) if cw(sec)==1 else sec
#     s=offset_points(sec,r)
#     if s_intv1(seg(s))!=[]:
#         s1=unique(s_intv(seg(s)),axis=0).tolist()
#         for p in cleaning_sec_inner(sec,r):
#             s2=pies1(p,s1)
#             s1=exclude_points(s1,s2)
#         s1=array(s1)[cKDTree(s1).query(sec)[1]].tolist()
#         return s1
#     else:
#         return s

def r_sec(r1,r2,cp1,cp2):
    l=tctpf(r1,r2,cp1,cp2)
    l=l[:2]+arc_2p(l[1],l[2],r1)+l[2:]+arc_2p(l[3],l[0],r2)
    return l

def inner_offset(sec,d):
    p=sec+[sec[0]]
    r=abs(d)
    a=array(sec)[array(list_r(sec))==0]
    a=seg(a)
    p1=array([a[i] for i in range(len(a)) if i%2!=0]).tolist()
    ol=[offset_l(p,d) for p in p1]
    om=seg(offset_points_cw(sec,d))
#     o_circles=array([tctp(r,r,p[i],p[i+1])for i in range(len(p)-1)])
    o_circle=offset_pointsv(sec,d)
    # ip1=s_intv1(seg(o_circles.reshape(-1,2)))
    ip1=s_intv1(ol+om)
    if ip1==[]:
#         op=sort_pointsv(sec,o_circles.reshape(-1,2))
        op=offset_pointsv(sec,d)
    else:
#         ocp=o_circles.reshape(-1,2).tolist()+ip1
        ocp=o_circle+ip1
        cs=[r_sec(r-.01,r-.01,p2[0],p2[1]) for p2 in p1]
        j=[pies(cs[i],ocp) for i in range(len(cs)) if pies(cs[i],ocp)!=[]]
        j= j if j==[] else concatenate(j)
        op=exclude_points(ocp,j)
        op=sort_pointsv(sec,op)
    return op

def out_offset(sec,r):
    sec=flip(sec) if cw(sec)==1 else sec
    s=offset_points(sec,r)
    if s_intv1(seg(s))!=[]:
        s1=unique(s_intv(seg(s)),axis=0).tolist()
        for p in cleaning_sec_outer(sec,r):
            s2=pies1(p,s1)
            s1=exclude_points(s1,s2)
        s1=array(s1)[cKDTree(s1).query(sec)[1]].tolist()
        return s1
    else:
        return s


def swp(bead2):
    n1=arange(len(bead2[0])).tolist()
    n2=array([[[[(j+1)+i*len(bead2[0]),j+i*len(bead2[0]),j+(i+1)*len(bead2[0])],[(j+1)+i*len(bead2[0]),j+(i+1)*len(bead2[0]),(j+1)+(i+1)*len(bead2[0])]] \
             if j<len(bead2[0])-1 else \
             [[0+i*len(bead2[0]),j+i*len(bead2[0]),j+(i+1)*len(bead2[0])],[0+i*len(bead2[0]),j+(i+1)*len(bead2[0]),0+(i+1)*len(bead2[0])]] \
                 for j in range(len(bead2[0]))] for i in range(len(bead2)-1)]).reshape(-1,3).tolist()
    n3=(array(flip(arange(len(bead2[0]))))+(len(bead2)-1)*len(bead2[0])).tolist()
    n=[n1]+n2+[n3]
    pnt=array(bead2).reshape(-1,3).round(4).tolist()
    return f'polyhedron({pnt},{n},convexity=10);'

def swp_c(bead2):
    n1=arange(len(bead2[0])).tolist()
    n2=array([[[[(j+1)+i*len(bead2[0]),j+i*len(bead2[0]),j+(i+1)*len(bead2[0])],[(j+1)+i*len(bead2[0]),j+(i+1)*len(bead2[0]),(j+1)+(i+1)*len(bead2[0])]] \
             if j<len(bead2[0])-1 else \
             [[0+i*len(bead2[0]),j+i*len(bead2[0]),j+(i+1)*len(bead2[0])],[0+i*len(bead2[0]),j+(i+1)*len(bead2[0]),0+(i+1)*len(bead2[0])]] \
                 for j in range(len(bead2[0]))] for i in range(len(bead2)-1)]).reshape(-1,3).tolist()
    n3=(array(flip(arange(len(bead2[0]))))+(len(bead2)-1)*len(bead2[0])).tolist()
    n=[n1]+n2+[n3]
    pnt=array(bead2).reshape(-1,3).round(4).tolist()
    return f'polyhedron({pnt},{n2},convexity=10);'

def resurf(surf,f):
    base=array(c3t2(surf)).reshape(-1,2).tolist()
    c=[]
    for i in range(len(surf)):
        if len(base)<=2:
            break
        else:
            base1=concave_hull(base,f)
            base=exclude_points(base,base1)
            c.append(base1)
    base=concave_hull(array(c3t2(surf)).reshape(-1,2).tolist(),f)
    c=[array(p)[cKDTree(p).query(base)[1]].tolist() for p in c]
    base=array(c3t2(surf)).reshape(-1,2).tolist()
    surf=array(surf).reshape(-1,3)
    c= [surf[cKDTree(base).query(p)[1]].tolist() for p in c]
    return c

def surf_extrudef(surf,t=-.05):
    '''
    surface with a polyline 2d sketch and a 3d path. thickness of the surface can be set with parameter "t". 
    positive and negative value creates thickness towards +z and -z directions respectively
    refer file "example of various functions"
    '''
    s=cpo(surf)
    s1=trns([0,0,t],[flip(p) for p in s])
    s2=array([s,s1]).transpose(1,0,2,3)
    
    i,j,k,l=s2.shape
    s2=s2.reshape(i,j*k,l).tolist()
    return s2 if t>0 else flip(s2)



def swp_prism_h(prism_big,prism_small):
    p1=prism_big
    p2=flip(prism_small)
    p3=p1+p2+[p1[0]]
    return p3
    
def pmdp(line,pnts): #perpendicular minimum distance point
    if pnts==[]:
        return line
    else:
        a=[perp_dist(line,p) for p in pnts]
        b=array(pnts)[min(a)==array(a)][0].tolist()
        return [line[0],b,line[1]]
    


def surf_base(surf,h=0):
    s=cpo(surf)
    s1=trns([0,0,h],c2t3(c3t2([flip(p) for p in s])))
    s2=array([s,s1]).transpose(1,0,2,3)
    
    i,j,k,l=s2.shape
    s2=s2.reshape(i,j*k,l).tolist()
    t=array(surf).reshape(-1,3).mean(0)[2]
    return s2 if h>t else flip(s2)

def cr_3d(p,s=5): # Corner radius 3d where 'p' are the list of points (turtle movement) and 's' is number of segments for each arc
    pnts=array(p)[:,0:3]
    pnts=pnts.cumsum(0)

    rds=array(p)[:,3]
    c=[]
    for i in range(len(pnts)):
        if i==0:
            p0=pnts[len(pnts)-1]
            p1=pnts[i]
            p2=pnts[i+1]
        elif i<len(pnts)-1:
            p0=pnts[i-1]
            p1=pnts[i]
            p2=pnts[i+1]
        else:
            p0=pnts[i-1]
            p1=pnts[i]
            p2=pnts[0]
        c.append(fillet_3p_3d(p0,p1,p2,rds[i],s)[1:])
    c=array(c).reshape(-1,3).tolist()
    return remove_extra_points(c) 

def p_exc(sec,path,option=0):
    p=array(path)
    c,d,e=[],[],[]
    a2,j=0,0
    for i in range(len(p)):
        i_plus=i+1 if i<len(p)-1 else 0
        p0=p[i]
        p1=p[i_plus]
        v1=uv(p1-p0)
        vz=[0,0,1]
        v2=cross(vz,v1).tolist()
        theta=0 if v2==[0,0,0] else arccos(array(vz)@array(v1))*180/pi
        a=0 if theta==0 else ang(v2[0],v2[1])
        a1=0 if v1[2]==0 else ang(v1[0],v1[1]) if v1[2]<0 else -ang(v1[0],v1[1])
        d.append(a1)
        if i>0:
            j= j+1 if abs(a1-d[i-1])>179 else j
            e.append(j)
            a2=a1+j*180
        if option==0:
            sec1=trns(path[i],[q(v2,q([0,0,1],p,a+a2),theta) for p in sec])
        else:
            sec1=trns(path[i],[q(v2,q([0,0,1],p,a+a1),theta) for p in sec])
            
        c.append(sec1)
    c=c+[c[0]]
    return c

def p_ex(sec,path,option=0):
    p=array(path)
    c,d,e=[],[],[]
    a2,j=0,0
    for i in range(len(p)-1):
        i_plus=i+1 if i<len(p)-1 else 0
        p0=p[i]
        p1=p[i_plus]
        v1=uv(p1-p0)
        vz=[0,0,1]
        v2=cross(vz,v1).tolist()
        theta=0 if v2==[0,0,0] else arccos(array(vz)@array(v1))*180/pi
        a=0 if theta==0 else ang(v2[0],v2[1])
        a1=0 if v1[2]==0 else ang(v1[0],v1[1]) if v1[2]<0 else -ang(v1[0],v1[1])
        d.append(a1)
        if i>0:
            j= j+1 if abs(abs(a1)-d[i-1])>100 else j
            e.append(j)
            a2=a1+j*180
        if option==0:
            sec1=trns(path[i],[q(v2,q([0,0,1],p,a+a2),theta) for p in sec])
        else:
            sec1=trns(path[i],[q(v2,q([0,0,1],p,a+a1),theta) for p in sec])
            
        c.append(sec1)
    c=c+[trns(array(path[-1])-array(path[-2]),c[-1])]
    return c

def helix(radius=10,pitch=10, number_of_coils=1, step_angle=1):
    return [[radius*cos(i*pi/180),radius*sin(i*pi/180),i/360*pitch] for i in arange(0,360*number_of_coils,step_angle)]

def surf_offset(surf,o):
    c=[]
    for i in range(len(surf)):
        for j in range(len(surf[0])):
            j_plus=j+1 if j<len(surf[0])-1 else 0
            p0=surf[i][j]
            p1=surf[i][j_plus] if i<len(surf)-1 else surf[i-1][j]
            p2=surf[i+1][j] if i<len(surf)-1 else surf[i][j_plus]
            p0,p1,p2=array([p0,p1,p2])
            v1=p1-p0
            v2=p2-p0
            p=p0+array(uv(cross(v1,v2)))*o
            c.append(p.tolist())
    l,m,n=array(surf).shape
    return array(c).reshape(l,m,n).tolist()

def path_to_vectors(path):
    c=[]
    for i in range(len(path)):
        i_plus=i+1 if i<len(path)-1 else 0
        p0=path[i]
        p1=path[i_plus]
        p0,p1=array([p0,p1])
        v1=p1-p0
        c.append(v1.round(4).tolist())
    return vector_correct(c)

def vector_correct(c):
    for i in range(len(c)):
        if i>0 and i<len(c)-1:
            if c[i][0]==0 and abs(c[i-1][0])>0 and abs(c[i+1][0])>0:
                c[i][0]=.001
            if c[i][1]==0 and abs(c[i-1][1])>0 and abs(c[i+1][1])>0:
                c[i][1]=.001
            if c[i][2]==0 and abs(c[i-1][2])>0 and abs(c[i+1][2])>0:
                c[i][2]=.001
    path=c
    return path

def concave_hull(pnts,x=1,loops=10):
    '''
    x is sensitivity where 1 is max and 100 is almost like a convex hull, 
    loops can be any number less than the number of points
    refer file "example of various functions" for application example
    '''
    c=c_hull(pnts)
    for j in range(loops):
        c1=seg(c)
        pnts1=exclude_points(pnts,c)
        c2=[]
        for i in range(len(c1)):
            p0,p1=array(c1[i])
            v1=p1-p0
            u1=array(uv(v1))
            v1norm=linalg.norm(v1)
            pnts2=[p for p in array(pnts1) if ((u1@(p-p0))>=0)&((u1@(p-p0))<=v1norm) & (abs(cross(v1,p-p0))/v1norm <= v1norm/x) ]
            if pnts2!=[]:
                lengths=[cross(v1,(p-p0))/v1norm for p in array(pnts2)]
                pnt=array(pnts2)[lengths==min(lengths)][0]
                pnts1=exclude_points(pnts1,pnt)
                c2.append([p0.tolist(),pnt.tolist(),p1.tolist()])
            else:
                c2.append(c1[i])


        c3=remove_extra_points(concatenate(c2).tolist())
        n=s_intv1(seg(c3))
        if n!=[]:
            d=[[p[1] for p1 in array(n) if (array(uv(p1-p[0])).round(4)==array(uv(p[1]-p[0])).round(4)).all() ] for p in array(seg(c3))]
            d=concatenate([p for p in d if p!=[]]).tolist()
            c3=exclude_points(c3,d)
        c=c3
    while s_intv1(seg(c))!=[]:
        n=s_intv1(seg(c3))
        if n==[]:
            break
        else:
            d=[[p[1] for p1 in array(n) if (array(uv(p1-p[0])).round(4)==array(uv(p[1]-p[0])).round(4)).all() ] for p in array(seg(c3))]
            d=concatenate([p for p in d if p!=[]]).tolist()
            c3=exclude_points(c3,d)
        
        
    return c3


# def ipfillet(p,p1,r=1,s=5,o=0):
  
#     pa=[[[[p[i][j],p[i][j+1],p[i+1][j]],[p[i+1][j+1],p[i+1][j],p[i][j+1]]] if j<len(p[0])-1 else \
#          [[p[i][j],p[i][0],p[i+1][j]],[p[i+1][0],p[i+1][j],p[i][0]]] \
#          for j in arange(len(p[0]))] for i in arange(len(p)-1)]
#     pa=array(pa).reshape(-1,3,3)

#     pb=[[[p1[i][j],p1[i+1][j]] for j in arange(len(p1[0]))] for i in arange(len(p1)-1)]
#     pb=array(pb).reshape(-1,2,3)
#     a1,a2,a3=pa[:,0],pa[:,1],pa[:,2]
#     b1,b2=pb[:,0],pb[:,1]
#     v1,v2,v3=b2-b1,a2-a1,a3-a1
#     i,j=len(v1),len(v2)
#     v1=v1.repeat(j,0)
#     v2=array((v2).tolist()*i)
#     v3=array((v3).tolist()*i)
#     c=linalg.pinv(array([v1,-v2,-v3]).transpose(1,0,2).transpose(0,2,1))
#     d=array(a1.tolist()*i)-b1.repeat(j,0)
#     t=einsum('ijk,ik->ij',c,d)
#     p0=b1.repeat(j,0)
#     pnt=p0+einsum('ij,i->ij',v1,t[:,0])
#     v1norm=1/sqrt(einsum('ij,ij->i',v1,v1))
#     u1=einsum('ij,i->ij',v1,v1norm)
#     pnt1=pnt+u1*r
#     cond=(t[:,0]>=0)&(t[:,0]<=1)&(t[:,1]>=0)&(t[:,1]<=1)&(t[:,2]>=0)&(t[:,2]<=1)&((t[:,1]+t[:,2])>=0)&((t[:,1]+t[:,2])<=1)
#     pnt=pnt[cond]
#     pnt1=pnt1[cond]
#     ip=array([pnt,pnt1]).transpose(1,0,2)
#     if o==0:
#         e=[ip[i][0]+array(uv(cross(ip[i+1][0]-ip[i][0],ip[i][1]-ip[i][0])))*r if i<len(ip)-1 else \
#            ip[i][0]+array(uv(cross(ip[0][0]-ip[i][0],ip[i][1]-ip[i][0])))*r \
#            for i in arange(len(ip))]
#     elif o==1:
#         e=[ip[i][0]+array(uv(cross(ip[i][1]-ip[i][0],ip[i+1][0]-ip[i][0])))*r if i<len(ip)-1 else \
#            ip[i][0]+array(uv(cross(ip[i][1]-ip[i][0],ip[0][0]-ip[i][0])))*r \
#            for i in arange(len(ip))]

#     f=[[ip[i][0]+q(ip[i+1][0]-ip[i][0],e[i]-ip[i][0], theta) if i<len(ip)-1 else \
#         ip[i][0]+q(ip[0][0]-ip[i][0],e[i]-ip[i][0] , theta) \
#         for theta in linspace(-90,90,3)] for i in arange(len(ip))]
#     f=array([seg(array(p).tolist())[0:-1] for p in f]).reshape(-1,2,3)

#     a1,a2,a3=pa[:,0],pa[:,1],pa[:,2]
#     b1,b2=f[:,0],f[:,1]
#     v1,v2,v3=b2-b1,a2-a1,a3-a1
#     i,j=len(v1),len(v2)
#     v1=v1.repeat(j,0)
#     v2=array((v2).tolist()*i)
#     v3=array((v3).tolist()*i)
#     c=linalg.pinv(array([v1,-v2,-v3]).transpose(1,0,2).transpose(0,2,1))
#     d=array(a1.tolist()*i)-b1.repeat(j,0)
#     t=einsum('ijk,ik->ij',c,d)
#     p0=b1.repeat(j,0)
#     pnt2=p0+einsum('ij,i->ij',v1,t[:,0])
#     cond=(t[:,0]>=0)&(t[:,0]<=1)&(t[:,1]>=0)&(t[:,1]<=1)&(t[:,2]>=0)&(t[:,2]<=1)&((t[:,1]+t[:,2])>=0)&((t[:,1]+t[:,2])<=1)
#     pnt2=pnt2[cond]

#     g=array([pnt2,pnt,pnt1]).transpose(1,0,2)
#     h=[fillet_3p_3d(p0,p1,p2,r_3p_3d([p0,p1,p2]),s) for (p0,p1,p2) in g]

#     return h+[h[0]]

def path_extrude(sec,path):
    '''
    function to extrude a section 'sec' along a open path 'path'
    refer to file "example of various functions" for application example
    '''
    s=q_rot(['x90','z-90'],sec)
    p=array(path)
    s2=[]
    for i in range(len(p)-1):
        v1=p[i+1]-p[i]+array([0,0,0.00001])
        va=[v1[0],v1[1],0]
        u1=array(uv(v1))
        ua=array(uv(va))
        v2=cross(va,v1)
        a1=arccos(u1@ua)*180/pi
        a2=ang(v1[0],v1[1])
        s1=q_rot([f'z{a2}'],s)
        if i<len(p)-1:
            s2.append(trns(p[i],[q(v2,p,a1) for p in s1]))
        else:
            s2.append(trns(p[i],[q(v2,p,a1) for p in s1]))
            s2.append(trns(p[i+1],[q(v2,p,a1) for p in s1]))
        
    return flip(s2)

def path_extrudec(sec,path):
    '''
    function to extrude a section 'sec' along a closed loop path 'path'
    refer to file "example of various functions" for application example
    '''
    s=q_rot(['x90','z-90'],sec)
    p=array(path)
    s2=[]
    for i in range(len(p)):
        v1=(p[i+1]-p[i] if i<len(p)-1 else p[0]-p[i])+array([0,0,0.00001])
        va=[v1[0],v1[1],0]
        u1=array(uv(v1))
        ua=array(uv(va))
        v2=cross(va,v1)
        a1=arccos(u1@ua)*180/pi
        a2=ang(v1[0],v1[1])
        s1=q_rot([f'z{a2}'],s)
        s2.append(trns(p[i],[q(v2,p,a1) for p in s1]))
        
    return flip(s2+[s2[0]])


def multiple_sec_extrude(path_points=[],radiuses_list=[],sections_list=[],option=0,s=10):
    '''
    explanation of the function 'multiple_sec_extrude'
    path_points: are the points at which sections needs to be placed,
    radiuses: radius required at each path_point. this can be '0' in case no radius required in the path
    sections_list= list of sections required at each path_points. same section can be provided for various path_points as well
    option: can be '0' in case the number of points in each section do not match or '1' in case number of points for each section are same
    s: in case value of radiuses is provided 's' is the number of segments in that path curve
    
    refer to file "example of various functions" for application example
    '''
    p=array(path_points)
    r=radiuses_list
    if option==0:
        sections=[sections_list[0]]+[sort_pointsv(sections_list[0],p) for p in sections_list[1:]]
    else:
        sections=sections_list
        
    s1=[]
    for i in range(len(p)):
        if r[i]==0 and i<len(p)-1:
            p0=p[i].tolist()
            p1=(p0+(p[i+1]-p[i])*.01).tolist()
            s1.append([p0,p1])
        elif r[i]==0 and i==len(p)-1:
            p0=p[i].tolist()
            p1=(p0+(p[i]-p[i-1])*.01).tolist()
            s1.append([p0,p1])
        else:
            s1.append(fillet_3p_3d(p[i-1],p[i],p[i+1],r[i],s)[1:])
    
    s1=[remove_extra_points(p) for p in s1]

    s4=[]
    for i in range(len(s1)):
        for j in range(len(s1[i])-1):
            p0,p1=array([s1[i][j],s1[i][j+1]])
            v1=p1-p0
            va=[v1[0],v1[1]+.00001,0]
            u1=array(uv(v1))
            ua=array(uv(va))
            v2=cross(v1,va)
            a1=arccos(u1@ua)*180/pi
            a2=ang(v1[0],v1[1])
            s2=q_rot(['x90','z-90',f'z{a2}'],sections[i])
            s3=trns(p0,flip([q(v2,p,-a1) for p in s2]))
            s4.append(s3)
    return s4

def pntsnfaces(bead2):
    '''
    function returns points and faces of a prism
    refer file "example of various functions" for application example
    '''
    n1=arange(len(bead2[0])).tolist()
    n2=array([[[[(j+1)+i*len(bead2[0]),j+i*len(bead2[0]),j+(i+1)*len(bead2[0])],[(j+1)+i*len(bead2[0]),j+(i+1)*len(bead2[0]),(j+1)+(i+1)*len(bead2[0])]] \
             if j<len(bead2[0])-1 else \
             [[0+i*len(bead2[0]),j+i*len(bead2[0]),j+(i+1)*len(bead2[0])],[0+i*len(bead2[0]),j+(i+1)*len(bead2[0]),0+(i+1)*len(bead2[0])]] \
                 for j in range(len(bead2[0]))] for i in range(len(bead2)-1)]).reshape(-1,3).tolist()
    n3=(array(flip(arange(len(bead2[0]))))+(len(bead2)-1)*len(bead2[0])).tolist()
    n=[n1]+n2+[n3]
    pnt=array(bead2).reshape(-1,3).round(4).tolist()
    return [pnt,n]

def path_offset(path,d):
    '''
    function to offset a 'path' by 'd' distance
    refer file "example of various functions" for application example
    '''
    p=array([offset_l(p,d) for p in seg(path)[:-1]])
    return p[:,0].tolist()+[p[len(p)-1][1].tolist()]


def fillet_sol2sol(p=[],p1=[],r=1,s=10,o=0):
    ''' 
    function to calculate fillet at the intersection point of 2 solids
    'p': solid 1
    'p1': solid 2
    'r': radius of the fillet
    's': number of segments in the fillet, more number of segments will give finer finish
    'o': option '0' produces fillet in outer side of the intersection and '1' in the inner side of the intersections
    refer file "example of various functions" for application example
    '''
    pa=[[[[p[i][j],p[i][j+1],p[i+1][j]],[p[i+1][j+1],p[i+1][j],p[i][j+1]]] if j<len(p[0])-1 else \
         [[p[i][j],p[i][0],p[i+1][j]],[p[i+1][0],p[i+1][j],p[i][0]]] \
         for j in range(len(p[0]))] for i in range(len(p)-1)]
    pa=array(pa).reshape(-1,3,3)

#     pb=[[[p1[i][j],p1[i+1][j]] for j in range(len(p1[0]))] for i in range(len(p1)-1)]
#     pb=array(pb).reshape(-1,2,3)
    p2=cpo(p1)
    pb=[[[p2[i][j],p2[i][j+1]] for j in range(len(p2[0])-1)] for i in range(len(p2))]
    pb=array(pb).reshape(-1,2,3)
    
    p01,p02,p03,p04,p05=pa[:,0],pa[:,1],pa[:,2],pb[:,0],pb[:,1]

    v1,v2,v3=p05-p04,p02-p01,p03-p01
    i,j=len(v1),len(v2)
#     array([(-v1).tolist()]*j).transpose(1,0,2).shape,array([v2]*i).shape,array([cross(v2,v3)]*i).shape,(p04[:,None]-p01).shape
#     cross(v3,-v1[:,None]).shape,cross(-v1[:,None],v2).shape
    a=einsum('ijk,ijk->ij',array([cross(v2,v3)]*i),p04[:,None]-p01)
    b=(1/einsum('ijk,ijk->ij',array([-v1]*j).transpose(1,0,2),array([cross(v2,v3)+.00001]*i)))
    t1=einsum('ij,ij->ij',a,b)

    a=einsum('ijk,ijk->ij',cross(v3,-v1[:,None]),p04[:,None]-p01)
    b=(1/einsum('ijk,ijk->ij',array([-v1]*j).transpose(1,0,2),array([cross(v2,v3)+.00001]*i)))
    t2=einsum('ij,ij->ij',a,b)

    a=einsum('ijk,ijk->ij',cross(-v1[:,None],v2),p04[:,None]-p01)
    b=(1/einsum('ijk,ijk->ij',array([-v1]*j).transpose(1,0,2),array([cross(v2,v3)+.00001]*i)))
    t3=einsum('ij,ij->ij',a,b)

    condition=(t1>=0) & (t1<=1) & (t2>=0) & (t2<=1) & (t3>=0) & (t3<=1) & (t2+t3>=0) & (t2+t3<=1)
#     condition.shape

    pnt1=(p04[:,None]+einsum('ijk,ij->ijk',array([v1]*j).transpose(1,0,2),t1))[condition]
#     pnt1.shape

    uv1=v1/linalg.norm(v1,axis=1).reshape(-1,1)
    uv1=array([uv1]*j).transpose(1,0,2)[condition]
#     uv1.shape
#     pnt2=pnt1+uv1*r

    a=cross(v2,v3)
    b=a/(linalg.norm(a,axis=1).reshape(-1,1)+.00001)
    b=array([b]*i)[condition]
#     b.shape

    nxt_pnt=array(pnt1[1:].tolist()+[pnt1[0]])
    v_rot=nxt_pnt-pnt1

    if o==0:
        cir=array([[pnt1[i]+array(q(v_rot[i],b[i]*r,t)) for t in linspace(0,180,5)] for i in arange(len(pnt1))]).tolist()
    else:
        cir=array([[pnt1[i]+array(q(v_rot[i],b[i]*r,-t)) for t in linspace(0,180,5)] for i in arange(len(pnt1))]).tolist()

    pc=array([[[cir[i][j],cir[i][j+1]]  for j in arange(len(cir[0])-1)] for i in arange(len(cir))]).reshape(-1,2,3)
#     pc.shape

    p01,p02,p03,p04,p05=pa[:,0],pa[:,1],pa[:,2],pc[:,0],pc[:,1]

    v1,v2,v3=p05-p04,p02-p01,p03-p01
    i,j=len(v1),len(v2)

    a1=einsum('ijk,ijk->ij',array([cross(v2,v3)]*i),p04[:,None]-p01)
    b1=(1/einsum('ijk,ijk->ij',array([-v1]*j).transpose(1,0,2),array([cross(v2,v3)+.00001]*i)))
    t1=einsum('ij,ij->ij',a1,b1)

    a1=einsum('ijk,ijk->ij',cross(v3,-v1[:,None]),p04[:,None]-p01)
    b1=(1/einsum('ijk,ijk->ij',array([-v1]*j).transpose(1,0,2),array([cross(v2,v3)+.00001]*i)))
    t2=einsum('ij,ij->ij',a1,b1)

    a1=einsum('ijk,ijk->ij',cross(-v1[:,None],v2),p04[:,None]-p01)
    b1=(1/einsum('ijk,ijk->ij',array([-v1]*j).transpose(1,0,2),array([cross(v2,v3)+.00001]*i)))
    t3=einsum('ij,ij->ij',a1,b1)

    condition=(t1>=0) & (t1<=1) & (t2>=0) & (t2<=1) & (t3>=0) & (t3<=1) & (t2+t3>=0) & (t2+t3<=1)
#     condition.shape

    pnt3=(p04[:,None]+einsum('ijk,ij->ijk',array([v1]*j).transpose(1,0,2),t1))[condition]
    pnt3=sort_pointsv(pnt1,pnt3) if len(pnt1)!=len(pnt3) else pnt3.tolist()

#     if o==0:
    cir=array([[pnt1[i]+array(q(v_rot[i],b[i]*r,-t)) for t in linspace(-90,90,5)] for i in arange(len(pnt1))]).tolist()
#     else:
#         cir=array([[pnt1[i]+array(q(v_rot[i],b[i]*r,t)) for t in linspace(-90,90,5)] for i in arange(len(pnt1))]).tolist()
    
    pa=[[[[p1[i][j],p1[i][j+1],p1[i+1][j]],[p1[i+1][j+1],p1[i+1][j],p1[i][j+1]]] if j<len(p1[0])-1 else \
         [[p1[i][j],p1[i][0],p1[i+1][j]],[p1[i+1][0],p1[i+1][j],p1[i][0]]] \
         for j in range(len(p1[0]))] for i in range(len(p1)-1)]
    pa=array(pa).reshape(-1,3,3)
    
    pc=array([[[cir[i][j],cir[i][j+1]]  for j in arange(len(cir[0])-1)] for i in arange(len(cir))]).reshape(-1,2,3)

    p01,p02,p03,p04,p05=pa[:,0],pa[:,1],pa[:,2],pc[:,0],pc[:,1]

    v1,v2,v3=p05-p04,p02-p01,p03-p01
    i,j=len(v1),len(v2)

    a1=einsum('ijk,ijk->ij',array([cross(v2,v3)]*i),p04[:,None]-p01)
    b1=(1/einsum('ijk,ijk->ij',array([-v1]*j).transpose(1,0,2),array([cross(v2,v3)+.00001]*i)))
    t1=einsum('ij,ij->ij',a1,b1)

    a1=einsum('ijk,ijk->ij',cross(v3,-v1[:,None]),p04[:,None]-p01)
    b1=(1/einsum('ijk,ijk->ij',array([-v1]*j).transpose(1,0,2),array([cross(v2,v3)+.00001]*i)))
    t2=einsum('ij,ij->ij',a1,b1)

    a1=einsum('ijk,ijk->ij',cross(-v1[:,None],v2),p04[:,None]-p01)
    b1=(1/einsum('ijk,ijk->ij',array([-v1]*j).transpose(1,0,2),array([cross(v2,v3)+.00001]*i)))
    t3=einsum('ij,ij->ij',a1,b1)

    condition=(t1>=0) & (t1<=1) & (t2>=0) & (t2<=1) & (t3>=0) & (t3<=1) & (t2+t3>=0) & (t2+t3<=1)
#     condition.shape

    pnt2=(p04[:,None]+einsum('ijk,ij->ijk',array([v1]*j).transpose(1,0,2),t1))[condition]
    pnt2=sort_pointsv(pnt1,pnt2) if len(pnt2)!=len(pnt1) else pnt2.tolist()

    
    sol=array([pnt3,pnt1,pnt2]).transpose(1,0,2)
    sol=[fillet_3p_3d(p3,p2,p1,r_3p_3d([p1,p2,p3])*1.9,s) for (p1,p2,p3) in sol]
    sol=sol+[sol[0]]
    return sol

def fillet_surf2sol(p=[],p1=[],r=1,s=10,o=0):
    '''
    function to calculate fillet at the intersection point of 2 solids
    'p': solid 1
    'p1': solid 2
    'r': radius of the fillet
    's': number of segments in the fillet, more number of segments will give finer finish
    'o': option '0' produces fillet in outer side of the intersection and '1' in the inner side of the intersections
    refer file "example of various functions" for application
    '''
    pa=[[[[p[i][j],p[i][j+1],p[i+1][j]],[p[i+1][j+1],p[i+1][j],p[i][j+1]]] if j<len(p[0])-1 else \
         [[p[i][j],p[i][0],p[i+1][j]],[p[i+1][0],p[i+1][j],p[i][0]]] \
         for j in range(len(p[0])-1)] for i in range(len(p)-1)]
    pa=array(pa).reshape(-1,3,3)

#     pb=[[[p1[i][j],p1[i+1][j]] for j in range(len(p1[0]))] for i in range(len(p1)-1)]
#     pb=array(pb).reshape(-1,2,3)
    p2=cpo(p1)
    pb=[[[p2[i][j],p2[i][j+1]] for j in range(len(p2[0])-1)] for i in range(len(p2))]
    pb=array(pb).reshape(-1,2,3)
    
    p01,p02,p03,p04,p05=pa[:,0],pa[:,1],pa[:,2],pb[:,0],pb[:,1]

    v1,v2,v3=p05-p04,p02-p01,p03-p01
    i,j=len(v1),len(v2)
#     array([(-v1).tolist()]*j).transpose(1,0,2).shape,array([v2]*i).shape,array([cross(v2,v3)]*i).shape,(p04[:,None]-p01).shape
#     cross(v3,-v1[:,None]).shape,cross(-v1[:,None],v2).shape
    a=einsum('ijk,ijk->ij',array([cross(v2,v3)]*i),p04[:,None]-p01)
    b=(1/einsum('ijk,ijk->ij',array([-v1]*j).transpose(1,0,2),array([cross(v2,v3)+.00001]*i)))
    t1=einsum('ij,ij->ij',a,b)

    a=einsum('ijk,ijk->ij',cross(v3,-v1[:,None]),p04[:,None]-p01)
    b=(1/einsum('ijk,ijk->ij',array([-v1]*j).transpose(1,0,2),array([cross(v2,v3)+.00001]*i)))
    t2=einsum('ij,ij->ij',a,b)

    a=einsum('ijk,ijk->ij',cross(-v1[:,None],v2),p04[:,None]-p01)
    b=(1/einsum('ijk,ijk->ij',array([-v1]*j).transpose(1,0,2),array([cross(v2,v3)+.00001]*i)))
    t3=einsum('ij,ij->ij',a,b)

    condition=(t1>=0) & (t1<=1) & (t2>=0) & (t2<=1) & (t3>=0) & (t3<=1) & (t2+t3>=0) & (t2+t3<=1)
#     condition.shape

    pnt1=(p04[:,None]+einsum('ijk,ij->ijk',array([v1]*j).transpose(1,0,2),t1))[condition]
#     pnt1.shape

    uv1=v1/linalg.norm(v1,axis=1).reshape(-1,1)
    uv1=array([uv1]*j).transpose(1,0,2)[condition]
#     uv1.shape
#     pnt2=pnt1+uv1*r

    a=cross(v2,v3)
    b=a/(linalg.norm(a,axis=1).reshape(-1,1)+.00001)
    b=array([b]*i)[condition]
#     b.shape

    nxt_pnt=array(pnt1[1:].tolist()+[pnt1[0]])
    v_rot=nxt_pnt-pnt1

    if o==0:
        cir=array([[pnt1[i]+array(q(v_rot[i],b[i]*r,t)) for t in linspace(0,180,5)] for i in arange(len(pnt1))]).tolist()
    else:
        cir=array([[pnt1[i]+array(q(v_rot[i],b[i]*r,-t)) for t in linspace(0,180,5)] for i in arange(len(pnt1))]).tolist()

    pc=array([[[cir[i][j],cir[i][j+1]]  for j in arange(len(cir[0])-1)] for i in arange(len(cir))]).reshape(-1,2,3)
#     pc.shape

    p01,p02,p03,p04,p05=pa[:,0],pa[:,1],pa[:,2],pc[:,0],pc[:,1]

    v1,v2,v3=p05-p04,p02-p01,p03-p01
    i,j=len(v1),len(v2)

    a1=einsum('ijk,ijk->ij',array([cross(v2,v3)]*i),p04[:,None]-p01)
    b1=(1/einsum('ijk,ijk->ij',array([-v1]*j).transpose(1,0,2),array([cross(v2,v3)+.00001]*i)))
    t1=einsum('ij,ij->ij',a1,b1)

    a1=einsum('ijk,ijk->ij',cross(v3,-v1[:,None]),p04[:,None]-p01)
    b1=(1/einsum('ijk,ijk->ij',array([-v1]*j).transpose(1,0,2),array([cross(v2,v3)+.00001]*i)))
    t2=einsum('ij,ij->ij',a1,b1)

    a1=einsum('ijk,ijk->ij',cross(-v1[:,None],v2),p04[:,None]-p01)
    b1=(1/einsum('ijk,ijk->ij',array([-v1]*j).transpose(1,0,2),array([cross(v2,v3)+.00001]*i)))
    t3=einsum('ij,ij->ij',a1,b1)

    condition=(t1>=0) & (t1<=1) & (t2>=0) & (t2<=1) & (t3>=0) & (t3<=1) & (t2+t3>=0) & (t2+t3<=1)
#     condition.shape

    pnt3=(p04[:,None]+einsum('ijk,ij->ijk',array([v1]*j).transpose(1,0,2),t1))[condition]
    pnt3=sort_pointsv(pnt1,pnt3) if len(pnt3)!= len(pnt1) else pnt3.tolist()

#     if o==0:
    cir=array([[pnt1[i]+array(q(v_rot[i],b[i]*r,-t)) for t in linspace(-90,90,5)] for i in arange(len(pnt1))]).tolist()
#     else:
#         cir=array([[pnt1[i]+array(q(v_rot[i],b[i]*r,t)) for t in linspace(-90,90,5)] for i in arange(len(pnt1))]).tolist()
    
    pa=[[[[p1[i][j],p1[i][j+1],p1[i+1][j]],[p1[i+1][j+1],p1[i+1][j],p1[i][j+1]]] if j<len(p1[0])-1 else \
         [[p1[i][j],p1[i][0],p1[i+1][j]],[p1[i+1][0],p1[i+1][j],p1[i][0]]] \
         for j in range(len(p1[0]))] for i in range(len(p1)-1)]
    pa=array(pa).reshape(-1,3,3)
    
    pc=array([[[cir[i][j],cir[i][j+1]]  for j in arange(len(cir[0])-1)] for i in arange(len(cir))]).reshape(-1,2,3)

    p01,p02,p03,p04,p05=pa[:,0],pa[:,1],pa[:,2],pc[:,0],pc[:,1]

    v1,v2,v3=p05-p04,p02-p01,p03-p01
    i,j=len(v1),len(v2)

    a1=einsum('ijk,ijk->ij',array([cross(v2,v3)]*i),p04[:,None]-p01)
    b1=(1/einsum('ijk,ijk->ij',array([-v1]*j).transpose(1,0,2),array([cross(v2,v3)+.00001]*i)))
    t1=einsum('ij,ij->ij',a1,b1)

    a1=einsum('ijk,ijk->ij',cross(v3,-v1[:,None]),p04[:,None]-p01)
    b1=(1/einsum('ijk,ijk->ij',array([-v1]*j).transpose(1,0,2),array([cross(v2,v3)+.00001]*i)))
    t2=einsum('ij,ij->ij',a1,b1)

    a1=einsum('ijk,ijk->ij',cross(-v1[:,None],v2),p04[:,None]-p01)
    b1=(1/einsum('ijk,ijk->ij',array([-v1]*j).transpose(1,0,2),array([cross(v2,v3)+.00001]*i)))
    t3=einsum('ij,ij->ij',a1,b1)

    condition=(t1>=0) & (t1<=1) & (t2>=0) & (t2<=1) & (t3>=0) & (t3<=1) & (t2+t3>=0) & (t2+t3<=1)
#     condition.shape

    pnt2=(p04[:,None]+einsum('ijk,ij->ijk',array([v1]*j).transpose(1,0,2),t1))[condition]
    pnt2=sort_pointsv(pnt1,pnt2) if len(pnt2)!= len(pnt1) else pnt2.tolist()

    
    sol=array([pnt3,pnt1,pnt2]).transpose(1,0,2)
    sol=[fillet_3p_3d(p3,p2,p1,r_3p_3d([p1,p2,p3])*1.9,s) for (p1,p2,p3) in sol]
    sol=sol+[sol[0]]
    return sol