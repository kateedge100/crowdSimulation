# Simualtions Assignment Script
# Author: Kate Edge

import maya.cmds as cmds
import random as rand
import math as math

PI = 3.14159

# Class contains information for each boid
class Agent:
     # contructor
     def __init__(self, id, radius, predatorBool):
         
         # size of boid         
         self.radius = radius
         # allows spawning in -1 - 1 rather the 0 - 1
         self.position = [(rand.random()- rand.random())*20,self.radius, (rand.random()- rand.random())*20]
         self.velocity = [0, 0, 0]
         # rotation dictated by velocity in updateRotation function
         self.rotation = [0,0,0]
         # the name of each boid, set in scene class constructor
         self.id = id
         # booleon setting whether boid is a predator or not
         self.predator = predatorBool
         
         
         
         # if predator move towards main group of prey (makes more interesting flocking and elimates chance that it will be too far from prey)
         if self.predator== True:
             self.velocity[0] = 1
             self.velocity[2] = -1
             
         # if prey spawn with velocity between -1,1 in x and z direction, limit velocity   
         else:
             self.velocity = [rand.random()- rand.random(),0,rand.random()- rand.random()]
             
             self.velocity = normalizeVector(self.velocity)
             
             self.limitVel(0.1)
         
         # max force of boids, the greater this force the faster they change direction
         self.maxForce = 0.1     
         
         # whether or not a predator has been detected
         self.flockFlag = False
         
         # the detected predator
         self.detectedPredator = None
         

         # if predator spawn outside main group of prey (makes more interesting flocking)
         if self.predator == True:
             self.position = [- rand.random()*40,0.2,rand.random()*25]
         
         # create boid geometry
         cmds.polyCone(n = id, r = self.radius, h = 0.8, axis = (0,0,1))
         
         # cones are created with correct orientation
         self.updateRotation()
     
     # returns the distance between the current agent and an input agent    
     def distanceToAgent(self, Agent):
         distance = math.sqrt((self.position[0]-Agent.position[0])*(self.position[0]-Agent.position[0]) + (self.position[2]-Agent.position[2])*(self.position[2]-Agent.position[2]))
         
         return distance
     
     # if the agents velcity is above the input velocity it limits it to this value   
     def limitVel(self, limit):
         velLim = limit
         newVelocity = [0,0,0]
         
         if vectorMagnitude(self.velocity) > velLim:
             newVelocity[0] = (self.velocity[0]/vectorMagnitude(self.velocity))*velLim
             newVelocity[2] = (self.velocity[2]/vectorMagnitude(self.velocity))*velLim
             
             self.velocity = newVelocity
             
             
     # limits the input force to the agents preset max force          
     def limitForce(self, force):
         newForce = [0,0,0]
         
         if vectorMagnitude(force) > self.maxForce:
             newForce[0] = (force[0]/vectorMagnitude(force))*self.maxForce
             newForce[2] = (force[2]/vectorMagnitude(force))*self.maxForce
             
             return newForce
         else:
             return force
                 
     # updates rotation so that the boid faces the direction of its velocity
     def updateRotation(self):
       
         # rotation 0 when facing in z axis
         facing = [0,0,1]       
         
         #only update if moving             
         if self.velocity != [0,0,0]:
             
             mag1 = vectorMagnitude(facing)
             mag2 = vectorMagnitude(self.velocity)    
             
             # find angle between z axis and boids velocity vector    
             steer = math.acos(dotProduct(facing, self.velocity)/(mag1*mag2))
             
             # convert from radians to degrees
             steer = steer * (180/PI)
             
             # find the difference between the current rotation and desired rotation 
             diff = self.rotation[1] - steer
               
             # if rotation past 180 degrees must take away from 360, then update boid rotation
             if self.velocity[0]>0:
                 self.rotation[1] = steer
             else:
                 self.rotation[1]= 360-steer

                 
         
