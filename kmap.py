from math import log


class minterm:
    def __init__(self, _number, _binform, _value):
        self.number = _number
        self.binform = _binform
        self.value = _value
        self.neighbors_h = list()
        self.neighbors_v = list()
        self.neighbors_totalh = list()
        self.neighbors_totalv = list()
        self.coverd = 0

    def total_maker(self):
        i: minterm
        for i in self.neighbors_h:
            if i not in self.neighbors_totalh:
                self.neighbors_totalh.append(i)
            for j in i.neighbors_h:
                if j not in self.neighbors_totalh:
                    self.neighbors_totalh.append(j)
        for i in self.neighbors_v:
            if i not in self.neighbors_totalv:
                self.neighbors_totalv.append(i)
            for j in i.neighbors_v:
                if j not in self.neighbors_totalv:
                    self.neighbors_totalv.append(j)

    def one_couter(self):
        one_h = 0
        one_v = 0
        i: minterm
        for i in self.neighbors_totalh:
            if (i.value == '1') and (i not in uncovered_minterm):
                one_h += 1
        for i in self.neighbors_totalv:
            if (i.value == '1') and (i not in uncovered_minterm):
                one_v += 1
        if one_h > one_v:
            return 1
        elif one_v > one_h:
            return -1
        else:
            return 0


def neighbor_maker(minterm):
    index = 0
    for i in range(variables):
        bin_f = minterm.binform
        if minterm.binform[index] == '1':
            bin_f = list(bin_f)
            bin_f[index] = '0'
            bin_f = ''.join(bin_f)
        elif minterm.binform[index] == '0':
            bin_f = list(bin_f)
            bin_f[index] = '1'
            bin_f = ''.join(bin_f)
        index += 1
        nei = int(bin_f, 2)
        for obj in minterms_saver:
            if obj.number == nei and (obj.value == '1' or obj.value == 'd'):
                if bin_f[-2] + bin_f[-1] == minterm.binform[-2] + minterm.binform[-1]:
                    minterm.neighbors_v.append(obj)
                elif (variables == 3 and (bin_f[0] == minterm.binform[0])) or (
                        variables == 4 and (bin_f[0] + bin_f[1] == minterm.binform[0] + minterm.binform[1])):
                    minterm.neighbors_h.append(obj)
                break


def change_cover(min: minterm, m_list):
    min.coverd = 1
    item: minterm
    for item in m_list:
        item.coverd = 1


def full_bin(binary, n):
    return (n * "0") + binary


def nei_len(elm: minterm):
    return len(elm.neighbors_v + elm.neighbors_h)


def sop(result_list):
    finall_ans = ""
    for i in result_list:
        res = i[0].binform
        for j in i:
            counter = 0
            temp = ""
            for ch in j.binform:
                if ch != res[counter]:
                    temp += '-'
                else:
                    temp += ch
                counter += 1
            res = temp
        ascii_counter = 0
        for char in temp:
            if char == '1':
                finall_ans += chr(65 + ascii_counter)
            elif char == '0':
                finall_ans += chr(65 + ascii_counter)
                finall_ans += '`'
            ascii_counter += 1
        finall_ans += '+'
    finall_ans = finall_ans[0:len(finall_ans) - 1]
    print(finall_ans)


def haming_def(obj1, obj2):
    counter = 0
    dif = 0
    for ch in obj1:
        if ch != obj2[counter]:
            dif += 1
        counter += 1
    return dif


minterms_saver = list()
variables = int(input("pleas insert number of variables = "))
for i in range(2 ** variables):
    temp = str(input(f"pleas insert minterm {i} = "))
    if temp == '1':
        binform = format(i, "b")
        minterms_saver.append(minterm(i, full_bin(binform, variables - len(binform)), '1'))
    elif temp == 'd':
        binform = format(i, "b")
        minterms_saver.append(minterm(i, full_bin(binform, variables - len(binform)), 'd'))
for min in minterms_saver:
    neighbor_maker(min)
for min in minterms_saver:
    min.total_maker()
minterms_saver.sort(key=nei_len)
uncovered_minterm = list()
for min in minterms_saver:
    if min.value == '1':
        uncovered_minterm.append(min)
