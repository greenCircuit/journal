
from os import listdir
from PIL import Image
from datetime import datetime
from os.path import isfile, join
import traceback
import json
# from django.db import models

# matching timestamps from journal to pictures
# looking for each every time, not caching items
# legacy
class PictureFinder:
    def __init__(self, return_amount, ):
        self.return_amount = return_amount


    # get all pictures that are in range of start and end date
    def get_valid_range(self):
        found_pics = []
        mypath = '/home/shef/Desktop/PycharmProjects/journal/journal/story/search/mounted/2023_all'
        pics_names = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for pic in pics_names:
            image_dir = mypath + "/" + pic
            try:
                image = Image.open(image_dir)
                exifdata = image.getexif()
                str_date = exifdata[306].split()[0]

                pic_date = datetime.strptime(str_date, '%Y:%m:%d')
                if self.start_date <= pic_date and self.end_date >= pic_date:
                    found_pics.append(pic)
                    # print(str_date)
            except:
                print("can't get metadata for: " + image_dir)

        print("Matching pictures found for date range: " + str(len(found_pics)))
        # print(found_pics)
        return found_pics[:1]

# x = PictureFinder(2, "2023-01-01" , "2023-06-01")
# y = x.get_valid_range()

# create 'json db' so don't need to rerun everytime to get correct data
# the way we are using now
class PictureSorted:
    def __init__(self, input_data):
        self.input_data = input_data
        self.base_dir = '/home/shef/Desktop/PycharmProjects/journal/journal/story/search/mounted/'


    # creates dictionary {date: [pics with matched date] for a given folder
    def sort_dates(self, path_searching: str) -> dict:
        sorted_pics = {}
        pics_names = [f for f in listdir(path_searching) if isfile(join(path_searching, f))]
        curr_folder: str = path_searching.split('/')[-1]  # saving what folder is looking for pics ex. 2023_all
        correct_count = 0
        for pic_name in pics_names:
            image_dir: str = path_searching + "/" + pic_name
            # ensuring that going to try to extract metadata from imgs files
            picture_formats_end = [ '.jpg', '.png', '.jpeg', '.JPEG', '.JPG', ]
            correct_format = False
            for picture_format in picture_formats_end:
                if image_dir.endswith(picture_format):
                    correct_format = True


            if correct_format:
                try:
                    correct_count += 1
                    # finding metadata for date
                    img_metadata = {}
                    image = Image.open(image_dir)
                    exifdata = image.getexif()

                    correct_date_key = ''
                    if exifdata[306] is not None:
                        correct_date_key = exifdata[306]
                    else:
                        correct_date_key = 36867

                    str_date = correct_date_key.split()[0].replace(':', '-')

                    # adding pictures
                    if str_date not in sorted_pics:
                        sorted_pics.update({str_date: [curr_folder + '/'+ pic_name]})
                    else:
                        curr_list = sorted_pics[str_date]
                        curr_list.append(curr_folder + '/' + pic_name)
                        sorted_pics.update({str_date: curr_list})

                except Exception:
                    print("can't extract metadata: "+ pic_name)
                    print(path_searching)
                    print('exifdata:')
                    print(exifdata)
                    print("image.getexif():")
                    print(image.getexif())
                    traceback.print_exc()
                    print('=================================================')
                # else:
                #     sorted_pics.update({pic_date: pic[pic_date].append(pic)})
            else:
                print("wrong data format for: " + image_dir)
                print('=================================================')
        print('=========================================')
        print('=========================================')
        print('found correct for folder ' + path_searching + ': ' + str(correct_count))
        print('=========================================')
        print('=========================================')

        return sorted_pics

    def save_all_data(self):
        all_years = {}

        dirrs_found: [] = listdir(self.base_dir)
        print(dirrs_found)
        for sub_folder in dirrs_found:
            full_path: str = self.base_dir + sub_folder
            year_str = sub_folder[:4]
            print("Creating fake db for year: " + year_str)
            data_found = self.sort_dates(full_path)
            all_years.update({year_str: data_found})
        with open('data.json', 'w') as fp:
            json.dump(all_years, fp)

    # create 'db' only with one year
    def save_folder(self, folder_name: str):
        dir_search = self.base_dir + folder_name
        data_found = self.sort_dates(dir_search)
        with open('data.json', 'w') as fp:
            json.dump(data_found, fp)

    # update specified year
    def update_year(self, folder_name: str, year: str):
        with open('/home/shef/Desktop/PycharmProjects/journal/journal/story/search/data.json') as data_file:
            picture_data = json.load(data_file)

        folder_path = self.base_dir + folder_name
        found_data = self.sort_dates(folder_path)
        picture_data.update({year: found_data})


        with open('data.json', 'w') as fp:
            json.dump(picture_data, fp)


def save_all():
    x = PictureSorted("2023-06-01")
    # x.save_all_data()
    x.update_year('2024_all', '2024')
    # x.save_folder("2023_all")


# save_all()

### DEBUG SCRACHPAD
# base_dir = '/home/shef/Desktop/PycharmProjects/journal/journal/story/search/mounted/'
# pic_location='2023_all/DSCF1933.jpg'
# image_dir = base_dir + pic_location
#
# image = Image.open(image_dir)
# exifdata = image.getexif()

# ret = {}
# for tag, value in info.items():
#     decoded = TAGS.get(tag, tag)
#     ret[decoded] = value
#     print(ret[decoded])
# print(type(ret.get('DateTimeOriginal')))
#
# x = 'test.jpg'
# correct_format = ['.jpg', '.png', '.jpeg', '.JPEG', '.JPG', ]
# res = [x for x in correct_format if x in x]
# print(res)