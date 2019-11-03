
name = getArgument;
if (name=="") exit("No argument!");

run("Bio-Formats Importer", "open=[" + name + "] autoscale color_mode=Default open_all_series view=Hyperstack stack_order=XYCZT");
// get dimension from original image
getDimensions(width,height,channels,slices,frames);
// apply additional operation 
run("Z Project...", "start=1 stop=" + slices + " projection=[Max Intensity]"); // do maximum intensity projection
run("Fire"); // apply special LUT
saveAs("PNG",  "C:/Training/fiji.png");
run("Quit");
