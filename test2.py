import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from py3dbp import Packer, Bin, Item

containers = [
    (580, 225, 220, 25000),  # Smaller container dimensions and max weight
    (1190, 225, 220, 26700),  # Larger container dimensions and max weight
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

item_colors = {}

def submit_package():
    dimensions = (int(float(entry_length.get())), int(float(entry_width.get())), int(float(entry_height.get())))
    weight = float(entry_weight.get())
    quantity = int(entry_quantity.get())
    non_stackable = bool(non_stackable_var.get())
    color = colors[len(packages) % len(colors)]
    packages.append((dimensions, weight, quantity, non_stackable, color))
    update_packages_list()

def update_packages_list():
    listbox_packages.delete(0, tk.END)
    for i, (dimensions, weight, quantity, non_stackable, _) in enumerate(packages):
        ns = "NS" if non_stackable else ""
        listbox_packages.insert(tk.END, f"Package {i+1}: {dimensions}x{quantity}, Weight: {weight}kg each {ns}")

def remove_package():
    try:
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
    bin = Bin('Container', *container[:3], container[3])
    packer = Packer()
    packer.add_bin(bin)
    
    # Sort packages by volume (largest first)
    sorted_packages = sorted(packages, key=lambda x: x[0][0] * x[0][1] * x[0][2], reverse=True)
    
    for dimensions, weight, quantity, non_stackable, color in sorted_packages:
        for _ in range(quantity):
            item = Item(f'Package-{dimensions}', *dimensions, weight)
            packer.add_item(item)
            item_colors[item.name] = color
            if non_stackable:
                # Add an invisible protective package above the non-stackable package
                protective_item = Item(f'Invisible-{dimensions}', dimensions[0], dimensions[1], 1, 0)
                packer.add_item(protective_item)
                item_colors[protective_item.name] = (1, 1, 1, 0)  # Invisible color (white with 0 alpha)
    
    packer.pack()
    return any(b.unfitted_items == [] for b in packer.bins)

def visualize_packages(container, packages):
    bin = Bin('Container', *container[:3], container[3])
    packer = Packer()
    packer.add_bin(bin)
    
    sorted_packages = sorted(packages, key=lambda x: x[0][0] * x[0][1] * x[0][2], reverse=True)
    
    for dimensions, weight, quantity, non_stackable, color in sorted_packages:
        for _ in range(quantity):
            item = Item(f'Package-{dimensions}', *dimensions, weight)
            packer.add_item(item)
            item_colors[item.name] = color
            if non_stackable:
                # Add an invisible protective package above the non-stackable package
                protective_item = Item(f'Invisible-{dimensions}', dimensions[0], dimensions[1], 1, 0)
                packer.add_item(protective_item)
                item_colors[protective_item.name] = (1, 1, 1, 0)  # Invisible color (white with 0 alpha)
    
    packer.pack()
    
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.bar3d(0, 0, 0, container[0], container[1], container[2], alpha=0.1, color='gray', edgecolor='black')
    
    for b in packer.bins:
        for item in b.items:
            c = item_colors.get(item.name, 'blue')
            x, y, z = item.position
            dx, dy, dz = item.width, item.height, item.depth
            if c == (1, 1, 1, 0):  # Skip drawing invisible items
                continue
            ax.bar3d(x, y, z, dx, dy, dz, color=c, edgecolor='black', linewidth=0.5)
    
    ax.set_xlabel('Length', labelpad=20)
    ax.set_ylabel('Width')
    ax.set_zlabel('Height')
    ax.set_title('Container')
    ax.set_box_aspect([container[0]/container[1], 1, container[2]/container[1]])  # Aspect ratio adjusted for the container
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

non_stackable_var = tk.IntVar()
non_stackable_check = ttk.Checkbutton(root, text="Non-Stackable", variable=non_stackable_var)
non_stackable_check.grid(row=5, column=0, columnspan=2)

submit_button = ttk.Button(root, text="Submit", command=submit_package)
submit_button.grid(row=6, column=1)

remove_button = ttk.Button(root, text="Remove Selected Package", command=remove_package)
remove_button.grid(row=7, column=1)

choose_container_button = ttk.Button(root, text="Choose Container", command=choose_container)
choose_container_button.grid(row=6, column=2)

listbox_packages = tk.Listbox(root, height=10, width=50)
listbox_packages.grid(row=8, column=0, columnspan=3)

selected_container_label = ttk.Label(root, text="No container selected yet.")
selected_container_label.grid(row=9, column=0, columnspan=3)

root.mainloop()
