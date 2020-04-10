import os
import re
import argparse


# https://askubuntu.com/questions/781497/how-can-i-compress-images
# (scroll to botton answer for bash-command batch resizing of images)

def yn_to_bool(yn):
    assert yn in ('y', 'n')
    return yn == 'y'


def get_args():
    parser = argparse.ArgumentParser(description="""Rename image file names from different
    sources (e.g. different camera apps).
    Usage example: python $PATH_TO_REPO/rename_imgs_diff_src/rename_imgs.py -i=~/Desktop/phone_img_bak -m=n
    """)
    parser.add_argument(
        '-i', '--img_dir', dest='img_dir',
        help="Directory path of image files to rename, e.g. -i=~/Desktop/phone_img_bak",
        required=True
    )
    parser.add_argument(
        '-m', '--multiples_on_ts', dest='multiples_on_ts',
        help="PDF orientation. Accepts y for landscape or n for vertical. "
             "Default value is y. e.g. --landscape=y",
        default='y',
        choices=['y', 'n']
    )

    args = parser.parse_args()
    # args, unknown = parser.parse_known_args()

    # convert to bool
    args.multiples_on_ts = yn_to_bool(args.multiples_on_ts)

    return args


def reconstruct_img_fn(fn, pat):
    result = re.match(pat, fn)
    src, dt, time, ext = result.groups()
    return f'{dt}_{time}_{src}.{ext}'


def cur_dir():
    return os.path.basename(os.getcwd())


def main():
    args = get_args()

    img_dir = args.img_dir
    multiples_on_ts = args.multiples_on_ts

    if multiples_on_ts:
        # todo: implement multiples_on_ts
        raise NotImplementedError('The method "multiples_on_ts" is not yet implemented. Please drop this argument')

    img_dir = os.path.expanduser(img_dir)

    img_pat = r'(\w+)_(\d{8})_(\d{6})\.(.*$)'
    img_fnames = os.listdir(img_dir)

    for img_fname in img_fnames:
        try:
            rec_img_fname = reconstruct_img_fn(img_fname, img_pat)
            print(rec_img_fname)
        except Exception as e:
            print('ERROR')
            print(f'Failed on: {img_fname}')
            raise e

    # if no failures
    [
        os.rename(
            fn,
            reconstruct_img_fn(fn, img_pat)
        )
        for fn in img_fnames
    ]

    print('FIN')


if __name__ == '__main__':
    main()
