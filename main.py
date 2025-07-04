import streamlit as st
import random
import time
import pandas as pd
import altair as alt
from textwrap import dedent
import base64
import os

# THIS MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="Sorting Visualizer", layout="wide")

def set_bg_from_local(image_file):
    if not os.path.exists(image_file):
        return  # Do not call any Streamlit function here
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('data:image/jpg;base64,{encoded}');
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set the background image (assume the file is named 'background.jpg')
set_bg_from_local("background.jpg")

# --- Personal Info ---
NAME = "Hardik Sharma"
GITHUB = "https://github.com/hardiksharma0511/Sorting_Visualizer"
LINKEDIN = "https://www.linkedin.com/in/hardiksharma05"  # <-- Replace with your real LinkedIn

# --- Algorithm Info ---
ALGO_INFO = {
    'Bubble Sort': {
        'desc': 'Repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order.',
        'complexity': 'O(n²)'
    },
    'Insertion Sort': {
        'desc': 'Builds the sorted array one item at a time by repeatedly inserting the next element into the correct position.',
        'complexity': 'O(n²)'
    },
    'Selection Sort': {
        'desc': 'Repeatedly selects the minimum element from the unsorted part and puts it at the beginning.',
        'complexity': 'O(n²)'
    },
    'Merge Sort': {
        'desc': 'Divides the array into halves, sorts them and merges them back together.',
        'complexity': 'O(n log n)'
    },
    'Quick Sort': {
        'desc': 'Divides the array into partitions and sorts them recursively.',
        'complexity': 'O(n log n) average, O(n²) worst'
    },
    'Heap Sort': {
        'desc': 'Builds a heap and repeatedly extracts the maximum element.',
        'complexity': 'O(n log n)'
    },
}

# --- Main Title and Description ---
st.title("Sorting Algorithm Visualizer 🧮")
st.markdown("""
Welcome to the **Sorting Algorithm Visualizer**! 🎨

- **Choose** from six classic algorithms
- **Customize** array size, speed, and order
- **Watch** the sorting process step-by-step
- **Learn** with color-coded bars and algorithm info
""")

# --- Controls ---
algo_options = list(ALGO_INFO.keys())
algorithm = st.selectbox("Select Algorithm", algo_options)
array_size = st.slider("Array Size", 5, 100, 30)
speed = st.slider("Speed (seconds per step)", 0.01, 1.0, 0.05, step=0.01)
order = st.radio("Sorting Order", ["Ascending", "Descending"], horizontal=True)

# --- Algorithm Info ---
st.markdown(f"**{algorithm}**: {ALGO_INFO[algorithm]['desc']}")
st.caption(f"Time Complexity: {ALGO_INFO[algorithm]['complexity']}")

# --- Generate/Reset Array ---
def generate_array():
    return [random.randint(10, 100) for _ in range(array_size)]

if 'array' not in st.session_state or st.button("Generate New Array"):
    st.session_state['array'] = generate_array()
    st.session_state['stats'] = {'comparisons': 0, 'swaps': 0}
    st.session_state['sorting'] = False
    st.session_state['step'] = 0
array = st.session_state['array']

if st.button("Reset Array"):
    st.session_state['array'] = generate_array()
    st.session_state['stats'] = {'comparisons': 0, 'swaps': 0}
    st.session_state['sorting'] = False
    st.session_state['step'] = 0
    array = st.session_state['array']

# --- Color Map ---
color_map = {
    'red': '#e74c3c',
    'green': '#00ff99',  # Sorted
    'yellow': '#ffe066', # Compared
    'purple': '#9b59b6',
    'orange': '#ff9900', # Swapping
    'blue': '#3498db',   # Swapping (new)
    'white': '#ecf0f1'
}

# --- Enhanced Sorting Algorithm Generators with Animation Colors ---
def bubble_sort(data, ascending=True):
    n = len(data)
    stats = {'comparisons': 0, 'swaps': 0}
    for i in range(n - 1):
        for j in range(n - i - 1):
            stats['comparisons'] += 1
            # First, show comparison
            yield data[:], ['yellow' if x == j or x == j + 1 else 'red' for x in range(len(data))], stats.copy()
            if (data[j] > data[j + 1]) if ascending else (data[j] < data[j + 1]):
                data[j], data[j + 1] = data[j + 1], data[j]
                stats['swaps'] += 1
                # Then, show swap
                yield data[:], ['blue' if x == j or x == j + 1 else 'red' for x in range(len(data))], stats.copy()
    yield data[:], ['green' for _ in range(len(data))], stats.copy()

