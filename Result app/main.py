import pdfplumber
import pandas as pd
import re
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

pdf_path = ""
generated_file = ""

# ---------------- CLEAN ----------------
def clean_subject_name(name):
    return re.sub(r'\s+', ' ', name.replace("*", "")).strip()

def extract_result_class(block):

    # Extract CGPA
    cgpa_match = re.search(r'CGPA\s*:\s*([\d.]+)', block)
    cgpa = float(cgpa_match.group(1)) if cgpa_match else None

    # Extract result separately (more flexible)
    result_match = re.search(
        r'(FIRST CLASS WITH DISTINCTION|FIRST CLASS|SECOND CLASS|PASS|FAIL)',
        block,
        re.IGNORECASE
    )

    result = result_match.group(1) if result_match else ""

    return cgpa, result

# ---------------- ANALYSIS ----------------
def generate_analysis(df):
    analysis = {}

    if df["CGPA"].dropna().empty:
        analysis["topper"] = "No data"
        analysis["avg"] = 0
    else:
        topper = df.loc[df["CGPA"].idxmax()]
        analysis["topper"] = f'{topper["Name"]} ({topper["CGPA"]})'
        analysis["avg"] = round(df["CGPA"].mean(), 2)

    pass_df = df[df["Result"].str.contains("PASS", case=False, na=False)]
    total = len(df) if len(df) > 0 else 1
    analysis["pass_percent"] = round((len(pass_df)/total)*100,2)

    subject_cols = df.columns[4:]
    subject_avg = df[subject_cols].mean(numeric_only=True)

    analysis["best_subject"] = subject_avg.idxmax() if not subject_avg.empty else "N/A"
    analysis["weak_subject"] = subject_avg.idxmin() if not subject_avg.empty else "N/A"

    analysis["top5"] = df.sort_values(by="CGPA", ascending=False).head(5)

    subject_pass = {}
    for sub in subject_cols:
        subject_pass[sub] = round((df[sub] >= 40).sum()/total*100,2)
    analysis["subject_pass"] = subject_pass

    return analysis

# ---------------- UPLOAD ----------------
def upload_pdf():
    global pdf_path
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files","*.pdf")])
    if pdf_path:
        file_label.config(text=os.path.basename(pdf_path))

