import sys
import arcpy

in_txt = r"canada_min.txt"
out_shp = r"..\..\..\..\data\canada_week11\canada_test.shp"

def main():
    global arcpy

    if sys.argv != 3:
        print("Usage: geom_obj01.py in_txt out_shp")
        sys.exit()

    in_txt = sys.argv[1]
    out_shp = sys.argv[2]
    import arcpy 

    txt_to_polyline(in_txt, out_shp)

def txt_to_polyline(in_txt,out_shp):
    arcpy.env.overwriteOutput =  True
    sr = arcpy.SpatialReference(4326)
    # feature_dict = {}
    features = []
    # this is a list of polylines
    with open(in_txt,'r') as in_file:
        next(in_file)
        # this_is_the_end = "END"
        # in_file.writerow(this_is_the_end)
        # reader = in_file.read()
        polyline = arcpy.Array()
        # this ia list of points for a given polyline
        
        for row in in_file:
            if '-' in row:
                coords= arcpy.Point(float(row.split(' ')[0]), float(row.split(' ')[1].strip('\n')))
                polyline.append(coords)
            # elif row == "END":
            #     features.append(arcpy.Polyline(polyline))
            #     polyline = arcpy.Array()
            else: 
                features.append(arcpy.Polyline(polyline))
                polyline = arcpy.Array()
    
    new_fc = arcpy.CopyFeatures_management(features,out_shp)
    arcpy.DefineProjection_management(new_fc,sr)


txt_to_polyline(in_txt,out_shp)

if __name__ == "__main__":
    main()