8# Simualtions Script

import maya.cmds as cmds
import random as rand
import math as math

PI = 3.14159



class Agent:
     # contructor
     def __init__(self, id, radius, predatorBool):
         
         self.radius = radius
         # allows spawning in -1 - 1 rather the 0 - 1
         self.position = [(rand.random()- rand.random())*20,self.radius, (rand.random()- rand.random())*20]
         self.velocity = [0, 0, 0]
         self.oldVelocity = [0,0,1] # used for orientation
         self.rotation = [0,0,0]
         self.acceleration = [0,0,0]
         self.id = id
         self.predator = predatorBool
         
         
         self.maxSpeed = 1      
         
         self.flockFlag = False
         
         self.detectedPredator = None
         
         predatorPos = [-15,0.2,18]
         
         if self.predator == True:
             self.position = [-20,0.2,25]
         

         cmds.polyCone(n = id, r = self.radius, h = 0.8, axis = (0,0,1))
         
         # cones are created with correct orientation
         #self.updateRotation
         
     def distanceToAgent(self, Agent):
         distance = math.sqrt((self.position[0]-Agent.position[0])*(self.position[0]-Agent.position[0]) + (self.position[2]-Agent.position[2])*(self.position[2]-Agent.position[2]))
         
         return distance
        
     def limitVel(self, limit):
         velLim = limit
         newVelocity = [0,0,0]
         
         if vectorMagnitude(self.velocity) > velLim:
             newVelocity[0] = (self.velocity[0]/vectorMagnitude(self.velocity))*velLim
             newVelocity[2] = (self.velocity[2]/vectorMagnitude(self.velocity))*velLim
             
             self.velocity = newVelocity
         
      
           
     
     def updateRotation(self):
         
  
         
         # rotation 0 when facing in z axis
         facing = [0,0,1]       
         
         #only update if moving             
         if self.velocity != [0,0,0]:    
                 
             steer = math.acos(dotProduct(facing, self.velocity))
           
             steer = steer * (180/PI)
             
              
             diff = self.rotation[1] - steer
               
             # if rotation past 180 degrees must take away from 360 
             if self.velocity[0]>0:
                 self.rotation[1] = steer
             else:
                 self.rotation[1]= 360-steer

                 
         
         
