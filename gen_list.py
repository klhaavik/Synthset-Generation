import random
import os
from pathlib import Path
home = Path.home()
# num_slices_vert = num slices per col
# num_slices_horz = num slices per row


def gen_list_trainval(num_slices_vert, num_slices_horz, num_iters, num_samples: int=None, ignore_slices: set=None, val_percentage=0.2):
    train_str, val_str = "", ""
    total_counter, val_counter = 0, 0

    if not num_samples:
        num_samples = num_slices_vert * num_slices_horz * num_iters

    for i in range (0, num_slices_vert):
        for j in range (0, num_slices_horz):
            if ignore_slices and (i, j) in ignore_slices: continue
            for k in range(0, num_iters):
                if total_counter < num_samples or val_counter < num_samples * val_percentage:
                    if val_counter < num_samples * val_percentage and random.random() > 1 - val_percentage:
                        val_str += input_str % (i, j, k, i, j, k)
                        val_str += '\n'
                        val_counter += 1
                    else:
                        train_str += input_str % (i, j, k, i, j, k)
                        train_str += '\n'
                    total_counter += 1
    return train_str.rstrip(), val_str.rstrip()


def gen_list_testval(num_slices_vert, num_slices_horz, num_iters):
    test_str = ""

    for i in range (0, num_slices_vert):
        for j in range (0, num_slices_horz):
            for k in range(0, num_iters):
                test_str += input_str % (i, j, k, i, j, k)
                test_str += '\n'

    return test_str.rstrip()

def gen_list_trainval_mixed(num_slices_vert, num_slices_horz, num_slices_vert_synthset, num_slices_horz_synthset, num_samples: int=None, ignore_slices: set=None, val_percentage=0.2):
    train_str, val_str = "", ""
    total_counter, val_counter, synth_counter = 0, 0, 0
    output_str = ""

    if not num_samples:
        num_samples = num_slices_vert * num_slices_horz * num_iters

    for i in range (0, num_slices_vert):
        for j in range (0, num_slices_horz):
            if ignore_slices and (i, j) in ignore_slices: continue
            if total_counter < num_samples:
                if synth_counter == 7:
                    while(True):
                        x = i % num_slices_vert_synthset
                        y = j % num_slices_horz_synthset
                        z = random.randint(0, num_iters - 1)
                        if train_str.find(input_str.replace("real", "synthset") % (x, y, z, x, y, z)) == -1:
                            break

                    output_str = input_str.replace("real", "synthset") % (x, y, z, x, y, z)
                    synth_counter = 0
                else:
                    output_str = input_str.replace("synthset", "real") % (i, j, 0, i, j, 0)
                if val_counter < num_samples * val_percentage and random.random() > 1 - val_percentage and "synth" not in output_str:
                    val_str += output_str
                    val_str += '\n'
                    val_counter += 1
                else:
                    train_str += output_str
                    train_str += '\n'
                    if "synth" not in output_str:
                        synth_counter += 1
                total_counter += 1
    return train_str.rstrip(), val_str.rstrip()

def read_ignore_slices_from_file(filename, num_slices_horz):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
        ignore_slices = set()
        for line in lines:
            if '-' in line:
                # handle special case here
                indices = line.split(' - ')
                # big = row, little = col
                start_big_index = int(indices[0].split('_')[0])
                end_big_index = int(indices[1].split('_')[0])
                start_little_index = int(indices[0].split('_')[1])
                end_little_index = int(indices[1].split('_')[1])
                start_index = start_big_index * num_slices_horz + start_little_index
                end_index = end_big_index * num_slices_horz + end_little_index
                row_index = start_big_index
                col_index = start_little_index

                # need the num slices, maybe can infer from if file exists?
                # for now use variable which is set at top

                for i in range(start_index, end_index + 1):
                    ignore_slices.add((row_index, col_index))
                    col_index += 1
                    if col_index % num_slices_horz == 0:
                        col_index = 0
                        row_index += 1
            else:
                indices = line.split('_')
                ignore_slices.add((int(indices[0]), int(indices[1])))
    return ignore_slices


if __name__ == "__main__":
    random.seed(304)

    #Update as necessary
    num_slices_vert = 19
    num_slices_horz = 19
    num_slices_vert_synthset = 19
    num_slices_horz_synthset = 19
    num_iters = 5
    num_samples = None
    val_percentage = 0.2

    dataset_type = "real"
    city = "toronto"
    train_or_test = "train"
    mix = True
    # filename = f"data/{city} slices to remove.txt"
    # ignore_slices = read_ignore_slices_from_file(filename, num_slices_horz)
    # for item in ignore_slices:
    #     print(item)
    ignore_slices = None


    input_str = f"{city}/{city}_{dataset_type}/color/slice_%d_%d_%d.png\t{city}/{city}_{dataset_type}/sem_seg/slice_%d_%d_%d.png"

    if mix:
        strs = gen_list_trainval_mixed(num_slices_vert, num_slices_horz, num_slices_vert_synthset, num_slices_horz_synthset, num_samples=num_samples, ignore_slices=ignore_slices, val_percentage=val_percentage)
        file = open(os.path.join(str(home), f"Documents\\GitHub\\HRNet-Semantic-Segmentation\\{dataset_type}mixed_train.lst"), "w")
        file.write(strs[0])
        file = open(os.path.join(str(home), f"Documents\\GitHub\\HRNet-Semantic-Segmentation\\{dataset_type}mixed_val.lst"), "w")
        file.write(strs[1])
    elif train_or_test == "train":
        strs = gen_list_trainval(num_slices_vert, num_slices_horz, num_iters, num_samples=num_samples, ignore_slices=ignore_slices, val_percentage=val_percentage)
        file = open(os.path.join(str(home), f"Documents\\GitHub\\HRNet-Semantic-Segmentation\\{dataset_type}_train.lst"), "w")
        file.write(strs[0])
        file = open(os.path.join(str(home), f"Documents\\GitHub\\HRNet-Semantic-Segmentation\\{dataset_type}_val.lst"), "w")
        file.write(strs[1])
    elif train_or_test == "test":
        strs = gen_list_testval(num_slices_vert, num_slices_horz, num_iters)
        file = open(os.path.join(str(home), f"Documents\\GitHub\\HRNet-Semantic-Segmentation\\{dataset_type}_test.lst"), "w")
        file.write(strs)