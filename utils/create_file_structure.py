import os
import shutil

def sort_data_into_common_directory(
    rgb_image_paths,
    annotations_parent_directory,
    new_parent_directory,
    training):
    """ Takes every rgb image in 'rgb_image_paths' and its corresponding
        2D annotation and saves them in the same directory under
        'new_parent_directory'. 'training' is a flag that dictates whether the
        data is training or testing data."""
    image_number = 1
    file_prefix = 'training_' if training else 'testing_'
    offset = 5050 if training else 0
    for image_path in rgb_image_paths:
        image_path = image_path.strip('\n')
        image_identifier = file_prefix + str(image_number).zfill(4)
        new_path = os.path.join(new_parent_directory, image_identifier)
        if not os.path.exists(new_path):
            os.makedirs(new_path)

            shutil.copy(image_path, new_path)
            image_filename = image_path.split('/')[-1]
            os.rename(os.path.join(new_path, image_filename),
                os.path.join(new_path, image_identifier + '.jpg'))

            label_filename = ('img-'
                + str(image_number + offset).zfill(6) + '.png')
            label_full_path = os.path.join(annotations_parent_directory,
                label_filename)
            shutil.copy(label_full_path, new_path)
            os.rename(os.path.join(new_path, label_filename),
                os.path.join(new_path, image_identifier + '_2DAnnotation.png'))
        image_number = image_number + 1
    return

if __name__ == '__main__':
    TRAINING_PATH = 'data/training'
    TESTING_PATH = 'data/testing'
    ANNOTATION_PATH = 'sunrgbd_train_test_labels'

    # Create directories to store testing and training images, annotations and
    # depth information.
    if not os.path.exists(TRAINING_PATH):
        os.makedirs(TRAINING_PATH)
    if not os.path.exists(TESTING_PATH):
        os.makedirs(TESTING_PATH)

    # Read files containing the paths for the testing and training images
    # respectively.
    training_images_file = open('training_images.txt', 'r')
    training_images_paths = training_images_file.readlines()
    testing_images_file = open('testing_images.txt', 'r')
    testing_images_paths = testing_images_file.readlines()

    sort_data_into_common_directory(training_images_paths, ANNOTATION_PATH,
        TRAINING_PATH, True)
    sort_data_into_common_directory(testing_images_paths, ANNOTATION_PATH,
        TESTING_PATH, False)
