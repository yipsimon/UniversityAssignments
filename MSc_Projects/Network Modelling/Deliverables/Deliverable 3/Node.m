classdef Node < handle
    properties
        nodeID;
        applications;
        totalSendingRate;
        networkLinks;
    end %properties
    
    methods (Static)
        
        function NN = Node(ID)
            
            NN.nodeID = ID;
            NN.applications = [];
            NN.totalSendingRate = 0;
            NN.networkLinks = [];
            
        end % function Node()
        
        function A = registerApplication(simulationManager,nodeID,app)
            
            result = findobj(simulationManager.nodes,'nodeID',nodeID);
            result.applications = [result.applications;app];
            A = simulationManager;
            
        end %function registerApplication()
        
        function A = registerNetworkLink(simulationManager,nodeID,newLink)
            
            result = findobj(simulationManager.nodes,'nodeID',nodeID);
            result.networkLinks = [result.networkLinks;newLink];
            A = simulationManager;
            
        end %function registerNetworkLink()
        
    end %methods
    
end %classdef