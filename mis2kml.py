import re
import os

class mis2kml:

    def __init__(self, mis_dir):
        """
        2019.08.30. KangMin Park, LSM
        The Code for changing multmis format of Phatom to KML format.
        This code will be updated.
        :param mis_dir:
        """
        self.mis_dir = mis_dir
        self.info_list = None
        self.extract_mis()
        self.save_kml()

    def extract_mis(self):

        mis_f = open(self.mis_dir, 'rb')
        mis_str = str(mis_f.read())

        # extracting
        comp = "00{(.*?)}}"
        compile_contents = re.compile(comp, mis_str)
        lon_re = '"lng":(.*?),'
        lat_re = '"lat":(.*?),'
        alt_re = '"altitude":(.*?),'

        info_list = []
        for index, part in enumerate(compile_contents):
            lon_all = re.findall(lon_re, str(part))
            lat_all = re.findall(lat_re, str(part))
            alt_all = re.findall(alt_re, str(part))
            for lon, lat, alt in zip(lon_all, lat_all, alt_all):
                info_list.append([index, lon, lat, alt])

        self.info_list = info_list

    def save_kml(self):
        kml_format_f = open("kml_format.txt", 'r')
        kml_format_str = str(kml_format_f.read())
        idx = 0
        course = ""
        for info_part in self.info_list:
            if info_part[0] == idx:
                course = course + info_part[1]+","+info_part[2]+","+info_part[3]+"\n"
            else:
                kml_f = open(os.path.dirname(self.mis_dir)+"kml_version{0}.kml".format(str(idx)), 'w')
                text = kml_format_str[:751] + course + kml_format_str[751:]
                kml_f.write(text)
                idx = idx+1
                course = info_part[1]+","+info_part[2]+","+info_part[3]+"\n"
        kml_f = open(os.path.dirname(self.mis_dir) + "kml_version{0}.kml".format(str(idx)), 'w')
        text = kml_format_str[:751] + course + kml_format_str[751:]
        kml_f.write(text)

        print("Saved mis format file to kml format.")

if __name__ == "__main__":
    mis_dir = "D:\\2019ALSM\\01해양감시망5차년도\\03실험\\20190624-26군산연도\\010YUDFBC0C4001X_export_20190627162621.multmis"
    a = mis2kml(mis_dir)