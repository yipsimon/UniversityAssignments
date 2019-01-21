function varargout = courseworkGUI(varargin)
% COURSEWORKGUI MATLAB code for courseworkGUI.fig
%      COURSEWORKGUI, by itself, creates a new COURSEWORKGUI or raises the existing
%      singleton*.
%
%      H = COURSEWORKGUI returns the handle to a new COURSEWORKGUI or the handle to
%      the existing singleton*.
%
%      COURSEWORKGUI('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in COURSEWORKGUI.M with the given input arguments.
%
%      COURSEWORKGUI('Property','Value',...) creates a new COURSEWORKGUI or raises
%      the existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before courseworkGUI_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to courseworkGUI_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help courseworkGUI

% Last Modified by GUIDE v2.5 19-Feb-2018 14:58:40

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @courseworkGUI_OpeningFcn, ...
                   'gui_OutputFcn',  @courseworkGUI_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end

% End initialization code - DO NOT EDIT

% --- Executes just before courseworkGUI is made visible.
function courseworkGUI_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to courseworkGUI (see VARARGIN)
handles.simulationManager = simulationManager();

% Choose default command line output for courseworkGUI
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);



% UIWAIT makes courseworkGUI wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = courseworkGUI_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;

function num_nodes_Callback(hObject, eventdata, handles)
% hObject    handle to num_nodes (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of num_nodes as text
%        str2double(get(hObject,'String')) returns contents of num_nodes as a double
input = str2num(get(hObject,'String'));
if(isempty(input))
    set(hObject,'String','0')
end
guidata(hObject,handles);


% --- Executes during object creation, after setting all properties.
function num_nodes_CreateFcn(hObject, eventdata, handles)
% hObject    handle to num_nodes (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function num_app_Callback(hObject, eventdata, handles)
% hObject    handle to num_app (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of num_app as text
%        str2double(get(hObject,'String')) returns contents of num_app as a double
input = str2num(get(hObject,'String'));
if(isempty(input))
    set(hObject,'String','0')
end
guidata(hObject,handles);

% --- Executes during object creation, after setting all properties.
function num_app_CreateFcn(hObject, eventdata, handles)
% hObject    handle to num_app (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function seed_num_Callback(hObject, eventdata, handles)
% hObject    handle to seed_num (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of seed_num as text
%        str2double(get(hObject,'String')) returns contents of seed_num as a double
input = str2num(get(hObject,'String'));
if(isempty(input))
    set(hObject,'String','0')
end
guidata(hObject,handles);

% --- Executes during object creation, after setting all properties.
function seed_num_CreateFcn(hObject, eventdata, handles)
% hObject    handle to seed_num (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function sim_time_Callback(hObject, eventdata, handles)
% hObject    handle to sim_time (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of sim_time as text
%        str2double(get(hObject,'String')) returns contents of sim_time as a double
input = str2num(get(hObject,'String'));
if(isempty(input))
    set(hObject,'String','0')
end
guidata(hObject,handles);

% --- Executes during object creation, after setting all properties.
function sim_time_CreateFcn(hObject, eventdata, handles)
% hObject    handle to sim_time (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in prioritise_button.
function prioritise_button_Callback(hObject, eventdata, handles)
% hObject    handle to prioritise_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
input = get(hObject,'Value');
if(isempty(input))
    set(hObject,'Value','0')
end
guidata(hObject,handles);
% Hint: get(hObject,'Value') returns toggle state of prioritise_button


% --- Executes on button press in runRandomSimulation.
function runRandomSimulation_Callback(hObject, eventdata, handles)
% hObject    handle to runRandomSimulation (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

%disable button while simulation executes
set(handles.runRandomSimulation,'Enable','off');

generateRandomTopology(hObject, handles);

%re-enable button
set(handles.runRandomSimulation,'Enable','on');



function generateRandomTopology(hObject, handles)

%clear any existing topology
handles.simulationManager = simulationManager();

%generate random topology based on the following values

%maximum/minimum network link size
maxNetLink = 100000; %Kb/s
minNetLink = 50000; %Kb/s

%maximum error rate of network link
maxErrorRate = 0.5;
minErrorRate = 0.1;

%maximum/minimum send rate of application
maxSendRate = 60000; %Kb/s
minSendRate = 10000; %Kb/s

%maximum priority of application
maxPriority = 10;

%get seed value for random numbers
seed = str2num(get(handles.seed_num,'String'));

%number of nodes in system
numOfNodes = str2num(get(handles.num_nodes,'String'));

%number of applications randomly distributed across the nodes
numOfApplications = str2num(get(handles.num_app,'String'));

%create random number set for network link max bandwidth
RandStream.setGlobalStream(RandStream('mt19937ar','seed',seed));
seed = seed + 1;
linkMaxBandwidth = rand(1,numOfNodes);
linkMaxBandwidth = (linkMaxBandwidth.*(maxNetLink-minNetLink))+minNetLink;

%create random number set for network link error rate
RandStream.setGlobalStream(RandStream('mt19937ar','seed',seed));
seed = seed + 1;
linkErrorRate = rand(1,numOfNodes);
linkErrorRate = (linkErrorRate.*(maxErrorRate-minErrorRate))+minErrorRate;

%associate the network links with the nodes
for i = 1:numOfNodes
    newNode = Node(i);
    handles.simulationManager = simulationManager.registerNode(handles.simulationManager,newNode);
    newLink = NetworkLink(i,round(linkMaxBandwidth(1,i)),linkErrorRate(1,i));
    handles.simulationManager = Node.registerNetworkLink(handles.simulationManager,i,newLink);
end

%create random number set to decide which node to put an application on
RandStream.setGlobalStream(RandStream('mt19937ar','seed',seed));
seed = seed + 1;
appNode = rand(1,numOfApplications);
appNode = appNode.*numOfNodes;

%create random number set for application sending rate
RandStream.setGlobalStream(RandStream('mt19937ar','seed',seed));
seed = seed + 1;
appSendingRate = rand(1,numOfApplications);
appSendingRate = (appSendingRate.*(maxSendRate-minSendRate))+minSendRate;

%create random number set for application priority
RandStream.setGlobalStream(RandStream('mt19937ar','seed',seed));
appPriority = rand(1,numOfApplications);
appPriority = appPriority.*maxPriority;

%Create applications and associate with nodes
for i = 1:numOfApplications        
    newApp = Application(i, round(appSendingRate(1,i)), ceil(appPriority(1,i)));
    handles.simulationManager = Node.registerApplication(handles.simulationManager,ceil(appNode(1,i)),newApp);
end

% Update handles structure
guidata(hObject, handles);

%call function to run the simulation
runSimulation(hObject, handles);



function runSimulation(hObject, handles)

%set length of time to run simulation
totalSimulationTime = str2num(get(handles.sim_time,'String'));

%determine the number of nodes in the generated topology
numberOfNodes = size(handles.simulationManager.nodes,1);

%set whether prioritisation of applications is used
prioritise = get(handles.prioritise_button,'Value');

%calculate the total data rate required for each node and perform
%prioritisation if required

for i=1:numberOfNodes

    handles.simulationManager.nodes(i).totalSendingRate = handles.simulationManager.nodes(i).networkLinks(1).maximumBandwidth + 1;

    %loop will always enter at least once
    while handles.simulationManager.nodes(i).totalSendingRate > handles.simulationManager.nodes(i).networkLinks(1).maximumBandwidth

        %start by calculating the total sending rate required
        totalSendingRate = 0;
        lowestPriority = [1000000000000000, 0];

        for j=1:size(handles.simulationManager.nodes(i).applications)

            if handles.simulationManager.nodes(i).applications(j).enabled == 1

                totalSendingRate = totalSendingRate + handles.simulationManager.nodes(i).applications(j).sendingRate;

                if handles.simulationManager.nodes(i).applications(j).priority < lowestPriority(1,1)

                    lowestPriority = [handles.simulationManager.nodes(i).applications(j).priority, j];

                end
            end

        end

        %save the total sending rate without network errors for the given
        %node
        handles.simulationManager.nodes(i).totalSendingRate = totalSendingRate;
        
        %If prioritise == 1 then use the priority of appplications to
        %adjust those that are allowed to send, based on available network
        %link bandwidth
        if prioritise == 1
            
            if totalSendingRate > handles.simulationManager.nodes(i).networkLinks(1).maximumBandwidth

                %deactivate lowest priority app
                handles.simulationManager.nodes(i).applications(lowestPriority(1,2)).enabled = 0;

            end
        else
            %if prioritisation is not required then break from the loop
            break;
            
        end

    end

end
networkLinkUsage = zeros(numberOfNodes,2);
%apply error rate to nodes
for i=1:totalSimulationTime
    
    %display(i);
    
    %for each node
    for j=1:numberOfNodes
        
        %assuming data lost through error is retransmitted and received
        %correctly the second time
        
        %calculate the probability of an error occuring 
        errorProbability = rand(1);
        
        %calculate the bandiwdth required given this error
        actualBandwidthRequired = handles.simulationManager.nodes(j).totalSendingRate * ...
            (1 + (errorProbability * handles.simulationManager.nodes(j).networkLinks(1).errorRate));
        
        %save the network link utilisation both with and without errors as
        %a percentage of the maximum available
        networkLinkUsage(j,1) = (handles.simulationManager.nodes(j).totalSendingRate/handles.simulationManager.nodes(j).networkLinks(1).maximumBandwidth)*100;
        networkLinkUsage(j,2) = (actualBandwidthRequired/handles.simulationManager.nodes(j).networkLinks(1).maximumBandwidth)*100;   
    end
    
    display(networkLinkUsage);
    %pause to display output
    pause(0.25);

end
figure
bar(networkLinkUsage);
title('Network resources consumed by each node');
xlabel('Node number')
ylabel('A percentage of the total network resources required')
legend('Before Error','After Error');

fid=fopen('courseworkGUIOutput.csv','w');	
for i=1:numberOfNodes
    fprintf(fid,'%f,%f\n',networkLinkUsage(i,1),networkLinkUsage(i,2));	
end
fclose(fid);	
