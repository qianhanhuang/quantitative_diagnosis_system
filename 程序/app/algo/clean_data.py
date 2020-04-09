import xlrd
import xpinyin
import re
import numpy as np
import math

#读数据项
def read_data(path):
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(0)
    bingshi, cizheng, shexiang, maixiang, zhengxing = [], [], [], [], []
    rows = sheet.nrows
    cols = sheet.ncols
    for i in range(rows - 1):
        bingshi.append(sheet.row_values(i + 1)[0])
        cizheng.append(sheet.row_values(i + 1)[1])
        shexiang.append(sheet.row_values(i + 1)[2])
        maixiang.append(sheet.row_values(i + 1)[3])
        zhengxing.append(sheet.row_values(i + 1)[4])
    return [bingshi, cizheng, shexiang, maixiang, zhengxing]

#数据项预处理
def pretreatment(i, is_feature):
    dict={'':'无'}
    if i == '':
        i = '无'
    i = i.replace(' ', ',')
    i = i.replace('兼', ',')
    if not is_feature:
        i = i.replace('证', '')
        i = i.replace('症', '')
    return i

#提取特征矩阵
def extract_feature(raw_data):
    data = [[] for i in range(5)]
    for j in range(5):
        for i in raw_data[j]:
            if j == 4:
                i = pretreatment(i, False)
            else:
                i = pretreatment(i, True)
            for x in re.split('，|,|、', i):
                if x not in data[j]:
                    data[j].append(x)

    print(len(data[0]), len(data[1]), len(data[2]), len(data[3]), len(data[4]))
    return data

#转成特征图像
def feat2img(path, featureSet, tag_num, tagSet, size):
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(0)
    rows = size + 1  # sheet.nrows
    feature_matrix = [[0 for i in range(1024)] for i in range(rows - 1)]
    tag_matrix = [[0 for i in range(tag_num)] for i in range(rows - 1)]
    feat_index_list = [0, 1, 2, 3]

    for i in range(rows - 1):
        for k in range(len(feat_index_list)):
            temp_list = re.split('，|,|、', pretreatment(sheet.row_values(i + 1)[feat_index_list[k]], True))
            for j in temp_list:
                feature_matrix[i][featureSet.index(j)] = 1

        temp_list = re.split('，|,|、', pretreatment(sheet.row_values(i + 1)[4], False))
        for j in temp_list:
            tag_matrix[i][tagSet.index(j)] = 1
    return feature_matrix, tag_matrix

#输出下一批样本
def next_batch(size):
    path = r'data/data.xlsx'
    raw_data = read_data(path)
    features = extract_feature(raw_data)
    featureSet = []
    for i in features:
        featureSet = featureSet + i
    feature_matrix, tag_matrix = feat2img(path, featureSet, len(features[-1]), features[-1], size)
    return [np.array(feature_matrix), np.array(tag_matrix)]

#构建社团划分的点边图
def xls2txt(path):
    wb = xlrd.open_workbook(path)
    file = open('data.txt', 'w+')
    st = wb.sheets()[0]
    rows = st.nrows
    cols = st.ncols
    dic = {}
    for i in range(1, rows - 1):
        line = st.cell(i, 0).value + '，' + st.cell(i, 1).value + '，' + st.cell(i, 2).value
        ver = line.split('，')
        for j in range(len(ver) - 1):
            for k in range(j + 1, len(ver)):
                if ver[j] == '' or ver[k] == '':
                    continue
                if (ver[j] <= ver[k]):
                    key = ver[j] + '\t' + ver[k]
                else:
                    key = ver[k] + '\t' + ver[j]

                if dic.__contains__(key):
                    dic[key] += 1
                else:
                    dic[key] = 1
    for i, j in dic.items():
        file.write(str(i) + '\t' + str(j) + '\n')
    file.close()

#统计特征
def show_feature_rank(rpath, wpath):
    workbook = xlrd.open_workbook(rpath)
    sheet = workbook.sheet_by_index(1)
    file = open(wpath, 'w')
    rows = sheet.nrows
    cols = sheet.ncols
    features = {}
    for i in range(1, rows):
        line = sheet.row_values(i)[4]
        words = line.split(',')
        for j in words:
            if j == '':
                continue
            if j not in features:
                features[j] = 1
            else:
                features[j] += 1

    for i in range(1, rows):
        line = sheet.row_values(i)[4]
        words = line.split(',')
        new = []
        for j in words:
            if j == '':
                continue
            if features[j] > 0 and j not in new:
                new.append(j)
        file.write(','.join(new) + '\n')
    file.close()
    features = sorted(features.items(), key=lambda x: x[1], reverse=True)
    write_features(features, wpath)

#写特征
def write_features(features, wpath):
    p = xpinyin.Pinyin()
    file = open(wpath, 'w')
    for i in features:
        if i[1] > 50:
            file.write(i[0] + '\t' + p.get_initials(i[0], u'').lower() + '\t' + '0' + '\t' + str(i[1]) + '\n')

