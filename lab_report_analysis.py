import pandas as pd
import matplotlib.pyplot as plt

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
        dfs[i][j].attrs["w"] = specs[i + " w (mm)"][j]
        dfs[i][j].attrs["t"] = specs[i + " t (mm)"][j]

        # Unnecessary column "Starin 1 mm/mm"
        if "Strain 1 mm/mm" in dfs[i][j].columns:
            dfs[i][j].drop("Strain 1 mm/mm", axis=1, inplace=True)

# Plotting function (one figure for each material)
def plot_stress_strain(material, ax):
    for i in range(3):
        df = dfs[material][i]
        strain = df["Strain %"]
        stress = df["Load N"] * df.attrs["w"] * df.attrs["t"] / 1000 # kPa
        ax.plot(strain, stress, label=f"{material} Trial {i+1}")
        ax.set_xlabel("Strain (%)")
        ax.set_ylabel("Stress (kPa)")
    ax.grid()
    ax.legend()


# Plotting the final graphs (using plot())
fig, ax = plt.subplots(2, 2, figsize=(16, 16))
for i, material in zip(range(4), dfs.keys()):
    plot_stress_strain(material, ax[i % 2][i // 2]) # i%2, i//2 -> left column fills first

# Show & Save Plot
plt.savefig(r"stress_strain_graphs.png")
plt.show()