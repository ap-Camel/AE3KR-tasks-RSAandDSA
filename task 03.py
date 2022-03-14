from tkinter import *
from tkinter import filedialog
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from tkinter import scrolledtext

import hashlib
import os

import math
import random
import sympy
import pathlib

master = tk.Tk()
master.title("RSA")
master.geometry("460x900")


binary_length = 10
block_length = 7


# function for getting the data from device
def brows_data_file():
    master.filename = filedialog.askopenfilename(initialdir=r"/",
                                                 title="select a file",
                                                 filetypes=(("all files", "*.*") ,("text files", "*.txt")))
    source = master.filename
    entry_source_data.insert(0, source)
    with open(source) as file:
        content = file.read()
        txt_file_content.config(state = "normal")
        txt_file_content.delete("1.0", "end")
        txt_file_content.insert("end", content)
        txt_file_content.config(state = "disabled")
        entry_file_name.config(state = "normal")
        entry_file_name.delete(0, "end")
        entry_file_name.insert("end", pathlib.Path(source).name)
        entry_file_name.config(state = 'readonly')
        entry_file_type.config(state = "normal")
        entry_file_type.delete(0, "end")
        entry_file_type.insert("end", pathlib.Path(source).suffix)
        entry_file_type.config(state = 'readonly')
        entry_file_size.config(state = "normal")
        entry_file_size.delete(0, "end")
        entry_file_size.insert("end", f"{pathlib.Path(source).stat().st_size}Kb")
        entry_file_size.config(state = 'readonly')



# function for generating the keys if user does not have their own keys to save
def generate_keys():
    p = 0
    q = 0

    while p == q:
        p = sympy.randprime(1000000000000000, 9999999999999999)
        q = sympy.randprime(1000000000000000, 9999999999999999)

    n = p * q

    pn = (p - 1) * (q - 1)

    r = 0
    while r != 1:
        e = random.randint(1, pn)
        r = math.gcd(e, pn)

    d = pow(e, -1, pn)

    entry_n.delete(0, "end")
    entry_n.insert(0, n)

    entry_e.delete(0, "end")
    entry_e.insert(0, e)

    entry_d.delete(0, "end")
    entry_d.insert(0, d)


# saving the keys entered or generated
def save_keys():

    n = entry_n.get()
    e = entry_e.get()
    d = entry_d.get()

    if n == "" or e == "" or d == "":
        tk.messagebox.showerror(title = None, message = "one or more of the key values are empty")
        tk.messagebox.showinfo(title = None, message = "the file was not saved")
    else:
        try:
            n = int(n)
            e = int(e)
            d = int(d)

            with open("public.pub", 'w') as public_key:
                public_key.write(f"{d}\n{n}")

            with open("private.priv", 'w') as private_key:
                private_key.write(f"{e}\n{n}")

            tk.messagebox.showinfo(title=None, message="the keys were saved")

        except:
            tk.messagebox.showerror(title=None, message="the key values can only be an integer")
            tk.messagebox.showinfo(title=None, message="the file was not saved")



# generating the hash
def generate_hash():
    content = txt_file_content.get("1.0", "end")

    if content == "":
        tk.messagebox.showerror(title=None, message="a file was note chosen or is empty")
    else:
        access = hashlib.new("sha3_512", content.encode())
        hash = access.hexdigest()

        entry_hash.config(state = "normal")
        entry_hash.delete(0, "end")
        entry_hash.insert(0, hash)
        entry_hash.config(state = "readonly")


