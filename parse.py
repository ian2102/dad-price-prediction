import re
import scheme

NUMBERS_REGEX = r'-?\d+\.\d+|-?\d+'

def parse_text(og_text):
    # remove everything thats not a number or letter
    text = re.sub(r"[^a-zA-Z0-9 \n.-]", " ", og_text).lower()

    item = {
        "name": "AdventurerBoots",
        "rarity": "Common",
        "pp": [],
        "sp": []
    }

    # indexs of lines we want to remove
    indexs = []

    # rarity
    escape = False
    lines = text.split("\n")
    for index, line in enumerate(lines):
        if escape:
            break
        for rarity in scheme.raritys:
            if rarity.lower() in line:
                item["rarity"] = rarity
                indexs.extend(range(index + 1, len(lines)))
                escape = True
                break
    
    # name
    for index, line in enumerate(lines):
        hits = []
        for name in scheme.names:
            if name.lower() in line.replace(" ", ""):
                hits.append(name)

        # if its FrostlightCrusaderHelm we dont want to go with CrusaderHelm
        if hits:
            name = max(hits, key=len)
            item["name"] = name
            indexs.append(index)
    
    # list of propertys we know the item has
    pp_names = scheme.name_to_pps[item["name"]]

    # we dont want to update the property if we find it in both primary and secondary
    found = []

    # primary propertys
    for index, line in enumerate(lines):
        for pp_name in pp_names:
            name = pp_name.removeprefix("p_")
            name_text = scheme.p_to_tooltip[name]
            if name_text.lower() in line and pp_name not in found:
                value = 0
                numbers = re.findall(NUMBERS_REGEX, line)
                if numbers:
                    value = float(numbers[-1])

                # apply change from percentage to decimal
                if name in scheme.percentage_propertys_to_ratio:
                    value *= scheme.percentage_propertys_to_ratio[name]

                item["pp"].append((pp_name, value)) # TODO add all pps to default value if some failed to parse
                found.append(pp_name)
                indexs.append(index)
    
    # remove unnecessary lines
    clean_lines = []
    for index in range(len(lines)):
        if index not in indexs:
            clean_lines.append(lines[index])

    lines = [line for line in clean_lines if re.search(NUMBERS_REGEX, line)]

    text = "\n".join(clean_lines)

    # secondary propertys
    for line in lines:
        hits = []
        for sp_name in scheme.sp:
            name = sp_name.removeprefix("s_")
            name_text = scheme.p_to_tooltip[name]
            if name_text.lower() in line:
                hits.append(sp_name)

        # if its max health bonus we dont want to go with max health
        if hits:
            sp_name = max(hits, key=len)
            name = sp_name.removeprefix("s_")
            value = 0
            numbers = re.findall(NUMBERS_REGEX, line)
            if numbers:
                value = float(numbers[0])

            # apply change from percentage to decimal
            if name in scheme.percentage_propertys_to_ratio:
                value *= scheme.percentage_propertys_to_ratio[name]

            item["sp"].append((sp_name, value))
    
    # add extra default secondary propertys if some failed to parse
    while len(item["sp"]) < scheme.rarity_to_property_count[item["rarity"]]:
        item["sp"].append(('s_Will', 2.0))

    return (item, og_text)

def compare_parse_results(item):
    parse_result, og_text = item["text"]
    del item["text"]
    del item["price"]

    network_result = {
        "name": "",
        "rarity": "",
        "pp": [],
        "sp": []
    }

    for key, value in item.items():
        if value != 0:
            if key.startswith("s_"):
                network_result["sp"].append((key, float(value)))
            elif key.startswith("p_"):
                network_result["pp"].append((key, float(value)))
            else:
                network_result[key] = value

    # sort by property type for consistency
    network_result["sp"].sort(key=lambda x: x[0])
    network_result["pp"].sort(key=lambda x: x[0])
    parse_result["sp"].sort(key=lambda x: x[0])
    parse_result["pp"].sort(key=lambda x: x[0])
    if parse_result != network_result:
        print(og_text)
        print("parse_result:   ", parse_result)
        print("network_result: ", network_result)

input = """Frostlight Crusader Helm

- Armor Rating 37 -
- Projectile Damage Reduction1.8% -
- Headshot Damage Reduction18% -
- Move Speed -6 -
- Strength 3 -
- Vigor 3 -
+2.5% Armor Penetration -
+1% Max Health Bonus -
+1.2% Physical Damage Reduction -

OIOIOIC)

+1 True Magical Damage -

Fighter, Cleric
Head
Plate
Handled
Epic

An imposing crusader helm crafted from

Froststone Ingots, intertwining the chilling

touch of the frozen abyss with the enduring
might of the noble and the devout.

" Crafted by blooddrinker333 "
"""

if __name__ == "__main__":
    item, og_text = parse_text(input)
    print(og_text)
    print(item)