def insertion_sort(data, ascending=True):
    stats = {'comparisons': 0, 'swaps': 0}
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and ((key < data[j]) if ascending else (key > data[j])):
            stats['comparisons'] += 1
            # Show comparison
            yield data[:], ['yellow' if x == j or x == j + 1 else 'red' for x in range(len(data))], stats.copy()
            data[j + 1] = data[j]
            j -= 1
            stats['swaps'] += 1
            # Show swap
            yield data[:], ['blue' if x == j or x == j + 1 else 'red' for x in range(len(data))], stats.copy()
        data[j + 1] = key
        yield data[:], ['yellow' if x == i else 'red' for x in range(len(data))], stats.copy()
    yield data[:], ['green' for _ in range(len(data))], stats.copy()

def selection_sort(data, ascending=True):
    stats = {'comparisons': 0, 'swaps': 0}
    for i in range(len(data)):
        min_idx = i
        for j in range(i + 1, len(data)):
            stats['comparisons'] += 1
            # Show comparison
            yield data[:], ['yellow' if x == min_idx or x == j else 'red' for x in range(len(data))], stats.copy()
            if (data[j] < data[min_idx]) if ascending else (data[j] > data[min_idx]):
                min_idx = j
        # Show swap
        data[i], data[min_idx] = data[min_idx], data[i]
        stats['swaps'] += 1
        yield data[:], ['blue' if x == i or x == min_idx else 'red' for x in range(len(data))], stats.copy()
    yield data[:], ['green' for _ in range(len(data))], stats.copy()

def merge_sort(data, ascending=True):
    stats = {'comparisons': 0, 'swaps': 0}
    yield from merge_sort_helper(data, 0, len(data) - 1, ascending, stats)
    yield data[:], ['green' for _ in range(len(data))], stats.copy()

def merge_sort_helper(data, left, right, ascending, stats):
    if left < right:
        mid = (left + right) // 2
        yield from merge_sort_helper(data, left, mid, ascending, stats)
        yield from merge_sort_helper(data, mid + 1, right, ascending, stats)
        yield from merge(data, left, mid, right, ascending, stats)

def merge(data, left, mid, right, ascending, stats):
    left_part = data[left:mid + 1]
    right_part = data[mid + 1:right + 1]
    left_idx = right_idx = 0
    sorted_idx = left
    while left_idx < len(left_part) and right_idx < len(right_part):
        stats['comparisons'] += 1
        # Show comparison
        yield data[:], ['yellow' if x == sorted_idx else 'red' for x in range(len(data))], stats.copy()
        if (left_part[left_idx] <= right_part[right_idx]) if ascending else (left_part[left_idx] >= right_part[right_idx]):
            data[sorted_idx] = left_part[left_idx]
            left_idx += 1
        else:
            data[sorted_idx] = right_part[right_idx]
            right_idx += 1
        # Show swap
        yield data[:], ['blue' if x == sorted_idx else 'red' for x in range(len(data))], stats.copy()
        sorted_idx += 1
    while left_idx < len(left_part):
        data[sorted_idx] = left_part[left_idx]
        left_idx += 1
        sorted_idx += 1
        stats['swaps'] += 1
        yield data[:], ['blue' if x == sorted_idx-1 else 'purple' if left <= x <= right else 'red' for x in range(len(data))], stats.copy()
    while right_idx < len(right_part):
        data[sorted_idx] = right_part[right_idx]
        right_idx += 1
        sorted_idx += 1
        stats['swaps'] += 1
        yield data[:], ['blue' if x == sorted_idx-1 else 'purple' if left <= x <= right else 'red' for x in range(len(data))], stats.copy()

def quick_sort(data, ascending=True):
    stats = {'comparisons': 0, 'swaps': 0}
    yield from quick_sort_helper(data, 0, len(data) - 1, ascending, stats)
    yield data[:], ['green' for _ in range(len(data))], stats.copy()

def quick_sort_helper(data, low, high, ascending, stats):
    if low < high:
        pivot_idx, states = yield from partition(data, low, high, ascending, stats)
        for state in states:
            yield state
        yield from quick_sort_helper(data, low, pivot_idx - 1, ascending, stats)
        yield from quick_sort_helper(data, pivot_idx + 1, high, ascending, stats)

def partition(data, low, high, ascending, stats):
    pivot = data[high]
    i = low - 1
    states = []
    for j in range(low, high):
        stats['comparisons'] += 1
        # Show comparison
        states.append((data[:], ['yellow' if x == i or x == j else 'red' for x in range(len(data))], stats.copy()))
        if (data[j] <= pivot) if ascending else (data[j] >= pivot):
            i += 1
            data[i], data[j] = data[j], data[i]
            stats['swaps'] += 1
            # Show swap
            states.append((data[:], ['blue' if x == i or x == j else 'red' for x in range(len(data))], stats.copy()))
    data[i + 1], data[high] = data[high], data[i + 1]
    stats['swaps'] += 1
    states.append((data[:], ['blue' if x == i + 1 or x == high else 'red' for x in range(len(data))], stats.copy()))
    return i + 1, states

