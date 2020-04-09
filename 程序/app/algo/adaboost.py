from sklearn.ensemble import AdaBoostClassifier
from app.algo import cnn

def assess(y_, y):
    n = len(y)
    accuracy = sum([1. if y_[i] == y[i] else 0 for i in range(n)])/n
    tpfp = [0 for i in range(50)]
    tpfn = [0 for i in range(50)]
    tp = [0 for i in range(50)]
    for i in range(n):
        tpfp[y_[i]] += 1.
        tpfn[y[i]] += 1.
        if y[i] == y_[i]:
            tp[y_[i]] += 1.
    mp = [tp[i]/tpfp[i] for i in range(50) if tpfp[i] != 0]
    mi = [tp[i]/tpfn[i] for i in range(50) if tpfn[i] != 0]
    micro_precise = sum(mp)/len(mp)
    micro_recall = sum(mi)/len(mi)
    micro_f1 = 2./(1./micro_precise + 1./micro_recall)
    macro_precise = sum(tp) / sum(tpfp)
    macro_recall = sum(tp) / sum(tpfn)
    macro_f1 = 2./(1./macro_precise + 1./macro_recall)
    return accuracy, micro_precise, micro_recall, micro_f1, macro_precise, macro_recall, macro_f1



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
    X, y_ = cnn.create_matrix(raw, feature_dict, tag_dict)
    y = [i.index(1) for i in y_]
    classifier = AdaBoostClassifier()
    classifier.fit(X, y)
    y_ = classifier.predict(X)
    accuracy, micro_precise, micro_recall, micro_f1, macro_precise, macro_recall, macro_f1 = assess(y_, y)
    print('Accuracy:' + str(accuracy) + '\t Micro_Precise:' + str(micro_precise) + '\t Micro_Recall:' + str(micro_recall) + '\t Micro_F1:' + str(micro_f1) + '\t Macro_Precise:' + str(macro_precise) + '\t Macro_Recall:' + str(macro_recall) + '\t Macro_F1:' + str(macro_f1))

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
    X, y_ = cnn.create_matrix(raw, feature_dict, tag_dict)
    y = [i.index(1) for i in y_]
    classifier = AdaBoostClassifier()
    classifier.fit(X, y)
    feature_dict, tag_dict = cnn.create_dict('./app/algo/data/')
    vec = cnn.create_vec(main_sym, add_sym, ton, pul, feature_dict)
    y_ = classifier.predict([vec])[0]
    return [list(tag_dict.keys())[list(tag_dict.values()).index(y_)]]

if __name__ == '__main__':
    train()
