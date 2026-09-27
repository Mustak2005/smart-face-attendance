import tkinter as tk
from tkinter import ttk


# ============================================================
# SMART FACE ATTENDANCE - GUI
# ============================================================

class AttendanceGUI:

    def __init__(self, root):
        self.root = root

        self.root.title(
            "Smart Face Recognition Attendance System"
        )

        self.root.geometry("1100x700")
        self.root.minsize(950, 600)

        self.root.configure(bg="#0b0f14")

        self.create_header()
        self.create_sidebar()
        self.create_dashboard()

    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg="#101720",
            height=80
        )

        header.pack(
            side="top",
            fill="x"
        )

        title = tk.Label(
            header,
            text="SMART FACE ATTENDANCE",
            font=("Segoe UI", 22, "bold"),
            fg="#00aaff",
            bg="#101720"
        )

        title.pack(
            side="left",
            padx=30,
            pady=20
        )

        subtitle = tk.Label(
            header,
            text="YuNet + SFace Recognition",
            font=("Segoe UI", 11),
            fg="#9aa7b2",
            bg="#101720"
        )

        subtitle.pack(
            side="left",
            padx=10
        )

  # ========================================================
    # SIDEBAR
    # ========================================================

    def create_sidebar(self):

        sidebar = tk.Frame(
            self.root,
            bg="#0f151c",
            width=230
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        sidebar.pack_propagate(False)

        menu_title = tk.Label(
            sidebar,
            text="MAIN MENU",
            font=("Segoe UI", 10, "bold"),
            fg="#6f7d89",
            bg="#0f151c"
        )

        menu_title.pack(
            anchor="w",
            padx=25,
            pady=(25, 15)
        )

        buttons = [
            "Dashboard",
            "Register Student",
            "Start Attendance",
            "Today's Attendance",
            "Attendance History",
            "Search Attendance",
            "Statistics",
            "Export Report",
            "Registered Students"
        ]
        for name in buttons:

            command = None

            if name == "Today's Attendance":
                command = self.show_todays_attendance

            elif name == "Start Attendance":
                command = self.start_face_attendance

            elif name == "Attendance History":
                command = self.show_attendance_history

            elif name == "Registered Students":
                command = self.show_registered_students

            button = tk.Button(
                sidebar,
                text=name,
                font=("Segoe UI", 10),
                fg="#dce6ee",
                bg="#151e27",
                activeforeground="#ffffff",
                activebackground="#008dcc",
                relief="flat",
                bd=0,
                anchor="w",
                padx=20,
                pady=10,
                cursor="hand2",
                command=command
            )

            button.pack(
                fill="x",
                padx=12,
                pady=3
            )
    # ========================================================
    # START FACE ATTENDANCE
    # ========================================================

    def start_face_attendance(self):

        try:
            import smart_face_attendance

            smart_face_attendance.start_attendance()

        except Exception as error:

            from tkinter import messagebox

            messagebox.showerror(
                "Attendance Error",
                f"Could not start face attendance.\n\n{error}"
            )
    # ========================================================
    # TODAY'S ATTENDANCE
    # ========================================================

    def show_todays_attendance(self):

        import csv
        import os
        from datetime import datetime
        if hasattr(self, "content"):
            self.content.destroy()

        today = datetime.now().strftime("%Y-%m-%d")


        # Remove current content
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                if widget.winfo_y() > 0:
                    pass

        # Create attendance page
        self.content = tk.Frame(
            self.root,
            bg="#0b0f14"
        )

        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

        title = tk.Label(
            self.content,
            text="Today's Attendance",
            font=("Segoe UI", 26, "bold"),
            fg="#ffffff",
            bg="#0b0f14"
        )

        title.pack(
            anchor="w",
            padx=35,
            pady=(30, 5)
        )

        date_label = tk.Label(
            self.content,
            text=f"Attendance for {today}",
            font=("Segoe UI", 11),
            fg="#8c9aa6",
            bg="#0b0f14"
        )

        date_label.pack(
            anchor="w",
            padx=35,
            pady=(0, 20)
        )

        table_frame = tk.Frame(
            self.content,
            bg="#101720"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=10
        )

        columns = (
            "Student ID",
            "Name",
            "Time",
            "Status"
        )

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:

            tree.heading(
                column,
                text=column
            )

            tree.column(
                column,
                width=150,
                anchor="center"
            )

        tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        total_present = 0

        if os.path.exists("attendance.csv"):

            try:

                with open(
                    "attendance.csv",
                    "r",
                    newline="",
                    encoding="utf-8"
                ) as file:

                    reader = csv.DictReader(file)

                    for row in reader:

                        if (
                            row.get("Date", "").strip()
                            == today
                        ):

                            tree.insert(
                                "",
                                "end",
                                values=(
                                    row.get(
                                        "Student ID",
                                        ""
                                    ),
                                    row.get(
                                        "Name",
                                        ""
                                    ),
                                    row.get(
                                        "Time",
                                        ""
                                    ),
                                    row.get(
                                        "Status",
                                        ""
                                    )
                                )
                            )

                            if (
                                row.get(
                                    "Status",
                                    ""
                                ).strip().lower()
                                == "present"
                            ):
                                total_present += 1

            except OSError:
                pass

        summary = tk.Label(
            self.content,
            text=f"Total Present: {total_present}",
            font=("Segoe UI", 13, "bold"),
            fg="#20d68b",
            bg="#0b0f14"
        )

        summary.pack(
            anchor="w",
            padx=35,
            pady=20
        )
    # ========================================================
    # ATTENDANCE HISTORY
    # ========================================================

    def show_attendance_history(self):

        import csv
        import os

        if hasattr(self, "content"):
            self.content.destroy()

        self.content = tk.Frame(
            self.root,
            bg="#0b0f14"
        )

        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

        title = tk.Label(
            self.content,
            text="Attendance History",
            font=("Segoe UI", 26, "bold"),
            fg="#ffffff",
            bg="#0b0f14"
        )

        title.pack(
            anchor="w",
            padx=35,
            pady=(30, 5)
        )

        subtitle = tk.Label(
            self.content,
            text="Complete attendance records",
            font=("Segoe UI", 11),
            fg="#8c9aa6",
            bg="#0b0f14"
        )

        subtitle.pack(
            anchor="w",
            padx=35,
            pady=(0, 20)
        )

        table_frame = tk.Frame(
            self.content,
            bg="#101720"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=10
        )

        columns = (
            "Date",
            "Student ID",
            "Name",
            "Time",
            "Status"
        )

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:

            tree.heading(
                column,
                text=column
            )

            tree.column(
                column,
                width=140,
                anchor="center"
            )

        tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        total_records = 0

        if os.path.exists("attendance.csv"):

            try:

                with open(
                    "attendance.csv",
                    "r",
                    newline="",
                    encoding="utf-8"
                ) as file:

                    reader = csv.DictReader(file)

                    for row in reader:

                        tree.insert(
                            "",
                            "end",
                            values=(
                                row.get(
                                    "Date",
                                    ""
                                ),
                                row.get(
                                    "Student ID",
                                    ""
                                ),
                                row.get(
                                    "Name",
                                    ""
                                ),
                                row.get(
                                    "Time",
                                    ""
                                ),
                                row.get(
                                    "Status",
                                    ""
                                )
                            )
                        )

                        total_records += 1

            except OSError:
                pass

        summary = tk.Label(
            self.content,
            text=f"Total Attendance Records: {total_records}",
            font=("Segoe UI", 13, "bold"),
            fg="#20d68b",
            bg="#0b0f14"
        )

        summary.pack(
            anchor="w",
            padx=35,
            pady=20
        )
        # ========================================================
    # REGISTERED STUDENTS
    # ========================================================

    def show_registered_students(self):
        print("REGISTERED STUDENTS BUTTON CLICKED")

        if hasattr(self, "content"):
            self.content.destroy()

        self.content = tk.Frame(
            self.root,
            bg="#0b0f14"
        )

        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

        title = tk.Label(
            self.content,
            text="Registered Students",
            font=("Segoe UI", 26, "bold"),
            fg="#ffffff",
            bg="#0b0f14"
        )

        title.pack(
            anchor="w",
            padx=35,
            pady=(30, 5)
        )

        subtitle = tk.Label(
            self.content,
            text="Students registered for face recognition",
            font=("Segoe UI", 11),
            fg="#8c9aa6",
            bg="#0b0f14"
        )

        subtitle.pack(
            anchor="w",
            padx=35,
            pady=(0, 20)
        )

        table_frame = tk.Frame(
            self.content,
            bg="#101720"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=10
        )

        columns = (
            "Student ID",
            "Name"
        )

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        tree.heading(
            "Student ID",
            text="Student ID"
        )

        tree.heading(
            "Name",
            text="Name"
        )

        tree.column(
            "Student ID",
            width=220,
            anchor="center"
        )

        tree.column(
            "Name",
            width=300,
            anchor="center"
        )

        tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        total_students = 0

        try:

            import smart_face_attendance

            people = (
                smart_face_attendance
                .load_registered_people()
            )

            for person in people:

                tree.insert(
                    "",
                    "end",
                    values=(
                        person.get(
                            "student_id",
                            ""
                        ),
                        person.get(
                            "name",
                            ""
                        )
                    )
                )

                total_students += 1

        except Exception as error:

            print(
                f"[ERROR] Could not load students: {error}"
            )

        summary = tk.Label(
            self.content,
            text=f"Total Registered Students: {total_students}",
            font=("Segoe UI", 13, "bold"),
            fg="#20d68b",
            bg="#0b0f14"
        )

        summary.pack(
            anchor="w",
            padx=35,
            pady=20
        )
    # ========================================================
    # DASHBOARD
    # ========================================================

    def create_dashboard(self):

        import json
        import csv
        import os
        from datetime import datetime

        self.content = tk.Frame(
            self.root,
            bg="#0b0f14"
        )

        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

        heading = tk.Label(
            self.content,
            text="Dashboard",
            font=("Segoe UI", 26, "bold"),
            fg="#ffffff",
            bg="#0b0f14"
        )

        heading.pack(
            anchor="w",
            padx=35,
            pady=(30, 5)
        )

        today = datetime.now().strftime("%Y-%m-%d")

        # ----------------------------------------------------
        # LOAD REGISTERED STUDENTS
        # ----------------------------------------------------

        total_students = 0
        registered_ids = set()

        json_file = os.path.join(
            "data",
            "registered_faces.json"
        )

        try:
            if os.path.exists(json_file):

                with open(
                    json_file,
                    "r",
                    encoding="utf-8"
                ) as file:

                    data = json.load(file)

                if isinstance(data, list):

                    for person in data:

                        if isinstance(person, dict):

                            student_id = str(
                                person.get(
                                    "student_id",
                                    ""
                                )
                            ).strip()

                            if student_id:
                                registered_ids.add(
                                    student_id
                                )

                elif isinstance(data, dict):

                    for student_id in data.keys():

                        if str(student_id).strip():
                            registered_ids.add(
                                str(student_id).strip()
                            )

        except Exception:
            registered_ids = set()

        total_students = len(
            registered_ids
        )

        # ----------------------------------------------------
        # LOAD TODAY'S ATTENDANCE
        # ----------------------------------------------------

        present_ids = set()

        if os.path.exists("attendance.csv"):

            try:

                with open(
                    "attendance.csv",
                    "r",
                    newline="",
                    encoding="utf-8"
                ) as file:

                    reader = csv.DictReader(file)

                    for row in reader:

                        date = row.get(
                            "Date",
                            ""
                        ).strip()

                        student_id = row.get(
                            "Student ID",
                            ""
                        ).strip()

                        status = row.get(
                            "Status",
                            ""
                        ).strip().lower()

                        if (
                            date == today
                            and student_id in registered_ids
                            and status == "present"
                        ):
                            present_ids.add(
                                student_id
                            )

            except Exception:
                present_ids = set()

        present_today = len(
            present_ids
        )

        not_marked = max(
            total_students - present_today,
            0
        )

        if total_students > 0:

            attendance_percentage = (
                present_today
                / total_students
            ) * 100

        else:

            attendance_percentage = 0

        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        description = tk.Label(
             self.content,
            text=(
                f"Smart attendance monitoring  •  "
                f"{today}"
            ),
            font=("Segoe UI", 11),
            fg="#8c9aa6",
            bg="#0b0f14"
        )

        description.pack(
            anchor="w",
            padx=35
        )

        # ----------------------------------------------------
        # DASHBOARD CARDS
        # ----------------------------------------------------

        cards_frame = tk.Frame(
            self.content,
            bg="#0b0f14"
        )

        cards_frame.pack(
            fill="x",
            padx=35,
            pady=30
        )

        self.create_card(
            cards_frame,
            "TOTAL STUDENTS",
            str(total_students)
        )

        self.create_card(
            cards_frame,
            "PRESENT TODAY",
            str(present_today)
        )

        self.create_card(
            cards_frame,
            "NOT MARKED",
            str(not_marked)
        )

        self.create_card(
            cards_frame,
            "ATTENDANCE",
            f"{attendance_percentage:.1f}%"
        )

        # ----------------------------------------------------
        # SYSTEM STATUS
        # ----------------------------------------------------

        system_frame = tk.Frame(
            self.content,
            bg="#101720"
        )

        system_frame.pack(
            fill="x",
            padx=35,
            pady=10
        )

        system_title = tk.Label(
            system_frame,
            text="SYSTEM STATUS",
            font=("Segoe UI", 13, "bold"),
            fg="#ffffff",
            bg="#101720"
        )

        system_title.pack(
            anchor="w",
            padx=25,
            pady=(20, 10)
        )

        status = tk.Label(
            system_frame,
            text="● SYSTEM ACTIVE",
            font=("Segoe UI", 11, "bold"),
            fg="#20d68b",
            bg="#101720"
        )

        status.pack(
            anchor="w",
            padx=25,
            pady=5
        )

        engine = tk.Label(
            system_frame,
            text=(
                "Detection Engine : YuNet\n"
                "Recognition Engine: SFace\n"
                "Storage           : JSON + CSV"
            ),
            font=("Consolas", 10),
            fg="#aebbc6",
            bg="#101720",
            justify="left"
        )

        engine.pack(
            anchor="w",
            padx=25,
            pady=(5, 20)
        )
    # ========================================================
    # DASHBOARD CARD
    # ========================================================

    def create_card(
        self,
        parent,
        title,
        value
    ):

        card = tk.Frame(
            parent,
            bg="#101720",
            width=170,
            height=120
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=6
        )

        card.pack_propagate(False)

        title_label = tk.Label(
            card,
            text=title,
            font=("Segoe UI", 9, "bold"),
            fg="#7f8d99",
            bg="#101720"
        )

        title_label.pack(
            anchor="w",
            padx=18,
            pady=(18, 5)
        )

        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 25, "bold"),
            fg="#00aaff",
            bg="#101720"
        )

        value_label.pack(
            anchor="w",
            padx=18
        )


# ============================================================
# START GUI
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = AttendanceGUI(root)

    root.mainloop()
    
