import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from typing import List, Tuple
from numba import jit
import numpy as np
import math


containers = [
    (580, 225, 220, 25000),  # 20 DC
    (1190, 225, 220, 26700), # 40 DC
    (1190, 225, 250, 26460),  # 40 HC
    (1360, 240, 260, 24000)  # TRUCK
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
   
    dimensions = (math.ceil(float(entry_length.get())), math.ceil(float(entry_width.get())), math.ceil(float(entry_height.get())))
    weight = float(entry_weight.get())
    quantity = int(entry_quantity.get())
    is_stackable = var_stackable.get()
    container_type = var_container_type.get()
    true_dimensions = dimensions
    

    # Adjust height based on container type and stackability
    if not is_stackable:
        if container_type == "HC":
            dimensions = (dimensions[0], dimensions[1], 250)
        elif container_type == "TRUCK":
            dimensions = (dimensions[0], dimensions[1], 260)
        else:  # Default to 220 for DC or Both
            dimensions = (dimensions[0], dimensions[1], 220)
    
    # Assign alpha based on stackability
    alpha = 0.7 if not is_stackable else 1.0
    color = colors[len(packages) % len(colors)] + (alpha,)
    
    packages.append((dimensions, weight, quantity, color, is_stackable, true_dimensions))
    update_packages_list()
    update_total_info()


def update_total_info():
    total_weight = 0
    total_volume = 0
    for dimensions, weight, quantity, _, _, true_dimensions in packages:
        package_volume = dimensions[0]/100 * dimensions[1]/100 * true_dimensions[2]/100
        total_weight += weight * quantity
        total_volume += package_volume * quantity

    total_info_label.config(text=f"Total Weight: {round(total_weight,2)} kg, Total Volume: {round(total_volume,3)} cbm")


def update_packages_list():
    listbox_packages.delete(0, tk.END)
    for i, (_, weight, quantity, _, is_stackable, true_dimensions) in enumerate(packages):
        stackable_str = "Non-stackable" if not is_stackable else "Stackable"
        listbox_packages.insert(tk.END, f"Package {i+1}: {true_dimensions}x{quantity}, Weight: {weight}kg each, {stackable_str}")

def remove_package():
    try:
        # Get the index of the selected package and remove it
        index = listbox_packages.curselection()[0]
        packages.pop(index)
        update_packages_list()
        update_total_info()
    except IndexError:
        pass

def choose_container():
    container_type = var_container_type.get()
    if not container_type:
        messagebox.showwarning("Container Type Required", "Please select a container type (DC, HC or TRUCK).")
        return
    
    # Aktualizacja wymiaru wysokości dla paczek non-stackable na podstawie wybranego kontenera
    for i, (dimensions, weight, quantity, color, is_stackable, true_dimensions) in enumerate(packages):
        if not is_stackable:
            if container_type == "HC":
                new_dimensions = (dimensions[0], dimensions[1], 250)
            elif container_type == "TRUCK":
                new_dimensions = (dimensions[0], dimensions[1], 260)
            else:  # Default to 220 for DC
                new_dimensions = (dimensions[0], dimensions[1], 220)
            packages[i] = (new_dimensions, weight, quantity, color, is_stackable, true_dimensions)

    update_packages_list()
    update_total_info()
    container_type = var_container_type.get()
    # Filter containers based on the selected type
    filtered_containers = []
    if container_type == "DC":
        filtered_containers = [c for c in containers if c[2] == 220]
    elif container_type == "HC":
        filtered_containers = [c for c in containers if c[2] == 250]
    elif container_type == "TRUCK":
        filtered_containers = [c for c in containers if c[2] == 260]
    else:  # Both
        filtered_containers = containers

    remaining_packages = packages.copy()
    containers_info.delete(0, tk.END)  # Clear previous container info
    mapping_container = {
    (580, 225, 220, 25000): "20 DC",
    (1190, 225, 220, 26700): "40 DC",
    (1190, 225, 250, 26460): "40 HC",
    (1360, 240, 260, 24000): "TRUCK"
    }
    if container_type == "DC":
        for dimensions, weight, quantity, _, _, _ in remaining_packages:
            if (dimensions[0] > 1190 or dimensions[1] > 225 or dimensions[2] > 220):
                selected_container_label.config(text="one of the packages exceeds the dimensions limits")
                return
            if weight > 26700:
                selected_container_label.config(text="one of the packages exceeds the weight limit")
                return
        # Sprawdzenie, czy paczki mogą być umieszczone w kontenerze
        while remaining_packages:    
            for container in filtered_containers:
                if can_fit_all_packages(container, remaining_packages):

                    #selected_container_label.config(text=f"Selected container: {container[0]}x{container[1]}x{container[2]}, Max weight: {container[3]}")
                    package_positions, current_weight, current_volume = generate_package_positions(container, remaining_packages)
                    visualize_packages(container, package_positions)
                    remaining_packages = remove_placed_packages(package_positions, remaining_packages)
                    container_name = mapping_container.get(container, "Unknown Container")
                    containers_info.insert(tk.END, f"Container: {container_name}, Weight: {current_weight} kg, Volume: {current_volume} cbm")
                    break  # Przerwanie pętli, gdy znajdzie odpowiedni kontener
            else:
                total_weight = sum(weight * quantity for _, weight, quantity, _, _, _ in remaining_packages)
                total_volume = sum(dimensions[0] *dimensions[1]*dimensions[2] * quantity for dimensions, _, quantity, _, _, _ in remaining_packages)
                if total_volume/total_weight <1100:
                    
                    package_positions, current_weight, current_volume = generate_package_positions(filtered_containers[0], remaining_packages)
                    visualize_packages(filtered_containers[0], package_positions)
                    remaining_packages = remove_placed_packages(package_positions, remaining_packages)
                    container_name = mapping_container.get(filtered_containers[0], "Unknown Container")
                    containers_info.insert(tk.END, f"Container: {container_name}, Weight: {current_weight} kg, Volume: {current_volume} cbm")
                    
                else:
                # Ten blok wykona się tylko, jeśli pętla for nie została przerwana przez break
                    
                    package_positions, current_weight, current_volume = generate_package_positions(filtered_containers[1], remaining_packages)
                    visualize_packages(filtered_containers[1], package_positions)
                    remaining_packages = remove_placed_packages(package_positions, remaining_packages)
                    container_name = mapping_container.get(filtered_containers[1], "Unknown Container")
                    containers_info.insert(tk.END, f"Container: {container_name}, Weight: {current_weight} kg, Volume: {current_volume} cbm")
                    

    if container_type == "HC":
        for dimensions, weight, quantity, _, _, _ in remaining_packages:
            if (dimensions[0] > 1190 or dimensions[1] > 225 or dimensions[2] > 250):
                selected_container_label.config(text="one of the packages exceeds the dimensions limits")
                return
            if weight > 26460:
                selected_container_label.config(text="one of the packages exceeds the weight limit")
                return
        # Sprawdzenie, czy paczki mogą być umieszczone w kontenerze
        while remaining_packages:
            container = filtered_containers[0]    
            if can_fit_all_packages(container, remaining_packages):
                #selected_container_label.config(text=f"Selected container: {container[0]}x{container[1]}x{container[2]}, Max weight: {container[3]}")
                package_positions, current_weight, current_volume = generate_package_positions(container, remaining_packages)
                visualize_packages(container, package_positions)
                remaining_packages = remove_placed_packages(package_positions, remaining_packages)
                container_name = mapping_container.get(container, "Unknown Container")
                containers_info.insert(tk.END, f"Container: {container_name}, Weight: {current_weight} kg, Volume: {current_volume} cbm")
                break  # Przerwanie pętli, gdy znajdzie odpowiedni kontener
            else:
                # Ten blok wykona się tylko, jeśli pętla for nie została przerwana przez break
                
                package_positions, current_weight, current_volume = generate_package_positions(container, remaining_packages)
                visualize_packages(container, package_positions)
                remaining_packages = remove_placed_packages(package_positions, remaining_packages)
                container_name = mapping_container.get(container, "Unknown Container")
                containers_info.insert(tk.END, f"Container: {container_name}, Weight: {current_weight} kg, Volume: {current_volume} cbm")

    if container_type == "TRUCK":
        for dimensions, weight, quantity, _, _, _ in remaining_packages:
            if (dimensions[0] > 1360 or dimensions[1] > 240 or dimensions[2] > 260):
                selected_container_label.config(text="one of the packages exceeds the dimensions limits")
                return
            if weight > 24000:
                selected_container_label.config(text="one of the packages exceeds the weight limit")
                return
        # Sprawdzenie, czy paczki mogą być umieszczone w kontenerze
        while remaining_packages:
            container = filtered_containers[0]    
            if can_fit_all_packages(container, remaining_packages):
                #selected_container_label.config(text=f"Selected container: {container[0]}x{container[1]}x{container[2]}, Max weight: {container[3]}")
                package_positions, current_weight, current_volume = generate_package_positions(container, remaining_packages)
                visualize_packages(container, package_positions)
                remaining_packages = remove_placed_packages(package_positions, remaining_packages)
                container_name = mapping_container.get(container, "Unknown Container")
                containers_info.insert(tk.END, f"Container: {container_name}, Weight: {current_weight} kg, Volume: {current_volume} cbm")
                break  # Przerwanie pętli, gdy znajdzie odpowiedni kontener
            else:
                # Ten blok wykona się tylko, jeśli pętla for nie została przerwana przez break
                
                package_positions, current_weight, current_volume = generate_package_positions(container, remaining_packages)
                visualize_packages(container, package_positions)
                remaining_packages = remove_placed_packages(package_positions, remaining_packages)
                container_name = mapping_container.get(container, "Unknown Container")
                containers_info.insert(tk.END, f"Container: {container_name}, Weight: {current_weight} kg, Volume: {current_volume} cbm")

            
@jit(nopython=True)
def remove_placed_packages(package_positions, remaining_packages):
    placed_packages = []
    updated_remaining_packages = []

    # Create a dictionary to keep track of the count of each package type
    package_count = {}
    for dimensions, weight, quantity, color, is_stackable, true_dimensions in remaining_packages:
        package_count[(dimensions, weight, color, is_stackable, true_dimensions)] = quantity

    for position in package_positions:
        for package in remaining_packages:
            if package[0] == position[3] and package_count[(package[0], package[1], package[3], package[4], package[5])] > 0:
                placed_packages.append(package)
                package_count[(package[0], package[1], package[3], package[4], package[5])] -= 1
                break
    
    # Update the remaining packages with the updated quantities
    for package in remaining_packages:
        remaining_quantity = package_count[(package[0], package[1], package[3], package[4], package[5])]
        if remaining_quantity > 0:
            updated_remaining_packages.append((package[0], package[1], remaining_quantity, package[3], package[4], package[5]))
    print(updated_remaining_packages)
    return updated_remaining_packages



@jit(nopython=True)
def can_fit_all_packages(container, packages):
    max_weight = container[3]  # Maksymalna waga dla kontenera
    current_weight = 0  # Obecna łączna waga umieszczonych pakietów
    print(container)
    # Inicjalizacja przestrzeni kontenera
    space = np.ones((container[0], container[1], container[2]), dtype=np.bool_)
    
    # Sortowanie pakietów
    sorted_packages = sorted(packages, key=lambda x: -x[0][0] * x[0][1] * x[0][2] * x[2])
    
    for dimensions, weight, quantity, _, _, _ in sorted_packages:
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
    current_weight = 0  # Track the current total weight of placed packages
    current_volume = 0

    for dimensions, weight, quantity, color, is_stackable, true_dimensions in sorted_packages:
        for _ in range(quantity):
            if current_weight + weight > container[3]:
                # If adding this package would exceed the weight limit, break out of the loop
                break
            for x in range(container[0] - dimensions[0] + 1):
                for y in range(container[1] - dimensions[1] + 1):
                    for z in range(container[2] - dimensions[2] + 1):
                        if can_place(x, y, z, dimensions, space, container):
                            positions.append((x, y, z, dimensions, color, is_stackable, true_dimensions))
                            mark_space_as_filled(x, y, z, dimensions, space)
                            current_weight += weight
                            current_volume += (true_dimensions[0]/100 *true_dimensions[1]/100*true_dimensions[2]/100)
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
    return positions, round(current_weight, 2), round(current_volume, 3)


def visualize_packages(container, package_positions):
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111, projection='3d')
    ax.bar3d(0, 0, 0, container[0], container[1], container[2], alpha=0.1, color='gray', edgecolor='black')

    for x, y, z, dimensions, color, is_stackable, true_dimensions in package_positions:
        r, g, b, alpha = color  # Rozpakowujemy wartości RGBA
        
        # Dodanie napisu "NS" dla paczek non-stackable
        if not is_stackable:
            ax.bar3d(x, y, z, dimensions[0], dimensions[1], true_dimensions[2], color=(r, g, b, alpha), edgecolor='black', linewidth=0.5)
            ax.text(x + dimensions[0]/2, y + dimensions[1]/2, z + true_dimensions[2]/2, "NS", color='black', ha='center', va='center', fontsize=10, weight='bold')
        else:
            ax.bar3d(x, y, z, dimensions[0], dimensions[1], dimensions[2], color=(r, g, b, alpha), edgecolor='black', linewidth=0.5) 
    # Mapa kontenerów
    mapping_container = {
        (580, 225, 220, 25000): "20 DC",
        (1190, 225, 220, 26700): "40 DC",
        (1190, 225, 250, 26460): "40 HC",
        (1360, 240, 260, 24000): "TRUCK"
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
root.geometry("600x450")

total_info_label = ttk.Label(root, text="")
total_info_label.grid(row=6, column=0, columnspan=6)


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

ttk.Label(root, text="Stackable:").grid(row=1, column=4)
var_stackable = tk.BooleanVar(value=True)
chk_stackable = ttk.Checkbutton(root, variable=var_stackable)
chk_stackable.grid(row=1, column=5)

ttk.Label(root, text="Container Type:").grid(row=2, column=0)
var_container_type = tk.StringVar(value="")
rb_dc = ttk.Radiobutton(root, text="DC", variable=var_container_type, value="DC")
rb_dc.grid(row=2, column=1)
rb_hc = ttk.Radiobutton(root, text="HC", variable=var_container_type, value="HC")
rb_hc.grid(row=2, column=2)
rb_hc = ttk.Radiobutton(root, text="TRUCK", variable=var_container_type, value="TRUCK")
rb_hc.grid(row=2, column=3)

ttk.Button(root, text="Submit Package", command=submit_package).grid(row=3, column=4)
ttk.Button(root, text="Remove Package", command=remove_package).grid(row=3, column=5)

listbox_packages = tk.Listbox(root, width=70, height=10)
listbox_packages.grid(row=4, column=0, columnspan=6)

selected_container_label = ttk.Label(root, text="")
selected_container_label.grid(row=5, column=0, columnspan=6)

total_info_label = ttk.Label(root, text="")
total_info_label.grid(row=7, column=0, columnspan=6)

containers_info = tk.Listbox(root, width=70, height=7)
containers_info.grid(row=8, column=0, columnspan=6)

ttk.Button(root, text="RUN", command=choose_container).grid(row=6, column=0, columnspan=6)

root.mainloop()
