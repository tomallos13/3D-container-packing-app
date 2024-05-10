import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

containers = [
    (580, 225, 220, 25000),  # Container 1 dimensions and max weight
    (1190, 225, 220, 26700),  # Container 2 dimensions and max weight
]

packages = []
colors = [
    (0.121, 0.466, 0.705),  # Blue
    (1.000, 0.498, 0.055),  # Orange
    (0.172, 0.627, 0.172),  # Green
    (0.839, 0.153, 0.157),  # Red
    (0.580, 0.404, 0.741),  # Purple
    (0.549, 0.337, 0.294),  # Brown
    (0.890, 0.466, 0.760),  # Pink
    (0.498, 0.498, 0.498),  # Gray
    (0.737, 0.741, 0.133),  # Yellow
    (0.090, 0.745, 0.812),  # Turquoise
    (0.984, 0.686, 0.894),  # Light pink
    (0.816, 0.376, 0.494),  # Chestnut
    (0.576, 0.494, 0.776),  # Purple-gray
    (0.988, 0.690, 0.400),  # Light beige
    (0.490, 0.835, 0.553),  # Light green
    (0.800, 0.800, 0.800),  # Light gray
    (0.737, 0.741, 0.133),  # Light yellow
    (0.090, 0.745, 0.812),  # Light turquoise
    (0.984, 0.686, 0.894),  # Light pink
    (0.816, 0.376, 0.494)   # Chestnut
]



def submit_package():
    dimensions = (int(float(entry_length.get())), int(float(entry_width.get())), int(float(entry_height.get())))
    weight = float(entry_weight.get())
    quantity = int(entry_quantity.get())
    color = colors[len(packages) % len(colors)]
    packages.append((dimensions, weight, quantity, color))
    update_packages_list()



def update_packages_list():
    listbox_packages.delete(0, tk.END)
    for i, (dimensions, weight, quantity, _) in enumerate(packages):
        listbox_packages.insert(tk.END, f"Package {i+1}: {dimensions}x{quantity}, Weight: {weight}kg each")

def remove_package():
    try:
        # Get the index of the selected package and remove it
        index = listbox_packages.curselection()[0]
        packages.pop(index)
        update_packages_list()
    except IndexError:
        pass

def choose_container():
    for container in containers:
        if can_fit_all_packages(container, packages):
            selected_container_label.config(text=f"Selected container: {container[0]}x{container[1]}x{container[2]}, Max weight: {container[3]}")
            visualize_packages(container, packages)
            return
    selected_container_label.config(text="No container found that can fit all packages.")


def can_fit_all_packages(container, packages):
    space = [[[True for _ in range(container[2])] for _ in range(container[1])] for _ in range(container[0])]
    sorted_packages = sorted(packages, key=lambda x: -x[0][0] * x[0][1] * x[0][2] * x[2])
    for dimensions, weight, quantity, _ in sorted_packages:
        for _ in range(quantity):
            if not place_package_simulated(dimensions, space, container):
                return False
    return True

def place_package_simulated(dimensions, space, container):
    
    for x in range(container[0] - dimensions[0] + 1):
        for y in range(container[1] - dimensions[1] + 1):
            for z in range(container[2] - dimensions[2] + 1):
                if can_place(x, y, z, dimensions, space, container):
                    mark_space_as_filled(x, y, z, dimensions, space)
                    return True
    return False

def mark_space_as_filled(x, y, z, dimensions, space):
    dx, dy, dz = dimensions
    for i in range(dx):
        for j in range(dy):
            for k in range(dz):
                space[x + i][y + j][z + k] = False

def can_place(x, y, z, dimensions, space, container):
    dx, dy, dz = dimensions
    if x + dx > container[0] or y + dy > container[1] or z + dz > container[2]:
        return False
    for i in range(dx):
        for j in range(dy):
            for k in range(dz):
                if not space[x + i][y + j][z + k]:
                    return False
    return True

def visualize_packages(container, packages):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.bar3d(0, 0, 0, container[0], container[1], container[2], alpha=0.1, color='gray', edgecolor='black')
    space = [[[True for _ in range(container[2])] for _ in range(container[1])] for _ in range(container[0])]
    sorted_packages = sorted(packages, key=lambda x: -x[0][0] * x[0][1] * x[0][2] * x[2])
    for dimensions, weight, quantity, color in sorted_packages:
        for _ in range(quantity):
            for x in range(container[0] - dimensions[0] + 1):
                for y in range(container[1] - dimensions[1] + 1):
                    for z in range(container[2] - dimensions[2] + 1):
                        if can_place(x, y, z, dimensions, space, container):
                            ax.bar3d(x, y, z, dimensions[0], dimensions[1], dimensions[2], color=color, edgecolor='black', linewidth=0.5)
                            mark_space_as_filled(x, y, z, dimensions, space)
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
    ax.set_xlabel('Length')
    ax.set_ylabel('Width')
    ax.set_zlabel('Height')
    ax.set_box_aspect([4, 1, 1])  # Equal aspect ratio
    plt.show()

root = tk.Tk()
root.title("Package and Container Management")

ttk.Label(root, text="Length:").grid(row=0, column=0)
entry_length = ttk.Entry(root)
entry_length.grid(row=0, column=1)

ttk.Label(root, text="Width:").grid(row=1, column=0)
entry_width = ttk.Entry(root)
entry_width.grid(row=1, column=1)

ttk.Label(root, text="Height:").grid(row=2, column=0)
entry_height = ttk.Entry(root)
entry_height.grid(row=2, column=1)

ttk.Label(root, text="Weight:").grid(row=3, column=0)
entry_weight = ttk.Entry(root)
entry_weight.grid(row=3, column=1)

ttk.Label(root, text="Quantity:").grid(row=4, column=0)
entry_quantity = ttk.Entry(root)
entry_quantity.grid(row=4, column=1)

submit_button = ttk.Button(root, text="Submit", command=submit_package)
submit_button.grid(row=5, column=1)

remove_button = ttk.Button(root, text="Remove Selected Package", command=remove_package)
remove_button.grid(row=7, column=1)

choose_container_button = ttk.Button(root, text="Choose Container", command=choose_container)
choose_container_button.grid(row=5, column=2)

listbox_packages = tk.Listbox(root, height=10, width=50)
listbox_packages.grid(row=6, column=0, columnspan=3)

selected_container_label = ttk.Label(root, text="No container selected yet.")
selected_container_label.grid(row=8, column=0, columnspan=3)

root.mainloop()