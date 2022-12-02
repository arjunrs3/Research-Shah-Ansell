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
    ax.scatter3D(scatter1, scatter2, scatter3, c = scatter3, cmap = 'Reds', s=0.5)
    plt.show()

#Outdated, was used as preliminary validation of the x and y coordinates transferring correctly
#meant to open interpolated.json with the same number of sections, thus the interpolation should yield the same document
#still works to check x and y coordinates, but has not been updated for non-constant section spacing
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
    newz = np.linspace(0, 150, 150)
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
    #plot3d(railz, railx, raily, originalz, originalx, originaly)   
    with open(output_json_file_name, 'w') as f:
        json.dump([final_data], f, indent=4)  

#Same as the above method, but ensures that a smooth connection when mirrored across z = 0 by mirroring the profiles and interpolating over the whole thing
def interpolate_airfoils_symmetry(input_json_file_name: str, output_json_file_name: str, no_of_output_sections):
    interpx = [] #list of x values to interpolate along 
    interpy = [] #list of y values to interpolate along
    interpz = [] #list of z values that the final interpolation function depends on 
    railx = [] #List of x coordinates of the lines that connect sections (includes interpolated sections)
    raily = [] #List of y coordinates of the lines that connect sections (includes interpolated sections)
    railz = [] #List of z coordinates of the lines that connect sections (includes interpolated sections)
    originalx = [] #only kept for plotting purposes 
    originaly = [] #only kept for plotting purposes
    originalz = [] #only kept for plotting purposes
    tempsection = [] #takes the rail data from only one section
    final_data = [] #output
    final_spacing = [] #final spacing
    newz = [] #new z values for output sections
    with open(input_json_file_name, 'r') as f:
        airfoil_data_dict = json.load(f)
    no_sections = len(airfoil_data_dict["airfoil_coords"]) * 2 -1
    span = airfoil_data_dict["span_ft"]
    # populating spacing first with all of the z values below zero 
    spacing = np.negative(airfoil_data_dict["2y_over_b"][::-1])
    # extending spacing with a mirror (positive values) and removing duplicate zero
    positivespacing = airfoil_data_dict["2y_over_b"]
    positivespacing.pop(0)
    spacing = np.concatenate((spacing, positivespacing))
    zvalues = np.multiply(spacing, span / 2)
    # generating z values for new sections
    output_sections_per_input = int(no_of_output_sections / len(airfoil_data_dict["airfoil_coords"])) + 1
    # generate same amount of output sections for input sections with linear spacing in between sections
    print(f"output sections per input: {output_sections_per_input}")
    for i in range(len(zvalues)-1): 
        newz.extend(np.linspace(zvalues[i], zvalues[i+1], output_sections_per_input, endpoint=False))
    # include the last zvalue as well (last original airfoil)
    newz.append(zvalues[len(zvalues)-1])
    # newz = np.linspace(zvalues[0], zvalues[len(zvalues)-1], no_of_output_sections * 2 -1)
    for point in range(len(airfoil_data_dict["airfoil_coords"][0])): 
        interpx.clear()
        interpy.clear()
        interpz.clear()
        #first, iterate through the reversed list of coords because the z values are negative and go to zero
        for section in range(int((no_sections + 1)/2)): 
            interpx.append(airfoil_data_dict["airfoil_coords"][::-1][section][point][0])
            interpy.append(airfoil_data_dict["airfoil_coords"][::-1][section][point][1])
            interpz.append(zvalues[section])
            #originals only used for plotting
            originalx.append(airfoil_data_dict["airfoil_coords"][::-1][section][point][0])
            originaly.append(airfoil_data_dict["airfoil_coords"][::-1][section][point][1])
            originalz.append(zvalues[section])
        #after reaching z = 0, then iterate through the unreversed list of coords because the z values are positive and increasing
        for section in range(1, int((no_sections +1)/2)): 
            interpx.append(airfoil_data_dict["airfoil_coords"][section][point][0])
            interpy.append(airfoil_data_dict["airfoil_coords"][section][point][1])
            interpz.append(zvalues[section+int((no_sections + 1)/2)-1])
            #originals only used for plotting
            originalx.append(airfoil_data_dict["airfoil_coords"][section][point][0])
            originaly.append(airfoil_data_dict["airfoil_coords"][section][point][1])
            originalz.append(zvalues[section+int((no_sections + 1)/2)-1])
        #perform the interpolation in each axis independently
        fx = interpolate.interp1d(interpz, interpx, 'quadratic')
        fy = interpolate.interp1d(interpz, interpy, 'quadratic')
        newx = fx(newz)
        newy = fy(newz)
        railx.extend(newx)
        raily.extend(newy)
        railz.extend(newz)
    #Get data from rail format into section format that can be dumped to the json 
    for i in range(len(newz)):
        tempsection = []
        for c in range(len(railx)- i):
            if ((c % len(newz) == 0) and (railz[c+i] >= 0)):
                tempsection.append([railx[c+i], raily[c+i]])
        if(newz[i] >=0): 
            final_spacing.append(newz[i])
        if (len(tempsection) > 1):
            final_data.append(tempsection)
    final_spacing = np.multiply(final_spacing, 2/span)
    #plot the points on the rails and the original sections for validation
    plot3d(railz, railx, raily, originalz, originalx, originaly)

    with open(output_json_file_name, 'w') as f:
        json.dump({"2y_over_b": final_spacing.tolist(), "airfoil_coords": final_data}, f, indent=4)

interpolate_airfoils_symmetry("airfoil_data.json", "interpolated.json", 40)
#check("interpolated.json", "check.json")