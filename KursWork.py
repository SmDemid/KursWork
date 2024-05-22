import csv
import matplotlib.pyplot as plt

def quick_sort(array):
    if len(array)> 1:
        pivot=array.pop()
        grtr_lst, equal_lst, smlr_lst = [], [pivot], []
        for item in array:
            if item[-1] == pivot[-1]:
                equal_lst.append(item)
            elif item[-1] < pivot[-1]:
                grtr_lst.append(item)
            else:
                smlr_lst.append(item)
        return (quick_sort(smlr_lst) + equal_lst + quick_sort(grtr_lst))
    else:
        return array

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = [value]
        self.next = None


class HashTable:
    def __init__(self):
        self.capacity = 10
        self.size = 0
        self.cell = [None] * self.capacity

    def add(self, key, value):
        index = hash(key) % self.capacity
        chain = self.cell[index]
        while chain:
            if chain.key == key:
                chain.value.append(value)
                return
            chain = chain.next
        new_node = Node(key, value)
        new_node.next = self.cell[index]
        self.cell[index] = new_node
        self.size += 1
        if self.size > 0.8 * self.capacity:
            self.resize

    def resize(self):
        new_capacity = self.capacity * 2
        new_cell = [None] * new_capacity
        for i in range(self.capacity):
            chain = self.cell[i]
            while chain:
                index = hash(chain.key) % new_capacity
                if new_cell[i]:
                    new_chain = new_cell[index]
                    while new_chain.next:
                        new_chain = new_chain.next
                    new_chain.next = Node(chain.key, chain.value)
                else:
                    new_cell[index] = Node(chain.key, chain.value)
                chain = chain.next
        self.capacity = new_capacity
        self.cell = new_cell

    def get(self, key):
        index = hash(key) % self.capacity
        chain = self.cell[index]
        while chain:
            if chain.key == key:
                return chain.value
            chain = chain.next
        return None

    def remove(self, key):
        index = hash(key) % self.capacity
        chain = self.cell[index]
        prev = None
        while chain:
            if chain.key == key:
                if prev:
                    prev.next = chain.next
                else:
                    self.cell[index] = chain.next
                self.size -= 1
                return
            prev = chain
            chain = chain.next


ht = HashTable()
with open('KursWork.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        row[0], row[4], row[5], row[6] = int(row[0]), int(row[4]), int(row[5]), int(row[6])
        ht.add(row[2], row)

earnings = 0
max_profit = [0, '']
most_popular = [[0, '']]
arr = []
labels_arr = []
arr1 = []
for i in ht.cell:
    while i:
        profit = 0
        quantity = 0
        for j in i.value:
            profit += j[-1]
            quantity += j[-3]
            arr.append(profit)
            labels_arr.append(i.key)
        if profit > max_profit[0]:
            max_profit[0], max_profit[1] = profit, i.key
        if quantity > most_popular[0][0]:
            most_popular.clear()
            most_popular.append([quantity, i.key])
        elif quantity == most_popular[0][0]:
            most_popular.append([quantity, i.key])
        earnings += profit
        i = i.next

for i in ht.cell:
    while i:
        profit = 0
        quantity = 0
        for j in i.value:
            profit += j[-1]
            quantity += j[-3]
        arr1.append([i.key, quantity, profit, round(((profit * 100) / earnings), 2)])
        i = i.next

arr1 = list(quick_sort(arr1))
for i in arr1:
    print("Товар", i[0], "продался", i[1], "раз на сумму", i[2], "что составило", str(i[3]) + '%')

print("Общая выручка составила:", earnings)
print("Самый прибыльный товар", str(max_profit[1]) + '.')
print("С продаж", max_profit[1], "выручка составила", max_profit[0], "рублей.")
print("Самые популярные товары:")
for i in most_popular:
    print(i[1], "был продан", i[0], "раз.")

fig, ax = plt.subplots(figsize=(12, 7), subplot_kw=dict(aspect="equal"), dpi=80)
def func(pct):
    absolute = int(pct/100.*earnings)
    return "{:.1f}%".format(pct, absolute)

wedges, texts, autotexts = ax.pie(arr, autopct=lambda pct: func(pct), textprops=dict(color="w"),
                                  colors=plt.cm.Dark2.colors, startangle=140)

ax.legend(wedges, labels_arr, title="Vehicle Class", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
plt.setp(autotexts, size=10, weight=700)
ax.set_title("Соотношение прибыли")
plt.show()
