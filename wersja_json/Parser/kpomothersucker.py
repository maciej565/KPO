import xml.etree.ElementTree as ET
import json
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

def parse_kml(kml_path):
    # file load
    tree = ET.parse(kml_path)
    root = tree.getroot()

    # remove namespaces
    for elem in root.iter():
        if '}' in elem.tag:
            elem.tag = elem.tag.split('}', 1)[1]

    placemarks = root.findall(".//Placemark")
    data_list = []

    for pm in placemarks:
        data = {}
        # get motherfuckers from tags
        name = pm.find("name")
        address = pm.find("address")
        description = pm.find("description")
    

        if name is not None:
            data["name"] = name.text
        if address is not None:
            data["address"] = address.text
        if description is not None:
            data["description"] = description.text


      
        extended = pm.find("ExtendedData")
        if extended is not None:
            for d in extended.findall("Data"):
                key = d.attrib.get("name")
                val_elem = d.find("value")
                val = val_elem.text if val_elem is not None else None
                # float convertion
                if key == "Wartość wsparcia" and val:
                    try:
                        val = float(val)
                    except ValueError:
                        pass
                data[key] = val

        data_list.append(data)

    return data_list

def main():
    #tkinkter
    Tk().withdraw()
    kml_file = askopenfilename(title="Wybierz plik KML", filetypes=[("KML files", "*.kml")])
    if not kml_file:
        print("Nie wybrano pliku.")
        return

    output_file = asksaveasfilename(title="Zapisz plik JSON jako", defaultextension=".json",
                                    filetypes=[("JSON files", "*.json")])
    if not output_file:
        print("Nie wybrano pliku do zapisu.")
        return

    data = parse_kml(kml_file)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Zapisano {len(data)} wpisów do {output_file}")

if __name__ == "__main__":
    main()
