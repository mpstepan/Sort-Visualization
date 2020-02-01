from tkinter import *
from random import randint
import time


class View:
    def __init__(self, w=1000, h=600, num_boxes=200):
        self.window = Tk()
        self.window.title("Sorting Visualizer")

        # creates the canvas and sets it inside of the window
        self.canvas = Canvas(self.window, width=w, height=h)
        self.canvas.pack()
        self.canvas.focus_set()

        # stores the ids of the rectangles in an array; stores the heights of the rectangles in another array
        self.rectangles = [None for x in range(num_boxes)]
        self.height_arr = [0 for x in range(num_boxes)]

        self.num_boxes = num_boxes

        # scramble button
        self.scramble_button = Button(self.window, text="Scramble", command=self.scramble)
        self.scramble_button_id = self.canvas.create_window(50, 25, window=self.scramble_button)

        # selection sort button
        self.select_sort_button = Button(self.window, text="Selection Sort", command=self.selection_sort)
        self.select_sort_id = self.canvas.create_window(150, 25, window=self.select_sort_button)

        # insertion sort button
        self.insert_sort_button = Button(self.window, text="Insertion Sort", command=self.insertion_sort)
        self.insert_sort_id = self.canvas.create_window(250, 25, window=self.insert_sort_button)

        # merge sort button
        self.merge_sort_button = Button(self.window, text="Merge Sort", command=self.merge_sort)
        self.merge_sort_id = self.canvas.create_window(350, 25, window=self.merge_sort_button)

        # quick sort button
        self.quick_sort_button = Button(self.window, text="Quick Sort", command=self.quick_sort)
        self.quick_sort_id = self.canvas.create_window(450, 25, window=self.quick_sort_button)

        # calculates the difference in color each box must be to go from blue (shortest) to red (tallest)
        self.step = int((0xFF0000 - 0x0000FF) / num_boxes)

        # makes the desired number of rectangles
        box_width = (w / self.num_boxes)
        for x in range(self.num_boxes):
            diff = 2 * (x + 1) + 90

            # 4 coordinates - bottom left(x0, y0) and top right (x1, y1)
            pos = x * box_width, h, (x + 1) * box_width, h - diff

            # generates a color based on the
            color = "#" + format(self.step * x % 0xFFFFFF, "06x")
            self.rectangles[x] = self.canvas.create_rectangle(pos, fill=color)
            self.height_arr[x] = diff

    # disables the buttons - used when algorithms are running
    def disable_buttons(self):
        self.scramble_button.config(state="disabled")
        self.select_sort_button.config(state="disabled")
        self.insert_sort_button.config(state="disabled")
        self.merge_sort_button.config(state="disabled")
        self.quick_sort_button.config(state="disabled")

    # re-enables the buttons - used when algorithms
    def enable_buttons(self):
        self.scramble_button.config(state="active")
        self.select_sort_button.config(state="active")
        self.insert_sort_button.config(state="active")
        self.merge_sort_button.config(state="active")
        self.quick_sort_button.config(state="active")

    def scramble(self):

        self.disable_buttons()
        for i in range(self.num_boxes - 1, 0, -1):

            # Pick a random index from 0 to i
            j = randint(0, i + 1)

            # Swap arr[i] with the element at random index
            self.height_arr[i], self.height_arr[j] = self.height_arr[j], self.height_arr[i]
            self.update_screen()

        self.enable_buttons()

    # ensures that all the rectangles are correct height; if not, updates the height and updates the view
    # small wait time just to make it more visible to the eye
    def update_screen(self):

        for x in range(self.num_boxes):
            h = self.height_arr[x]
            box = self.rectangles[x]

            # top left and bottom right points - need to keep x's
            x0, y0, x1, y1 = self.canvas.coords(box)

            if h != abs(y1 - y0):
                self.canvas.itemconfig(box, fill="#" + format(self.step * int((h - 90) / 2 - 1) % 0xFFFFFF, "06x"))
                self.canvas.coords(box, x0, y1, x1, y1 - h)
                self.canvas.update()
                self.canvas.update_idletasks()

    # working selection sort
    def selection_sort(self):

        # disables all the buttons while the sorting is in progress
        self.disable_buttons()

        l_len = self.num_boxes
        for i in range(l_len):

            max_ind = -1
            max_height = -1

            # finds the index of the largest bar
            for j in range(l_len-i):
                h = self.height_arr[j]

                # updates largest
                if h > max_height:
                    max_height = h
                    max_ind = j

            # swaps the greatest found height to the end of the list
            self.height_arr[max_ind], self.height_arr[l_len - i - 1] = \
                self.height_arr[l_len - i - 1], self.height_arr[max_ind]

            # updates the screen
            self.update_screen()
            time.sleep(0.05)

        # enables the buttons after the sorting has finished
        self.enable_buttons()

    # working insertion sort!
    def insertion_sort(self):

        self.disable_buttons()
        l_len = self.num_boxes

        # start looping from the second element
        for i in range(1, l_len):
            height1 = self.height_arr[i]

            ctr = i-1
            while ctr >= 0:
                height2 = self.height_arr[ctr]

                if height2 > height1:
                    self.height_arr[ctr], self.height_arr[ctr+1] = self.height_arr[ctr+1], self.height_arr[ctr]

                ctr -= 1

            self.update_screen()
            time.sleep(0.005)

        self.enable_buttons()

    # working merge sort - visualizer
    def merge_sort(self):
        self.disable_buttons()
        self.merge_sort_helper(self.height_arr, 0)
        self.enable_buttons()

    # recursive helper for merge sort, which does the actual sorting
    def merge_sort_helper(self, arr, start_loc):

        l_len = len(arr)

        if l_len > 1:
            mid = int(l_len / 2)
            left = arr[:mid]
            right = arr[mid:]
            self.merge_sort_helper(left, start_loc)
            self.merge_sort_helper(right, start_loc + mid)

            i = j = k = 0

            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    arr[k] = left[i]
                    i += 1
                else:
                    arr[k] = right[j]
                    j += 1
                k += 1
                self.canvas.update()
                self.canvas.update_idletasks()

            while i < len(left):
                arr[k] = left[i]
                i += 1
                k += 1
                self.canvas.update()
                self.canvas.update_idletasks()

            while j < len(right):
                arr[k] = right[j]
                j += 1
                k += 1
                self.canvas.update()
                self.canvas.update_idletasks()

            for x in range(start_loc, start_loc + len(arr), 1):
                self.height_arr[x] = arr[x - start_loc]
            self.update_screen()
            time.sleep(0.025)

    # method attached to button that gets called when the quick sort button is pressed
    def quick_sort(self):
        self.disable_buttons()
        self.quick_sort_helper(0, len(self.height_arr)-1)
        self.enable_buttons()

    # recursive function that calls the helper partition function
    def quick_sort_helper(self, low, high):
        if low < high:
            part_ind = self.partition(low, high)

            self.quick_sort_helper(low, part_ind-1)
            self.quick_sort_helper(part_ind+1, high)

    # everything below the partition is smaller, and everything above is greater
    def partition(self, low, high):
        i = low - 1
        pivot = self.height_arr[high]

        for j in range(low, high):
            if self.height_arr[j] < pivot:
                i = i + 1
                self.height_arr[i], self.height_arr[j] = self.height_arr[j], self.height_arr[i]
                self.update_screen()
                time.sleep(0.005)

        self.height_arr[i + 1], self.height_arr[high] = self.height_arr[high], self.height_arr[i + 1]
        self.update_screen()
        time.sleep(0.005)
        return i + 1




def main():
    view = View()
    view.window.mainloop()


if __name__ == '__main__':
    main()
