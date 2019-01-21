classdef Application < handle
    properties
        ID;
        sendingRate;
        priority;
        enabled;
    end %properties
    
    methods (Static)
        
        function AA = Application(ID, sendingRate, priority)
            
            AA.ID = ID;
            AA.sendingRate = sendingRate;
            AA.priority = priority;
            AA.enabled = 1;
            
        end % function Application()
        
    end %methods
    
end %classdef