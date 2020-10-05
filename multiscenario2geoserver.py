from news_util.gserver import GeoserverConnection
from news_util.rgis import mutliscenario_gen_paths
import os

# parent directory of docker volume mount containing data
volume_mount_root = '/asrc/ecr/danielv/'


def main():
    newswbm_gs = GeoserverConnection("http://10.16.12.61:9999/geoserver/rest/",
                                     workspace='newswbm', user='admin', password='geoserver')

    for group in mutliscenario_gen_paths(variable_keys=['qxt_watertemp', "Discharge", "airtemperature", "wetbulbtemp"]):
        for file_tuple in group:
            fpath_geoserver = os.path.join('/opt/geoserver', os.path.relpath(file_tuple[1], volume_mount_root, ))
            store_name = fpath_geoserver.split('/')[-1].split('.')[0].lower()
            rstore = newswbm_gs.create_store(store_name, fpath_geoserver)
            rlayer = newswbm_gs.create_layer(store_name, store_name)

            if 'discharge' in store_name:
                rstyle = newswbm_gs.set_style(store_name, 'discharge')
            elif 'runoff' in store_name:
                rstyle = newswbm_gs.set_style(store_name, 'runoff')
            elif 'watertemp' in store_name:
                rstyle = newswbm_gs.set_style(store_name, 'watertemp')
            elif 'airtemp' in store_name:
                rstyle = newswbm_gs.set_style(store_name, 'airtemperature')
            elif 'wetbulb' in store_name:
                rstyle = newswbm_gs.set_style(store_name, 'wetbulbtemperature')

            rlayergroup = newswbm_gs.create_layergroup(name=store_name + '_nolakes', layers=[store_name, 'lakes'], )

            print(("{}, store:{}, layer:{}, style:{}, layergroup:{}".format(store_name, rstore, rlayer, rstyle,
                                                                            rlayergroup)))


if __name__ == '__main__':
    main()
