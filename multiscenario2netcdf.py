from news_util.rgis import mutliscenario_gen_paths, rgis2netcdf_batch
import multiprocessing


def main():
    # Don't use more cpus than you have
    cores = 20
    inputs = mutliscenario_gen_paths(variable_keys=['qxt_watertemp', "Discharge","airtemperature", "wetbulbtemp"])

    with multiprocessing.Pool(cores) as p:
        p.map(rgis2netcdf_batch, inputs)
        p.close()
        p.join()


if __name__ == '__main__':
    main()


# def main1():
#
#     dirs_actual = []
#
#     for gcm in FOLDER_CONSTANTS['global_circ_models']:
#         for rcp in FOLDER_CONSTANTS['carbon_model']:
#             for es in FOLDER_CONSTANTS['energy_scenario']:
#                 for variable in FOLDER_CONSTANTS['netcdf_varnames'].keys():
#                     dirs_actual.append(dir_template.format(gcm=gcm, rcp=rcp, es=es, v='000', variable=variable))
#
#     for dirs in dirs_actual:
#         for dirpath, dirnames, filenames in os.walk(dirs):
#             structure = os.path.join(outputpath, os.path.relpath(dirpath, inputpath))
#             geoserver_path = os.path.join('/opt/geoserver/NEWS/StakeHolders',os.path.relpath(dirpath, inputpath))
#             for f in sorted(filenames):
#                     if dirpath in dirs_actual:
#                         source_gdbc = os.path.join(dirpath,f)
#
#                         path_split = source_gdbc.split('/')
#                         model = path_split[-7]
#                         variable = path_split[-5]
#                         interval = path_split[-2]
#                         year = path_split[-1][-12:-8]
#                         file_id = '_'.join([model,variable,interval,year])
#                         nc_filename = file_id + '.nc'
#
#                         if not os.path.isdir(structure):
#                             os.makedirs(structure)
#
#                         new_nc_path = os.path.join(structure,nc_filename)
#
#                         if not os.path.exists(new_nc_path):
#                             print("creating netcdf {}".format(nc_filename))
#                             sp.run(convert_nc.format(source_file=source_gdbc, out_file=new_nc_path).split())
#
#                         docker_nc_path = os.path.join(geoserver_path,nc_filename)
#                         print('importing to geoserver...')
#                         import_netcdf(docker_nc_path, file_id, 'news')
