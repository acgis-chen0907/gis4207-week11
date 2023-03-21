import sys
import arcpy

in_txt = r"canada_min.txt"
out_shp = r"..\..\..\..\data\canada_week11\canada_test_wkt.shp"

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
    features = []
    with open(in_txt,'r') as in_file:
        next(in_file)
        
        coords = ''

        for row in in_file:
            if '-' in row:
                coords+=row.strip('\n')
                coords+=','

            else: 
                coords = coords.strip(',')
                features.append(arcpy.FromWKT(f'LINESTRING ({coords})'))
                coords = ''
        coords = coords.strip(',')
        features.append(arcpy.FromWKT(f'LINESTRING ({coords})'))
    new_fc = arcpy.CopyFeatures_management(features,out_shp)
    arcpy.DefineProjection_management(new_fc,sr)


txt_to_polyline(in_txt,out_shp)

if __name__ == "__main__":
    main()