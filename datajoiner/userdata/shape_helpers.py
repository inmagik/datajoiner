import shapefile

def export_shapefile(base_shapefile, data_dict, new_field, lookup_field, default_value, out_file):
    source_shape = shapefile.Reader(base_shapefile)
    target_shape = shapefile.Writer()

    source_fields  = list(source_shape.fields)
    #lookup fields
    lookup_index = None
    for i, f in enumerate(source_fields):
        if f[0].lower() == lookup_field.lower():
            lookup_index = i-1


    if not lookup_index:
        raise ValueError("field %s not found in shapefile!" % lookup_field)

    target_shape.fields  = source_fields
    target_shape.field(*new_field)

    for rec in source_shape.records():

        code =  rec[lookup_index]
        if code in data_dict:
            x = data_dict[code]
        else:
            x = default_value
        
        rec.append(x)
        target_shape.records.append(rec)

    target_shape._shapes.extend(source_shape.shapes())
    target_shape.save(out_file)
    return out_file