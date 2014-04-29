import Base.Test

type Fumehood
	kind::Int	# there are different types, need to clarify them here
	height::Float32
	width::Float32
	minflowrate::Float32
	maxflowrate::Float32
	facevelocityoccupied::Float32
	facevelocityunoccupied::Float32
	maxsash::Float32
	maxcfm::Float32
	mincfm::Float32
	occupied::Bool
	bac::Int
	tag::String
	building::String
	room::Int
	hoodnumber::Int
	department::String
	uselevel::Int # 0 := light, 1 := medium, 2 := heavy
end

type Lab
	area::Float32
	hood_count::Int
	height::Float32
	minach::Float32
end

type Ventilation
	costpercfminput::Float32
	costpercfmoutput::Float32
end


function facevelocity(hood::Fumehood)
  if hood.occupied
    return hood.facevelocityoccupied
  else
    return hood.facevelocityunoccupied
  end
end

function faceintakecfm(hood::Fumehood)
  hood.facevelocity * hood.maxsash * hood.sashheight * hood.sashwidth / 144
end

function fumehoodcfm(hood::Fumehood)
  min([hood.maxcfm, max([hood.mincfm, faceintakecfm(hood)])])
end