# encrypting and saving the hash as a sign file
def signuture_file():

    hash = entry_hash.get()

    n = entry_n.get()
    e = entry_e.get()
    d = entry_d.get()

    if hash == "":
        tk.messagebox.showerror(title=None, message="generate hash first")
        tk.messagebox.showinfo(title=None, message="the file was not saved")
    elif n == "" or e == "" or d == "":
        tk.messagebox.showerror(title=None, message="one or more of the key values are empty")
        tk.messagebox.showinfo(title=None, message="the file was not saved")
    else:
        n = int(n)
        e = int(e)
        d = int(d)

        entry_hash.config(state = "normal")
        text = entry_hash.get()
        entry_hash.config(state = "readonly")

        str_index = 0;
        end_index = 7;

        final_result = ""

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

            print(decimal_result)

            # the actual encrypting
            CT_result = pow(decimal_result, e, n)

            final_result += f"{CT_result}\n"
            # incrementing the indexes to select the next part of the text
            str_index += 7
            end_index += 7

        with open("sign.sign", 'w') as sign_file:
                sign_file.write(f"{final_result}")
                script_dir = os.path.dirname(__file__)
                rel_path = "sign.sign"
                abs_file_path = os.path.join(script_dir, rel_path)
                entry_sign_location.insert(0, abs_file_path)

        tk.messagebox.showinfo(title=None, message="the file was saved")


# function for browsing the data that will be verified
def brows_data_verify():
    master.filename = filedialog.askopenfilename(initialdir=r"/",
                                                 title="select a file",
                                                 filetypes=(("all files", "*.*"), ("text files", "*.txt")))
    source = master.filename
    entry_data_location_verification.delete(0, "end")
    entry_data_location_verification.insert(0, source)
    with open(source) as file:
        content = file.read()
        txt_file_content_verify.config(state = "normal")
        txt_file_content_verify.delete("1.0", "end")
        txt_file_content_verify.insert("end", content)
        txt_file_content_verify.config(state = "disabled")



# function for browsing the sign file
def brows_sign_verify():
    master.filename = filedialog.askopenfilename(initialdir=r"/",
                                                 title="select a file",
                                                 filetypes=(("all files", "*.*"), ("text files", "*.txt")))
    source = master.filename

    if source.lower().endswith((".sign")):
        entry_brows_sign_location.delete(0, "end")
        entry_brows_sign_location.insert(0, source)
        with open(source) as file:
            content = file.read()
            txt_sign_file_content.config(state="normal")
            txt_sign_file_content.delete("1.0", "end")
            txt_sign_file_content.insert("end", content)
            txt_sign_file_content.config(state="disabled")
    else:
        tk.messagebox.showerror(title=None, message="please choose a sign file")


# function for browsing the public key used for verification
def brows_keys():
    master.filename = filedialog.askopenfilename(initialdir=r"/",
                                                 title="select a file",
                                                 filetypes=(("all files", "*.*"), ("text files", "*.txt")))
    source = master.filename
    if source.lower().endswith((".pub")):
        with open(source) as public_key:
            txt_public_key.config(state = "normal")
            txt_public_key.delete("1.0", "end")
            txt_public_key.insert("1.0", public_key.read())
            txt_public_key.config(state = "disabled")
    else:
        tk.messagebox.showerror(title=None, message="please choose a key file")



# function for decrypting the hash and comparing the two for verification
def verify():

    txt_file_content_verify.config(state = "normal")
    content = txt_file_content_verify.get("1.0", "end")
    txt_file_content_verify.config(state = "disabled")
    txt_sign_file_content.config(state = "normal")
    sign = txt_sign_file_content.get("1.0", "end")
    txt_sign_file_content.config(state = "disabled")
    txt_public_key.config(state = "normal")
    public_key = txt_public_key.get("1.0", "end").split()
    txt_public_key.config(state = "disabled")

    if len(content) == 1 and content[0] == "\n":
        tk.messagebox.showerror(title=None, message="please choose a content file")
    elif len(sign) == 1 and sign[0] == "\n":
        tk.messagebox.showerror(title=None, message="please choose a sign file")
    elif len(public_key) == 1 and sign[0] == "\n":
        tk.messagebox.showerror(title=None, message="please choose a key file")
    else:
        try:
            d = public_key[0]
            print(f"d is : {d}")
            n = public_key[1]
            print(f"n is : {n}")

            e = entry_e.get()



            d = int(d)
            n = int(n)
            #e = int(e)
            print(sign)
            # getting the text and splitting each line to make array
            text = sign.split()
            final_result = ""

            print(text)
            print(text[0])
            # going through each CT line and decrypting them one by one
            for i in range(len(text)):

                # the actual decryption
                decimal_result = pow(int(text[i]), d, n)
                print(decimal_result)
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

                    final_result += block_char

            access = hashlib.new("sha3_512", content.encode())
            hash = access.hexdigest()

            entry_sign_hash.insert(0, f"{final_result}")
            entry_data_hash.insert(0, hash)

            if hash.strip()[0:-1] == final_result.strip():
                lbl_verification.config(text = "they match")
            else:
                lbl_verification.config(text = "they do not match")

        except:
            tk.messagebox.showerror(title=None, message="the key values can only be an integer")





