import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from tkinter import scrolledtext
import math
import random
import sympy

# standard initialization of the graphics
master = tk.Tk()
master.title("RSA")
master.geometry("350x750")

# requirements from of the assignment
binary_length = 10
block_length = 7


# method for generating the keys
def GenerateKeys():

    p = 0
    q = 0

    while p == q:
        p = sympy.randprime(1000000000000000, 9999999999999999)
        q = sympy.randprime(1000000000000000, 9999999999999999)

    n = p * q

    entry_n.delete(0, "end")
    entry_n.insert(0, n)

    pn = (p - 1) * (q - 1)

    r = 0
    while r != 1:
        e = random.randint(1, pn)
        r = math.gcd(e, pn)

    entry_e.delete(0, "end")
    entry_e.insert(0, e)

    d = pow(e, -1, pn)

    entry_d.delete(0, "end")
    entry_d.insert(0, d)


# method for encrypting the text
def encrypt():

    global binary_length, block_length

    e = entry_e.get()
    n = entry_n.get()

    if  n == "" or e == "":
        tk.messagebox.showerror(title=None, message="one or more of the key values are empty")
    else:
        try:
            e = int(e)
            n = int(n)

            text = txt_enter.get("1.0", "end")

            str_index = 0;
            end_index = 7;

            txt_CT.delete("1.0", "end")

            # going through the text, getting a part of it, encrypting it and getting the next part
            for h in range(math.ceil(len(text) / 7)):

                # check for making sure no out of bounds index errors may occur
                # getting the selected part of the string
                if end_index <= len(text) and str_index != end_index:
                    block = text[str_index:end_index]
                elif end_index > len(text) and str_index != end_index:
                    block = text[str_index:-1]
                elif str_index == end_index:
                    block = text[str_index]

                # the test block will be worked on inside this array
                block_array = ["0" for i in range(block_length)]

                # if the length of the selected text is less than the assignment requirements *7, fill the rest with " "
                missing = block_length - len(block)
                add = " " * missing
                block += add

                # encrypting the text section by section
                for i in range(len(block_array)):

                    # get the text
                    block_array[i] = block[i]

                    # change text to int
                    block_array[i] = ord(block_array[i])

                    # change int to binary
                    block_array[i] = format(block_array[i], "b")

                    # if the length of the binary is less than the assignment requirement *10, fill the missing with 0
                    binary_array = ["0" for i in range(binary_length)]
                    for j in range(len(block_array[i])):
                        binary_array[-j - 1] = block_array[i][-j - 1]

                    block_array[i] = "".join(binary_array)

                binary_result = "".join(block_array)
                decimal_result = int(binary_result, 2)

                # the actual encrypting
                CT_result = pow(decimal_result, e, n)

                txt_CT.insert("end", f"{CT_result}\n")

                # incrementing the indexes to select the next part of the text
                str_index += 7
                end_index += 7

        except:
            tk.messagebox.showerror(title=None, message="the key values can only be an integer")


def decrypt():

    global binary_length, block_length

    d = entry_d.get()
    n = entry_n.get()

    if d == "" or n == "":
        tk.messagebox.showerror(title=None, message="one or more of the key values are empty")
    else:
        try:

            d = int(d)
            n = int(n)

            # getting the text and splitting each line to make array
            txt_OT.delete("1.0", "end")
            text = txt_CT.get("1.0", "end").split()

            # going through each CT line and decrypting them one by one
            for i in range(len(text)):

                # the actual decryption
                decimal_result = pow(int(text[i]), d, n)
                binary_result = format(decimal_result, "b")

                # filling in the 0(s) from the last binary part of the long binary
                missing = block_length * binary_length - len(binary_result)
                binary_result = missing * "0" + binary_result

                # for going through each section of the long binary
                str_index = 0
                end_index = 10

                # decoding the selected binary part into a character
                for j in range(int(len(binary_result) / binary_length)):
                    block = binary_result[str_index:end_index]

                    # for incrementing to the next section
                    str_index += binary_length
                    end_index += binary_length

                    if block[j] == "":
                        break

                    # binary to int then to character
                    block_int = int(block, 2)
                    block_char = chr(block_int)

                    # putting each of the characters one by one
                    txt_OT.insert("end", f"{block_char}")

        except:
            tk.messagebox.showerror(title=None, message="the key values and CT can only be an integer")








#    str01 = entry_str.get("1.0", "end")

#    print(str01)
#    str03 = str(str01)
#    str02 = ["0" for i in range(len(str01))]
#
#    for i in range(len(str02)):
#        str02[i] = str01[i]
#
#    str04 = ""
#
#    str04 += "".join(str02)
#    print(str04)
#    print(str03)

 #   entry_str01.insert("end", f"{str01}")

#btn_text = tk.Button(master, text = "do it", command = GenerateKeys)
#btn_text.grid(row = 2, column = 0)
#
#entry_str = tk.Text(master, width = 40, height=8)
#entry_str.grid(row=0, column = 0, padx = 3, pady = 3)
#
#entry_str01 = tk.Text(master, width = 40)
#entry_str01.grid(row=1, column = 0, padx = 3, pady = 3)
#
#text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD,
#                                      width=40, height=8,
#                                      font=("Times New Roman", 15))
#
#text_area.grid(column=0, row=2, pady=3, padx=3)


# the design section
txt_enter = tk.Text(master, width = 40, height = 8)
txt_enter.grid(row = 0, column = 0, columnspan = 2 ,padx = 7, pady = 7)
lbl_break_01 = tk.Label(master, text = "-----------------------------------------------------------").grid(row = 1, column = 0, columnspan = 2)

btn_generateKeys = tk.Button(master, text = "generate Keys", command = GenerateKeys).grid(row = 2, columnspan = 2, column = 0)

lbl_n = tk.Label(master, text = "n :").grid(row = 3, column = 0, pady = 10)
entry_n = tk.Entry(master, width = 40)
entry_n.grid(row = 3, column = 1, pady = 10)

lbl_d = tk.Label(master, text = "d :").grid(row = 4, column = 0, pady = 10)
entry_d = tk.Entry(master, width = 40)
entry_d.grid(row = 4, column = 1, pady = 10)

lbl_e = tk.Label(master, text = "e :").grid(row = 5, column = 0, pady = 10)
entry_e = tk.Entry(master, width = 40)
entry_e.grid(row = 5, column = 1, pady = 10)

lbl_break_02 = tk.Label(master, text = "-----------------------------------------------------------").grid(row = 7, column = 0, columnspan = 2)

btn_encrypt = tk.Button(master, text = "encode text", command = encrypt).grid(row = 6, columnspan = 2, column = 0)
txt_CT = tk.Text(master, width = 40, height = 8)
txt_CT.grid(row = 8, column = 0, columnspan = 2 ,padx = 10, pady = 10)

lbl_break_03 = tk.Label(master, text = "-----------------------------------------------------------").grid(row = 10, column = 0, columnspan = 2)

btn_decrypt = tk.Button(master, text = "decode Cipher text", command = decrypt).grid(row = 9, columnspan = 2, column = 0)
txt_OT = tk.Text(master, width = 40, height = 8)
txt_OT.grid(row = 11, column = 0, columnspan = 2 ,padx = 10, pady = 10)

master.mainloop()