using DataFrames

function loadflowdatastream(file)
    flowdataframe = readtable(file)
    bacgroups = groupby(flowdataframe, :BAC)
end