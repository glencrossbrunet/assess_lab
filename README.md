# Fume Hood Lab Assessment Software


## Available Produced Statistics and Plots




### A Note on Data Management in This Repository

Because I have added the output CSVs and PDFs to the Github, a lot of data gets modified every time I run the code and thus pushed to the Github.
Regularly this would be terrible, but it inevitably proves useful to keep a current copy of the results with the code that generates them so I'm leaving it like this!
Change it to be more proper from a programmer's perspective if you prefer, and I will keep local copies of the results.

## Agents

Lab := agent container
Fume Hood := ventilation device


## Variables

### Fume Hood

    type::UInt8	# there are different types, need to clarify them here
    height::Float32
    width::Float32
    minflowrate::Float32
    maxflowrate::Float32
    facevelocityoccupied::Float32
    facevelocityunoccupied::Float32
    maxsash::Float32
    hoodmaxcfm::Float32
    hoodmincfm::Float32
    occupied::Bool

### Lab Information

    area::Float32
    hood_count::UInt16
    height::Float32
    min_ach::Float32


### Ventilation

    cost_per_cfm


## Equations

    function facevelocity
      if occupied
        return facevelocityoccupied
      else
        return facevelocityunoccupied
      end
    end

    function faceintakecfm
      facevelocity * maxsash * sashheight * sashwidth / 144
    end

    function fumehoodcfm
      min([hoodmaxcfm, max([hoodmincfm, faceintakecfm])])
    end

# TODO

## Analysis

Check frequency of NA in the dataset.
