classdef simulationManager < handle
    properties
        nodes;
    end %properties
    
    methods (Static)
        
        function SM = simulationManager()
            
            SM.nodes = [];
            
        end % function Node()
        
        function A = registerNode(simulationManager,node)
            
            simulationManager.nodes = [simulationManager.nodes;node];
            A = simulationManager;
            
        end %function registerNode()
        
    end %methods
    
end %classdef