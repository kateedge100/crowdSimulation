# Simualtions Script

import maya.cmds as cmds
import random as rand
import math as math

PI = 3.14159



class Agent:
     # contructor
     def __init__(self, id, radius, predatorBool):
         # allows spawning in -1 - 1 rather the 0 - 1
         self.position = [(rand.random()- rand.random())*10,radius, (rand.random()- rand.random())*10]
         self.velocity = [rand.random()/40, 0, rand.random()/40]
         self.oldVelocity = [0,0,1] # used for orientation
         self.rotation = [0,0,0]
         self.acceleration = [0,0,0]
         self.id = id
         self.predator = predatorBool
         
        
         
         self.flockFlag = False
         
         #cmds.sphere(n = id, r = sphereRadius)
         cmds.polyCone(n = id, r = radius, h = 0.8, axis = (0,0,1))
         cmds.move(self.position[0], self.position[1], self.position[2], id)
         
         # cones are created with correct orientation
         #self.updateRotation
         
     def distanceToAgent(self, Agent):
         distance = math.sqrt((self.position[0]-Agent.position[0])*(self.position[0]-Agent.position[0]) + (self.position[2]-Agent.position[2])*(self.position[2]-Agent.position[2]))
         
         return distance
        
        
     
     def updateRotation(self):
         #print self.oldVelocity[0]
         #print self.velocity[0]
         if self.oldVelocity != self.velocity:
             
             #print 'Rotating'
             mag1 = vectorMagnitude(self.velocity)
             mag2 = vectorMagnitude(self.oldVelocity)
             
             steer = math.acos(dotProduct(self.oldVelocity, self.velocity)/(mag1 * mag2))
             
             steer = steer * (180/PI)
             
             #print steer
             
             #print self.rotation[1]
             self.rotation[1] = self.rotation[1] + steer 
             #print self.rotation[1]
             
         #else:
             #print 'no change in velocity'
                 
         
         
