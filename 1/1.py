from abc import ABCMeta, abstractmethod

class AbstractFactory(metaclass=ABCMeta):

    @abstractmethod
    def sort(cls):
        pass

    def input(self):
        self.l = []
        with open('1input.txt', 'r') as f:
            l = f.read().split()

        for i in l:
            self.l.append(int(i))

        print(self.l)

    def output(self):
        with open('1output.txt', 'w') as f:
            f.write(self.__class__.__name__)
            f.write(str(self.res))

class selection(AbstractFactory):

    def sort(self):
        l = self.l
        for f in range(0, len(l) - 1):
            min_pos = len(l) - 1
            for location in range(f, len(l)):
                if l[location] < l[min_pos]:
                    min_pos = location

            t = l[f]
            l[f] = l[min_pos]
            l[min_pos] = t

        self.res = l
        return l

class merge(AbstractFactory):

    def sort_min(self, a):
        res = []
        if len(a) == 1:
            return a
        l = len(a) // 2

        x = self.sort_min(a[:l])
        b = self.sort_min(a[l:])

        i = 0
        j = 0

        while i < len(x) and j < len(b):
            if x[i] < b[j]:
                res.append(x[i])
                i += 1
            else:
                res.append(b[j])
                j += 1

        res += x[i:] + b[j:]

        return res
    def sort(self):
        a = self.l
        res = []
        if len(a) == 1:
            return a
        l = len(a) // 2

        x = self.sort_min(a[:l])
        b = self.sort_min(a[l:])

        i = 0
        j = 0

        while i < len(x) and j < len(b):
            if x[i] < b[j]:
                res.append(x[i])
                i += 1
            else:
                res.append(b[j])
                j += 1

        res += x[i:] + b[j:]

        self.res = res

        return res

class intersection(AbstractFactory):

    def sort(self):
        l = self.l
        for i in range(len(l) - 2, -1, -1):

            curr = l[i]
            pos = i

            while pos < len(l) - 1 and l[pos + 1] < curr:
                l[pos] = l[pos + 1]
                pos += 1

            l[pos] = curr

        self.res = l
        return l

sort = input('Введите название сортировки(intersection, merge, selection): ')
if sort == 'intersection':
    f = intersection()
elif sort == 'merge':
    f = merge()
elif sort == 'selection':
    f = selection()

f.input()
f.sort()
f.output()
