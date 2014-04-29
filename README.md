# Fume Hood Lab Assessment Software

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