class Scene:
    def __init__(self, preyAgents, predatorAgents):
        self.preyAgents = preyAgents
        self.predatorAgents = predatorAgents
        self.agents = self.preyAgents + self.predatorAgents
        self.agentArray = []
        
        self.preyArray = []
        self.predatorArray = []
        
        #target = cmds.polyCube(n = 'target')
       
        
        
    def populateScene(self):  
        #init prey             
        for i in range(0,self.preyAgents):
            currentAgent = Agent("agentPrey" + str(i), 0.2, False)
            self.agentArray.append(currentAgent)
            self.preyArray.append(currentAgent)
        # init predators
        for i in range(0,self.predatorAgents):
            currentAgent = Agent("agentPredator" + str(i), 0.4, True)
            self.agentArray.append(currentAgent)
            self.predatorArray.append(currentAgent)
            
        cmds.group("agent*", name = "Agents")
        
        if self.predatorAgents != 0:
            cmds.select(self.predatorArray[0].id)
        else:
            cmds.select(self.preyArray[0].id)   
       
        
    def simulation(self, ballRadius, agentArray):
        maxFrame = 80
        cmds.playbackOptions(minTime=1, maxTime = maxFrame, animationStartTime=1, animationEndTime = maxFrame)
        for i in range(1, maxFrame+1):
            for j in range(self.agents): 
              
                self.agentArray[j].oldVelocity = self.agentArray[j].velocity[:] 
                
                
                
                # detects prey in range of predator and sets flag
                if self.agentArray[j].predator == True:
                    self.detectPredator(self.agentArray[j])
                    
                 
            
                
                
                
                # Seek target and seperate --------------------------------------------------------------
                """targetPos = [float(math.sin(i/10)*10),0,0]
                targetVec = [0,0,0]
                targetVec[0] =  (targetPos[0] - self.agentArray[j].position[0])
                targetVec[2] =  (targetPos[2] - self.agentArray[j].position[2])
                
                targetVec = normalizeVector(targetVec)
                
                #self.agentArray[j].velocity[0] += self.computeSeperation(self.agentArray[j])[0]
                #self.agentArray[j].velocity[2] += self.computeSeperation(self.agentArray[j])[2]
                
                self.flock(agentArray[j])
                
                dist = math.sqrt((self.agentArray[j].position[0]-float(math.sin(i/10)*10))*(self.agentArray[j].position[0]-float(math.sin(i/10)*10)) + (self.agentArray[j].position[2]-float(math.sin(i/10)*10))*(self.agentArray[j].position[2]-float(math.sin(i/10)*10)))
         
                seekWeight = 0.5 
                #if dist < 5:        
                seek = [0,0,0]
                seek = self.steer(self.agentArray[j],targetVec) 
                
                seek[0] *= seekWeight 
                seek[2] *= seekWeight 
                
                self.agentArray[j].velocity[0] += seek[0]
                self.agentArray[j].velocity[2] += seek[2]
                
                self.agentArray[j].velocity = normalizeVector(self.agentArray[j].velocity )"""
                 #----------------------------------------------------------------------------------------------------------   
                    
                # flocks prey within range of predator
                #if self.agentArray[j].flockFlag == True:
                    #self.flock(self.agentArray[j])
                
                # predator chases prey  
                if self.agentArray[j].predator == True:
                    self.chase(self.agentArray[j]) 
                 
                       
                if self.agentArray[j].flockFlag == True:
                #if self.agentArray[j].predator == False:            
                    self.flock(self.agentArray[j])
                    # if prey flocking it can alert surrounding prey to predator    
                    self.alertPrey(self.agentArray[j])
                elif self.agentArray[j].flockFlag == False and  self.agentArray[j].predator == False:
                    self.idlePrey(self.agentArray[j])
                
                
                
                
                
                                            
                #UPDATE ROTATION BASED ON DIRECTION OF VELOCITY  
                cmds.setKeyframe(self.agentArray[j].id, attribute="rx", v=self.agentArray[j].rotation[0], t=[i], inTangentType="spline", outTangentType="spline")
                cmds.setKeyframe(self.agentArray[j].id, attribute="ry", v=self.agentArray[j].rotation[1], t=[i], inTangentType="spline", outTangentType="spline")
                cmds.setKeyframe(self.agentArray[j].id, attribute="rz", v=self.agentArray[j].rotation[2], t=[i], inTangentType="spline", outTangentType="spline")  
                   
                cmds.setKeyframe(self.agentArray[j].id, attribute="tx", v=self.agentArray[j].position[0], t=[i], inTangentType="spline", outTangentType="spline")
                cmds.setKeyframe(self.agentArray[j].id, attribute="ty", v=self.agentArray[j].position[1], t=[i], inTangentType="spline", outTangentType="spline")
                cmds.setKeyframe(self.agentArray[j].id, attribute="tz", v=self.agentArray[j].position[2], t=[i], inTangentType="spline", outTangentType="spline")
	            
	            #target
                #cmds.setKeyframe('target', attribute="tx", v=float(math.sin(i/10)*10), t=[i], inTangentType="spline", outTangentType="spline")
                #cmds.setKeyframe('target', attribute="ty", v=0, t=[i], inTangentType="spline", outTangentType="spline")
                #cmds.setKeyframe('target', attribute="tz", v=0, t=[i], inTangentType="spline", outTangentType="spline")
	            
	            
	            # UPDATING VELOCITY, POSITION AND ROTATION
                # update velocity based on acceleration

                #self.agentArray[j].velocity[0] += self.agentArray[j].acceleration[0]
                #self.agentArray[j].velocity[2] += self.agentArray[j].acceleration[2]
                
               
	             
	            # update the position of all the balls following their current velocity
                self.agentArray[j].position[0] += self.agentArray[j].velocity[0]
                self.agentArray[j].position[1] += self.agentArray[j].velocity[1]
                self.agentArray[j].position[2] += self.agentArray[j].velocity[2]
                
                #if self.agentArray[j].flockFlag == True or self.agentArray[j].predator == True:                 
                self.agentArray[j].updateRotation()
                
                #print self.agentArray[j].oldVelocity
                #print self.agentArray[j].velocity
             	            
                 	            	        
                #for j in range(self.agents):
                    #cmds.move(agentArray[j].position[0], agentArray[j].position[1], agentArray[j].position[2], agentArray[j].id)

  	
  	
  		
    def flock(self, currentAgent):
        
         steer = [0,0,0]
         
         alignment = self.computeAlignment(currentAgent)
         cohesion = self.computeCohesion(currentAgent)
         separation = self.computeSeperation(currentAgent)
        
         alignmentWeight = 1
         cohesionWeight = 1 
         separationWeight = 1.5
        
         
         #currentAgent.velocity[0] += (cohesion[0] * cohesionWeight) + (alignment[0] * alignmentWeight) + (separation[0] * separationWeight);
         #currentAgent.velocity[2] += (cohesion[2] * cohesionWeight) + (alignment[2] * alignmentWeight) + (separation[2] * separationWeight);
         
         # steer towards desired flocking vector
         steer[0] += (cohesion[0] * cohesionWeight) + (alignment[0] * alignmentWeight) + (separation[0] * separationWeight);
         steer[2] += (cohesion[2] * cohesionWeight) + (alignment[2] * alignmentWeight) + (separation[2] * separationWeight);
        
         steer = normalizeVector(steer) 
         
         currentAgent.velocity[0] += steer[0]
         currentAgent.velocity[2] += steer[2]
         
         currentAgent.velocity = normalizeVector(currentAgent.velocity)
         
         # steer away from predator if near
         if currentAgent.flockFlag == True:# and currentAgent.distanceToAgent(currentAgent.detectedPredator) < 8:
         
             fleeVec = [0,0,0]
             
             fleeVec[0] = -(currentAgent.detectedPredator.position[0] - currentAgent.position[0])
             fleeVec[2] = -(currentAgent.detectedPredator.position[2] - currentAgent.position[2])
                         
             fleeVec = normalizeVector(fleeVec)
             
             predatorDist = currentAgent.distanceToAgent(currentAgent.detectedPredator)
             
             avoidWeight = 2.5/predatorDist
             
             #print avoidWeight
             
             # 0 to max force eg 0.5
                
             currentAgent.velocity[0] += self.steer(currentAgent, fleeVec)[0]*avoidWeight
             currentAgent.velocity[2] += self.steer(currentAgent, fleeVec)[2]*avoidWeight
                
             currentAgent.velocity = normalizeVector(currentAgent.velocity) 
         
    				
    def computeAlignment(self, currentAgent):
        numberOfNeighbours = 0
    	alignmentVector = [0,0,0]
    	steer = [0,0,0]    
    	for agent in self.preyArray:
    	    # only flock with other flocking boids
    	    if agent != currentAgent:
    	        if agent.flockFlag == True:
        	        if currentAgent.distanceToAgent(agent) < 3:
        	            
        	            alignmentVector[0] += agent.velocity[0]
        	            # ignore y axis    	                
        	            alignmentVector[2] += agent.velocity[2]
        	                
        	            numberOfNeighbours += 1
    	# avoid dividing by zero
        if numberOfNeighbours != 0:
            
                
            alignmentVector[0] /= numberOfNeighbours
            alignmentVector[2] /= numberOfNeighbours
        	
           
            alignmentVector = normalizeVector(alignmentVector)
            
            alignmentVector[0] *= currentAgent.maxSpeed
            alignmentVector[2] *= currentAgent.maxSpeed
            
            
            
            steer = self.steer(currentAgent, alignmentVector)
            
          
    	               
    	return alignmentVector
    	
    def computeCohesion(self, currentAgent):
        numberOfNeighbours = 0
    	cohesionVector = [0,0,0]
    	steer = [0,0,0]    
    	for agent in self.preyArray:
    	    if agent != currentAgent: 
    	        if agent.flockFlag == True:
        	        if currentAgent.distanceToAgent(agent) < 10:
        	            
        	            
        	            
        	            cohesionVector[0] += agent.position[0]
        	            # ignore y axis    	                
        	            cohesionVector[2] += agent.position[2]
        	                
        	            numberOfNeighbours += 1
    	# avoid dividing by zero
        if numberOfNeighbours != 0:                
            cohesionVector[0] /= numberOfNeighbours
            cohesionVector[2] /= numberOfNeighbours
        	
            #cohesionVector = normalizeVector(cohesionVector)
            
            cohesionVector[0] = (agent.position[0] - cohesionVector[0])
            cohesionVector[2] = (agent.position[2] - cohesionVector[2])
            
            cohesionVector = normalizeVector(cohesionVector)
            
            cohesionVector[0]*= currentAgent.maxSpeed 
            cohesionVector[2] *= currentAgent.maxSpeed 

            steer = self.steer(currentAgent, cohesionVector)
            
            #steer
            #cohesionVector[0]= cohesionVector[0] - currentAgent.velocity[0]
            #cohesionVector[2]= cohesionVector[2] - currentAgent.velocity[2]
            
          
    	               
        return cohesionVector
    	
    def computeSeperation(self, currentAgent):
        numberOfNeighbours = 0
        seperationVector = [0,0,0]
    	steer = [0,0,0]    
        for agent in self.preyArray:
            if agent != currentAgent:
                if agent.flockFlag == True:
                    if currentAgent.distanceToAgent(agent) <1.0:
                        
                        seperationVector[0] += agent.position[0]-currentAgent.position[0]
                        # ignore y axis    	                
                        seperationVector[2] += agent.position[2]-currentAgent.position[2]
                        
                        seperationVector = normalizeVector(seperationVector)
                        
                        # -2 so that distance is zero at edge of cone
                        seperationVector[0] /= (currentAgent.distanceToAgent(agent)-0.4)
                        seperationVector[2] /= (currentAgent.distanceToAgent(agent)-0.4)   
                        
                        numberOfNeighbours += 1
        
        # avoid dividing by zero
        if numberOfNeighbours != 0:               
            seperationVector[0] /= numberOfNeighbours
            seperationVector[2] /= numberOfNeighbours
            seperationVector[0] *= -1;
            seperationVector[2] *= -1;
        
            seperationVector = normalizeVector(seperationVector)
            
            seperationVector[0] *= currentAgent.maxSpeed
            seperationVector[2] *= currentAgent.maxSpeed 
                       
                       
        return seperationVector
        
    def detectPredator(self, currentPredator):
        for agent in self.agentArray:
            if agent.predator == False:
                if currentPredator.distanceToAgent(agent) < 4:
                    
                    
                    agent.flockFlag = True  
                    
                    agent.detectedPredator = currentPredator
                                                           
               # else:
                    
                    #agent.flockFlag = False
                   
                
        
    def steer(self, currentAgent, target):
        steer = [0,0,0]
        steer[0] = target[0] - currentAgent.velocity[0]
        steer[2] = target[2] - currentAgent.velocity[2]
        
        steer = normalizeVector(steer)
        
        return steer
        
    def chase(self, currentPredator):
        
        numberOfNeighbours = 0
    	chaseVector = [0,0,0]
    	steer = [0,0,0]  
    	  
    	for prey in self.preyArray:    	    
	        if currentPredator.distanceToAgent(prey) < 20:
	            chaseVector[0] += prey.position[0]
	            # ignore y axis    	                
	            chaseVector[2] += prey.position[2]
	                
	            numberOfNeighbours += 1
	            
    	# avoid dividing by zero
        if numberOfNeighbours != 0:                
            chaseVector[0] /= numberOfNeighbours
            chaseVector[2] /= numberOfNeighbours
            
            chaseVector[0] = (chaseVector[0] - currentPredator.position[0])
            chaseVector[2] = (chaseVector[2] - currentPredator.position[2])
            
            chaseVector = normalizeVector(chaseVector)

            steer = self.steer(currentPredator, chaseVector)
            
        currentPredator.velocity[0]+= steer[0]*0.4
        currentPredator.velocity[2]+= steer[2]*0.4
        
        currentPredator.velocity = normalizeVector(currentPredator.velocity)
        
        
    def alertPrey(self, currentPrey):
        # search prey around current prey and alert to predator 
        for prey in self.preyArray:
            if currentPrey.distanceToAgent(prey) <4:
                if prey.flockFlag == False:
                    
                    
                    prey.flockFlag = True
                    
                    prey.detectedPredator = currentPrey.detectedPredator
                    
    def idlePrey(self, currentAgent):
        target = [0,0,0]
        targetDist = 2
        targetRadius = 0.3
        angle = rand.random()*5.0

        #target a point targetDist ahead of the prey
        target[0] = currentAgent.position[0] + (currentAgent.velocity[0]*targetDist)
        target[1] = 0
        target[2] = currentAgent.position[2] + (currentAgent.velocity[2]*targetDist)

        
        #pick taarget as random point on circumference
        target[0] = target[0] + targetRadius * math.cos(angle)
        target[2] = target[2] + targetRadius * math.sin(angle)
 
        # pick random goal position
        goalPos = target
         
  	    
        goalPos[0] = goalPos[0] - currentAgent.position[0]
        goalPos[2] = goalPos[2] - currentAgent.position[2]

        goalPos = normalizeVector(goalPos)

        steer = self.steer(currentAgent, goalPos)

        currentAgent.velocity[0] += steer[0] *0.5
        currentAgent.velocity[2] += steer[2] *0.5

        currentAgent.velocity = normalizeVector(currentAgent.velocity)
        
        
        
        numberOfNeighbours = 0
        seperationVector = [0,0,0]
    	  
        for agent in self.preyArray:
            if agent != currentAgent:               
                if currentAgent.distanceToAgent(agent) <2.0:
                    
                    seperationVector[0] += agent.position[0]-currentAgent.position[0]
                    # ignore y axis    	                
                    seperationVector[2] += agent.position[2]-currentAgent.position[2]
                    
                    seperationVector = normalizeVector(seperationVector)
                    
                    # -2 so that distance is zero at edge of cone
                    seperationVector[0] /= (currentAgent.distanceToAgent(agent)-0.4)
                    seperationVector[2] /= (currentAgent.distanceToAgent(agent)-0.4)   
                    
                    numberOfNeighbours += 1
        
        # avoid dividing by zero
        if numberOfNeighbours != 0:               
            seperationVector[0] /= numberOfNeighbours
            seperationVector[2] /= numberOfNeighbours
            seperationVector[0] *= -1;
            seperationVector[2] *= -1;
        
            seperationVector = normalizeVector(seperationVector)
            
           
            steer = self.steer(currentAgent, seperationVector)           
            
            currentAgent.velocity += steer*2
        
            currentAgent.velocity = normalizeVector(currentAgent.velocity)
        
        currentAgent.limitVel(0.2)
        
        
        
        
        #currentAgent.velocity = normalizeVector(currentAgent.velocity)
        
        
    
              
        
            
                                        	

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
    
    numberOfPrey = 60
    numberOfPredators = 1
    
    boidsRadius = 0.2
    
    scene = Scene(numberOfPrey, numberOfPredators )  
    
    scene.populateScene()
    
    scene.simulation(boidsRadius, scene.agentArray)
    