import argparse
import os
import pickle
import json
from galaxy import load_data

RESFILEINDEX = "stillness/resfileindex.txt"
RESFILES = "ResFiles"
STARMAP = 'res:/staticdata/starmapcache.pickle'
US_LOCAL = 'res:/localizationfsd/localization_fsd_en-us.pickle'
MAIN_LOCAL = 'res:/localizationfsd/localization_fsd_main.pickle'
CELESTIALS = 'data/celestials.json' #Temporary until I figure out how to link IDs to types

def make_json_serializable(data):
	if isinstance(data, dict):
		return {k: make_json_serializable(v) for k, v in data.items()}
	elif isinstance(data, list):
		return [make_json_serializable(i) for i in data]
	elif isinstance(data, set):  # Convert sets to lists
		return list(data)
	elif isinstance(data, bytes):  # Decode bytes
		return data.decode("utf-8", errors="ignore")
	elif hasattr(data, "__dict__"):  # Convert custom objects
		return make_json_serializable(data.__dict__)
	else:
		return data

def get_json(path:str):
		with open(path, 'rb') as f:
			data = pickle.load(f)
		json_data = make_json_serializable(data)
		return json_data

def extract_resource_path(res:str):
	"""Extracts the path of the resource out of the string"""
	split_res = res.split(',')
	return split_res[1]

def write_json_file(outfile:str, data:str):
		with open(outfile, 'w') as f:
			json.dump(data, f, ensure_ascii=False, indent=4)

def get_static_data(install_dir: str):
	"""Return the resource paths based on the install directory"""
	index_file = os.path.join(install_dir, os.path.normpath("stillness/resfileindex.txt"))
	starmap = None
	us_local = None
	main_local = None

	with open(index_file, 'r') as f:
		data = f.read()
		datalist = data.split('\n')
		for d in datalist:
			if STARMAP in d:
				starmap = d
			if US_LOCAL in d:
				us_local = d
			if MAIN_LOCAL in d:
				main_local = d

	if starmap is None:
		print(f"starmapcache not found in {index_file}")
		exit(1)
	if us_local is None:
		print(f"US localization not found in {index_file}")
		exit(1)
	if main_local is None:
		print(f"Main localization not found in {index_file}")
		exit(1)

	starmap = extract_resource_path(starmap)
	us_local = extract_resource_path(us_local)
	main_local = extract_resource_path(main_local)

	res_path = os.path.join(install_dir, RESFILES)
	path = os.path.join(res_path,  os.path.normpath(starmap))
	starmap_data = get_json(path)
	path = os.path.join(res_path,  os.path.normpath(us_local))
	us_local_data = get_json(path)
	path = os.path.join(res_path,  os.path.normpath(main_local))
	main_local_data = get_json(path)

	#Temp until celetials ID/Name is found
	with open(os.path.normpath(CELESTIALS), 'r', encoding='utf-8') as f:
		celestial_data = json.load(f) #Temp

	return starmap_data, us_local_data, main_local_data, celestial_data

def write_file(galaxy, outfile, outtype):
	print(f'writing {outtype} to {outfile}')
	with open(outfile, 'wb') as f:
		pickle.dump(galaxy, f)


def main(install_dir: str, outfile: str, outtype: str):
	"""Takes in install directory, outfile path/name and file type and writes a map file."""
	print("Extracting data and building Galaxy. This may take a few minutes.")
	starmap, us_local, main_local, celestial_data = get_static_data(install_dir)
	galaxy = load_data(starmap, us_local, main_local, celestial_data)
	write_file(galaxy, outfile, outtype)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract map data from installtion file.")
    parser.add_argument('--outfile', help='Path and file name to save outfile. Example: data/map.pkl')
    parser.add_argument('--installdirectory', help='Location of the install directory: Example:"If using windows: c:\\CPP\\EVE Frontier\\\nIf using WSL please use the WSL path."')
    args = parser.parse_args()

    outtype = "pkl"

    #Set outfile
    if args.outfile:
    	outfile = os.path.abspath(args.outfile)
    else:
        outfile = os.path.join(os.path.join(os.path.dirname(__file__), 'data'), f"mapdata.{outtype}")

    #Set install directory path
    if args.installdirectory:
    	install_dir = os.path.abspath(args.installdirectory)
    else:
        install_dir = os.path.abspath('C:\\CCP\\EVE Frontier')

    main(install_dir, outfile, outtype)
