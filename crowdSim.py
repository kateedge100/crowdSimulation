# Simualtions Script

import maya.cmds as cmds
import random as rand
import math as math


class Agent:
     # contructor
     def __init__(self, id, sphereRadius):
         # allows spawning in -1 - 1 rather the 0 - 1
         self.position = [(rand.random()- rand.random())*3,sphereRadius, (rand.random()- rand.random())*3]
         self.velocity = [rand.random()/40, 0, rand.random()/40]
         self.id = id
         
         cmds.sphere(n = id, r = sphereRadius)
         cmds.move(self.position[0], self.position[1], self.position[2], id)
         
     def distanceToAgent(self, Agent):
         distance = sqrt((self.position[0]-Agent.position[0])^2 + (self.position[1]-Agent.position[1])^2 + (self.position[2]-Agent.position[2])^2)
        
         
         
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
        print self.agentArray[0].id
        print self.agentArray[0].position
        
    def simulation(self, ballRadius, agentArray):
        maxFrame = 40
        cmds.playbackOptions(minTime=1, maxTime = maxFrame, animationStartTime=1, animationEndTime = maxFrame)
        for i in range(1, maxFrame+1):
	        for j in range(self.agents):    
	            cmds.setKeyframe(self.agentArray[j].id, attribute="tx", v=self.agentArray[j].position[0], t=[i], inTangentType="spline", outTangentType="spline")
	            cmds.setKeyframe(self.agentArray[j].id, attribute="ty", v=self.agentArray[j].position[1], t=[i], inTangentType="spline", outTangentType="spline")
	            cmds.setKeyframe(self.agentArray[j].id, attribute="tz", v=self.agentArray[j].position[2], t=[i], inTangentType="spline", outTangentType="spline")
	            # update the position of all the balls following their current velocity
	            self.agentArray[j].position[0] += self.agentArray[j].velocity[0]
	            self.agentArray[j].position[1] += self.agentArray[j].velocity[1]
	            self.agentArray[j].position[2] += self.agentArray[j].velocity[2]
	            
	            collisionWithBalls(self.agents, ballRadius, self.agentArray)
	            
	            compute = computeAlignment(self, j)
	            self.agentArray[j].velocity[0] += compute[0]
	            self.agentArray[j].velocity[1] += compute[1]
	            self.agentArray[j].velocity[2] += compute[2]
	            
	            
	        
	            for j in range(self.agents):
	                cmds.move(agentArray[j].position[0], agentArray[j].position[1], agentArray[j].position[2], agentArray[j].id)

        
		
    # Taken from Xiasongs code found at https://mybu.bournemouth.ac.uk/webapps/blackboard/content/listContent.jsp?course_id=_52391_1&content_id=_1420295_1&mode=reset	        
    def collisionWithBalls(numOfBalls, ballRadius, ballArray):
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
    				ballArray[i].position[0] = Pc1[0];ballArray[i].position[1] = Pc1[1];ballArray[i].position[2] = Pc1[2]
    				ballArray[j].position[0] = Qc1[0];ballArray[j].position[1] = Qc1[1];ballArray[j].position[2] = Qc1[2]
    				ballArray[i].velocity[0] = Vp1[0];ballArray[i].velocity[1] = Vp1[1];ballArray[i].velocity[2] = Vp1[2]
    				ballArray[j].velocity[0] = Vq1[0];ballArray[j].velocity[1] = Vq1[1];ballArray[j].velocity[2] = Vq1[2]
    				
    	def computeAlignment(self, currentAgent):
    	    numberOfNeighbours = 0
    	    alignmentVector = [0,0,0]
    	    
    	    for agent in range(self.agentArray):
    	        if agent != currentAgent:
    	            if currentAgent.distanceToAgent(agent) < 4:
    	                alignmentVector[0] += agent.velocity[0]    	                
    	                alignmentVector[2] += agent.velocity[2]
    	                
    	                numberOfNeighbours += 1
    	                
    	    alignmentVector[0] /= numberOfNeighbours
    	    alignmentVector[2] /= numberOfNeighbours
    	    alignmentVector = normalize(alignmentVector)
    	               
    	    return alignmentVector
    	    
    	    

def normalize(vector):
    normVector = sqrt((vector[0] + vector[0])^2 + (vector[1] + vector[1])^2 + (vector[2] + vector[2])^2)
    return normVector
            
        
         
if __name__ == "__main__":
  
    cmds.select(all=True)
    cmds.delete()
    
    numberOfBois = 10
    boisRadius = 0.2
    
    scene = Scene(numberOfBois)  
    
    scene.populateScene()
    
    scene.simulation(boisRadius, scene.agentArray)

          
    
	
  
        
    