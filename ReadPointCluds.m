%[FILENAME, PATHNAME] = uigetfile('*.ply','MultiSelect', 'on');
%fileName = strcat(PATHNAME,FILENAME);

[FILENAME, PATHNAME] = uigetfile('*.ply','MultiSelect', 'on');
 num_Files = length(FILENAME);
 
for ndx = 1:num_Files
    fileName = strcat(PATHNAME,FILENAME{ndx});

    %ptCloud = plyToMatSO(filename);
    disp(fileName);

    idx = 1;
    fid = fopen(fileName, 'r');
    while isempty(strfind(fgets(fid), 'end_header'))
        idx = idx + 1;
    end
    fclose(fid);

    data = textread(fileName, '%s','delimiter', '\n');
    data = data(idx+1:length(data),1);
    data = (cellfun(@(x) strread(x,'%s','delimiter',' '), data, 'UniformOutput', false));

    if isempty(data{length(data)})
        data(length(data))=[];
    end

    pc = str2double([data{:}].');

    image = pointcloud2image(pc(:,3),pc(:,2),pc(:,1), 83, 95);
    figure1 = imshow(image)
    saveas(figure1,strcat(FILENAME{ndx}(1:(length(FILENAME{ndx})-4)),'.png'))
    
    image = pointcloud2image(pc(:,3),pc(:,2),pc(:,1), 83*2, 95*2);
    figure1 = imshow(image)
    saveas(figure1,strcat(FILENAME{ndx}(1:(length(FILENAME{ndx})-4)),'_extra_pixels.png'))    
end