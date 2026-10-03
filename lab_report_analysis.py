import pandas as pd

data = {
    "aluminium": r".\Dataset\Al alloy.xlsx",
    "mild steel": r".\Dataset\Mild steel.xlsx",
    "acrylic": r".\Dataset\Acrylic.xlsx",
    "nylon 6": r".\Dataset\Nylon 6.xlsx"
}
specs = pd.read_excel(r".\Dataset\Specimen dimensions.xlsx", sheet_name=0)
dfs = {}

# Each Dataset = dfs["material"][index (0-2)]
for i in data.keys():
    dfs[i] = list(pd.read_excel(data[i], sheet_name=None).values())
    # Saving specimen dimensions as attributes for the respective df.
    for j in range(3):
        dfs[i][j].attrs["w (mm)"] = specs[i + " w (mm)"][j]
        dfs[i][j].attrs["t (mm)"] = specs[i + " t (mm)"][j]
        print(dfs[i][j].attrs)

# Plotting function (one figure for each material)