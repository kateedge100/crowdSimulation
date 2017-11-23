import maya.cmds as cmds
import random as rand
import math as math
def setupScene(sizeOfBox, numOfBalls, ballRadius):
	cmds.polyCube(depth = sizeOfBox, height = sizeOfBox, width = sizeOfBox)
	ballArray = []
	ballNameArray = []
	for i in range(numOfBalls):
		posx = (rand.random()-0.5)*(sizeOfBox-ballRadius*2.0)
		posy = ballRadius
		
		posz = (rand.random()-0.5)*(sizeOfBox-ballRadius*2.0)
		velocityX = (rand.random()-0.5)/20
		velocityY = 0
		velocityZ = (rand.random()-0.5)/20
		ballName = cmds.sphere(r=ballRadius)
		cmds.move(posx, posy, posz, ballName[0])
		ballNameArray.append(ballName[0])
		ballArray.append([ballName[0], [posx, posy, posz],[velocityX, velocityY, velocityZ]])
	cmds.group(ballNameArray, name = "balls")
	return ballArray
	
def collisionWithWalls(sizeOfBox, numOfBalls, ballRadius, ballArray):
	# a, b, c, d of plane equation
	wallEquationArray = [(1, 0, 0, sizeOfBox/2.0), (-1, 0, 0, sizeOfBox/2.0), (0, 1, 0, sizeOfBox/2.0), (0, -1, 0, sizeOfBox/2.0), (0, 0, 1, sizeOfBox/2.0), (0, 0, -1, sizeOfBox/2.0)] 
	numOfWalls = len(wallEquationArray)
	for i in range(numOfBalls):
		for j in range(numOfWalls):
			distToWall = ballArray[i][1][0]*wallEquationArray[j][0] + ballArray[i][1][1]*wallEquationArray[j][1] + ballArray[i][1][2]*wallEquationArray[j][2] + wallEquationArray[j][3]
			if  distToWall < ballRadius:
				# collision with wall happened
				# update the right position after bouncing on the wall
				ballArray[i][1][0] = ballArray[i][1][0] - 2 * wallEquationArray[j][0]* (distToWall - ballRadius)
				ballArray[i][1][1] = ballArray[i][1][1] - 2 * wallEquationArray[j][1]* (distToWall - ballRadius)
				ballArray[i][1][2] = ballArray[i][1][2] - 2 * wallEquationArray[j][2]* (distToWall - ballRadius)
				# update the right velocity after bouncing
				dotVN = ballArray[i][2][0]*wallEquationArray[j][0] + ballArray[i][2][1]*wallEquationArray[j][1] + ballArray[i][2][2]*wallEquationArray[j][2]
				ballArray[i][2][0] = - dotVN * wallEquationArray[j][0] + ballArray[i][2][0]-dotVN*wallEquationArray[j][0]
				ballArray[i][2][1] = - dotVN * wallEquationArray[j][1] + ballArray[i][2][1]-dotVN*wallEquationArray[j][1]
				ballArray[i][2][2] = - dotVN * wallEquationArray[j][2] + ballArray[i][2][2]-dotVN*wallEquationArray[j][2]

def dotProduct(V1, V2):
	return V1[0]*V2[0]+V1[1]*V2[1]+V1[2]*V2[2]

def findTheRightT(t1, t2):
	if 0.0<t1<1.0:
		return t1
	elif 0.0<t2<1.0:
		return t2
	else:
		print "none of the T value in the range [0, 1]", t1, t2
		return t1 #theory not right

def normalizeVector(v):
	sum = 0.0
	for i in range(len(v)):
		sum +=v[i]*v[i]
	sum = math.sqrt(sum)
	for i in range(len(v)):
		v[i]/=sum
	return v