# the style section
btn_brows_data = tk.Button(master, text = "brows", width = 10, command = brows_data_file).grid(row = 0, column = 0, padx = 10, pady = 5)
entry_source_data = tk.Entry(master, width = 50, highlightbackground = "Blue", highlightcolor = "blue", highlightthickness = 2)
entry_source_data.grid(row = 0, column = 1, columnspan = 3)

lbl_file_name = tk.Label(master, text = "file name: ", width = 10).grid(row = 1, column = 0, padx = 5, pady = 5)
entry_file_name = tk.Entry(master, width = 20)
entry_file_name.grid(row = 1, column = 1, padx = 5, pady = 5)

lbl_file_type = tk.Label(master, text = "file type: ", width = 10).grid(row = 1, column = 2, padx = 5, pady = 5)
entry_file_type = tk.Entry(master, width = 20)
entry_file_type.grid(row = 1, column = 3, padx = 5, pady = 5)

lbl_file_size = tk.Label(master, text = "file size: ", width = 10).grid(row = 2, column = 2, padx = 5, pady = 5)
entry_file_size = tk.Entry(master, width = 20)
entry_file_size.grid(row = 2, column = 3, padx = 5, pady = 5)

txt_file_content = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=50, height=4, font=("Times New Roman", 12))
txt_file_content.grid(row = 3, column = 0, columnspan = 4, padx = 10, pady = 5)

lbl_break_01 = tk.Label(master, text = "-----------------------------------------------------------------------------").grid(row = 4, column = 0, columnspan = 4)

btn_generate_keys = Button(master, text = "generate keys", width = 15, command = generate_keys).grid(row = 5, column = 0, columnspan = 2, padx = 10, pady = 3)
btn_save_keys = Button(master, text = "save keys", width = 15, command = save_keys).grid(row = 5, column = 2, columnspan = 2, padx = 10, pady = 3)

lbl_n = tk.Label(master, text = "n :", width = 10).grid(row = 6, column = 0, pady = 3)
entry_n = tk.Entry(master, width = 40)
entry_n.grid(row = 6, column = 1, pady = 3, padx = 5, columnspan = 3)

lbl_d = tk.Label(master, text = "d :", width = 10).grid(row = 7, column = 0, pady = 3)
entry_d = tk.Entry(master, width = 40)
entry_d.grid(row = 7, column = 1, pady = 3, padx = 5, columnspan = 3)

lbl_e = tk.Label(master, text = "e :", width = 10).grid(row = 8, column = 0, pady = 3)
entry_e = tk.Entry(master, width = 40)
entry_e.grid(row = 8, column = 1, pady = 3, padx = 5, columnspan = 3)

lbl_break_02 = tk.Label(master, text = "-----------------------------------------------------------------------------").grid(row = 9, column = 0, columnspan = 4)

btn_generate_hash = tk.Button(master, text = "generate hash", width = 10, command = generate_hash).grid(row = 10, column = 0, padx = 10, pady = 5)
entry_hash = tk.Entry(master, width = 50, highlightbackground = "Blue", highlightcolor = "blue", highlightthickness = 2)
entry_hash.grid(row = 10, column = 1, columnspan = 3)

