import arcpy
import csv


stops_workspace = r'C:\acgis_ii\gis4207_prog\data\Ottawa\Stops'
stop_name = 'GLADSTONE'
stop_id_fc = r'Stops_UTM.shp'
dissemination_area = r'..\OttawaDA_UTM\OttawaDA_UTM.shp'
da_population_field = 'POP_2016'


def get_stop_id_to_da_data():
    stop_id_to_buffer = {}
    global stops_workspace
    arcpy.env.workspace = stops_workspace
    stop_id_field = arcpy.AddFieldDelimiters(stops_workspace, 'stop_id')
    stop_name_field = arcpy.AddFieldDelimiters(stops_workspace, 'stop_name')
    where_clause = f"{stop_id_field}='CI380'"
    where_clause = f"{stop_name_field} LIKE '%{stop_name}%'"
    with arcpy.da.SearchCursor(stop_id_fc, 
                            ['stop_id','SHAPE@', 'stop_name'], 
                            where_clause=where_clause) as cursor:
        for row in cursor:
            stopid = row[0]
            shape = row[1]
            stop_id_to_buffer[stopid] = shape.buffer(150)

    stop_id_to_DA_data = {}
    for stopid in stop_id_to_buffer:
        stop_buffer = stop_id_to_buffer[stopid]
        intersected_da_data = []
        with arcpy.da.SearchCursor(dissemination_area, ['DACODE',da_population_field,'SHAPE@']) as cursor:
            for row in cursor:            
                da_code = row[0]   
                population = row[1]
                da_poly = row[2] 
                dimension = 4  # Resulting geometry is a polygon

                if stop_buffer.overlaps(da_poly) == True:
                    intersect_poly = stop_buffer.intersect(da_poly, 
                                                        dimension)
                    intersect_area = int(intersect_poly.area)
                    da_poly_area = int(da_poly.area)
                    per_da_area = (intersect_area/da_poly_area)*100
                    stop_pop = int(population*(per_da_area/100))
                    data = (da_code, 
                            population, 
                            per_da_area,
                            stop_pop)
                    intersected_da_data.append(data)
        stop_id_to_DA_data[stopid] = intersected_da_data
    
    return stop_id_to_DA_data

    


get_stop_id_to_da_data()

def write_report(out_csv):

    with open (out_csv, 'w',newline='') as outfile:
        stop_id_to_DA_data = get_stop_id_to_da_data()
        writer = csv.writer(outfile)
        headers = ['STOP ID', 'DACODE', 'DA_POPULATION', '%DA AREA', 'STOP_POP']
        writer.writerow(headers)
        for stop_id in stop_id_to_DA_data:
            for data in stop_id_to_DA_data[stop_id]:
                row_to_write = [stop_id,data[0],data[1],data[2],data[3]]
                writer.writerow(row_to_write)
                # print(row_to_write)
