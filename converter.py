import argparse, csv, sys
import hashlib
parser = argparse.ArgumentParser()
parser.add_argument('src_path',type=str)
parser.add_argument('out_path', type=str)
args = vars(parser.parse_args())

def gen_hashed_fm_feats(feats, nr_bins):
    feats = ['{0}:{1}:1'.format(field-1, hashstr(feat, nr_bins)) for (field, feat) in feats]
    return feats

feat_dict = {}
col_str = 'numeric1,numeric2,numeric3,numeric4,numeric5,numeric6,numeric7,numeric8,numeric9,numeric10,numeric11,numeric12,numeric13,label,cat14,cat15,cat16,cat17,cat18,cat19,cat20,cat21,cat22,cat23,cat24,cat25,cat26,cat27,cat28,cat29,cat30,cat31,cat32,cat33,cat34,cat35,cat36,cat37,cat38,cat39'
col_list = col_str.split(',')
for i,col in enumerate(col_list):
    feat_dict[col] = i+1

with open(args['out_path'], 'w') as f:
    for row in csv.DictReader(open(args['src_path'])):
        feats = []
        for feat in row:
            if feat=='label' :continue
            field = feat_dict[feat]
            value=row[feat]
            fvalue=str(feat)+'-'+str(value)
            hash_value=int(hashlib.md5(fvalue.encode('utf8')).hexdigest(), 16)%(1e6-1)+1
            fv=str(field)+':'+str(int(hash_value))+':'+str(1)
            feats.append(fv)
        f.write(row['label']+' '+' '.join(feats)+'\n')
        