btn_sign_file = tk.Button(master, text = "sign and save", width = 10, command = signuture_file).grid(row = 11, column = 0, padx = 10, pady = 5)
entry_sign_location = tk.Entry(master, width = 50, highlightbackground = "Blue", highlightcolor = "blue", highlightthickness = 2)
entry_sign_location.grid(row = 11, column = 1, columnspan = 3)

lbl_break_03 = tk.Label(master, text = "-----------------------------------------------------------------------------").grid(row = 12, column = 0, columnspan = 4)

btn_brows_data_verification = tk.Button(master, text = "brows data", width = 10, command = brows_data_verify).grid(row = 13, column = 0, padx = 10, pady = 5)
entry_data_location_verification = tk.Entry(master, width = 50, highlightbackground = "Blue", highlightcolor = "blue", highlightthickness = 2)
entry_data_location_verification.grid(row = 13, column = 1, columnspan = 3, padx = 5, pady = 5)

txt_file_content_verify = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=50, height=4, font=("Times New Roman", 12))
txt_file_content_verify.grid(row = 14, column = 0, columnspan = 4, padx = 10, pady = 5)

btn_brows_sign_file = tk.Button(master, text = "sign file", width = 10, command = brows_sign_verify).grid(row = 15, column = 0, padx = 10, pady = 5)
entry_brows_sign_location = tk.Entry(master, width = 50, highlightbackground = "Blue", highlightcolor = "blue", highlightthickness = 2)
entry_brows_sign_location.grid(row = 15, column = 1, columnspan = 3)

txt_sign_file_content = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=50, height=4, font=("Times New Roman", 12))
txt_sign_file_content.grid(row = 16, column = 0, columnspan = 4, padx = 10, pady = 5)

btn_brows_public_key = tk.Button(master, text = "public key", width = 10, command = brows_keys).grid(row = 17, column = 0, padx = 10, pady = 5)
#entry_brows_public_key = tk.Entry(master, width = 50, highlightbackground = "Blue", highlightcolor = "blue", highlightthickness = 2)
#entry_brows_public_key.grid(row = 17, column = 1, columnspan = 3)

txt_public_key = tk.Text(master, width = 35, height = 2, highlightbackground = "Blue", highlightcolor = "blue", highlightthickness = 2)
txt_public_key.grid(row = 17, column = 1, columnspan = 3, padx = 5, pady = 5)

#btn_brows_private_key = tk.Button(master, text = "private key", width = 10, command = brows_keys).grid(row = 18, column = 0, padx = 10, pady = 3)
#entry_brows_private_key = tk.Entry(master, width = 50, highlightbackground = "Blue", highlightcolor = "blue", highlightthickness = 2)
#entry_brows_private_key.grid(row = 18, column = 1, columnspan = 3)

#txt_private_key = tk.Text(master, width = 35, height = 2, highlightbackground = "Blue", highlightcolor = "blue", highlightthickness = 2)
#txt_private_key.grid(row = 18, column = 1, columnspan = 3, padx = 3, pady = 3)

lbl_data_hash = tk.Label(master, width = 10, text = "data hash").grid(row = 19, column = 0, padx = 10, pady = 5)
entry_data_hash = tk.Entry(master, width = 50, highlightbackground = "Blue", highlightcolor = "blue", highlightthickness = 2)
entry_data_hash.grid(row = 19, column = 1, columnspan = 3)

lbl_sign_hash = tk.Label(master, width = 10, text = "signiture hash").grid(row = 20, column = 0, padx = 10, pady = 5)
entry_sign_hash = tk.Entry(master, width = 50, highlightbackground = "Blue", highlightcolor = "blue", highlightthickness = 2)
entry_sign_hash.grid(row = 20, column = 1, columnspan = 3)

btn_verify = Button(master, width = 20, text = "verify", command = verify).grid(row = 21, column = 1, columnspan = 2, padx = 15, pady = 5)

lbl_verification = tk.Label(master, width = 20, text = "not verified yet")
lbl_verification.grid(row = 22, column = 1, columnspan = 2, padx = 15, pady = 5)

master.mainloop()