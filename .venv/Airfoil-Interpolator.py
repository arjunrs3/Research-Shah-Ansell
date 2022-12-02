#A function to generate a given number of airfoils from a smaller set of airfoils by interpolation. 

from array import array
from configparser import InterpolationSyntaxError
import numpy as np 
import matplotlib.pyplot as plt 
from scipy import interpolate
from mpl_toolkits import mplot3d
import json

def plot3d(xcoords: array, ycoords: array, zcoords: array, scatter1: array, scatter2: array, scatter3: array): 
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter3D(xcoords, ycoords, zcoords, c = zcoords, cmap = 'Blues')
    ax.scatter3D(scatter1, scatter2, scatter3, c = scatter3, cmap = 'Reds')
    plt.show()


def interpolate_airfoils(input_json_file_name: str, output_json_file_name: str):
    interpx = []
    interpy = []
    interpz = []
    railx = []
    raily = []
    railz = []
    originalx = []
    originaly = []
    originalz = []
    tempsection = [] 
    final_data = []
    with open(input_json_file_name, 'r') as f:
        airfoil_data_dict = json.load(f)
    no_sections = len(airfoil_data_dict["airfoil_coords"])
    zvalues = np.linspace(0, 150, no_sections)
    newz = np.linspace(0, 150, 20)
    for point in range(len(airfoil_data_dict["airfoil_coords"][0])): 
        interpx.clear()
        interpy.clear()
        interpz.clear()
        for section in range(no_sections): 
            interpx.append(airfoil_data_dict["airfoil_coords"][section][point][0])
            interpy.append(airfoil_data_dict["airfoil_coords"][section][point][1])
            interpz.append(zvalues[section])
            originalx.append(airfoil_data_dict["airfoil_coords"][section][point][0])
            originaly.append(airfoil_data_dict["airfoil_coords"][section][point][1])
            originalz.append(zvalues[section])
        fx = interpolate.interp1d(interpz, interpx, 'quadratic')
        fy = interpolate.interp1d(interpz, interpy, 'quadratic')
        newx = fx(newz)
        newy = fy(newz)
        railx.extend(newx)
        raily.extend(newy)
        railz.extend(newz)
    for i in range(len(newz)):
        tempsection = []
        for c in range(len(railx)- i):
            if ((c) % len(newz) == 0):
                tempsection.append([railx[c+i], raily[c+i], railz[c+i]])
        final_data.append(tempsection)
    plot3d(railz, railx, raily, originalz, originalx, originaly)

    with open(output_json_file_name, 'w') as f:
        json.dump([final_data], f, indent=4)

def check(input_json_file_name: str, output_json_file_name: str): 
    interpx = []
    interpy = []
    interpz = []
    railx = []
    raily = []
    railz = []
    originalx = []
    originaly = []
    originalz = []
    tempsection = [] 
    final_data = []
    with open(input_json_file_name, 'r') as f:
        airfoil_data_dict = json.load(f)
    no_sections = len(airfoil_data_dict[0])
    zvalues = np.linspace(0, 150, no_sections)
    newz = np.linspace(0, 150, 20)
    for point in range(len(airfoil_data_dict[0][0])): 
        interpx.clear()
        interpy.clear()
        interpz.clear()
        for section in range(no_sections): 
            interpx.append(airfoil_data_dict[0][section][point][0])
            interpy.append(airfoil_data_dict[0][section][point][1])
            interpz.append(zvalues[section])
            originalx.append(airfoil_data_dict[0][section][point][0])
            originaly.append(airfoil_data_dict[0][section][point][1])
            originalz.append(zvalues[section])
        fx = interpolate.interp1d(interpz, interpx, 'quadratic')
        fy = interpolate.interp1d(interpz, interpy, 'quadratic')
        newx = fx(newz)
        newy = fy(newz)
        railx.extend(newx)
        raily.extend(newy)
        railz.extend(newz)
    for i in range(len(newz)):
        tempsection = []
        for c in range(len(railx)- i):
            if ((c) % len(newz) == 0):
                tempsection.append([railx[c+i], raily[c+i], railz[c+i]])
        final_data.append(tempsection)
    plot3d(railz, railx, raily, originalz, originalx, originaly)   
    with open(output_json_file_name, 'w') as f:
        json.dump([final_data], f, indent=4)  

  
interpolate_airfoils("airfoil_data2.json", "interpolated.json")
check("interpolated.json", "check.json")