import requests
import json
from dicttoxml import dicttoxml

rest = "http://10.16.12.61:9999/geoserver/rest/"
credentials = ('admin', 'geoserver')
headers_xml = {'content-type': 'text/xml'}
headers_json = {"accept": "application/json", "content-type": "application/json"}


class GeoserverConnection:
    def __init__(self, rest_url, user, password):
        self.rest_url = rest_url
        self.user = user
        self.password = password


def dicttoxml_body(d):
    return dicttoxml(d, root=False, attr_type=False).decode('utf-8')


def store_xml(name, url, workspace, type="NetCDF"):
    store = {
        "coverageStore": {
            "name": name,
            "workspace": workspace,
            "enabled": "true",
            "type": type,
            "url": url,
        }
    }

    return dicttoxml_body(store)


def create_store(name, url, workspace):
    r_create_coveragestore = requests.post(
        rest + 'workspaces/{workspace}/coveragestores?configure=all'.format(workspace=workspace),
        auth=('admin', 'geoserver'),
        data=store_xml(name, 'file:' + url, workspace),
        headers=headers_xml)
    return r_create_coveragestore


def create_layer(store_name, layer_name, workspace):

    nativeCoverageName = ""
    name_lower = layer_name.lower()
    if 'discharge' in name_lower:
        nativeCoverageName = 'discharge'
    elif 'runoff' in name_lower:
        nativeCoverageName = 'runoff'
    elif 'watertemp' in name_lower:
        nativeCoverageName = 'QxT_WaterTemp'
    else:
        raise("Coverage Name not detected")

    body = {
        "coverage": {
            "name": layer_name,
            "nativeName": layer_name,
            "namespace": {
                "name": "news",
                "href": "http:\/\/10.16.12.61:9999\/geoserver\/rest\/namespaces\/news.json"
            },
            "title": layer_name,
            "description": "Generated from NetCDF",
            "keywords": {
                "string": [
                    "WCS",
                    "NetCDF"
                ]
            },
            "nativeCRS": "GEOGCS[\"WGS 84\", \n  DATUM[\"World Geodetic System 1984\", \n    SPHEROID[\"WGS 84\", 6378137.0, 298.257223563, AUTHORITY[\"EPSG\",\"7030\"]], \n    AUTHORITY[\"EPSG\",\"6326\"]], \n  PRIMEM[\"Greenwich\", 0.0, AUTHORITY[\"EPSG\",\"8901\"]], \n  UNIT[\"degree\", 0.017453292519943295], \n  AXIS[\"Geodetic longitude\", EAST], \n  AXIS[\"Geodetic latitude\", NORTH], \n  AUTHORITY[\"EPSG\",\"4326\"]]",
            "srs": "EPSG:4326",
            "nativeBoundingBox": {
                "minx": -138,
                "maxx": -52.00000000000138,
                "miny": 5,
                "maxy": 60.999999999999105,
                "crs": "EPSG:4326"
            },
            "latLonBoundingBox": {
                "minx": -138,
                "maxx": -52.00000000000138,
                "miny": 5,
                "maxy": 60.999999999999105,
                "crs": "EPSG:4326"
            },
            "projectionPolicy": "REPROJECT_TO_DECLARED",
            "enabled": True,
            "metadata": {
                "entry": [
                    {
                        "@key": "elevation",
                        "dimensionInfo": {
                            "enabled": False
                        }
                    },
                    {
                        "@key": "time",
                        "dimensionInfo": {
                            "enabled": True,
                            "presentation": "DISCRETE_INTERVAL",
                            "resolution": 86400000,
                            "units": "ISO8601",
                            "defaultValue": {
                                "strategy": "MINIMUM"
                            },
                            "nearestMatchEnabled": True,
                            "rawNearestMatchEnabled": False
                        }
                    },
                    {
                        "@key": "NetCDFOutput.Key",
                        "netcdfLayerSettingsContainer": {
                            "compressionLevel": 0,
                            "shuffle": True,
                            "copyAttributes": False,
                            "copyGlobalAttributes": False,
                            "dataPacking": "NONE"
                        }
                    },
                    {
                        "@key": "dirName",
                        "$": layer_name
                    }
                ]
            },
            "serviceConfiguration": False,
            "nativeFormat": "NetCDF",
            "grid": {
                "@dimension": "2",
                "range": {
                    "low": "0 0",
                    "high": "1720 1120"
                },
                "transform": {
                    "scaleX": 0.0499999999999992,
                    "scaleY": -0.0499999999999992,
                    "shearX": 0,
                    "shearY": 0,
                    "translateX": -137.975,
                    "translateY": 60.9749999999991
                },
                "crs": "EPSG:4326"
            },
            "supportedFormats": {
                "string": [
                    "ENVIHdr",
                    "NetCDF",
                    "EHdr",
                    "ImageMosaic",
                    "RPFTOC",
                    "ArcGrid",
                    "ImageMosaicJDBC",
                    "GIF",
                    "PNG",
                    "JPEG",
                    "TIFF",
                    "SRP",
                    "GEOTIFF",
                    "ERDASImg",
                    "AIG",
                    "DTED",
                    "RST",
                    "NITF",
                    "VRT",
                    "GeoPackage (mosaic)",
                    "ImagePyramid"
                ]
            },
            "interpolationMethods": {
                "string": [
                    "nearest neighbor",
                    "bilinear",
                    "bicubic"
                ]
            },
            "defaultInterpolationMethod": "nearest neighbor",
            "requestSRS": {
                "string": [
                    "EPSG:4326"
                ]
            },
            "responseSRS": {
                "string": [
                    "EPSG:4326"
                ]
            },
            "parameters": {
                "entry": [
                    {
                        "string": "Bands",
                        "null": ""
                    },
                    {
                        "string": "Filter",
                        "null": ""
                    }
                ]
            },
            "nativeCoverageName": nativeCoverageName
        }
    }

    r_create_coverage = requests.post(
        rest + 'workspaces/{workspace}/coveragestores/{store}/coverages'.format(workspace=workspace, store=store_name),
        auth=('admin', 'geoserver'),
        data=json.dumps(body),
        headers=headers_json
    )
    return r_create_coverage


def set_style(layer, workspace, style_name):
    body = {
        "layer": {
            "defaultStyle": {
                "name": style_name,
            },
            "styles": {
                "style": [
                    {
                        "name": style_name
                    }
                ]
            },
        }
    }

    r_set_style = requests.put(rest + 'workspaces/{workspace}/layers/{layer}'.format(workspace=workspace, layer=layer),
                               auth=('admin', 'geoserver'),
                               data=json.dumps(body),
                               headers=headers_json
                               )
    return r_set_style


def import_netcdf(filepath, name, workspace):
    r_store = create_store(name, filepath, workspace)
    r_layer = create_layer(name, name, workspace)

    name_lower = name.lower()
    if 'discharge' in name_lower:
        r_style = set_style(name, workspace, 'discharge')
    elif 'runoff' in name_lower:
        r_style = set_style(name, workspace, 'runoff')
    elif 'watertemp' in name_lower:
        r_style = set_style(name, workspace, 'watertemp')

    print("store:{}, layer:{}, style:{}".format(r_store.status_code, r_layer.status_code, r_style.status_code))
