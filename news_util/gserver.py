import requests
import json
from dicttoxml import dicttoxml
from .news import FOLDER_CONSTANTS

credentials = ('admin', 'geoserver')
headers_xml = {'content-type': 'text/xml'}
headers_json = {"accept": "application/json", "content-type": "application/json"}


def dicttoxml_body(d):
    return dicttoxml(d, root=False, attr_type=False).decode('utf-8')


class GeoserverConnection:
    def __init__(self, rest_url, workspace, user, password):
        self.rest_url = rest_url
        self.workspace = workspace
        self.user = user
        self.password = password

    def store_xml(self, name, url, type="NetCDF"):
        store = {
            "coverageStore": {
                "name": name,
                "workspace": self.workspace,
                "enabled": "true",
                "type": type,
                "url": url,  # url = (filepath)
            }
        }

        return dicttoxml_body(store)

    def create_store(self, name, url):
        r_create_coveragestore = requests.post(
            self.rest_url + 'workspaces/{workspace}/coveragestores?configure=all'.format(workspace=self.workspace),
            auth=(self.user, self.password),
            data=self.store_xml(name=name, url='file://' + url),  # url = (filepath)
            headers=headers_xml)
        return r_create_coveragestore

    def create_layer(self, store_name, layer_name):

        netcdf_varnames = FOLDER_CONSTANTS['netcdf_varnames']

        nativeCoverageName = ""
        name_lower = layer_name.lower()
        if 'discharge' in name_lower:
            nativeCoverageName = netcdf_varnames['Discharge']
        elif 'runoff' in name_lower:
            nativeCoverageName = netcdf_varnames['Runoff']
        elif 'watertemp' in name_lower:
            nativeCoverageName = netcdf_varnames['qxt_watertemp']
        elif 'airtemperature' in name_lower:
            nativeCoverageName = netcdf_varnames['airtemperature']
        elif 'wetbulb' in name_lower:
            nativeCoverageName = netcdf_varnames['wetbulbtemp']
        else:
            raise ("Coverage Name not detected")

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
            self.rest_url + 'workspaces/{workspace}/coveragestores/{store}/coverages'.format(workspace=self.workspace,
                                                                                             store=store_name),
            auth=(self.user, self.password),
            data=json.dumps(body),
            headers=headers_json
        )
        return r_create_coverage

    def set_style(self, layer, style_name):
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

        r_set_style = requests.put(
            self.rest_url + 'workspaces/{workspace}/layers/{layer}'.format(workspace=self.workspace, layer=layer),
            auth=(self.user, self.password),
            data=json.dumps(body),
            headers=headers_json
            )
        return r_set_style

    def create_layergroup(self, name, layers):

        # "styles": {
        #     "style": [
        #         {   # name should be workspace:name is style localized to workspace
        #             "name": styles[0],
        #         },
        #         {
        #             "name": styles[1],
        #         }
        #     ]
        # },

        body = {
            "layerGroup": {
                "name": name,
                "mode": "SINGLE",
                "workspace": {
                    "name": self.workspace
                },
                "publishables": {
                    "published": [
                        {
                            "@type": "layer",
                            "name": "{workspace}:{layer}".format(workspace=self.workspace, layer=layers[0]),
                        },
                        {
                            "@type": "layer",
                            "name": "{workspace}:{layer}".format(workspace=self.workspace, layer=layers[1]),
                        }
                    ]
                },

                "bounds": {
                    "minx": -138,
                    "maxx": -52,
                    "miny": 5,
                    "maxy": 61,
                    "crs": "EPSG:4326"
                }
            }
        }

        r = requests.post(self.rest_url + 'workspaces/{workspace}/layergroups'.format(workspace=self.workspace),
                          auth=(self.user, self.password),
                          data=json.dumps(body),
                          headers=headers_json
                          )
        return r
