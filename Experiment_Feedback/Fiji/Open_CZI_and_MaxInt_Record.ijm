run("Bio-Formats Importer", "open=C:\\testdata\\EF_Open_Fiji_after_End.czi autoscale color_mode=Default open_all_series view=Hyperstack stack_order=XYCZT");
run("Z Project...", "projection=[Max Intensity]");
run("Fire");
