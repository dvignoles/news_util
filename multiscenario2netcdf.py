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