result = list()
for min in uncovered_minterm:
    if min.coverd == 0:
        one_found = 1
        len_h = len(min.neighbors_totalh)
        len_v = len(min.neighbors_totalv)
        if len_h == 0 and len_v == 0:
            result.append([min])
            change_cover(min, [])
        elif len_v == 0:
            logarithm = log(len_h, 2)
            if int(logarithm) == logarithm:
                result.append(min.neighbors_totalh)
                change_cover(min, min.neighbors_totalh)
            else:
                result.append([min])
                for item in min.neighbors_h:
                    if item.value == '1':
                        result[-1].append(item)
                        one_found = 0
                        change_cover(min, [item])
                        break
                if one_found:
                    result[-1].append(min.neighbors_h[0])
                    change_cover(min, [min.neighbors_h[0]])
        elif len_h == 0:
            logarithm = log(len_v, 2)
            if int(logarithm) == logarithm:
                result.append(min.neighbors_totalv)
                change_cover(min, min.neighbors_totalv)
            else:
                result.append([min])
                for item in min.neighbors_v:
                    if item.value == '1':
                        result[-1].append(item)
                        one_found = 0
                        change_cover(min, [item])
                        break
                if one_found:
                    result[-1].append(min.neighbors_v[0])
                    change_cover(min, [min.neighbors_v[0]])
        else:
            log_v = log(len_v, 2)
            log_h = log(len_h, 2)
            temp_list = list()
            flag = 1
            if int(log_v) == log_v and int(log_h) == log_h:
                dec = min.one_couter()
                if dec == 1:
                    result.append(min.neighbors_totalh)
                    change_cover(min, min.neighbors_totalh)
                    item: minterm
                    item_2: minterm
                    for item in min.neighbors_v:
                        if len(item.neighbors_totalh) == len_h:
                            temp_list.extend(item.neighbors_totalh)
                            flag = 0
                        elif len(item.neighbors_totalh) < len_h:
                            flag = 0
                    if flag:
                        for item in min.neighbors_v:
                            for item_2 in item.neighbors_h:
                                if haming_def(item_2.binform, min.neighbors_h[0].binform) == 1:
                                    result[-1].append(item_2)
                                    change_cover(item_2, [item])
                    qubesize = log(len(temp_list) + len_h, 2)
                    if int(qubesize) == qubesize:
                        result[-1].extend(temp_list)
                        change_cover(min, temp_list)
                elif dec == -1:
                    result.append(min.neighbors_totalv)
                    change_cover(min, min.neighbors_totalv)
                    item: minterm
                    for item in min.neighbors_h:
                        if len(item.neighbors_totalv) == len_v:
                            temp_list.extend(item.neighbors_totalv)
                            flag = 0
                        elif len(item.neighbors_totalv) < len_v:
                            flag = 0
                    if flag:
                        for item in min.neighbors_h:
                            for item_2 in item.neighbors_v:
                                if haming_def(item_2.binform, min.neighbors_v[0].binform) == 1:
                                    result[-1].append(item_2)
                                    change_cover(item_2, [item])
                    qubesize = log(len(temp_list) + len_v, 2)
                    if int(qubesize) == qubesize:
                        result[-1].extend(temp_list)
                        change_cover(min, temp_list)
                else:
                    if (len_h == len_v) or (len_h > len_v):
                        result.append(min.neighbors_totalh)
                        change_cover(min, min.neighbors_totalh)
                        item: minterm
                        for item in min.neighbors_v:
                            if len_h == 2:
                                for item_2 in item.neighbors_h:
                                    if item_2 in min.neighbors_h[0].neighbors_v:
                                        result[-1].extend([item_2, item])
                                        change_cover(item, [item_2])
                            elif len(item.neighbors_totalh) == len_h:
                                temp_list.extend(item.neighbors_totalh)
                                flag = 0
                            elif len(item.neighbors_totalh) < len_h:
                                flag = 0
                        if flag:
                            for item in min.neighbors_v:
                                for item_2 in item.neighbors_h:
                                    if haming_def(item_2.binform, min.neighbors_h[0].binform) == 1:
                                        result[-1].append(item_2)
                                        change_cover(item_2, [item])
                        qubesize = log(len(temp_list) + len_h, 2)
                        if int(qubesize) == qubesize:
                            result[-1].extend(temp_list)
                            change_cover(min, temp_list)
                    else:
                        result.append(min.neighbors_totalv)
                        change_cover(min, min.neighbors_totalv)
                        item: minterm
                        for item in min.neighbors_h:
                            if len(item.neighbors_totalv) == len_v:
                                temp_list.extend(item.neighbors_totalv)
                                flag = 0
                            elif len(item.neighbors_totalv) < len_v:
                                flag = 0
                        if flag:
                            for item in min.neighbors_h:
                                for item_2 in item.neighbors_v:
                                    if haming_def(item_2.binform, min.neighbors_v[0].binform) == 1:
                                        result[-1].append(item_2)
                                        change_cover(item_2, [item])
                        qubesize = log(len(temp_list) + len_v, 2)
                        if int(qubesize) == qubesize:
                            result[-1].extend(temp_list)
                            change_cover(min, temp_list)
            elif int(log_v) == log_v and int(log_h) != log_h:
                result.append(min.neighbors_totalv)
                change_cover(min, min.neighbors_totalv)
                item: minterm
                for item in min.neighbors_h:
                    if len(item.neighbors_totalv) == len_v:
                        temp_list.extend(item.neighbors_totalv)
                        flag = 0
                    elif len(item.neighbors_totalv) < len_v:
                        flag = 0
                if flag:
                    for item in min.neighbors_h:
                        for item_2 in item.neighbors_v:
                            if haming_def(item_2.binform, min.neighbors_v[0].binform) == 1:
                                result[-1].append(item_2)
                                change_cover(item_2, [item])
                qubesize = log(len(temp_list) + len_v, 2)
                if int(qubesize) == qubesize:
                    result[-1].extend(temp_list)
                    change_cover(min, temp_list)
            elif int(log_v) != log_v and int(log_h) == log_h:
                result.append(min.neighbors_totalh)
                change_cover(min, min.neighbors_totalh)
                item: minterm
                for item in min.neighbors_v:
                    if len(item.neighbors_totalh) == len_h:
                        temp_list.extend(item.neighbors_totalh)
                        flag = 0
                    elif len(item.neighbors_totalh) < len_h:
                        flag = 0
                if flag:
                    for item in min.neighbors_v:
                        for item_2 in item.neighbors_h:
                            if haming_def(item_2.binform, min.neighbors_h[0].binform) == 1:
                                result[-1].append(item_2)
                                change_cover(item_2, [item])
                qubesize = log(len(temp_list) + len_h, 2)
                if int(qubesize) == qubesize:
                    result[-1].extend(temp_list)
                    change_cover(min, temp_list)
            else:
                flag = 0
                ok_min = None
                for item in min.neighbors_v:
                    if item.coverd == 0 and item.value == '1':
                        result.append([min, item])
                        flag = -1
                        ok_min = item
                        change_cover(min, [item])
                        break
                if flag == -1:
                    for item in min.neighbors_h:
                        for item_2 in item.neighbors_v:
                            if haming_def(item_2.binform, ok_min.binform) == 1:
                                result[-1].extend([item, item_2])
                                change_cover(item, [item_2])

                if not flag:
                    for item in min.neighbors_h:
                        if item.coverd == 0 and item.value == '1':
                            result.append([min, item])
                            flag = 1
                            ok_min = item
                            change_cover(min, [item])
                            break
                if flag == 1:
                    for item in min.neighbors_v:
                        for item_2 in item.neighbors_h:
                            if haming_def(item_2.binform, ok_min.binform) == 1:
                                result[-1].extend([item, item_2])
                                change_cover(item, [item_2])

                if not flag:
                    result.append([min, min.neighbors_v[0]])
                    ok_min = min.neighbors_v[0]
                    for item in min.neighbors_h:
                        for item_2 in item.neighbors_v:
                            if haming_def(item_2.binform, ok_min.binform) == 1:
                                result[-1].extend([item, item_2])
                                change_cover(item, [item_2])
                    change_cover(min, [min.neighbors_v[0]])

sop(result)
# print(result)
