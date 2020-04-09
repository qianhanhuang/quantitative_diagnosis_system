import numpy as np
from app.algo import cnn
from sklearn.cluster import SpectralClustering
from sklearn import metrics


# 定义欧式距离
def ou_dis(v1, v2):
    return np.linalg.norm(v1 - v2)


# 定义余弦相似度
def cosin_sim(v1, v2):
    np.seterr(divide='ignore', invalid='ignore')
    product = v1.dot(v2)
    normA = np.sqrt(v1.dot(v1))
    normB = np.sqrt(v2.dot(v2))
    return product / (normA * normB)


# 定义高斯相似度
def gaussian_simfunc(v1, v2, sigma=1):
    tee = (-np.linalg.norm(v1 - v2) ** 2) / (2 * (sigma ** 2))
    return np.exp(tee)


# 构建相似度矩阵W
def construct_W(vec):
    n = len(vec)
    W = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            W[i, j] = W[j, i] = cosin_sim(vec[i], vec[j])
    return W

def train():
    ncluster = 10
    nsample = 500
    feature_dict, tag_dict = cnn.create_dict('./data/')
    workbook = cnn.xlrd.open_workbook('data/data.xlsx')
    sheet = workbook.sheet_by_index(1)
    rows = sheet.nrows
    raw = []
    for i in range(1, rows):
        row = []
        for j in range(5):
            row.append(sheet.row_values(i)[j])
        # print(row)
        raw.append(row)
    X,y = cnn.create_matrix(raw, feature_dict, tag_dict)
    X = np.array(X[0:nsample])
    X = construct_W(X)
    y_pred = SpectralClustering(n_clusters=ncluster, gamma=1, affinity='nearest_neighbors').fit_predict(X)
    clusters = [[] for  i in range(ncluster)]
    tags = []
    for i in range(nsample):
        clusters[y_pred[i]].append(y[i])
    for i in clusters:
        count = np.sum(i, axis=0)
        thre = np.max(count) * 0.75
        tag = [1 if j > thre else 0 for j in count]
        tags.append(tag)
    y_ = [tags[y_pred[i]] for i in range(nsample)]
    h, o, c = cnn.assess(y_, y[0:nsample])
    print('Hamming Loss:' + str(h) + '\t One-Error:' + str(o) + '\t Coverage:' + str(c))

def prediction(main_sym, add_sym, ton, pul):
    ncluster = 10
    nsample = 500
    feature_dict, tag_dict = cnn.create_dict('./app/algo/data/')
    vec = cnn.create_vec(main_sym, add_sym, ton, pul, feature_dict)
    workbook = cnn.xlrd.open_workbook('./app/algo/data/data.xlsx')
    sheet = workbook.sheet_by_index(1)
    rows = sheet.nrows
    raw = []
    for i in range(1, rows):
        row = []
        for j in range(5):
            row.append(sheet.row_values(i)[j])
        raw.append(row)
    X,y = cnn.create_matrix(raw, feature_dict, tag_dict)
    X = X[0:nsample]
    X.append(vec)
    X = construct_W(np.array(X))
    y_pred = SpectralClustering(n_clusters=ncluster, gamma=1, affinity='precomputed', n_jobs=1).fit_predict(X)
    cluster = []
    for i in range(nsample):
        if y_pred[i] == y_pred[-1]:
            cluster.append(y[i])
    count = np.sum(cluster, axis=0)
    thre = np.max(count) * 0.75
    res = []
    for i in range(len(count)):
        if count[i] >= thre:
            res.append(list(tag_dict.keys())[list(tag_dict.values()).index(i)])
    return res

if __name__ == '__main__':
    train()
