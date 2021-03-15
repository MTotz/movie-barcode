import tkinter as tk

from movie_barcode import barcode

window = tk.Tk()
window.title("Movie Barcode")

lbl_header = tk.Label(window, text="Movie Barcode")
lbl_header.config(font=("Courier", 44))
lbl_header.grid(row=1, column=1, columnspan=6, sticky=tk.W+tk.E)

txt_subheader = tk.Label(
    window, text="Create a barcode out of your favorite video!")
txt_subheader.config(font=("Courier", 25))
txt_subheader.grid(row=2, column=1, pady=(10, 50),
                   columnspan=6, sticky=tk.W+tk.E)


# type
lbl_type = tk.Label(window, text="Choose method:")
lbl_type.grid(row=4, column=1)

rad_squeeze = tk.Radiobutton(window, text="Squeezed")
rad_squeeze.grid(row=5, column=1)

rad_average = tk.Radiobutton(window, text="Averaged")
rad_average.grid(row=6, column=1)

# n frames
lbl_frames1 = tk.Label(window, text="Take every")
lbl_frames1.grid(row=4, column=2, sticky="e")

ent_average = tk.Entry(window, width=3, relief=tk.GROOVE)
ent_average.grid(row=4, column=3)

lbl_frames2 = tk.Label(window, text="th frames")
lbl_frames2.grid(row=4, column=4, sticky="w")

lbl_or = tk.Label(window, text="OR")
lbl_or.grid(row=5, column=3, pady=10)

# n seconds
lbl_seconds1 = tk.Label(window, text="Take one frame every")
lbl_seconds1.grid(row=6, column=2, sticky="e")

ent_seconds1 = tk.Entry(window, width=3, relief=tk.GROOVE)
ent_seconds1.grid(row=6, column=3)

lbl_seconds2 = tk.Label(window, text=" seconds")
lbl_seconds2.grid(row=6, column=4, sticky="w")

# stop
lbl_stop = tk.Label(window, text="Stop at")
lbl_stop.grid(row=4, column=5, sticky="e")

ent_stop = tk.Entry(window, width=3, relief=tk.GROOVE)
ent_stop.grid(row=4, column=6, sticky="w")

# create button
btn_create = tk.Button(window, text="Create Barcode")
btn_create.grid(row=7, column=1, columnspan=6, pady=50, bg="gray")

tk.mainloop()
