import os
import subprocess as sp
from news_util.news import FOLDER_CONSTANTS

inputpath = '/asrc/ecr/NEWS/StakeHolders/'
multiscenario_inputpath = '/asrc/ecr/NEWS/MultiScenario/'

outputpath = '/asrc/ecr/danielv/NEWS/StakeHolders/'
multiscenario_outputpath = '/asrc/ecr/danielv/NEWS/MultiScenario/'

dir_template = "/asrc/ecr/NEWS/StakeHolders/{gcm}/{rcp}/{es}/v{v}/RGISresults/" \
                        "{gcm}_{rcp}_{es}_v{v}/USA/{variable}/Pristine/Static/Daily"
multiscenario_dir_template = "/asrc/ecr/NEWS/MultiScenario/{gcm}/{rcp}/ReEDS_Priming/RGISresults" \
                        "/USA/{variable}/Pristine/Static/Daily"


def mutliscenario_gen_paths(gcms=FOLDER_CONSTANTS['global_circ_models'], rcps=FOLDER_CONSTANTS['carbon_model'],
                            variable_keys=FOLDER_CONSTANTS['netcdf_varnames'], input_root=multiscenario_inputpath,
                            output_root=multiscenario_outputpath):
    variables = {k: FOLDER_CONSTANTS['netcdf_varnames'][k] for k in variable_keys}

    def multiscenario_name(gdbc_path):

        path_split = gdbc_path.split('/')
        gcm = path_split[-10]
        rcp = path_split[-9]
        variable = path_split[-5]
        interval = path_split[-2]
        year = path_split[-1][-12:-8]
        file_id = '_'.join(['multiscenario', gcm, rcp, variable, interval, year])
        nc_filename = file_id + '.nc'

        return nc_filename

    def multiscenario_output_fullpath(input_fullpath, output_root=output_root):
        indir = os.path.dirname(input_fullpath)
        nc_filename = multiscenario_name(input_fullpath)

        outdir = os.path.join(output_root, os.path.relpath(indir,
                                                           input_root))

        return os.path.join(outdir, nc_filename)

    for gcm in gcms:
        for rcp in rcps:
            for variable in variables.keys():
                dirpath = multiscenario_dir_template.format(gcm=gcm, rcp=rcp, variable=variable)
                filenames = os.listdir(dirpath)
                input_fullpaths = sorted([os.path.join(dirpath, f) for f in filenames])

                output_fullpaths = [multiscenario_output_fullpath(fpath) for fpath in input_fullpaths]

                yield list(zip(input_fullpaths, output_fullpaths))


def rgis2netcdf(path_tuple):
    convert_nc = "/usr/local/share/ghaas/bin/rgis2netcdf {source_file} {out_file}"

    input_path = path_tuple[0]
    output_path = path_tuple[1]

    output_dir = os.path.dirname(output_path)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    sp.run(convert_nc.format(source_file=input_path, out_file=output_path).split())


def rgis2netcdf_batch(path_tuples):
    for path_tuple in path_tuples:
        rgis2netcdf(path_tuple)

