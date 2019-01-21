classdef NetworkLink < handle
    properties
        ID;
        maximumBandwidth;
        errorRate;
    end %properties
    
    methods (Static)
        
        function NL = NetworkLink(ID, maximumBandwidth, errorRate)
            
            NL.ID = ID;
            NL.maximumBandwidth = maximumBandwidth;
            NL.errorRate = errorRate;
            
        end % function Application()
        
    end %methods
    
end %classdef