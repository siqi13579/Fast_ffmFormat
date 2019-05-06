import hashlib, csv, math, os, pickle, subprocess
import argparse
def split(path, nr_thread, has_header):
    def open_with_first_line_skipped(path, skip=True):
        f = open(path)
        if not skip:
            return f
        next(f)
        return f
    def open_with_header_witten(path, idx, header):
        f = open(path+'.__tmp__.{0}'.format(idx), 'w')
        if not has_header:
            return f 
        f.write(header)
        return f
    def calc_nr_lines_per_thread():
        nr_lines = int(list(subprocess.Popen('wc -l {0}'.format(path), shell=True, 
            stdout=subprocess.PIPE).stdout)[0].split()[0])
        if not has_header:
            nr_lines += 1 
        return math.ceil(float(nr_lines)/nr_thread)

    header = open(path).readline()

    nr_lines_per_thread = calc_nr_lines_per_thread()

    idx = 0
    f = open_with_header_witten(path, idx, header)
    for i, line in enumerate(open_with_first_line_skipped(path, has_header), start=1):
        if i%nr_lines_per_thread == 0:
            f.close()
            idx += 1
            f = open_with_header_witten(path, idx, header)
        f.write(line)
    f.close()

def parallel_convert(arg_paths, nr_thread):

    workers = []
    for i in range(nr_thread):
        cmd = 'python converter.py'
        for path in arg_paths:
            cmd += ' {0}'.format(path+'.__tmp__.{0}'.format(i))
        worker = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        workers.append(worker)
    for worker in workers:
        worker.communicate()

def cat(path, nr_thread):
    
    if os.path.exists(path):
        os.remove(path)
    for i in range(nr_thread):
        cmd = 'cat {svm}.__tmp__.{idx} >> {svm}'.format(svm=path, idx=i)
        p = subprocess.Popen(cmd, shell=True)
        p.communicate()
def delete(path, nr_thread):
    for i in range(nr_thread):
        os.remove('{0}.__tmp__.{1}'.format(path, i))
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name',type=str)
    parser.add_argument('workers', type=int)
    args = vars(parser.parse_args())
    fp = args['file_name']
    ws = args['workers']
    split(fp+'.csv', ws, True)
    parallel_convert([fp+'.csv',fp+'.ffm'], ws)
    cat(fp+'.ffm',ws)
    delete(fp+'.csv',ws)
    delete(fp+'.ffm',ws)
