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
mech_properties = {}

# Cleaning up data (removing points after fracture)
def data_cleanup():
    # Organising excel sheets into DataFrames; each dataset = dfs[material][index (0-2)]
    for i in data.keys():
        dfs[i] = list(pd.read_excel(data[i], sheet_name=None).values())
        # Saving specimen dimensions as attributes for the respective df.
        for j in range(3):
            # Each test's corresponding dataframe
            df= dfs[i][j]

            df.attrs["w"] = specs[i + " w (mm)"][j]
            df.attrs["t"] = specs[i + " t (mm)"][j]

            # Unnecessary column "Strain 1 mm/mm"
            if "Strain 1 mm/mm" in df.columns:
                df.drop("Strain 1 mm/mm", axis=1, inplace=True)

            df["Stress Pa"] = df["Load N"] / (specs[i + " w (mm)"][j]*10**(-3) * specs[i + " t (mm)"][j]*10**(-3))


# Finding mechanical property values
def properties(material, Ei):
    mech_properties[material] = pd.DataFrame(columns=["E", "Yield Strength", "UTS", "Fracture Strain"], index=[0, 1, 2])
    print(material)
    for i in range(3):
        mech_properties_j = mech_properties[material]
        df = dfs[material][i]
        stress = df["Stress Pa"]
        strain = df["Strain %"] / 100

        # E
        mech_properties_j.loc[i, "E"] = stress[Ei] / strain[Ei] # any point in elastic region

        # Yield Strength (acrylic has no yield strength)
        if material == "acrylic":
            mech_properties_j.loc[i, "Yield Strength"] = np.nan
        else:
            ratios = abs(stress/strain - 0.002)
            Yi = ratios.argmin() # when stress/strain ratio is closest to 0.002
            mech_properties_j.loc[i, "Yield Strength"] = stress[Yi]
            print(stress[Yi])

        # UTS
        mech_properties_j.loc[i, "UTS"] = np.max(stress)

        # Strain at Fracture
        mech_properties_j.loc[i, "Fracture Strain"] = np.max(strain) # points after fracture already removed

        print(mech_properties_j)

        mech_properties_j.to_csv(material + "_" + "mechanical_properties.csv")


# Plotting function (one figure for each material)
def plot_stress_strain(material, ax):
    for i in range(3):
        colors=["steelblue", "green", "darkorange"]
        df = dfs[material][i]
        strain = df["Strain %"]
        stress = df["Stress Pa"] / 1000 # kPa
        ax.plot(strain, stress, label=f"{material} Trial {i+1}", c=colors[i])
        ax.set_xlabel("Strain (%)")
        ax.set_ylabel("Stress (kPa)")
    ax.axvline(strain[25])
    ax.grid()
    ax.legend()


# Plotting the final graphs (using plot())
data_cleanup()
fig, ax = plt.subplots(2, 2, figsize=(16, 16))
for i, material in zip(range(4), dfs.keys()):
    properties(material, 25) # manually determined Ei
    plot_stress_strain(material, ax[i % 2][i // 2]) # i%2, i//2 -> left column fills first

# Show & Save Plot
plt.savefig(r"stress_strain_graphs.png")
plt.show()