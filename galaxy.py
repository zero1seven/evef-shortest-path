import json

IDS = {}
NAMES = {}
CONSTELLATIONS = {}
REGIONS = {}
SOLARSYSTEMS = {}
GALAXY = {}

class SolarSystem:
	def __init__(self, name:str, solarsystemid:int, region_name: str, constellation_name: int, center: list, neighbors: list, planets: list):
		self.name = name
		self.solarsystemid = solarsystemid
		self.region_name = region_name
		self.constellation_name = constellation_name
		self.center = center
		self.neighbors = neighbors
		self.planets = planets

	def __str__(self):
		return f"""Solar System: {self.name} ID: {self.solarsystemid} Region: {self.region_name} Constellation Name: {self.constellation_name} Neighbors: {', '.join(map(str, self.neighbors))} Planets: {','.join(map(str,self.planets))}"""

class Constellation:
	
	def __init__(self, name:str, constellationid:int, region_name: str, solarsystems: list):
		self.name = name
		self.constellationid = constellationid
		self.region_name = region_name
		self.solarsystems = solarsystems

	def __str__(self):
		return f"""Constellation: {self.name} ID: {self.constellationid} Region: {self.region_name} SolarSystems: {', '.join(map(str, self.solarsystems))}"""

class Region:
	def __init__(self, name:str, regionid:int, constellations: list, solarsystems: list):
		self.name = name
		self.regionid = regionid
		self.constellations = constellations
		self.solarsystems = solarsystems

	def __str__(self):
			return f"""Region: {self.name} ID: {self.regionid} Constellations: {', '.join(map(str, self.constellations))} SolarSystems: {', '.join(map(str, self.solarsystems))}"""

def messageid_to_name(us_localization: json, main_localization: json, celestial_data: json):

	for i in main_localization["labels"]:
		if 'Map/Regions' in main_localization["labels"][i]["FullPath"]:
			IDS[i] = int(main_localization["labels"][i]['label'][7:])
		elif 'Map/SolarSystems' in main_localization["labels"][i]["FullPath"]:
			IDS[i] = int(main_localization["labels"][i]['label'][13:])
		elif 'Map/Constellations' in main_localization["labels"][i]["FullPath"]:
			IDS[i] = int(main_localization["labels"][i]['label'][14:])

	for i in IDS:
		NAMES[i] = us_localization[1][i][0]

	###Temp until real celeste data found
	for i in celestial_data:
		ids = celestial_data[i]
		IDS[ids] = ids
		NAMES[ids] = i

def load_data(starmapdata: json, us_localization: json, main_localization: json, celestial_data: json):
	messageid_to_name(us_localization, main_localization, celestial_data) 
	SOLARSYSTEMS = get_starsystems(starmapdata)
	REGIONS = get_regions(starmapdata)
	CONSTELLATIONS = get_constellations(starmapdata)
	GALAXY = {
	"regions": REGIONS,
	"solarsystems": SOLARSYSTEMS,
	"constellations": CONSTELLATIONS
	}
	return GALAXY

def get_name(nameid:int):
	for m in IDS:
		if IDS[m] == nameid:
			return NAMES[m]
	return

def get_constellations(starmapdata: json):
	constellations = {}
	for c in starmapdata['constellations']:
		constellationid = int(c)
		region_name = get_name(starmapdata['constellations'][c]['regionID'])
		name = get_name(c)
		solarsystems = []
		for n in starmapdata['constellations'][c]['solarSystemIDs']:
			solarsystems.append(get_name(n))
		constellations[name] = Constellation(name, constellationid, region_name, solarsystems)
	return constellations

def get_regions(starmapdata: json):
	regions = {}
	for r in starmapdata['regions']:
		regionid = int(r)
		name = get_name(r)
		region_name = get_name(int(r))
		solarsystems = []
		constellations = []
		for n in starmapdata['regions'][r]['solarSystemIDs']:
			solarsystems.append(get_name(n))
		for n in starmapdata['regions'][r]['constellationIDs']:
			constellations.append(get_name(n))
		regions[region_name] = Region(name, regionid, constellations, solarsystems)
	return regions

def get_starsystems(starmapdata: json):
	starsystems = {}
	for s in starmapdata['solarSystems']:
		solarsystemid = int(s)
		region_name = get_name(starmapdata['solarSystems'][s]['regionID'])
		name = get_name(s)
		constellation_name = get_name(starmapdata['solarSystems'][s]['constellationID'])
		center = starmapdata['solarSystems'][s]['center']
		neighbors = []
		for n in starmapdata['solarSystems'][s]['neighbours']:
			neighbors.append(get_name(n))
		planets = []
		for p in starmapdata['solarSystems'][s]['planetCountByType']:
			ids = int(p)
			planet_name = get_name(ids)
			for i in range(starmapdata['solarSystems'][s]['planetCountByType'][p]):
				planets.append(planet_name)
		starsystems[name] = SolarSystem(name, solarsystemid, region_name, constellation_name, center, neighbors, planets)
	return starsystems

def get_solarsystem_by_name(solar_system_name: str):
	try:
		return SOLARSYSTEMS[solar_system_name]
	except KeyError:
		print(f"Solar system not found: {solar_system_name}")
		return None
