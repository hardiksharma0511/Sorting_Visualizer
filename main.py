import tkinter as tk
from tkinter import ttk
import random
import time

# Sorting Algorithms
def bubble_sort(data, draw_data, delay):
    for i in range(len(data) - 1):
        for j in range(len(data) - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
            color_array = ['green' if x == j or x == j + 1 else 'red' for x in range(len(data))]
            draw_data(data, color_array)
            time.sleep(delay)
    draw_data(data, ['green' for _ in range(len(data))])

def insertion_sort(data, draw_data, delay):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and key < data[j]:
            data[j + 1] = data[j]
            j -= 1
            color_array = ['green' if x == j or x == j + 1 else 'red' for x in range(len(data))]
            draw_data(data, color_array)
            time.sleep(delay)
        data[j + 1] = key
    draw_data(data, ['green' for _ in range(len(data))])

def selection_sort(data, draw_data, delay):
    for i in range(len(data)):
        min_idx = i
        for j in range(i + 1, len(data)):
            if data[j] < data[min_idx]:
                min_idx = j
            color_array = ['yellow' if x == min_idx or x == i else 'red' for x in range(len(data))]
            draw_data(data, color_array)
            time.sleep(delay)
        data[i], data[min_idx] = data[min_idx], data[i]
    draw_data(data, ['green' for _ in range(len(data))])

def merge_sort(data, draw_data, delay):
    merge_sort_helper(data, 0, len(data) - 1, draw_data, delay)

def merge_sort_helper(data, left, right, draw_data, delay):
    if left < right:
        mid = (left + right) // 2
        merge_sort_helper(data, left, mid, draw_data, delay)
        merge_sort_helper(data, mid + 1, right, draw_data, delay)
        merge(data, left, mid, right, draw_data, delay)

def merge(data, left, mid, right, draw_data, delay):
    left_part = data[left:mid + 1]
    right_part = data[mid + 1:right + 1]
    left_idx = right_idx = 0
    sorted_idx = left

    while left_idx < len(left_part) and right_idx < len(right_part):
        if left_part[left_idx] <= right_part[right_idx]:
            data[sorted_idx] = left_part[left_idx]
            left_idx += 1
        else:
            data[sorted_idx] = right_part[right_idx]
            right_idx += 1
        sorted_idx += 1
        color_array = ['purple' if left <= x <= right else 'red' for x in range(len(data))]
        draw_data(data, color_array)
        time.sleep(delay)

    while left_idx < len(left_part):
        data[sorted_idx] = left_part[left_idx]
        left_idx += 1
        sorted_idx += 1

    while right_idx < len(right_part):
        data[sorted_idx] = right_part[right_idx]
        right_idx += 1
        sorted_idx += 1

    color_array = ['green' if left <= x <= right else 'red' for x in range(len(data))]
    draw_data(data, color_array)
    time.sleep(delay)

def quick_sort(data, draw_data, delay):
    quick_sort_helper(data, 0, len(data) - 1, draw_data, delay)

def quick_sort_helper(data, low, high, draw_data, delay):
    if low < high:
        pivot_idx = partition(data, low, high, draw_data, delay)
        quick_sort_helper(data, low, pivot_idx - 1, draw_data, delay)
        quick_sort_helper(data, pivot_idx + 1, high, draw_data, delay)

def partition(data, low, high, draw_data, delay):
    pivot = data[high]
    i = low - 1
    for j in range(low, high):
        if data[j] <= pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
            color_array = ['orange' if x == i or x == j else 'red' for x in range(len(data))]
            draw_data(data, color_array)
            time.sleep(delay)
    data[i + 1], data[high] = data[high], data[i + 1]
    color_array = ['orange' if x == i + 1 or x == high else 'red' for x in range(len(data))]
    draw_data(data, color_array)
    time.sleep(delay)
    return i + 1

def heap_sort(data, draw_data, delay):
    n = len(data)

    for i in range(n // 2 - 1, -1, -1):
        heapify(data, n, i, draw_data, delay)

    for i in range(n - 1, 0, -1):
        data[i], data[0] = data[0], data[i]
        color_array = ['green' if x == i else 'red' for x in range(len(data))]
        draw_data(data, color_array)
        time.sleep(delay)
        heapify(data, i, 0, draw_data, delay)

def heapify(data, n, i, draw_data, delay):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and data[left] > data[largest]:
        largest = left

    if right < n and data[right] > data[largest]:
        largest = right

    if largest != i:
        data[i], data[largest] = data[largest], data[i]
        color_array = ['yellow' if x == i or x == largest else 'red' for x in range(len(data))]
        draw_data(data, color_array)
        time.sleep(delay)
        heapify(data, n, largest, draw_data, delay)

# GUI Application
class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")
        self.root.geometry("900x700")
        self.root.config(bg='#2C3E50')  # Dark background
        self.selected_algorithm = tk.StringVar()
        self.data = []

        self.setup_ui()

    def setup_ui(self):
        UI_frame = tk.Frame(self.root, width=900, height=300, bg='#34495E')
        UI_frame.grid(row=0, column=0, padx=10, pady=5)

        # Header label
        header_label = tk.Label(UI_frame, text="Sorting Visualizer", font=("Arial", 24, "bold"), fg="white", bg='#34495E')
        header_label.grid(row=0, column=0, columnspan=4, pady=10)

        # Algorithm frame with border
        algorithm_frame = tk.Frame(UI_frame, relief="solid", borderwidth=2, bg='#34495E')
        algorithm_frame.grid(row=1, column=0, padx=5, pady=5)
        tk.Label(algorithm_frame, text="Algorithm: ", bg='#34495E', fg="white", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        algo_menu = ttk.Combobox(algorithm_frame, textvariable=self.selected_algorithm,
                                 values=['Bubble Sort', 'Insertion Sort', 'Selection Sort', 'Merge Sort', 'Quick Sort', 'Heap Sort'])
        algo_menu.grid(row=0, column=1, padx=5, pady=5)
        algo_menu.current(0)

        # Size frame with border
        size_frame = tk.Frame(UI_frame, relief="solid", borderwidth=2, bg='#34495E')
        size_frame.grid(row=1, column=2, padx=5, pady=5)
        tk.Label(size_frame, text="Size: ", bg='#34495E', fg="white", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.size_entry = tk.Entry(size_frame, font=("Arial", 12))
        self.size_entry.grid(row=0, column=1, padx=5, pady=5)

        # Speed frame with border
        speed_frame = tk.Frame(UI_frame, relief="solid", borderwidth=2, bg='#34495E')
        speed_frame.grid(row=1, column=3, padx=5, pady=5)
        self.speed_scale = tk.Scale(speed_frame, from_=0.1, to=2.0, resolution=0.1, length=200, orient='horizontal', label='Speed [s]', bg='#34495E', fg='white', font=("Arial", 12))
        self.speed_scale.set(1.0)
        self.speed_scale.grid(row=0, column=0, padx=5, pady=5)

        # Buttons frame
        button_frame = tk.Frame(self.root, bg='#34495E')
        button_frame.grid(row=2, column=0, pady=5)

        # Buttons with same color
        button_color = '#3498DB'  # Same blue for all buttons
        generate_button = tk.Button(button_frame, text="Generate", command=self.generate_data, bg=button_color, fg='white', font=("Arial", 12, "bold"))
        generate_button.grid(row=0, column=0, padx=5, pady=5)

        start_button = tk.Button(button_frame, text="Start", command=self.start_sorting, bg=button_color, fg='white', font=("Arial", 12, "bold"))
        start_button.grid(row=0, column=1, padx=5, pady=5)

        reset_button = tk.Button(button_frame, text="Reset", command=self.reset_data, bg='#E74C3C', fg='white', font=("Arial", 12, "bold"))
        reset_button.grid(row=0, column=2, padx=5, pady=5)

        # Canvas for visualization
        self.canvas = tk.Canvas(self.root, width=900, height=400, bg='#1C2833')
        self.canvas.grid(row=3, column=0, padx=10, pady=5)

    def generate_data(self):
        size = int(self.size_entry.get()) if self.size_entry.get().isdigit() else 50
        self.data = [random.randint(10, 100) for _ in range(size)]
        self.draw_data(self.data, ['red' for _ in range(len(self.data))])

    def draw_data(self, data, color_array):
        self.canvas.delete("all")
        c_height = 400
        c_width = 900
        bar_width = c_width / (len(data) + 1)
        offset = 10
        spacing = 5
        normalized_data = [i / max(data) for i in data]

        for i, height in enumerate(normalized_data):
            x0 = i * bar_width + offset + spacing
            y0 = c_height - height * 350
            x1 = (i + 1) * bar_width + offset
            y1 = c_height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color_array[i])
            self.canvas.create_text(x0 + 2, y0, anchor=tk.SW, text=str(data[i]), fill="white")

        self.root.update_idletasks()

    def start_sorting(self):
        if not self.data:
            return

        if self.selected_algorithm.get() == 'Bubble Sort':
            bubble_sort(self.data, self.draw_data, self.speed_scale.get())
        elif self.selected_algorithm.get() == 'Insertion Sort':
            insertion_sort(self.data, self.draw_data, self.speed_scale.get())
        elif self.selected_algorithm.get() == 'Selection Sort':
            selection_sort(self.data, self.draw_data, self.speed_scale.get())
        elif self.selected_algorithm.get() == 'Merge Sort':
            merge_sort(self.data, self.draw_data, self.speed_scale.get())
        elif self.selected_algorithm.get() == 'Quick Sort':
            quick_sort(self.data, self.draw_data, self.speed_scale.get())
        elif self.selected_algorithm.get() == 'Heap Sort':
            heap_sort(self.data, self.draw_data, self.speed_scale.get())

    def reset_data(self):
        self.data = []
        self.draw_data(self.data, ['white' for _ in range(len(self.data))])

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()