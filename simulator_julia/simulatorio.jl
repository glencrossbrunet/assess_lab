function loadflowdatastream(file)
    flowstream = open(file)
    for line = eachline(stream)
        datapoint = processflowdatapoint(line)
    end
end

function processflowdatapoint(line)
    line = split(strip(line), ",")
end