def heap_sort(data, ascending=True):
    stats = {'comparisons': 0, 'swaps': 0}
    n = len(data)
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(data, n, i, ascending, stats)
    for i in range(n - 1, 0, -1):
        # Show swap
        yield data[:], ['blue' if x == i or x == 0 else 'red' for x in range(len(data))], stats.copy()
        data[i], data[0] = data[0], data[i]
        stats['swaps'] += 1
        yield from heapify(data, i, 0, ascending, stats)
    yield data[:], ['green' for _ in range(len(data))], stats.copy()

def heapify(data, n, i, ascending, stats):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n:
        stats['comparisons'] += 1
        # Show comparison
        yield data[:], ['yellow' if x == i or x == left else 'red' for x in range(len(data))], stats.copy()
        if (data[left] > data[largest]) if ascending else (data[left] < data[largest]):
            largest = left
    if right < n:
        stats['comparisons'] += 1
        # Show comparison
        yield data[:], ['yellow' if x == i or x == right else 'red' for x in range(len(data))], stats.copy()
        if (data[right] > data[largest]) if ascending else (data[right] < data[largest]):
            largest = right
    if largest != i:
        # Show swap
        yield data[:], ['blue' if x == i or x == largest else 'red' for x in range(len(data))], stats.copy()
        data[i], data[largest] = data[largest], data[i]
        stats['swaps'] += 1
        yield from heapify(data, n, largest, ascending, stats)

# --- Visualization ---
def draw_data(data, color_array):
    df = pd.DataFrame({
        'index': list(range(len(data))),
        'value': data,
        'color': [color_map.get(c, '#e74c3c') for c in color_array]
    })
    chart = alt.Chart(df).mark_bar(
        cornerRadiusTopLeft=5,
        cornerRadiusTopRight=5,
        stroke='black',
        strokeWidth=0.5
    ).encode(
        x=alt.X('index:O', title='', axis=alt.Axis(labelFontSize=14, title=None, ticks=False, domain=False)),
        y=alt.Y('value:Q', title='', axis=alt.Axis(labelFontSize=14, title=None, ticks=False, domain=False)),
        color=alt.Color('color:N', scale=None, legend=None),
        tooltip=['index', 'value']
    ).properties(
        width=1600,
        height=500
    )
    text = alt.Chart(df).mark_text(
        align='center',
        baseline='bottom',
        dy=-5,
        color='white',
        fontSize=12
    ).encode(
        x='index:O',
        y='value:Q',
        text='value:Q'
    )
    layered = alt.layer(chart, text).properties(
        width=1600,
        height=500,
        background='#181818'
    )
    st.altair_chart(layered, use_container_width=True)

# --- Show Code Expander ---
def get_algo_code(algo_name):
    import inspect
    func_map = {
        'Bubble Sort': bubble_sort,
        'Insertion Sort': insertion_sort,
        'Selection Sort': selection_sort,
        'Merge Sort': merge_sort,
        'Quick Sort': quick_sort,
        'Heap Sort': heap_sort
    }
    return dedent(inspect.getsource(func_map[algo_name]))

# --- C++ Code for Algorithms ---
def get_cpp_code(algo_name):
    cpp_codes = {
        'Bubble Sort': '''
void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n-1; i++) {
        for (int j = 0; j < n-i-1; j++) {
            if (arr[j] > arr[j+1]) {
                std::swap(arr[j], arr[j+1]);
            }
        }
    }
}
''',
        'Insertion Sort': '''
void insertionSort(int arr[], int n) {
    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }
}
''',
        'Selection Sort': '''
void selectionSort(int arr[], int n) {
    for (int i = 0; i < n-1; i++) {
        int min_idx = i;
        for (int j = i+1; j < n; j++) {
            if (arr[j] < arr[min_idx])
                min_idx = j;
        }
        std::swap(arr[min_idx], arr[i]);
    }
}
''',
        'Merge Sort': '''
void merge(int arr[], int l, int m, int r) {
    int n1 = m - l + 1;
    int n2 = r - m;
    int L[n1], R[n2];
    for (int i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (int j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];
    int i = 0, j = 0, k = l;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }
    while (i < n1) {
        arr[k] = L[i];
        i++; k++;
    }
    while (j < n2) {
        arr[k] = R[j];
        j++; k++;
    }
}
void mergeSort(int arr[], int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}
''',
        'Quick Sort': '''
int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = (low - 1);
    for (int j = low; j <= high - 1; j++) {
        if (arr[j] < pivot) {
            i++;
            std::swap(arr[i], arr[j]);
        }
    }
    std::swap(arr[i + 1], arr[high]);
    return (i + 1);
}
void quickSort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}
''',
        'Heap Sort': '''
void heapify(int arr[], int n, int i) {
    int largest = i;
    int l = 2 * i + 1;
    int r = 2 * i + 2;
    if (l < n && arr[l] > arr[largest])
        largest = l;
    if (r < n && arr[r] > arr[largest])
        largest = r;
    if (largest != i) {
        std::swap(arr[i], arr[largest]);
        heapify(arr, n, largest);
    }
}
void heapSort(int arr[], int n) {
    for (int i = n / 2 - 1; i >= 0; i--)
        heapify(arr, n, i);
    for (int i = n - 1; i > 0; i--) {
        std::swap(arr[0], arr[i]);
        heapify(arr, i, 0);
    }
}
''',
    }
    return cpp_codes.get(algo_name, "Not available.")