# ---------------- CONVERT ----------------
def convert_pdf():
    global pdf_path, generated_file

    if not pdf_path:
        messagebox.showwarning("Warning","Upload PDF first!")
        return

    try:
        full_text=""
        with pdfplumber.open(pdf_path) as pdf:
            for p in pdf.pages:
                t=p.extract_text()
                if t:
                    full_text+=t+"\n"

        students=full_text.split("SEAT NO.:")[1:]
        data=[]

        for block in students:
            d={}

            seat=re.search(r'(B\d+)',block)
            name=re.search(r'NAME\s*:\s*(.*?)\s*MOTHER',block)

            d["Seat No"]=seat.group(1) if seat else ""
            d["Name"]=name.group(1).strip() if name else ""

            cgpa,res=extract_result_class(block)
            d["CGPA"]=cgpa
            d["Result"]=res

            for line in block.split("\n"):

                # THEORY
                theory = re.search(
                    r'(\d{6})\s+(.+?)\s+(\d{3})/(\d{3})\s+(\d{3})/(\d{3})\s+(\d{3})/(\d{3})',
                    line
                )
                if theory:
                    d[clean_subject_name(theory.group(2))] = int(theory.group(7))
                    continue

                # LAB
                lab = re.search(
                    r'(\d{6})\s+(.+?)\s+---\s+---\s+---\s+(\d{3})/(\d{3})',
                    line
                )
                if lab:
                    d[clean_subject_name(lab.group(2))] = int(lab.group(3))
                    continue

            data.append(d)

        df=pd.DataFrame(data)
        generated_file="temp.xlsx"
        df.to_excel(generated_file,index=False)

        analysis=generate_analysis(df)

        # -------- SUMMARY --------
        summary_label.config(
            text=f"Topper: {analysis['topper']}\n"
                 f"Average CGPA: {analysis['avg']}\n"
                 f"Best Subject: {analysis['best_subject']}\n"
                 f"Weak Subject: {analysis['weak_subject']}"
        )

        # -------- TOP5 --------
        for i in top5.get_children(): top5.delete(i)
        for _,r in analysis["top5"].iterrows():
            top5.insert("", "end", values=(r["Name"], r["CGPA"]))

        # -------- SUBJECT --------
        for i in subject_table.get_children(): subject_table.delete(i)
        for s,v in analysis["subject_pass"].items():
            subject_table.insert("", "end", values=(s,f"{v}%"))

        # -------- GRAPH --------
        for w in graph_frame.winfo_children(): w.destroy()

        fig,ax=plt.subplots(figsize=(6,4))
        df["CGPA"].plot(kind="hist",ax=ax)
        ax.set_title("CGPA Distribution")

        canvas=FigureCanvasTkAgg(fig,graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    except Exception as e:
        messagebox.showerror("Error",str(e))

# ---------------- DOWNLOAD ----------------
def download_excel():
    if not generated_file: return
    path=filedialog.asksaveasfilename(defaultextension=".xlsx")
    if path:
        os.replace(generated_file,path)

# ---------------- GUI ----------------
root=tk.Tk()
root.title("Result Dashboard")
root.state("zoomed")
root.configure(bg="#dde6ed")

# HEADER
header=tk.Label(root,text="📊 RESULT ANALYSIS DASHBOARD",
                font=("Arial",22,"bold"),bg="#dde6ed")
header.pack(pady=10)

main=tk.Frame(root,bg="#dde6ed")
main.pack(fill="both",expand=True)

# LEFT PANEL
left=tk.Frame(main,bg="white",bd=2,relief="ridge")
left.place(relx=0.02,rely=0.05,relwidth=0.25,relheight=0.9)

tk.Button(left,text="Upload PDF",font=("Arial",11,"bold"),
          bg="#4CAF50",fg="white",width=18,command=upload_pdf).pack(pady=10)

tk.Button(left,text="Convert",font=("Arial",11,"bold"),
          bg="#2196F3",fg="white",width=18,command=convert_pdf).pack(pady=10)

tk.Button(left,text="Download",font=("Arial",11,"bold"),
          bg="#FF9800",fg="white",width=18,command=download_excel).pack(pady=10)

file_label=tk.Label(left,text="No file selected",bg="white")
file_label.pack(pady=5)

summary_label=tk.Label(left,text="",bg="white",justify="left",font=("Arial",11))
summary_label.pack(pady=20)

# RIGHT TOP
top_frame=tk.Frame(main,bg="white",bd=2,relief="ridge")
top_frame.place(relx=0.30, rely=0.05, relwidth=0.68, relheight=0.28)

tk.Label(top_frame,text="🏆 Top 5 Students",bg="white",font=("Arial",12,"bold")).pack()
top5=ttk.Treeview(top_frame,columns=("Name","CGPA"),show="headings")
top5.heading("Name",text="Name")
top5.heading("CGPA",text="CGPA")
top5.pack(fill="both",expand=True)

# RIGHT MID
mid_frame=tk.Frame(main,bg="white",bd=2,relief="ridge")
mid_frame.place(relx=0.30, rely=0.35, relwidth=0.68, relheight=0.35)

tk.Label(mid_frame,text="📘 Subject Pass %",bg="white",font=("Arial",12,"bold")).pack()
subject_table=ttk.Treeview(mid_frame,columns=("Sub","%"),show="headings")
subject_table.heading("Sub",text="Subject")
subject_table.heading("%",text="Pass %")
subject_table.pack(fill="both",expand=True)

# GRAPH
graph_frame=tk.Frame(main,bg="white",bd=2,relief="ridge")
graph_frame.place(relx=0.30,rely=0.72,relwidth=0.68,relheight=0.25)

root.mainloop()