class Scene:
    def __init__(self, preyAgents, predatorAgents):
        self.preyAgents = preyAgents
        self.predatorAgents = predatorAgents
        self.agents = self.preyAgents + self.predatorAgents
        self.agentArray = []
        
        self.preyMaxSpeed = 1
        
        
    def populateScene(self):  
        #init prey             
        for i in range(0,self.preyAgents):
            currentAgent = Agent("agentPrey" + str(i), 0.2, False)
            self.agentArray.append(currentAgent)
        # init predators
        for i in range(0,self.predatorAgents):
            currentAgent = Agent("agentPredator" + str(i), 0.2, True)
            self.agentArray.append(currentAgent)
            
        cmds.group("agent*", name = "Agents")
        cmds.select(self.agentArray[0].id)    
       
        
    def simulation(self, ballRadius, agentArray):
        maxFrame = 80
        cmds.playbackOptions(minTime=1, maxTime = maxFrame, animationStartTime=1, animationEndTime = maxFrame)
        for i in range(1, maxFrame+1):
            for j in range(self.agents): 
              
                self.agentArray[j].oldVelocity = self.agentArray[j].velocity[:] 
                
               # if self.agentArray[j].predator == True:
                    #self.detectPredator(self.agentArray[j])
               
                    
                    
                
                  
                #if self.agentArray[j].flockFlag == True:
                    #self.flock(self.agentArray[j])
                
                #if self.agentArray[j].predator == False:            
                self.flock(self.agentArray[j])
                
                
                
                
                                            
                #UPDATE ROTATION BASED ON DIRECTION OF VELOCITY  
                cmds.setKeyframe(self.agentArray[j].id, attribute="rx", v=self.agentArray[j].rotation[0], t=[i], inTangentType="spline", outTangentType="spline")
                cmds.setKeyframe(self.agentArray[j].id, attribute="ry", v=self.agentArray[j].rotation[1], t=[i], inTangentType="spline", outTangentType="spline")
                cmds.setKeyframe(self.agentArray[j].id, attribute="rz", v=self.agentArray[j].rotation[2], t=[i], inTangentType="spline", outTangentType="spline")  
                   
                cmds.setKeyframe(self.agentArray[j].id, attribute="tx", v=self.agentArray[j].position[0], t=[i], inTangentType="spline", outTangentType="spline")
                cmds.setKeyframe(self.agentArray[j].id, attribute="ty", v=self.agentArray[j].position[1], t=[i], inTangentType="spline", outTangentType="spline")
                cmds.setKeyframe(self.agentArray[j].id, attribute="tz", v=self.agentArray[j].position[2], t=[i], inTangentType="spline", outTangentType="spline")
	            
	            
	            # UPDATING VELOCITY, POSITION AND ROTATION
                # update velocity based on acceleration

                #self.agentArray[j].velocity[0] += self.agentArray[j].acceleration[0]
                #self.agentArray[j].velocity[2] += self.agentArray[j].acceleration[2]
	             
	            # update the position of all the balls following their current velocity
                self.agentArray[j].position[0] += self.agentArray[j].velocity[0]
                self.agentArray[j].position[1] += self.agentArray[j].velocity[1]
                self.agentArray[j].position[2] += self.agentArray[j].velocity[2]
                
                #self.agentArray[j].updateRotation()
                
                #print self.agentArray[j].oldVelocity
                #print self.agentArray[j].velocity
             	            
                 	            	        
                for j in range(self.agents):
                    cmds.move(agentArray[j].position[0], agentArray[j].position[1], agentArray[j].position[2], agentArray[j].id)

  		
    def flock(self, currentAgent):
         alignment = self.computeAlignment(currentAgent)
         cohesion = self.computeCohesion(currentAgent)
         separation = self.computeSeperation(currentAgent)
        
         alignmentWeight = 1
         cohesionWeight = 1 
         separationWeight = 1
        
         #self.agentArray[j].velocity[0] += alignment[0] + cohesion[0] + separation[0]
         #self.agentArray[j].velocity[2] += alignment[2] + cohesion[2] + separation[2]
        
         currentAgent.velocity[0] += (cohesion[0] * cohesionWeight) + (alignment[0] * alignmentWeight) + (separation[0] * separationWeight);
         currentAgent.velocity[2] += (cohesion[2] * cohesionWeight) + (alignment[2] * alignmentWeight) + (separation[2] * separationWeight);
        
         currentAgent.velocity = normalizeVector(currentAgent.velocity) 
         
            
    				
    def computeAlignment(self, currentAgent):
        numberOfNeighbours = 0
    	alignmentVector = [0,0,0]
    	    
    	for agent in self.agentArray:
    	    if agent != currentAgent:
    	        if currentAgent.distanceToAgent(agent) < 2:
    	            alignmentVector[0] += agent.velocity[0]
    	            # ignore y axis    	                
    	            alignmentVector[2] += agent.velocity[2]
    	                
    	            numberOfNeighbours += 1
    	# avoid dividing by zero
        if numberOfNeighbours != 0:
            
                
            alignmentVector[0] /= numberOfNeighbours
            alignmentVector[2] /= numberOfNeighbours
        	
           
            alignmentVector = normalizeVector(alignmentVector)
            
            #steer
            alignmentVector[0]= alignmentVector[0] - currentAgent.velocity[0]
            alignmentVector[2]= alignmentVector[2] - currentAgent.velocity[2]
          
    	               
    	return alignmentVector
    	
    def computeCohesion(self, currentAgent):
        numberOfNeighbours = 0
    	cohesionVector = [0,0,0]
    	    
    	for agent in self.agentArray:
    	    if agent != currentAgent:
    	        if currentAgent.distanceToAgent(agent) < 5:
    	            cohesionVector[0] += agent.position[0]
    	            # ignore y axis    	                
    	            cohesionVector[2] += agent.position[2]
    	                
    	            numberOfNeighbours += 1
    	# avoid dividing by zero
        if numberOfNeighbours != 0:                
            cohesionVector[0] /= numberOfNeighbours
            cohesionVector[2] /= numberOfNeighbours
        	
            
            cohesionVector[0] = (agent.position[0] - cohesionVector[0])
            cohesionVector[2] = (agent.position[2] - cohesionVector[2])
            
            cohesionVector = normalizeVector(cohesionVector)
            
            #steer
            cohesionVector[0]= cohesionVector[0] - currentAgent.velocity[0]
            cohesionVector[2]= cohesionVector[2] - currentAgent.velocity[2]
            
          
    	               
        return cohesionVector
    	
    def computeSeperation(self, currentAgent):
        numberOfNeighbours = 0
        seperationVector = [0,0,0]
    	    
        for agent in self.agentArray:
            if agent != currentAgent:
                if currentAgent.distanceToAgent(agent) <1.0:
                    seperationVector[0] += agent.position[0]-currentAgent.position[0]
                    # ignore y axis    	                
                    seperationVector[2] += agent.position[2]-currentAgent.position[2]
                    
                    seperationVector = normalizeVector(seperationVector)
                    
                    # -2 so that distance is zero at edge of cone
                    seperationVector[0] /= (currentAgent.distanceToAgent(agent)-0.2)
                    seperationVector[2] /= (currentAgent.distanceToAgent(agent)-0.2)   
                    
                    numberOfNeighbours += 1
        # avoid dividing by zero
        if numberOfNeighbours != 0:               
            seperationVector[0] /= numberOfNeighbours
            seperationVector[2] /= numberOfNeighbours
            seperationVector[0] *= -1;
            seperationVector[2] *= -1;
        
            seperationVector = normalizeVector(seperationVector)
            
            #steer
            seperationVector[0]= seperationVector[0] - currentAgent.velocity[0]
            seperationVector[2]= seperationVector[2] - currentAgent.velocity[2]
            
            
                       
        return seperationVector
        
    def detectPredator(self, currentPredator):
        for agent in self.agentArray:
            if agent.predator == False:
                if currentPredator.distanceToAgent(agent) < 5:
                    agent.flockFlag = True
                    fleeVector = [0,0,0]
                    
                
                    
                    fleeVector[0] = -(currentPredator.position[0] - agent.position[0])
                    fleeVector[2] = -(currentPredator.position[2] - agent.position[2])
                    
                    normalizeVector(fleeVector)
                    
                    self.steer(agent,fleeVector)
                    
                    #dist = currentPredator.distanceToAgent(agent)
                   # print 'Distance'
                    #print dist
                    #print 'Flag'
                    #print agent.flockFlag
        
    def steer(self, currentAgent, target):
        steer = [0,0,0]
        steer[0] = target[0] - currentAgent.velocity[0]
        steer[2] = target[2] - currentAgent.velocity[2]
                    
        currentAgent.velocity[0] += steer[0]
        currentAgent.velocity[2] += steer[2]
                    	
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
        if sum !=0:
            v[i]/=sum
    return v
    
def dotProduct(V1, V2):
	return V1[0]*V2[0]+V1[1]*V2[1]+V1[2]*V2[2]
                  
if __name__ == "__main__":
  
    cmds.select(all=True)
    cmds.delete()
    
    numberOfPrey = 20
    numberOfPredators = 1
    
    boisRadius = 0.2
    
    scene = Scene(numberOfPrey, numberOfPredators )  
    
    scene.populateScene()
    
    scene.simulation(boisRadius, scene.agentArray)
    