#构建关系网络的描述文件
def create_gexf():
    nodes = {}
    edges = {}
    all_nodes = []
    id_nodes = 0
    with open('data/sym.txt') as file:
        for i in range(100):
            line = file.readline()
            words = line.split('\t')
            all_nodes.append(words[0])
            nodes[words[0]] = {'id':id_nodes, 'name':words[0], 'freq':int(words[-1]), 'category':'0'}
            id_nodes += 1
    with open('data/ton.txt') as file:
        for i in range(10):
            line = file.readline()
            words = line.split('\t')
            all_nodes.append(words[0])
            nodes[words[0]] = {'id':id_nodes, 'name': words[0], 'freq': int(words[-1]), 'category': '1'}
            id_nodes += 1
    with open('data/pul.txt') as file:
        for i in range(10):
            line = file.readline()
            words = line.split('\t')
            all_nodes.append(words[0])
            nodes[words[0]] = {'id':id_nodes, 'name': words[0], 'freq': int(words[-1]), 'category': '2'}
            id_nodes += 1
    with open('data/syn.txt') as file:
        for i in range(20):
            line = file.readline()
            words = line.split('\t')
            all_nodes.append(words[0])
            nodes[words[0]] = {'id':id_nodes,'name': words[0], 'freq': int(words[-1]), 'category': '3'}
            id_nodes += 1

    id_nodes = 0
    workbook = xlrd.open_workbook('data/data.xlsx')
    sheet = workbook.sheet_by_index(1)
    rows = sheet.nrows
    for i in range(1, rows):
        line = sheet.row_values(i)[0] + ',' + sheet.row_values(i)[1] + ',' + sheet.row_values(i)[2] + ',' + sheet.row_values(i)[3] +',' + sheet.row_values(i)[4]
        words = line.split(',')
        std = []
        for j in words:
            if j in all_nodes and j not in std:
                std.append(j)
        for j in std:
            for k in std:
                if j != k:
                    key = j + '-' + k if j > k else k + '-' + j
                    if key in edges:
                        edges[key]['freq'] += 1
                    else:
                        edges[key] = {'id':id_nodes, 'freq': 1}
                        id_nodes += 1
                else:
                    continue

    header = '''<?xml version="1.0" encoding="UTF-8"?>
    <gexf xmlns="http://www.gexf.net/1.2draft" version="1.2" xmlns:viz="http://www.gexf.net/1.2draft/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd">
      <meta lastmodifieddate="2014-01-30">
        <creator>Gephi 0.8.1</creator>
        <description></description>
      </meta>
      <graph defaultedgetype="undirected" mode="static">
        <attributes class="node" mode="static">
          <attribute id="modularity_class" title="Modularity Class" type="integer"></attribute>
        </attributes>
        <nodes>
    '''

    body = '''    </nodes>
        <edges>
    '''

    end = '''    </edges>
      </graph>
    </gexf>
    '''

    node_model = '''      <node id="点编号" label="标签">
            <attvalues>
              <attvalue for="modularity_class" value="分类"></attvalue>
            </attvalues>
            <viz:size value="大小"></viz:size>
          </node>
    '''

    edge_model = '''      <edge id="边编号" source="源点" target="宿点" value="边长">
          </edge>
    '''
    #with open("../../templates/graph.gexf", "w", encoding='UTF-8') as file:
    #    file.write(header)
    #    for key, value in nodes.items():
    #        file.write(node_model.replace('点编号', str(value['id'])).replace('标签', key).replace('分类', value['category']).replace('大小', str(math.ceil(math.log(value['freq'],2)))))
    #    file.write(body)
    #    for key, value in edges.items():
    #        if value['freq'] > 300:
    #            file.write(edge_model.replace('边编号', str(value['id'])).replace('源点', str(nodes[key.split('-')[0]]['id'])).replace('宿点', str(nodes[key.split('-')[1]]['id'])).replace('边长', str(math.ceil(30.0/math.log(value['freq'],2)))))
    #    file.write(end)
    with open("../../templates/graph.gexf", "w", encoding='UTF-8') as file:
        file.write(header)
        added = []
        for key, value in edges.items():
            if value['freq'] > 300:
                if key.split('-')[0] not in added:
                    file.write(node_model.replace('点编号', str(nodes[key.split('-')[0]]['id'])).replace('标签', nodes[key.split('-')[0]]['name']).replace('分类', nodes[key.split('-')[0]]['category']).replace('大小', str(nodes[key.split('-')[0]]['freq'])))
                    added.append(key.split('-')[0])
                if key.split('-')[1] not in added:
                    file.write(node_model.replace('点编号', str(nodes[key.split('-')[1]]['id'])).replace('标签', nodes[key.split('-')[1]]['name']).replace('分类', nodes[key.split('-')[1]]['category']).replace('大小', str(nodes[key.split('-')[1]]['freq'])))
                    added.append(key.split('-')[1])
        file.write(body)
        for key, value in edges.items():
            if value['freq'] > 300:
                file.write(edge_model.replace('边编号', str(value['id'])).replace('源点', str(nodes[key.split('-')[0]]['id'])).replace('宿点', str(nodes[key.split('-')[1]]['id'])).replace('边长', str(math.ceil(100.0/math.log(value['freq'],2)))))
        file.write(end)

if __name__ == '__main__':
    create_gexf()
