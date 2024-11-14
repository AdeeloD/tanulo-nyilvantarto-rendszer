import tkinter as tk
from tkinter import messagebox, ttk
from HE_modul import HEOsztaly
from datetime import datetime


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Tanuló Nyilvántartó")


        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")


        self.db = HEOsztaly()


        title_label = tk.Label(root, text="Tanuló Nyilvántartó", font=("Arial", 20, "bold"), pady=10)
        title_label.pack()


        form_frame = tk.Frame(root, padx=20, pady=10)
        form_frame.pack(fill="x", padx=20, pady=10)


        tk.Label(form_frame, text="Tanuló Neve:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.nev_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.nev_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Neptun Kód:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.neptun_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.neptun_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Email:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.email_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.email_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Nemzetiség:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.nemzetiseg_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.nemzetiseg_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Ösztöndíjas:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.osztondijas_var = tk.BooleanVar()
        tk.Checkbutton(form_frame, variable=self.osztondijas_var).grid(row=4, column=1, padx=5, pady=5, sticky="w")

        tk.Label(form_frame, text="Születési Dátum (YYYY-MM-DD):", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.szuletesi_datum_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.szuletesi_datum_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(form_frame, text="Megjegyzés:", font=("Arial", 12)).grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.megjegyzes_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.megjegyzes_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        form_frame.grid_columnconfigure(1, weight=1)


        button_frame = tk.Frame(root, pady=10)
        button_frame.pack()

        tk.Button(button_frame, text="Tanuló Hozzáadása", font=("Arial", 12), command=self.tanulo_hozzaadasa_HE).grid(
            row=0, column=0, padx=10, pady=5)
        tk.Button(button_frame, text="Tanulók Listája", font=("Arial", 12), command=self.tanulok_listaja_HE).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(button_frame, text="Tanuló Törlése", font=("Arial", 12), command=self.tanulo_torlese_HE).grid(row=0, column=2, padx=10, pady=5)
        tk.Button(button_frame, text="Szerkesztés", font=("Arial", 12), command=self.tanulo_szerkesztese_HE).grid(row=0, column=3, padx=10, pady=5)


        self.mentes_button = tk.Button(button_frame, text="Mentés", font=("Arial", 12), command=self.tanulo_modositasa_HE)
        self.mentes_button.grid(row=0, column=4, padx=10, pady=5)
        self.mentes_button.grid_remove()  # Kezdetben rejtett


        self.tree = ttk.Treeview(root, columns=("nev", "neptun_kod", "email", "nemzetiseg", "osztondijas", "szuletesi_datum", "megjegyzes"), show="headings", height=10)
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)


        self.tree.heading("nev", text="Tanuló Neve")
        self.tree.heading("neptun_kod", text="Neptun Kód")
        self.tree.heading("email", text="Email")
        self.tree.heading("nemzetiseg", text="Nemzetiség")
        self.tree.heading("osztondijas", text="Ösztöndíjas")
        self.tree.heading("szuletesi_datum", text="Születési Dátum")
        self.tree.heading("megjegyzes", text="Megjegyzés")

        for col in ("nev", "neptun_kod", "email", "nemzetiseg", "osztondijas", "szuletesi_datum", "megjegyzes"):
            self.tree.column(col, width=100, anchor="center")

    def tanulo_hozzaadasa_HE(self):
        nev = self.nev_entry.get()
        neptun_kod = self.neptun_entry.get()
        email = self.email_entry.get()
        nemzetiseg = self.nemzetiseg_entry.get()
        osztondijas = self.osztondijas_var.get()
        szuletesi_datum = self.szuletesi_datum_entry.get()
        megjegyzes = self.megjegyzes_entry.get()

        try:
            datetime.strptime(szuletesi_datum, "%Y-%m-%d")
            eredmeny = self.db.uj_tanulo_hozzaadasa_HE(nev, neptun_kod, email, nemzetiseg, osztondijas, szuletesi_datum, megjegyzes)
            messagebox.showinfo("Eredmény", eredmeny)
            self.tanulok_listaja_HE()
        except ValueError:
            messagebox.showerror("Hiba", "A születési dátum formátuma helytelen. (YYYY-MM-DD)")

    def tanulok_listaja_HE(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        tanulok = self.db.tanulok_lekerdezese_HE()
        for tanulo in tanulok:
            self.tree.insert("", "end", values=tanulo)

    def tanulo_torlese_HE(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Figyelem", "Kérjük, válassza ki a törölni kívánt tanulót.")
            return

        tanulo_adatok = self.tree.item(selected_item)["values"]
        neptun_kod = tanulo_adatok[1]

        confirmed = messagebox.askyesno("Megerősítés", f"Biztosan törölni szeretné a következő tanulót: {tanulo_adatok[0]}?")
        if confirmed:
            eredmeny = self.db.tanulo_torlese_HE(neptun_kod)
            messagebox.showinfo("Eredmény", eredmeny)
            self.tanulok_listaja_HE()

    def tanulo_szerkesztese_HE(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Figyelem", "Kérjük, válassza ki a szerkeszteni kívánt tanulót.")
            return

        tanulo_adatok = self.tree.item(selected_item)["values"]
        self.nev_entry.delete(0, tk.END)
        self.nev_entry.insert(0, tanulo_adatok[0])
        self.neptun_entry.delete(0, tk.END)
        self.neptun_entry.insert(0, tanulo_adatok[1])
        self.neptun_entry.config(state="disabled")
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, tanulo_adatok[2])
        self.nemzetiseg_entry.delete(0, tk.END)
        self.nemzetiseg_entry.insert(0, tanulo_adatok[3])
        self.osztondijas_var.set(tanulo_adatok[4])
        self.szuletesi_datum_entry.delete(0, tk.END)
        self.szuletesi_datum_entry.insert(0, tanulo_adatok[5])
        self.megjegyzes_entry.delete(0, tk.END)
        self.megjegyzes_entry.insert(0, tanulo_adatok[6])

        self.mentes_button.grid()

    def tanulo_modositasa_HE(self):
        neptun_kod = self.neptun_entry.get()
        nev = self.nev_entry.get()
        email = self.email_entry.get()
        nemzetiseg = self.nemzetiseg_entry.get()
        osztondijas = self.osztondijas_var.get()
        szuletesi_datum = self.szuletesi_datum_entry.get()
        megjegyzes = self.megjegyzes_entry.get()

        try:
            datetime.strptime(szuletesi_datum, "%Y-%m-%d")
            eredmeny = self.db.tanulo_modositasa_HE(neptun_kod, nev, email, nemzetiseg, osztondijas, szuletesi_datum, megjegyzes)
            messagebox.showinfo("Eredmény", eredmeny)
            self.neptun_entry.config(state="normal")
            self.mentes_button.grid_remove()
            self.tanulok_listaja_HE()
        except ValueError:
            messagebox.showerror("Hiba", "A születési dátum formátuma helytelen. (YYYY-MM-DD)")

root = tk.Tk()
app = App(root)
root.mainloop()
