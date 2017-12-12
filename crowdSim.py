# Simualtions Script

import maya.cmds as cmds
import random as rand
import math as math



class Agent:
     # contructor
     def __init__(self, id, sphereRadius):
         # allows spawning in -1 - 1 rather the 0 - 1
         self.position = [(rand.random()- rand.random())*10,sphereRadius, (rand.random()- rand.random())*10]
         self.velocity = [rand.random()/40, 0, rand.random()/40]
         self.rotation = [0,0,0]
         self.id = id
         
         #cmds.sphere(n = id, r = sphereRadius)
         cmds.polyCone(n = id, r = sphereRadius, h = 0.4, axis = (0,0,1))
         cmds.move(self.position[0], self.position[1], self.position[2], id)
         
     def distanceToAgent(self, Agent):
         distance = math.sqrt((self.position[0]-Agent.position[0])*(self.position[0]-Agent.position[0]) + (self.position[2]-Agent.position[2])*(self.position[2]-Agent.position[2]))
     
     def updateRotation(self):
         print vectorMagnitude(self.velocity)/self.velocity[2]
         steer = math.acos(vectorMagnitude(self.velocity)/self.velocity[2])
         rotation = [0,steer,0]   
         
         
class Scene:
    def __init__(self, agents):
        self.agents = agents
        self.agentArray = []
        
        
    def populateScene(self):               
        for i in range(0,self.agents):
            currentAgent = Agent("agent" + str(i), 0.2)
            self.agentArray.append(currentAgent)
        cmds.group("agent*", name = "Agents")
        cmds.select(self.agentArray[0].id)    
       
        
    def simulation(self, ballRadius, agentArray):
        maxFrame = 80
        cmds.playbackOptions(minTime=1, maxTime = maxFrame, animationStartTime=1, animationEndTime = maxFrame)
        for i in range(1, maxFrame+1):
            for j in range(self.agents):    
                
                alignment = self.computeAlignment(self.agentArray[j])
                cohesion = self.computeCohesion(self.agentArray[j])
                separation = self.computeSeperation(self.agentArray[j])
                
                alignmentWeight = 1
                cohesionWeight = 1
                separationWeight = 1
                
                #self.agentArray[j].velocity[0] += alignment[0] + cohesion[0] + separation[0]
                #self.agentArray[j].velocity[2] += alignment[2] + cohesion[2] + separation[2]
                
                self.agentArray[j].velocity[0] += alignment[0] * alignmentWeight + cohesion[0] * cohesionWeight + separation[0] * separationWeight;
                self.agentArray[j].velocity[2] += alignment[2] * alignmentWeight + cohesion[2] * cohesionWeight + separation[2] * separationWeight;
 
                self.agentArray[j].velocity = normalizeVector(self.agentArray[j].velocity)
                
                agentArray[j].updateRotation()
                
                #UPDATE ROTATION BASED ON DIRECTION OF VELOCITY  
                cmds.setKeyframe(self.agentArray[j].id, attribute="rx", v=self.agentArray[j].rotation[0], t=[i], inTangentType="spline", outTangentType="spline")
                cmds.setKeyframe(self.agentArray[j].id, attribute="ry", v=self.agentArray[j].rotation[1], t=[i], inTangentType="spline", outTangentType="spline")
                cmds.setKeyframe(self.agentArray[j].id, attribute="rz", v=self.agentArray[j].rotation[2], t=[i], inTangentType="spline", outTangentType="spline")  
                   
                cmds.setKeyframe(self.agentArray[j].id, attribute="tx", v=self.agentArray[j].position[0], t=[i], inTangentType="spline", outTangentType="spline")
                cmds.setKeyframe(self.agentArray[j].id, attribute="ty", v=self.agentArray[j].position[1], t=[i], inTangentType="spline", outTangentType="spline")
                cmds.setKeyframe(self.agentArray[j].id, attribute="tz", v=self.agentArray[j].position[2], t=[i], inTangentType="spline", outTangentType="spline")
	            # update the position of all the balls following their current velocity
                self.agentArray[j].position[0] += self.agentArray[j].velocity[0]
                self.agentArray[j].position[1] += self.agentArray[j].velocity[1]
                self.agentArray[j].position[2] += self.agentArray[j].velocity[2]
	            
                #self.collisionWithBalls(self.agents, ballRadius, self.agentArray)
	            
                 	            	        
                for j in range(self.agents):
                    cmds.move(agentArray[j].position[0], agentArray[j].position[1], agentArray[j].position[2], agentArray[j].id)

       		
    # Taken from Xiasongs code found at https://mybu.bournemouth.ac.uk/webapps/blackboard/content/listContent.jsp?course_id=_52391_1&content_id=_1420295_1&mode=reset	        
    def collisionWithBalls(self, numOfBalls, ballRadius, ballArray):
    	for i in range(numOfBalls-1):
    		for j in range(i+1, numOfBalls):
    			# checking the collision between ball I and J
    			Pc = [ballArray[i].position[0], ballArray[i].position[1], ballArray[i].position[2]]
    			Qc = [ballArray[j].position[0], ballArray[j].position[1], ballArray[j].position[2]]
    			Vp = [ballArray[i].velocity[0], ballArray[i].velocity[1], ballArray[i].velocity[2]]
    			Vq = [ballArray[j].velocity[0], ballArray[j].velocity[1], ballArray[j].velocity[2]]
    			Vpq = [Pc[0]-Qc[0], Pc[1]-Qc[1], Pc[2]-Qc[2]]
    			if dotProduct(Vpq,Vpq)<4*ballRadius*ballRadius:
    				A = [Pc[0]-Vp[0]-Qc[0]+Vq[0], Pc[1]-Vp[1]-Qc[1]+Vq[1], Pc[2]-Vp[2]-Qc[2]+Vq[2]]
    				B = [Vp[0]-Vq[0], Vp[1]-Vq[1], Vp[2]-Vq[2]]
    				temp = dotProduct(A, B)*dotProduct(A, B)-dotProduct(B, B)*dotProduct(B, B)*(dotProduct(A, A)-ballRadius*ballRadius*4)
    				if temp<0.0:
    					print "something wrong with the calculation"
    					continue
    				t1 = (-dotProduct(A, B)+ math.sqrt(temp))/(dotProduct(B, B) * dotProduct(B, B))
    				t2 = (-dotProduct(A, B)- math.sqrt(temp))/(dotProduct(B, B) * dotProduct(B, B))
    				t = self.findTheRightT(t1, t2)
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
    				ballArray[i].position[0] = Pc1[0];ballArray[i].position[1] = Pc1[1];ballArray[i].position[2] = Pc1[2]
    				ballArray[j].position[0] = Qc1[0];ballArray[j].position[1] = Qc1[1];ballArray[j].position[2] = Qc1[2]
    				ballArray[i].velocity[0] = Vp1[0];ballArray[i].velocity[1] = Vp1[1];ballArray[i].velocity[2] = Vp1[2]
    				ballArray[j].velocity[0] = Vq1[0];ballArray[j].velocity[1] = Vq1[1];ballArray[j].velocity[2] = Vq1[2]
    				
    def computeAlignment(self, currentAgent):
        numberOfNeighbours = 0
    	alignmentVector = [0,0,0]
    	    
    	for agent in self.agentArray:
    	    if agent != currentAgent:
    	        if currentAgent.distanceToAgent(agent) < 4:
    	            alignmentVector[0] += agent.velocity[0]
    	            # ignore y axis    	                
    	            alignmentVector[2] += agent.velocity[2]
    	                
    	            numberOfNeighbours += 1
    	                
    	alignmentVector[0] /= numberOfNeighbours
    	alignmentVector[2] /= numberOfNeighbours
    	alignmentVector = normalizeVector(alignmentVector)
    	               
    	return alignmentVector
    	
    def computeCohesion(self, currentAgent):
        numberOfNeighbours = 0
    	cohesionVector = [0,0,0]
    	    
    	for agent in self.agentArray:
    	    if agent != currentAgent:
    	        if currentAgent.distanceToAgent(agent) < 15:
    	            cohesionVector[0] += agent.position[0]
    	            # ignore y axis    	                
    	            cohesionVector[2] += agent.position[2]
    	                
    	            numberOfNeighbours += 1
    	                
    	cohesionVector[0] /= numberOfNeighbours
    	cohesionVector[2] /= numberOfNeighbours
    	cohesionVector[0] = (cohesionVector[0] - agent.position[0])
    	cohesionVector[2] = (cohesionVector[2] - agent.position[2])
    	cohesionVector = normalizeVector(cohesionVector)
    	               
    	return cohesionVector
    	
    def computeSeperation(self, currentAgent):
        numberOfNeighbours = 0
        seperationVector = [0,0,0]
    	    
        for agent in self.agentArray:
            if agent != currentAgent:
                if currentAgent.distanceToAgent(agent) < 0.5:
                    seperationVector[0] += agent.position[0]-currentAgent.position[0]
                    # ignore y axis    	                
                    seperationVector[2] += agent.position[2]-currentAgent.position[2]
                        
                    numberOfNeighbours += 1
                        
        seperationVector[0] /= numberOfNeighbours
        seperationVector[2] /= numberOfNeighbours
        seperationVector[0] *= -1;
        seperationVector[2] *= -1;
        
        seperationVector = normalizeVector(seperationVector)
                       
        return seperationVector
        
    	
    def findTheRightT(self, t1, t2):
	    if 0.0<t1<1.0:
		    return t1
	    elif 0.0<t2<1.0:
		    return t2
	    else:
		    print "none of the T value in the range [0, 1]", t1, t2
		    return t1 #theory not right

def vectorMagnitude(v):
    sum = 0.0
    for i in range(len(v)):
        sum +=v[i]*v[i]
    sum = math.sqrt(sum)
	
    return sum
       	    
def normalizeVector(v):
    sum = vectorMagnitude(v)
    for i in range(len(v)):
        v[i]/=sum
    return v
    
def dotProduct(V1, V2):
	return V1[0]*V2[0]+V1[1]*V2[1]+V1[2]*V2[2]
                  
if __name__ == "__main__":
  
    cmds.select(all=True)
    cmds.delete()
    
    numberOfBois = 50
    boisRadius = 0.2
    
    scene = Scene(numberOfBois)  
    
    scene.populateScene()
    
    scene.simulation(boisRadius, scene.agentArray)