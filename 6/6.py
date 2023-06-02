from abc import ABC, abstractmethod


class SortAlgorithm(ABC):
    @abstractmethod
    def sort(self, data):
        pass


class SelectionSortDecorator(SortAlgorithm):
    def __init__(self, sort_algorithm):
        self.sort_algorithm = sort_algorithm

    def sort(self, data):
        for i in range(len(data)):
            min_idx = i
            for j in range(i + 1, len(data)):
                if data[j] < data[min_idx]:
                    min_idx = j
            data[i], data[min_idx] = data[min_idx], data[i]
        return data


class InsertionSortDecorator(SortAlgorithm):
    def __init__(self, sort_algorithm):
        self.sort_algorithm = sort_algorithm

    def sort(self, data):
        for i in range(1, len(data)):
            key = data[i]
            j = i - 1
            while j >= 0 and data[j] > key:
                data[j + 1] = data[j]
                j -= 1
            data[j + 1] = key
        print(data)
        return data


class MergeSortDecorator(SortAlgorithm):
    def __init__(self, sort_algorithm):
        self.sort_algorithm = sort_algorithm

    def merge(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def merge_sort(self, data):
        if len(data) <= 1:
            return data
        mid = len(data) // 2
        left = self.merge_sort(data[:mid])
        right = self.merge_sort(data[mid:])
        return self.merge(left, right)

    def sort(self, data):
        return self.merge_sort(data)


def read_input_data(input_file):
    with open(input_file, "r") as file:
        data = [int(x) for x in file.read().split()]
    return data


def write_output_data(output_file, sort_type, data):
    with open(output_file, "w") as file:
        file.write(f"Sort type: {sort_type}\n")
        file.write(" ".join(str(x) for x in data))


sort_type = input('Введите название сортировки(selection, insertion, merge): ')
input_file = 'input.txt'
output_file = 'output.txt'

data = read_input_data(input_file)

sort_algorithm = None
if sort_type == "selection":
    sort_algorithm = SelectionSortDecorator(SortAlgorithm)
elif sort_type == "insertion":
    sort_algorithm = InsertionSortDecorator(SortAlgorithm)
elif sort_type == "merge":
    sort_algorithm = MergeSortDecorator(SortAlgorithm)
else:
    print("Invalid sort type. Choose from 'selection', 'insertion', or 'merge'.")
    exit()

sorted_data = sort_algorithm.sort(data)
write_output_data(output_file, sort_type, sorted_data)