# --- Step-by-step Mode ---
step_mode = st.toggle("Step-by-step Mode", value=False)
if step_mode:
    if 'step' not in st.session_state:
        st.session_state['step'] = 0
    step = st.session_state['step']
else:
    st.session_state['step'] = 0

# --- Sorting ---
start_sort = st.button("Start Sorting", disabled=st.session_state.get('sorting', False))
progress_bar = st.progress(0.0, text="Sorting Progress")
stats_placeholder = st.empty()

if start_sort and not step_mode:
    st.session_state['sorting'] = True
    arr = array[:]
    ascending = (order == "Ascending")
    algo_map = {
        'Bubble Sort': bubble_sort,
        'Insertion Sort': insertion_sort,
        'Selection Sort': selection_sort,
        'Merge Sort': merge_sort,
        'Quick Sort': quick_sort,
        'Heap Sort': heap_sort
    }
    sort_gen = algo_map[algorithm](arr, ascending)
    steps = list(sort_gen)
    total_steps = len(steps)
    for i, (data, color_array, stats) in enumerate(steps):
        draw_data(data, color_array)
        progress_bar.progress((i+1)/total_steps, text=f"Step {i+1}/{total_steps}")
        stats_placeholder.info(f"Comparisons: {stats['comparisons']} | Swaps: {stats['swaps']}")
        time.sleep(0.05)  # 50ms for smooth animation
    st.session_state['array'] = arr
    st.session_state['sorting'] = False
elif step_mode:
    arr = array[:]
    ascending = (order == "Ascending")
    algo_map = {
        'Bubble Sort': bubble_sort,
        'Insertion Sort': insertion_sort,
        'Selection Sort': selection_sort,
        'Merge Sort': merge_sort,
        'Quick Sort': quick_sort,
        'Heap Sort': heap_sort
    }
    sort_gen = algo_map[algorithm](arr, ascending)
    steps = list(sort_gen)
    total_steps = len(steps)
    step = st.session_state['step']
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Previous Step"):
            step = max(step - 1, 1)
            st.session_state['step'] = step
    with col2:
        if st.button("Next Step"):
            step = min(step + 1, total_steps)
            st.session_state['step'] = step
    if step == 0:
        step = 1
    data, color_array, stats = steps[step - 1]
    draw_data(data, color_array)
    progress_bar.progress(step/total_steps, text=f"Step {step}/{total_steps}")
    stats_placeholder.info(f"Comparisons: {stats['comparisons']} | Swaps: {stats['swaps']}")
else:
    draw_data(array, ['red' for _ in range(len(array))])
    progress_bar.progress(0.0, text="Ready to sort!")
    stats_placeholder.info("Comparisons: 0 | Swaps: 0")

# --- Show Code Expander ---
with st.expander("Show Python Code for this Algorithm"):
    st.code(get_algo_code(algorithm), language="python")

with st.expander("Show C++ Code for this Algorithm"):
    st.code(get_cpp_code(algorithm), language="cpp")

# --- Footer ---
st.markdown("---")
st.markdown("<div style='text-align:center; font-size:18px;'><b>Made by Hardik Sharma</b></div>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align:center;'>
        <a href='https://github.com/hardiksharma0511' target='_blank'>GitHub Account</a> |
        <a href='https://github.com/hardiksharma0511/Sorting_Visualizer' target='_blank'>Repository Link</a> |
        <a href='https://www.linkedin.com/in/hardiksharma05' target='_blank'>LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True
)