# Class contains behavour of boids and methods for simulating         
class Scene:
    def __init__(self, preyAgents, predatorAgents, boidRadius):
        # number of prey boids
        self.preyAgents = preyAgents
        # number of predator boids
        self.predatorAgents = predatorAgents
        # total number of boids
        self.agents = self.preyAgents + self.predatorAgents
        # array storing all boids, used for simulation
        self.agentArray = []
        # array of prey boids, used for flocking
        self.preyArray = []
        # array of predator boids, used for predator detection
        self.predatorArray = []
        
        self.boidRadius = boidRadius
               
    # creates boids by creating objects of the boids class    
    def populateScene(self):  
        #init prey             
        for i in range(0,self.preyAgents):
            currentAgent = Agent("agentPrey" + str(i), self.boidRadius, False)
            self.agentArray.append(currentAgent)
            self.preyArray.append(currentAgent)
        # init predators
        for i in range(0,self.predatorAgents):
            currentAgent = Agent("agentPredator" + str(i), self.boidRadius + 0.2, True)
            self.agentArray.append(currentAgent)
            self.predatorArray.append(currentAgent)
        
        # group together agents    
        cmds.group("agent*", name = "Agents")
        
        # select the predator to make it easier to see
        if self.predatorAgents != 0:
            cmds.select(self.predatorArray[0].id)
        else:
            cmds.select(self.preyArray[0].id)   
       
    
    # simulate behaviour keyframe boids position and rotation    
    def simulation(self):
        # number of frames
        maxFrame = 120
        cmds.playbackOptions(minTime=1, maxTime = maxFrame, animationStartTime=1, animationEndTime = maxFrame)
        for i in range(1, maxFrame+1):
            for j in range(self.agents):                
                
                # detects prey in range of predator and sets flag
                if self.agentArray[j].predator == True:
                    self.detectPredator(self.agentArray[j])
                                  
                # predator chases prey  
                if self.agentArray[j].predator == True:
                    self.chase(self.agentArray[j]) 
                 
                # if predator detected prey flocks        
                if self.agentArray[j].flockFlag == True:
                      
                    self.flock(self.agentArray[j])
                    
                    # if prey flocking it can alert surrounding prey to predator    
                    self.alertPrey(self.agentArray[j])
                
                # if not flocking prey wander
                elif self.agentArray[j].flockFlag == False and  self.agentArray[j].predator == False:
                    self.idlePrey(self.agentArray[j])
                
                
                                            
                # keyframe position and rotation for each frame 
                cmds.setKeyframe(self.agentArray[j].id, attribute="rx", v=self.agentArray[j].rotation[0], t=[i], inTangentType="spline", outTangentType="spline")
                cmds.setKeyframe(self.agentArray[j].id, attribute="ry", v=self.agentArray[j].rotation[1], t=[i], inTangentType="spline", outTangentType="spline")
                cmds.setKeyframe(self.agentArray[j].id, attribute="rz", v=self.agentArray[j].rotation[2], t=[i], inTangentType="spline", outTangentType="spline")  
                   
                cmds.setKeyframe(self.agentArray[j].id, attribute="tx", v=self.agentArray[j].position[0], t=[i], inTangentType="spline", outTangentType="spline")
                cmds.setKeyframe(self.agentArray[j].id, attribute="ty", v=self.agentArray[j].position[1], t=[i], inTangentType="spline", outTangentType="spline")
                cmds.setKeyframe(self.agentArray[j].id, attribute="tz", v=self.agentArray[j].position[2], t=[i], inTangentType="spline", outTangentType="spline")
	            
                
                # limit velocity (1 is max)
                self.agentArray[j].limitVel(0.6) 
                
	            # update the position of all the boids based on their current velocity
                self.agentArray[j].position[0] += self.agentArray[j].velocity[0]
                self.agentArray[j].position[2] += self.agentArray[j].velocity[2]
                
                #if self.agentArray[j].flockFlag == True or self.agentArray[j].predator == True:                 
                self.agentArray[j].updateRotation()
                	
  	
  	# find flock vector and add to prey velocity	
    def flock(self, currentAgent):
        
         steer = [0,0,0]
         
         # compute the flocking component vectors
         alignment = self.computeAlignment(currentAgent)
         cohesion = self.computeCohesion(currentAgent)
         separation = self.computeSeperation(currentAgent)
        
         # flocking component weights
         alignmentWeight = 1
         cohesionWeight = 1 
         separationWeight = 2
                 
         # find resulting flocking vector
         steer[0] += (cohesion[0] * cohesionWeight) + (alignment[0] * alignmentWeight) + (separation[0] * separationWeight);
         steer[2] += (cohesion[2] * cohesionWeight) + (alignment[2] * alignmentWeight) + (separation[2] * separationWeight);
        
         steer = normalizeVector(steer) 
         
         # steer towards flocking vector
         currentAgent.velocity[0] += self.steer(currentAgent,steer)[0]
         currentAgent.velocity[2] += self.steer(currentAgent,steer)[2]
         
         currentAgent.velocity = normalizeVector(currentAgent.velocity)
         
         # steer away from predator if near
         if currentAgent.flockFlag == True and currentAgent.distanceToAgent(currentAgent.detectedPredator) < 8:
         
             fleeVec = [0,0,0]
             
             # vector in opossite direction to predator
             fleeVec[0] = -(currentAgent.detectedPredator.position[0] - currentAgent.position[0])
             fleeVec[2] = -(currentAgent.detectedPredator.position[2] - currentAgent.position[2])
                         
             fleeVec = normalizeVector(fleeVec)
             
             predatorDist = currentAgent.distanceToAgent(currentAgent.detectedPredator)
             
             # distance 0 at border and avoid weight max
             avoidWeight = 10/(predatorDist-0.2)
             
             # steer away from predator, steering force based on distance to predator         
             currentAgent.velocity[0] += self.steer(currentAgent, fleeVec)[0]*avoidWeight
             currentAgent.velocity[2] += self.steer(currentAgent, fleeVec)[2]*avoidWeight
                
             currentAgent.velocity = normalizeVector(currentAgent.velocity) 
         
    # compute alignment vector				
    def computeAlignment(self, currentAgent):
        numberOfNeighbours = 0
    	alignmentVector = [0,0,0]
    	steer = [0,0,0]    
    	for agent in self.preyArray:
    	    # only flock with other flocking boids
    	    if agent != currentAgent:
    	        if agent.flockFlag == True:
        	        if currentAgent.distanceToAgent(agent) < 2:
        	            
        	            alignmentVector[0] += agent.velocity[0]   	                
        	            alignmentVector[2] += agent.velocity[2]
        	                
        	            numberOfNeighbours += 1
    	# avoid dividing by zero
        if numberOfNeighbours != 0:
            
            # find average velocity of boids in the current boids neighborhood   
            alignmentVector[0] /= numberOfNeighbours
            alignmentVector[2] /= numberOfNeighbours
        	
           
            alignmentVector = normalizeVector(alignmentVector)         
    	               
    	return alignmentVector
    
    # compute cohesion vector	
    def computeCohesion(self, currentAgent):
        numberOfNeighbours = 0
    	cohesionVector = [0,0,0]
    	steer = [0,0,0]    
    	for agent in self.preyArray:
    	    if agent != currentAgent: 
    	        if agent.flockFlag == True:
        	        if currentAgent.distanceToAgent(agent) < 10:
        	                        
        	            cohesionVector[0] += agent.position[0]   	                
        	            cohesionVector[2] += agent.position[2]
        	                
        	            numberOfNeighbours += 1
        	            
    	# avoid dividing by zero
        if numberOfNeighbours != 0: 
            
            # find average position               
            cohesionVector[0] /= numberOfNeighbours
            cohesionVector[2] /= numberOfNeighbours
        	
            # find vector from agent to average position
            cohesionVector[0] = (agent.position[0] - cohesionVector[0])
            cohesionVector[2] = (agent.position[2] - cohesionVector[2])
            
            
            cohesionVector = normalizeVector(cohesionVector)        
    	               
        return cohesionVector
    
    # compute seperation vector	
    def computeSeperation(self, currentAgent):
        numberOfNeighbours = 0
        seperationVector = [0,0,0]
    	steer = [0,0,0]
    	
    	diff = [0,0,0]    
        for agent in self.preyArray:
            if agent != currentAgent:
                if agent.flockFlag == True:
                    if currentAgent.distanceToAgent(agent) <1.0:
                        
                        # vector from current boid to neighbor
                        diff[0] = agent.position[0]-currentAgent.position[0]  	                
                        diff[2] = agent.position[2]-currentAgent.position[2]
                        
                        diff = normalizeVector(diff)
                        
                        # the closer to its neighbors the greater the seperation vector
                        seperationVector[0] += diff[0] / (currentAgent.distanceToAgent(agent))
                        seperationVector[2] += diff[2] / (currentAgent.distanceToAgent(agent))   
                        
                        numberOfNeighbours += 1
        
        # avoid dividing by zero
        if numberOfNeighbours != 0:               
            seperationVector[0] /= numberOfNeighbours
            seperationVector[2] /= numberOfNeighbours
            # run in opposite direction to average neighbor position
            seperationVector[0] *= -1;
            seperationVector[2] *= -1;
        
            seperationVector = normalizeVector(seperationVector)             
                       
        return seperationVector
    
    # set predator detected flag if predator in range    
    def detectPredator(self, currentPredator):
        for agent in self.agentArray:
            if agent.predator == False:
                if currentPredator.distanceToAgent(agent) < 6:
   
                    agent.flockFlag = True  
                    
                    # identify predator if more then one present
                    agent.detectedPredator = currentPredator
                                                           
                   
                
    # implements Craig Reynolds steering method    
    def steer(self, currentAgent, target):
        steer = [0,0,0]
        steer[0] = target[0] - currentAgent.velocity[0]
        steer[2] = target[2] - currentAgent.velocity[2]
        
        steer = currentAgent.limitForce(steer)
        
        return steer
    
    # predator chases nearby prey    
    def chase(self, currentPredator):
        
        numberOfNeighbours = 0
    	chaseVector = [0,0,0]
    	steer = [0,0,0]  
    	  
    	for prey in self.preyArray:    	    
	        if currentPredator.distanceToAgent(prey) < 6:
	            
	            chaseVector[0] += prey.position[0]    	                
	            chaseVector[2] += prey.position[2]
	                
	            numberOfNeighbours += 1
	            
    	# avoid dividing by zero
        if numberOfNeighbours != 0:                
            chaseVector[0] /= numberOfNeighbours
            chaseVector[2] /= numberOfNeighbours
            
            chaseVector[0] = (chaseVector[0] - currentPredator.position[0])
            chaseVector[2] = (chaseVector[2] - currentPredator.position[2])
            
            chaseVector = normalizeVector(chaseVector)

            # steer towards average neighbor prey position
            steer = self.steer(currentPredator, chaseVector)
        
        # increase steering force of predator when chasing prey    
        currentPredator.velocity[0]+= steer[0]*1.5
        currentPredator.velocity[2]+= steer[2]*1.5
        
        currentPredator.velocity = normalizeVector(currentPredator.velocity)
        
    # alerts neighbors of flocking prey to predator    
    def alertPrey(self, currentPrey):
        for prey in self.preyArray:
            if currentPrey.distanceToAgent(prey) <4:
                if prey.flockFlag == False:
                    
                    # alert to predator
                    prey.flockFlag = True
                    
                    # tell prey which predator is nearby
                    prey.detectedPredator = currentPrey.detectedPredator
    
    # implenet Craig Reynolds wander method, compine with seperation                
    def idlePrey(self, currentAgent):
        target = [0,0,0]
        targetDist = 2
        targetRadius = 0.3
        goalPos = [0,0,0]
        
        # random angle to turn by
        angle = (rand.random()- rand.random())*20.0
        
        turn = [0,0,0]
        facing =[1,0,0]
        
        mag1 = vectorMagnitude(facing)
        mag2 = vectorMagnitude(currentAgent.velocity)    
        
        # angle between prey velocity and x axis, needed for polar coordinates        
        turning = math.acos(dotProduct(facing, currentAgent.velocity)/(mag1*mag2))
        
        # radians to degrees
        turning = turning * (180/PI)
        
        # find x axis to new heading angle    
        angle = angle + turning     
        
       
        # radians to degrees
        angle = angle * (PI/180)
        

        #target a point targetDist ahead of the prey
        target[0] = currentAgent.position[0] + (currentAgent.velocity[0]*targetDist)
        target[2] = currentAgent.position[2] + (currentAgent.velocity[2]*targetDist)
        
        
        #pick target as random point on circumference
        target[0] = target[0] + (targetRadius * math.cos(angle))
        target[2] = target[2] + (targetRadius * math.sin(angle))
          
  	    # find vector from current position to desired position
        goalPos[0] = target[0] - currentAgent.position[0]
        goalPos[2] = target[2] - currentAgent.position[2]

        goalPos = normalizeVector(goalPos)

        # steer to desired wandering spot
        steer = self.steer(currentAgent, goalPos)

        currentAgent.velocity[0] += steer[0] *0.5
        currentAgent.velocity[2] += steer[2] *0.5

        currentAgent.velocity = normalizeVector(currentAgent.velocity)
        
        # Add seperation
        numberOfNeighbours = 0
        seperationVector = [0,0,0]
        
        diff = [0,0,0]
    	  
        for agent in self.preyArray:
            if agent != currentAgent:               
                if currentAgent.distanceToAgent(agent) <1.5:
                 
                    # vector from current agent position to neighbor position
                    diff[0] = agent.position[0] - currentAgent.position[0]  	                
                    diff[2] = agent.position[2] - currentAgent.position[2]
                    
                    diff = normalizeVector(diff)
                    
                    # seperation vector greater when close to neighbor
                    seperationVector[0] += diff[0] / (currentAgent.distanceToAgent(agent))
                    seperationVector[2] += diff[2] / (currentAgent.distanceToAgent(agent))   
                    
                    numberOfNeighbours += 1
        
        # avoid dividing by zero
        if numberOfNeighbours != 0:               
            seperationVector[0] /= numberOfNeighbours
            seperationVector[2] /= numberOfNeighbours
            seperationVector[0] *= -1;
            seperationVector[2] *= -1;
        
            seperationVector = normalizeVector(seperationVector)

            # steer away from neighbors
            steer = self.steer(currentAgent, seperationVector)           
           
            currentAgent.velocity[0] += steer[0]*2
            currentAgent.velocity[2] += steer[2]*2
           
            currentAgent.velocity = normalizeVector(currentAgent.velocity)
        # limit velocity
        currentAgent.limitVel(0.05)
                 
        
            
                                        	
# return the magnitude of a vector
def vectorMagnitude(v):
 
    sum = 0.0
    for i in range(len(v)):

        sum +=v[i]*v[i]
    sum = math.sqrt(sum)
	
    return sum

# returns the normalized vector       	    
def normalizeVector(v):
    sum = vectorMagnitude(v)
    for i in range(len(v)):
        if sum !=0:
            v[i]/=sum
    return v
    
# returns the dot product of two vectors    
def dotProduct(V1, V2):
	return V1[0]*V2[0]+V1[1]*V2[1]+V1[2]*V2[2]
                  
if __name__ == "__main__":
  
    cmds.select(all=True)
    cmds.delete()
    
    numberOfPrey = 80
    numberOfPredators = 2
    
    boidsRadius = 0.2
    
    # create scenes
    scene = Scene(numberOfPrey, numberOfPredators, boidsRadius)  
    
    # populate scene
    scene.populateScene()
    
    # simulate scene
    scene.simulation()
    