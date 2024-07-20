import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from typing import List, Tuple
from numba import jit
import numpy as np


containers = [
    (580, 225, 220, 25000),  # Container 1 dimensions and max weight
    (1190, 225, 220, 26700),  # Container 2 dimensions and max weight
]

packages: List = []
colors: List[Tuple] = [
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
            print(container)
            selected_container_label.config(text=f"Selected container: {container[0]}x{container[1]}x{container[2]}, Max weight: {container[3]}")
            package_positions = generate_package_positions(container, packages)
            visualize_packages(container, package_positions)
            return
    selected_container_label.config(text="No container found that can fit all packages.")

@jit(nopython=True)
def can_fit_all_packages(container, packages):
    max_weight = container[3]  # Maksymalna waga dla kontenera
    current_weight = 0  # Obecna łączna waga umieszczonych pakietów

    # Inicjalizacja przestrzeni kontenera
    space = np.ones((container[0], container[1], container[2]), dtype=np.bool_)
    
    # Sortowanie pakietów
    sorted_packages = sorted(packages, key=lambda x: -x[0][0] * x[0][1] * x[0][2] * x[2])
    
    for dimensions, weight, quantity, _ in sorted_packages:
        total_weight = weight * quantity  # Całkowita waga wszystkich pakietów tego typu
        current_weight += total_weight  # Dodanie wagi pakietów do łącznej wagi

        if current_weight > max_weight:
            return False  # Nie można dopasować, jeśli przekracza maksymalną wagę

        for _ in range(quantity):
            if not place_package_simulated(dimensions, space, container):
                return False  # Jeśli nie można umieścić pakietu, zwraca False

    return True  # Wszystkie pakiety pasują do kontenera

@jit(nopython=True)
def place_package_simulated(dimensions, space, container):
    for x in range(container[0] - dimensions[0] + 1):
        for y in range(container[1] - dimensions[1] + 1):
            for z in range(container[2] - dimensions[2] + 1):
                if can_place(x, y, z, dimensions, space, container):
                    mark_space_as_filled(x, y, z, dimensions, space)
                    return True
    return False

@jit(nopython=True)
def mark_space_as_filled(x, y, z, dimensions, space):
    dx, dy, dz = dimensions
    space[x:x+dx, y:y+dy, z:z+dz] = False

@jit(nopython=True)
def can_place(x, y, z, dimensions, space, container):
    dx, dy, dz = dimensions
    if x + dx > container[0] or y + dy > container[1] or z + dz > container[2]:
        return False
    if not np.all(space[x:x+dx, y:y+dy, z:z+dz]):
        return False
    return True

@jit(nopython=True)
def generate_package_positions(container, packages):
    space = np.ones((container[0], container[1], container[2]), dtype=np.bool_)
    sorted_packages = sorted(packages, key=lambda x: -x[0][0] * x[0][1] * x[0][2] * x[2])
    positions = []
    for dimensions, weight, quantity, color in sorted_packages:
        for _ in range(quantity):
            for x in range(container[0] - dimensions[0] + 1):
                for y in range(container[1] - dimensions[1] + 1):
                    for z in range(container[2] - dimensions[2] + 1):
                        if can_place(x, y, z, dimensions, space, container):
                            positions.append((x, y, z, dimensions, color))
                            mark_space_as_filled(x, y, z, dimensions, space)
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
    return positions

def visualize_packages(container, package_positions):
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111, projection='3d')
    ax.bar3d(0, 0, 0, container[0], container[1], container[2], alpha=0.1, color='gray', edgecolor='black')

    for x, y, z, dimensions, color in package_positions:
        ax.bar3d(x, y, z, dimensions[0], dimensions[1], dimensions[2], color=color, edgecolor='black', linewidth=0.5)

    mapping_container = {   
        (580, 225, 220, 25000): "20ft",
        (1190, 225, 220, 26700): "40ft"
    }

    # Ustawienie tytułu wykresu na podstawie mapowania kontenerów
    container_name = mapping_container.get(container, "Unknown Container")
    ax.set_xlabel('Length', labelpad=20)
    ax.set_ylabel('Width')
    ax.set_zlabel('Height')
    ax.set_title(f'Container: {container_name}')
    ax.set_box_aspect([4, 1, 1])  # Equal aspect ratio
    plt.show()

root = tk.Tk()
root.title("Package and Container Management")

ttk.Label(root, text="Length:").grid(row=0, column=0)
entry_length = ttk.Entry(root)
entry_length.grid(row=0, column=1)

ttk.Label(root, text="Width:").grid(row=0, column=2)
entry_width = ttk.Entry(root)
entry_width.grid(row=0, column=3)

ttk.Label(root, text="Height:").grid(row=0, column=4)
entry_height = ttk.Entry(root)
entry_height.grid(row=0, column=5)

ttk.Label(root, text="Weight:").grid(row=1, column=0)
entry_weight = ttk.Entry(root)
entry_weight.grid(row=1, column=1)

ttk.Label(root, text="Quantity:").grid(row=1, column=2)
entry_quantity = ttk.Entry(root)
entry_quantity.grid(row=1, column=3)

ttk.Button(root, text="Submit Package", command=submit_package).grid(row=1, column=4)
ttk.Button(root, text="Remove Package", command=remove_package).grid(row=1, column=5)

listbox_packages = tk.Listbox(root, width=70, height=10)
listbox_packages.grid(row=2, column=0, columnspan=6)

selected_container_label = ttk.Label(root, text="")
selected_container_label.grid(row=3, column=0, columnspan=6)

ttk.Button(root, text="Choose Container", command=choose_container).grid(row=4, column=0, columnspan=6)

root.mainloop()
