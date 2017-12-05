# Simualtions Script

import maya.cmds as cmds
import random as rand
import math as math


class Agent:
     # contructor
     def __init__(self, id, sphereRadius):
         self.position = [rand.random(),sphereRadius, rand.random()]
         self.velocity = [rand.random()/40, 0, rand.random()/40]
         self.id = id
         
         cmds.sphere(n = id, r = sphereRadius)
         cmds.move(self.position[0], self.position[1], self.position[2], id)
        
         
         
class Scene:
    def __init__(self, agents):
        self.agents = agents
        self.agentArray = []
        
        
    def populateScene(self):               
        for i in range(0,self.agents):
            currentAgent = Agent("agent" + str(i), 0.2)
            self.agentArray.append(currentAgent)
        cmds.group("agent*", name = "Agents")
        cmds.select(agentArray[0].id)    
        print self.agentArray[0].id
        print self.agentArray[0].position
        
    def simulation(self, ballRadius, agentArray):
        maxFrame = 400
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
	        
	            for j in range(self.agents):
	                cmds.move(agentArray[j].position[0], agentArray[j].position[1], agentArray[j].position[2], agentArray[j].id)
                  
         
if __name__ == "__main__":
  
    cmds.select(all=True)
    cmds.delete()
    
    numberOfBois = 20
    boisRadius = 0.2
    
    scene = Scene(numberOfBois)  
    
    scene.populateScene()
    
    scene.simulation(boisRadius, scene.agentArray)

          
    
	
  
        
    