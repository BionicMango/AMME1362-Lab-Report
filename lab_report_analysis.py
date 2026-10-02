import pandas as pd

data = {
    "acrylic": r".\Dataset\Acrylic.xlsx",
    "aluminium": r".\Dataset\Al alloy.xlsx",
    "mild steel": r".\Dataset\Mild steel.xlsx",
    "nylon 6": r".\Dataset\Nylon 6.xlsx"
}
dfs = {}

# dataset = dfs["material"][index (0-2)]
for i in data.keys():
    dfs[i] = list(pd.read_excel(data[i], sheet_name=None).values())

