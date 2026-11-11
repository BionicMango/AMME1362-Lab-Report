import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = {
    "aluminium": r".\Dataset\Al alloy.xlsx",
    "mild steel": r".\Dataset\Mild steel.xlsx",
    "acrylic": r".\Dataset\Acrylic.xlsx",
    "nylon 6": r".\Dataset\Nylon 6.xlsx"
}
specs = pd.read_excel(r".\Dataset\Specimen dimensions.xlsx", sheet_name=0)
dfs = {}
# Cleaning up data (removing points after fracture)
fracture_strains = {
    "aluminium": [11.9, 10.4, 13.4],
    "mild steel": [28, 34.6, 31.57],
    "acrylic": [5.05, 4.7, 4.85],
    "nylon 6": [150, 232.3, 188]
}

def data_cleanup():
    # Organising excel sheets into DataFrames; each dataset = dfs["material"][index (0-2)]
    for i in data.keys():
        dfs[i] = list(pd.read_excel(data[i], sheet_name=None).values())
        # Saving specimen dimensions as attributes for the respective df.
        for j in range(3):
            # Each test's corresponding dataframe
            df, fracture_strain = dfs[i][j], fracture_strains[i][j]

            df.attrs["w"] = specs[i + " w (mm)"][j]
            df.attrs["t"] = specs[i + " t (mm)"][j]

            # Unnecessary column "Strain 1 mm/mm"
            if "Strain 1 mm/mm" in df.columns:
                df.drop("Strain 1 mm/mm", axis=1, inplace=True)

# Plotting function (one figure for each material)
def plot_stress_strain(material, ax):
    for i in range(3):
        colors=["steelblue", "green", "darkorange"]
        df = dfs[material][i]
        strain = df["Strain %"]
        stress = df["Load N"] * df.attrs["w"] * df.attrs["t"] / 1000 # kPa
        ax.plot(strain, stress, label=f"{material} Trial {i+1}", c=colors[i])
        ax.set_xlabel("Strain (%)")
        ax.set_ylabel("Stress (kPa)")
        ax.axvline(fracture_strains[material][i], c=colors[i], ls="--", lw=1)
    ax.grid()
    ax.legend()


# Plotting the final graphs (using plot())
data_cleanup()
fig, ax = plt.subplots(2, 2, figsize=(16, 16))
for i, material in zip(range(4), dfs.keys()):
    plot_stress_strain(material, ax[i % 2][i // 2]) # i%2, i//2 -> left column fills first

# Show & Save Plot
plt.savefig(r"stress_strain_graphs.png")
plt.show()