def collisionWithBalls(numOfBalls, ballRadius, ballArray):
	for i in range(numOfBalls-1):
		for j in range(i+1, numOfBalls):
			# checking the collision between ball I and J
			Pc = [ballArray[i][1][0], ballArray[i][1][1], ballArray[i][1][2]]
			Qc = [ballArray[j][1][0], ballArray[j][1][1], ballArray[j][1][2]]
			Vp = [ballArray[i][2][0], ballArray[i][2][1], ballArray[i][2][2]]
			Vq = [ballArray[j][2][0], ballArray[j][2][1], ballArray[j][2][2]]
			Vpq = [Pc[0]-Qc[0], Pc[1]-Qc[1], Pc[2]-Qc[2]]
			if dotProduct(Vpq,Vpq)<4*ballRadius*ballRadius:
				A = [Pc[0]-Vp[0]-Qc[0]+Vq[0], Pc[1]-Vp[1]-Qc[1]+Vq[1], Pc[2]-Vp[2]-Qc[2]+Vq[2]]
				B = [Vp[0]-Vq[0], Vp[1]-Vq[1], Vp[2]-Vq[2]]
				temp = dotProduct(A, B)*dotProduct(A, B)-dotProduct(B, B)*dotProduct(B, B)*(dotProduct(A, A)-ballRadius*ballRadius*4)
				if temp<0.0:
					print "something wrong with the calculation"
					continue
				t1 = (-dotProduct(A, B)+math.sqrt(temp))/(dotProduct(B, B) * dotProduct(B, B))
				t2 = (-dotProduct(A, B)-math.sqrt(temp))/(dotProduct(B, B) * dotProduct(B, B))
				t = findTheRightT(t1, t2)
				Pt = [Pc[0]-(1-t)*Vp[0], Pc[1]-(1-t)*Vp[1], Pc[2]-(1-t)*Vp[2]]
				Qt = [Qc[0]-(1-t)*Vq[0], Qc[1]-(1-t)*Vq[1], Qc[2]-(1-t)*Vq[2]]
				N = [Qt[0]-Pt[0], Qt[1]-Pt[1], Qt[2]-Pt[2]]
				N = normalizeVector(N)
				VpDotN = dotProduct(Vp, N)
				VqDotN = dotProduct(Vq, N) 
				Vp1 = [Vp[0]-VpDotN*N[0]+VqDotN*N[0], Vp[1]-VpDotN*N[1]+VqDotN*N[1], Vp[2]-VpDotN*N[2]+VqDotN*N[2]]
				Vq1 = [Vq[0]-VqDotN*N[0]+VpDotN*N[0], Vq[1]-VqDotN*N[1]+VpDotN*N[1], Vq[2]-VqDotN*N[2]+VpDotN*N[2]]
				Pc1 = [Pt[0]+Vp1[0]*(1-t), Pt[1]+Vp1[1]*(1-t), Pt[2]+Vp1[2]*(1-t)]
				Qc1 = [Qt[0]+Vq1[0]*(1-t), Qt[1]+Vq1[1]*(1-t), Qt[2]+Vq1[2]*(1-t)]
				ballArray[i][1][0] = Pc1[0];ballArray[i][1][1] = Pc1[1];ballArray[i][1][2] = Pc1[2]
				ballArray[j][1][0] = Qc1[0];ballArray[j][1][1] = Qc1[1];ballArray[j][1][2] = Qc1[2]
				ballArray[i][2][0] = Vp1[0];ballArray[i][2][1] = Vp1[1];ballArray[i][2][2] = Vp1[2]
				ballArray[j][2][0] = Vq1[0];ballArray[j][2][1] = Vq1[1];ballArray[j][2][2] = Vq1[2]

def simulation(sizeOfBox, numOfBalls, ballRadius, ballArray):
	maxFrame = 400
	cmds.playbackOptions(minTime=1, maxTime = maxFrame, animationStartTime=1, animationEndTime = maxFrame)
	for i in range(1, maxFrame+1):
		for j in range(numOfBalls):
			cmds.setKeyframe(ballArray[j][0], attribute="tx", v=ballArray[j][1][0], t=[i], inTangentType="spline", outTangentType="spline")
			cmds.setKeyframe(ballArray[j][0], attribute="ty", v=ballArray[j][1][1], t=[i], inTangentType="spline", outTangentType="spline")
			cmds.setKeyframe(ballArray[j][0], attribute="tz", v=ballArray[j][1][2], t=[i], inTangentType="spline", outTangentType="spline")
			# update the position of all the balls following their current velocity
			ballArray[j][1][0] += ballArray[j][2][0]
			ballArray[j][1][1] += ballArray[j][2][1]
			ballArray[j][1][2] += ballArray[j][2][2]
		collisionWithWalls(sizeOfBox, numOfBalls, ballRadius, ballArray)
		collisionWithBalls(numOfBalls, ballRadius, ballArray)
		for j in range(numOfBalls):
			cmds.move(ballArray[j][1][0], ballArray[j][1][1], ballArray[j][1][2], ballArray[j][0])


if __name__ == "__main__":
	cmds.select(all=True)
	cmds.delete()
	sizeOfBox = 10
	numOfBalls = 10
	ballRadius = 0.5*sizeOfBox/10.0
	ballArray = setupScene(sizeOfBox, numOfBalls, ballRadius)
	simulation(sizeOfBox, numOfBalls, ballRadius, ballArray)
