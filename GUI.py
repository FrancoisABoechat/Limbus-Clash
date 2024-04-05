import tkinter as tk
from Clash import *

def process_inputs():
    inputs = [entry.get() for entry in entry_boxes]
    if all(str.isdigit(ele) for ele in inputs):
        inputs = list(map(int, inputs))
        clash_calculator_old = ClashOld(inputs[:5],inputs[5:])
        clash_calculator_new = ClashNew(inputs[:5],inputs[5:])
        old_clash = clash_calculator_old.Clash_old()
        old_clash_text = clash_calculator_old._winrate_text(old_clash)
        actual_clash = clash_calculator_new.Clash_new()
        actual_clash_text = clash_calculator_new._winrate_text(actual_clash)
        output_label1.config(text=f"Old Clash Value: {str(old_clash)}, {old_clash_text}")
        output_label2.config(text=f"Actual Clash Value: {str(actual_clash)}, {actual_clash_text}")
    else:
        output_label1.config(text="Invalid entries")
        output_label2.config(text="Invalid entries")

def main():
    global entry_boxes
    global output_label1
    global output_label2

    # Create the main window
    root = tk.Tk()
    root.title("Clash calculator")
    labels = ["Base Power", "Coin Power", "Coin amount", "Sanity", "Level"]
    # Create entry boxes for inputs
    entry_boxes = []
    label = tk.Label(root, text="Sinner")
    label.grid(row=0, column=1, padx=5, pady=5)
    label = tk.Label(root, text="Enemy")
    label.grid(row=0, column=3, padx=5, pady=5)
    for i in range(10):
        if int(i/5) < 1:
            label = tk.Label(root, text=labels[i])
            label.grid(row=i+1, column=0, padx=5, pady=5)
            entry = tk.Entry(root)
            entry.grid(row=i+1, column=1, padx=5, pady=5)
            entry_boxes.append(entry)
        else:
            label = tk.Label(root, text=labels[i-5])
            label.grid(row=i-4, column=2, padx=5, pady=5)
            entry = tk.Entry(root)
            entry.grid(row=i-4, column=3, padx=5, pady=5)
            entry_boxes.append(entry)

    # Create button to process inputs
    process_button = tk.Button(root, text="Process Inputs", command=process_inputs)
    process_button.grid(row=8, columnspan=4, padx=5, pady=10)

    # Create label to display output
    output_label1 = tk.Label(root, text="Old Clash Value")
    output_label1.grid(row=9, column=1, padx=5, pady=5)
    output_label2 = tk.Label(root, text="Actual Clash Value")
    output_label2.grid(row=9, column=2, padx=5, pady=5)

    # Run the GUI
    root.mainloop()

if __name__ == "__main__":
    main()