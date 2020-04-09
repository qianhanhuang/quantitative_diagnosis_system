from sklearn.ensemble import RandomForestClassifier
from app.algo import cnn

def train():
    feature_dict, tag_dict = cnn.create_dict('./data/')
    workbook = cnn.xlrd.open_workbook('data/data.xlsx')
    sheet = workbook.sheet_by_index(1)
    rows = sheet.nrows
    raw = []
    for i in range(1, rows):
        row = []
        for j in range(5):
            row.append(sheet.row_values(i)[j])
        raw.append(row)
    X, y = cnn.create_matrix(raw, feature_dict, tag_dict)
    classifier = RandomForestClassifier()
    classifier.fit(X, y)
    y_ = classifier.predict(X)
    h, o, c = cnn.assess(y_, y)
    print('Hamming Loss:' + str(h) + '\t One-Error:' + str(o) + '\t Coverage:' + str(c))

def prediction(main_sym, add_sym, ton, pul):
    feature_dict, tag_dict = cnn.create_dict('./app/algo/data/')
    workbook = cnn.xlrd.open_workbook('./app/algo/data/data.xlsx')
    sheet = workbook.sheet_by_index(1)
    rows = sheet.nrows
    raw = []
    for i in range(1, rows):
        row = []
        for j in range(5):
            row.append(sheet.row_values(i)[j])
        raw.append(row)
    X, y = cnn.create_matrix(raw, feature_dict, tag_dict)
    classifier = RandomForestClassifier()
    classifier.fit(X, y)
    feature_dict, tag_dict = cnn.create_dict('./app/algo/data/')
    vec = cnn.create_vec(main_sym, add_sym, ton, pul, feature_dict)
    y_ = classifier.predict([vec])[0]
    res = []
    for i in range(len(y_)):
        if y_[i] == 1:
            res.append(list(tag_dict.keys())[list(tag_dict.values()).index(i)])
    return res


if __name__ == '__main__':
    train()
