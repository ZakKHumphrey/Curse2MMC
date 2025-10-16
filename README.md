# CurseForge → MultiMC Modpack Importer

A Python utility that converts **CurseForge modpacks** into **MultiMC** compatible instances.  
This tool automatically reads a CurseForge `manifest.json`, fetches the correct **Minecraft** and **mod loader** versions, and then generates an appropriate `mmc-pack.json` ready to import.

---

## 🧩 Features

- 🔍 Automatically detects installed CurseForge modpacks  
- 📦 Extracts Minecraft version and mod loader information from each `manifest.json`  
- 🌐 Fetches version data directly from Mojang’s official version manifest  
- ⚙️ Generates or updates `mmc-pack.json` with correct component entries  
- 💾 Preserves existing fields like `"formatVersion": 1`  
- 🪄 Supports multiple loaders:
  - Forge / FML → `net.minecraftforge`
  - NeoForge → `net.neoforged`
  - Fabric / Fabric Loader → `net.fabricmc`
  - Quilt / Quilt Loader → `org.quiltmc`

---

## 🧠 How It Works

1. Scans your CurseForge instances directory (e.g. `DRIVELETTER:/Minecraft/CurseForge/Instances/`)  
2. Lists all available modpacks  
3. You select which one to convert  
4. The script reads its `manifest.json`  
5. Fetches LWJGL and Minecraft version data from the Mojang API  
6. Creates a properly structured `mmc-pack.json` file for MultiMC or Prism Launcher

---

## 📁 Example Output (`mmc-pack.json`)

```json
{
    "components": [
        {
            "cachedName": "Minecraft",
            "cachedVersion": "1.21.1",
            "important": true,
            "uid": "net.minecraft",
            "version": "1.21.1"
        },
        {
            "cachedName": "neoforge",
            "cachedRequires": [
                {
                    "equals": "1.21.1",
                    "uid": "net.minecraft"
                }
            ],
            "cachedVersion": "21.1.209",
            "uid": "net.neoforged",
            "version": "21.1.209"
        }
    ],
    "formatVersion": 1
}
```
---
# ⚙️ Requirements
- Python 3.8+
- `requests` library
Install it with: `pip install requests`
---
# 🚀 Usage

1. Clone or download this repository
2. Update these paths at the top of the script with your CurseForge & MultiMC instances folders:
```python
curse_instances_loc = ""
multimc_instances_loc = ""
```
3. Run the script:
```bash
python convert.py
```
4. Select the modpack number you want to import.
5. The script will automatically build the `mmc-pack.json` and `instance.cfg` files, create a folder within your MultiMC instances folder with the correct pack name, and copy all contents of the CurseForge instance into the `.minecraft` folder of the MultiMC instance folder.
6. Close and Re-open MultiMC (if already open)
7. Play your modpack (curse free!)
---
# 🧰 Example Console Output
```markdown
Found 3 Packs:
[0]: Vault Hunters 1.18 ------ [Location]: G:/Minecraft/CurseForge/Instances/Vault Hunters 1.18
[1]: SkyFactory 4 ------ [Location]: G:/Minecraft/CurseForge/Instances/SkyFactory 4
[2]: Better MC ------ [Location]: G:/Minecraft/CurseForge/Instances/Better MC

Which modpack do you want to import in MultiMC? (Number 0-2):
```
