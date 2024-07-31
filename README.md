![image](https://github.com/user-attachments/assets/3be8dd72-7861-44fb-a494-d624dfc70618)


# Package and Container Management Tool

This tool is a graphical user interface (GUI) application built with Tkinter for managing packages and selecting appropriate containers based on package dimensions and weights. The tool can visualize the placement of packages in containers using 3D plots.

## Features

- **Add Packages:** Users can input package dimensions (length, width, height), weight, and quantity.
- **Remove Packages:** Users can remove selected packages from the list.
- **Choose Container:** The application selects an appropriate container (from a predefined list) that can fit all the added packages based on dimensions and weight constraints.
- **Visualize Packages:** The tool provides a 3D visualization of how packages are placed inside the selected container.

## Requirements

- Python 3.7 or later
- Tkinter
- Matplotlib
- NumPy
- Numba

## Installation

To install the required packages, you can use pip:

```bash
pip install matplotlib numpy numba
```

## Usage

Run the application by executing the script:

```bash
python package_container_management.py
```

## Functionality

### GUI Components

- **Entry Fields:** For package dimensions, weight, and quantity.
- **Buttons:**
  - **Submit Package:** Adds the package details to the list.
  - **Remove Package:** Removes the selected package from the list.
  - **Choose Container:** Selects an appropriate container and visualizes the package placement.
- **Listbox:** Displays the list of added packages.
- **Label:** Shows the selected container details.

### Backend Functions

- **submit_package():** Collects package details from the entry fields and adds them to the `packages` list.
- **update_packages_list():** Updates the listbox with the current packages.
- **remove_package():** Removes the selected package from the `packages` list.
- **choose_container():** Selects an appropriate container and visualizes the package placement.
- **can_fit_all_packages(container, packages):** Checks if all packages can fit into the given container.
- **place_package_simulated(dimensions, space, container):** Simulates the placement of a package in the container space.
- **mark_space_as_filled(x, y, z, dimensions, space):** Marks the space occupied by a package as filled.
- **can_place(x, y, z, dimensions, space, container):** Checks if a package can be placed at the given coordinates in the container.
- **generate_package_positions(container, packages):** Generates the positions for packages in the container.
- **visualize_packages(container, package_positions):** Creates a 3D visualization of the packages in the container using Matplotlib.

### Predefined Containers

Two container types are predefined in the script:

1. **Container 1:** 580x225x220 cm, max weight 25000 kg
2. **Container 2:** 1190x225x220 cm, max weight 26700 kg

### Color Scheme

A predefined list of colors is used to visually distinguish different packages in the 3D plot.

## Example

1. **Add Packages:**
   - Enter length, width, height, weight, and quantity for a package.
   - Click "Submit Package" to add it to the list.

2. **Remove Package:**
   - Select a package from the list.
   - Click "Remove Package" to delete it from the list.

3. **Choose Container:**
   - Click "Choose Container" to find a suitable container and visualize the package placement.

## Notes

- The tool uses the Numba library for just-in-time compilation to speed up the simulation of package placement.

## License

This project is licensed under the MIT License.
