#Author: Qi Zhu, Robotics Institute at Carnegie Mellon University
#Registrate materials and objects in one scene
import numpy as np

#Example of scene_generation
def scene_office():
	material_pool=['Ground_guiFloodedMud','Ground_MuddyGrass_DRY','Ground_MuddyGrass_WET',\
'MasterMaterial','Metal_BrushedCopper','Metal_BrushedSteel','Metal_CyberCube',\
'Metal_DiamondPlateSciFi','Metal_Gold','Metal_LeadRough','Metal_ReinforcedGridWall',\
'Metal_RustedSolid','Metal_sciFiCurveyWall','misc_WoodenCrate','Rock_HoleyWall',\
'Rock_JaggedCaveWall','Tile_Coloredtiles','Tile_WoodAndTileOffsetPattern',\
'Wood_GeofwoodenPlankClean','Wood_InterlockingFloor',\
'brick_ancientDiagonal','Brick_BathStone',\
'Brick_GuiBigCastleWall','brick_guiGen',\
'Ground_Dirt','Ground_DirtBrownTan','Ground_GrassThickGreen']

	Scissors1=np.array((20,20))

	DeskPhone=np.array((39,27))*1.110077
	DeskLamp=np.array((20,20))
	DeskAshtray=np.array((39,33))*0.569885
	DeskCup=np.array((16,11))
	DeskNameplate=np.array((5,32))*1.1

	Desk=np.array((180,120))
	obj_list=[Scissors1,DeskPhone,DeskLamp,DeskAshtray,DeskCup,DeskNameplate]
	obj_name=['scissors1','DeskPhone','DeskLamp','DeskAshtray',\
	'DeskCup','DeskNameplate']
	obj_changes=['DeskLamp','DeskCup','DeskNameplate']
	return Desk,material_pool,obj_list,obj_name,obj_changes