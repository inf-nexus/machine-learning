import csv
import urllib

#main_dir options
all_images_dir = '2017_07_all_image_urls'
bounding_box_dir = '2017_07_bounded_box_annotations'
human_annotations_dir = '2017_07_human_level_annotations'
machine_annotations_dir = '2017_07_machine_annotations'

#sub_dir options
test_dir = 'test'
train_dir = 'train'
validation_dir = 'validation'

#file which contains image url
images_file = 'images.csv'
bounding_box_file = 'annotations-human-bbox.csv'
human_annotations_file = 'annotations-human.csv'
machine_annotations_file = 'annotations-machine.csv'

#stop sign label name
stop_sign_label_name = '/m/02pv19'


class image_data:
    def __init__(self, imageId, confidence):
        self.imageId = imageId
        self.confidence = confidence
    def __hash__(self):
        return hash(self.imageId)
    def __str__(self):
        return 'stopsign_img_confidence:{}_imageID:{}'.format(self.confidence, self.imageId)

def concat_file_path(main_dir, sub_dir, file):
    return '{}/{}/{}'.format(main_dir, sub_dir, file)

#check the contents and format of the csv by reading first row
def parse_folder(filepath):
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        img_count = 0
        for row in reader:
            if img_count == 1:
                break
            print row
            img_count += 1

#read from human level annotations and machine level annotations
def get_imageIds_from_labelName(labelName, filepath):
    imageIDMap = {}
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        progression_count = 0
        for row in reader:
            if row['LabelName'] == labelName:
                imageIDMap[row['ImageID']] = image_data(row['ImageID'], row['Confidence'])
                progression_count += 1
                print '.',
                if (progression_count + 1) % 20 == 0:
                    print
    return imageIDMap

def download_image(url, _image_data, dest_fp):
    urllib.urlretrieve(url, dest_fp + str(_image_data) + ".jpg")

def parse_and_download_images(filepath, imageIDMap):
    imageid_set = imageIDMap.keys()
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        img_count = 0
        for idx, row in enumerate(reader):
            if row['ImageID'] in imageid_set:
                download_image(row['OriginalURL'], imageIDMap[row['ImageID']], 'parsed_images/')
                print '.',
                if (img_count + 1) % 20 == 0:
                    print
                img_count += 1

if __name__ == '__main__':
    #complete filepaths to training csv files
    all_url_fp = concat_file_path(all_images_dir, train_dir, images_file)
    bbox_fp = concat_file_path(bounding_box_dir, train_dir, bounding_box_file)
    human_annotations_fp = concat_file_path(human_annotations_dir, train_dir, human_annotations_file)
    machine_annotations_fp = concat_file_path(machine_annotations_dir, train_dir, machine_annotations_file)

    imageIds = get_imageIds_from_labelName(stop_sign_label_name, human_annotations_fp)
    print 'finished parsing human annotations number of matches: ', len(imageIds)

    parse_and_download_images(all_url_fp, imageIds)

    print 'finished downloading human annotation images'

    imageIds2 = get_imageIds_from_labelName(stop_sign_label_name, machine_annotations_fp)
    print 'finished parsing machine annotations number of matches: ', len(imageIds2)

    parse_and_download_images(all_url_fp, imageIds2)
    print 'finished downloading machine annotation images'
