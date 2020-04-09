import tensorflow as tf
import  xlrd
import copy

def standard(y_):
    mat = []
    for i in y_:
        row = []
        thre = max(i) * 0.5
        for j in i:
            if j >= thre:
                row.append(1)
            else:
                row.append(0)
        mat.append(row)
    return mat

def hamming(y_, y):
    count = 0
    for i in range(len(y)):
        if y_[i] != y[i]:
            count += 1.
    return count/len(y)

def one_error(y_, y):
    count = 0
    max_val = max(y_)
    num = 0
    for i in range(len(y)):
        if y_[i] == max_val :
            num += 1
            if  y[i] != 1:
                count += 1.
    return count/num/2

def coverage(y_, y):
    max_rank = 0
    sorted_y_ = copy.deepcopy(y_)
    sorted_y_.sort(reverse=True)
    for i in range(len(y)):
        rank = sorted_y_.index(y_[i])
        if y[i] == 1 and rank > max_rank:
            max_rank = rank
    return max_rank

def assess(y_, y):
    y_ = standard(y_)
    count_hamming = 0
    count_error = 0
    count_coverage = 0
    num = len(y)
    for i in range(num):
        #print(y_[i])
        #print(y[i])
        #print('***********')
        count_hamming += hamming(y_[i], y[i])
        count_error += one_error(y_[i], y[i])
        count_coverage += coverage(y_[i], y[i])
    return  count_hamming/num, count_error/num, count_coverage/num

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

def train(feature_mat, tag_mat):
    sess = tf.InteractiveSession()
    x, y_, keep_prob, y_conv = crete_tf()
    tf.global_variables_initializer().run()
    saver = tf.train.Saver(max_to_keep=1)
    count = len(feature_mat)
    base = 0
    i = 0
    while base + 100 < count:
        predict_y = y_conv.eval(feed_dict={x: feature_mat[base: base + 100], y_: tag_mat[base: base + 100], keep_prob: 0.8})
        base += 100
        i += 1
        h, o, c = assess(predict_y, tag_mat[base: base + 100])
        print('Hamming Loss:' + str(h) + '\t One-Error:' + str(o) + '\t Coverage:' + str(c))

    predict_y = y_conv.eval(feed_dict={x: feature_mat[base:], y_: tag_mat[base:], keep_prob: 0.8})
    h, o, c = assess(predict_y, tag_mat[base: base + 100])
    print('Hamming Loss:' + str(h) + '\t One-Error:' + str(o) + '\t Coverage:' + str(c))
    saver.save(sess, 'model/model')
    sess.close()

def create_dict(pre):
    i = 0
    feature_file = ['sym.txt', 'ton.txt', 'pul.txt']
    tag_file = 'syn.txt'
    feature_dict = {}
    tag_dict = {}
    for path in feature_file:
        with open(pre + path, 'r') as file:
            lines = file.readlines()
            for j in lines:
                feature = j.split('\t')[0]
                if feature not in feature_dict:
                    feature_dict[feature] = i
                    i += 1
    i = 0
    with open(pre + tag_file, 'r') as file:
        lines = file.readlines()
        for j in lines:
            tag = j.split('\t')[0]
            if tag not in tag_dict:
                tag_dict[tag] = i
                i += 1
    return feature_dict , tag_dict


def create_matrix(data, feature_dict, tag_dict):
    feature_mat = []
    tag_mat = []
    for i in data:
        vec = [0 for j in range(50)]
        line = i[4]
        tags = line.split(',')
        for j in tags:
            if j not in tag_dict:
                continue
            vec[tag_dict[j]] = 1
        if sum(vec) == 0:
            continue
        tag_mat.append(vec)
        #print(vec)

        vec = [0 for j in range(2304)]
        line = i[0] + ',' + i[1] + ',' + i[2] + ',' + i[3]
        features = line.split(',')
        for j in features:
            if j not in feature_dict:
                continue
            vec[feature_dict[j]] = 1
        feature_mat.append(vec)
        #print(vec)
    return feature_mat, tag_mat

def create_vec(main_sym, add_sym, ton, pul, feature_dict):
    vec = [0 for j in range(2304)]
    line = main_sym + ',' + add_sym + ',' + ton + ',' + pul
    features = line.split(',')
    for j in features:
        if j not in feature_dict:
            continue
        vec[feature_dict[j]] = 1
    return vec

def crete_tf():
    x = tf.placeholder(tf.float32, [None, 2304])
    y_ = tf.placeholder(tf.float32, [None, 50])
    x_image = tf.reshape(x, [-1, 48, 48, 1])

    W_conv1 = weight_variable([4, 4, 1, 256])
    b_conv1 = bias_variable([256])
    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    W_conv2 = weight_variable([4, 4, 256, 128])
    b_conv2 = bias_variable([128])
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

    W_fc1 = weight_variable([12 * 12 * 128, 4096])
    b_fc1 = weight_variable([4096])
    h_pool2_flat = tf.reshape(h_pool2, [-1, 12 * 12 * 128])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    w_fc2 = weight_variable([4096, 50])
    b_fc2 = weight_variable([50])
    y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, w_fc2) + b_fc2)
    y = tf.argmax(y_conv, 1)

    cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y_conv), reduction_indices=[1]))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
    return x, y_, keep_prob, y_conv

def prediction(main_sym, add_sym, ton, pul):
    sess = tf.InteractiveSession()
    x, y_, keep_prob, y_conv = crete_tf()
    tf.global_variables_initializer().run()
    model_file = tf.train.latest_checkpoint('./app/algo/model/')
    saver = tf.train.Saver(max_to_keep=3)
    saver.restore(sess, model_file)
    feature_dict, tag_dict = create_dict('./app/algo/data/')
    vec = create_vec(main_sym, add_sym, ton, pul, feature_dict)
    predict_y = y_conv.eval(feed_dict={x: [vec], keep_prob: 1})
    sess.close()
    thre = max(predict_y[0]) * 0.5
    res = []
    for i in range(len(predict_y[0])):
        if predict_y[0][i] >= thre:
            res.append(list(tag_dict.keys())[list(tag_dict.values()).index(i)])
    return res



if __name__ == '__main__':
    feature_dict, tag_dict = create_dict('./data/')
    workbook = xlrd.open_workbook('data/data.xlsx')
    sheet = workbook.sheet_by_index(1)
    rows = sheet.nrows
    raw = []
    for i in range(1, rows):
        row = []
        for j in range(5):
            row.append(sheet.row_values(i)[j])
        #print(row)
        raw.append(row)
    feature_mat, tag_mat = create_matrix(raw, feature_dict, tag_dict)
    #print(feature_mat[1])
    print(tag_mat[1])
    #train(feature_mat,tag_mat)