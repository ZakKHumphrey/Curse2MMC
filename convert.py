import os
import json
import requests
import shutil

manifest_url = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
curse_instances_loc = ""
multimc_instances_loc = ""


def get_modpack_data(manifest_file):
    with open(manifest_file, 'r') as f:
        json_data = json.load(f)
        data = json_data["minecraft"]
        mc_version = data['version']
        modLoader = data['modLoaders'][0]
        modLoaderID = modLoader['id']
    return mc_version, modLoaderID      #Tuple

def get_lwjgl_version(mc_version):
    mc_version_tuple = tuple(map(int, mc_version.split('.')))
    try:
        response = requests.get(manifest_url)
        response.raise_for_status()
        manifest_data = response.json()
    except requests.RequestException as e:
        print(f"Error fetching version manifest: {e}")
        return None
    version_entry = next((v for v in manifest_data["versions"] if v["id"] == mc_version), None)
    if not version_entry:
        print(f"Minecraft version '{mc_version}' not found in manifest.")
        return None

    version_url = version_entry["url"]

    try:
        response = requests.get(version_url)
        response.raise_for_status()
        version_data = response.json()
    except requests.RequestException as e:
        print(f"Error fetching version data for {mc_version}: {e}")
        return None

    for library in version_data.get("libraries", []):
        name = library.get("name")
        if name and "org.lwjgl" in name and "lwjgl" in name.split(':')[-2]:
            return name.split(':')[-1]
    return "LWJGL version not found in JSON"

def clear_tmp():
    for filename in os.listdir("tmp"):
        file_path = os.path.join("tmp", filename)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except OSError as e:
                continue

modPacks = []
for instance in os.listdir(curse_instances_loc):
    instance_loc = os.path.join(curse_instances_loc, instance)
    modPacks.append(instance)
print(f"\n\nFound {len(modPacks)} Packs: \n")
for index, pack in enumerate(modPacks):
    print(f"[{index}]: {pack} ------ [Location]: {os.path.join(curse_instances_loc, pack)}")



valid_input = False
while not valid_input:
    try:
        pack_num = int(input(f"Which modpack do you want to import in MultiMC? (Number 0-{len(modPacks)-1}):    "))
        if pack_num <= len(modPacks):
            valid_input = True
            pack = modPacks[pack_num]
        else:
            valid_input = False
    except ValueError:
        print("Invalid input. Please enter an integer")

instance_loc = os.path.join(curse_instances_loc, pack)
manifest = os.path.join(instance_loc, "manifest.json")

mc_version, modLoaderID = get_modpack_data(manifest)

lwjgl_version = get_lwjgl_version(mc_version)

modLoader = modLoaderID.split('-')[0]
modLoader_version = modLoaderID.split('-')[-1]

loader_map = {
    "forge": "net.minecraftforge",
    "fml": "net.minecraftforge",
    "neoforge": "net.neoforged",
    "fabric": "net.fabricmc",
    "fabricloader": "net.fabricmc",
    "quilt": "org.quiltmc",
    "quilt-loader": "org.quiltmc"
}

modLoader_uid = loader_map.get(modLoader, "unknown")

components = [
    {
        "cachedName": "Minecraft",
        "cachedVersion": f"{mc_version}",
        "important": True,
        "uid": "net.minecraft",
        "version": f"{mc_version}"
    },
    {
        "cachedName": f"{modLoader}",
        "cachedRequires": [
            {
                "equals": f"{mc_version}",
                "uid": "net.minecraft"
            }
        ],
        "cachedVersion": f"{modLoader_version}",
        "uid": f"{modLoader_uid}",
        "version": f"{modLoader_version}"
    }
]
### Make all files in tmp directory

def build_tmp():
    for file in os.listdir("resources"):
        source_file = f"resources/{file}"
        destination_dir = f"tmp/"
        shutil.copy(source_file, destination_dir)
    mmc_data = {}
    mmc_pack_path = "tmp/mmc-pack.json"
    cfg_path = "tmp/instance.cfg"
    with open(mmc_pack_path, "r") as f:
        mmc_data = json.load(f)
    mmc_data["components"].extend(components)
    with open(mmc_pack_path, "w", encoding="utf-8") as f:
        json.dump(mmc_data, f, indent=4)
    with open(cfg_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith("name="):
            lines[i] = f"name={pack}\n"
            break
    with open(cfg_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

build_tmp()

def create_mmc_instance():
    curse_dir = os.path.join(curse_instances_loc, pack)
    mmc_dir = os.path.join(multimc_instances_loc, pack)
    mmc_minecraft_dir = os.path.join(mmc_dir, ".minecraft")
    tmp_dir = "tmp"

    try:
        shutil.copytree(tmp_dir, mmc_dir)
        try:
            shutil.copytree(curse_dir, mmc_minecraft_dir)
        except Exception as e:
            print(f"\n❌ Instance folder failed to build: {mmc_dir}")
            print(f"[ERROR] --> {e}")
            print(f"MultMC Folder [{pack}] already exists at location: {mmc_dir}")
            exit()
        print(f"\n✅ Instance folder built successfully: {mmc_dir}")
    except Exception as e:
        print(f"[ERROR] --> {e}")
    clear_tmp()

create_mmc_instance()





# print(f"\n\n{components}")
