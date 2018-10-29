// read the filename that is passed from ZEN
name= getArgument; 

// error message if there was no filename
if (name=="") exit("No file selected!");

// Import the CZI file with Bio-formats
run("Bio-Formats Importer", "open=[" + name + "] autoscale color_mode=Default open_all_series view=Hyperstack stack_order=XYCZT");

// apply a maximum projection
run("Z Project...", "projection=[Max Intensity]");

// change the lookup table
run("Fire");
