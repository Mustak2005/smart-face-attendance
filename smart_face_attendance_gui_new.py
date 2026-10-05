import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
from datetime import datetime


# ============================================================
# SMART FACE ATTENDANCE - COMPLETE GUI
# ============================================================

class AttendanceGUI:

    BG = "#0b0f14"
    SIDEBAR = "#0f151c"
    PANEL = "#101720"
    BUTTON = "#151e27"
    BLUE = "#00aaff"
    GREEN = "#20d68b"
    RED = "#ff5c5c"
    TEXT = "#ffffff"
    MUTED = "#8c9aa6"

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Smart Face Recognition Attendance System"
        )

        self.root.geometry("1100x700")
        self.root.minsize(950, 600)

        self.root.configure(bg=self.BG)

        self.setup_treeview_style()

        self.create_header()
        self.create_sidebar()
        self.create_dashboard()

    # ========================================================
    # TREEVIEW STYLE
    # ========================================================

    def setup_treeview_style(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            background="#111922",
            foreground="#dce6ee",
            fieldbackground="#111922",
            rowheight=34,
            borderwidth=0,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#17222d",
            foreground="#00aaff",
            font=("Segoe UI", 10, "bold"),
            relief="flat"
        )

        style.map(
            "Treeview",
            background=[("selected", "#075a86")],
            foreground=[("selected", "#ffffff")]
        )

    # ========================================================
    # COMMON HELPERS
    # ========================================================

    def clear_content(self):

        if hasattr(self, "content"):

            try:
                self.content.destroy()
            except tk.TclError:
                pass

        self.content = tk.Frame(
            self.root,
            bg=self.BG
        )

        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

    def page_title(self, title, subtitle=""):

        tk.Label(
            self.content,
            text=title,
            font=("Segoe UI", 26, "bold"),
            fg=self.TEXT,
            bg=self.BG
        ).pack(
            anchor="w",
            padx=35,
            pady=(30, 5)
        )

        if subtitle:

            tk.Label(
                self.content,
                text=subtitle,
                font=("Segoe UI", 11),
                fg=self.MUTED,
                bg=self.BG
            ).pack(
                anchor="w",
                padx=35,
                pady=(0, 20)
            )

    def make_tree(self, columns, widths=None):

        table_frame = tk.Frame(
            self.content,
            bg=self.PANEL
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=10
        )

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for index, column in enumerate(columns):

            tree.heading(
                column,
                text=column
            )

            width = (
                widths[index]
                if widths
                else 150
            )

            tree.column(
                column,
                width=width,
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=tree.yview
        )

        tree.configure(
            yscrollcommand=scrollbar.set
        )

        tree.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(15, 0),
            pady=15
        )

        scrollbar.pack(
            side="right",
            fill="y",
            padx=(0, 15),
            pady=15
        )

        return tree

    # ========================================================
    # READ ATTENDANCE
    # ========================================================

    def read_attendance(self):

        records = []

        if not os.path.exists("attendance.csv"):
            return records

        try:

            with open(
                "attendance.csv",
                "r",
                newline="",
                encoding="utf-8"
            ) as file:

                reader = csv.DictReader(file)

                records = list(reader)

        except OSError:
            pass

        return records

    # ========================================================
    # READ REGISTERED PEOPLE
    # ========================================================

    def read_registered_people(self):

        try:

            import smart_face_attendance_before_gui

            return (
                smart_face_attendance_before_gui
                .load_registered_people()
            )

        except Exception:

            return []

    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg=self.PANEL,
            height=80
        )

        header.pack(
            side="top",
            fill="x"
        )

        tk.Label(
            header,
            text="SMART FACE ATTENDANCE",
            font=("Segoe UI", 22, "bold"),
            fg=self.BLUE,
            bg=self.PANEL
        ).pack(
            side="left",
            padx=30,
            pady=20
        )

        tk.Label(
            header,
            text="YuNet + SFace Recognition",
            font=("Segoe UI", 11),
            fg="#9aa7b2",
            bg=self.PANEL
        ).pack(
            side="left",
            padx=10
        )

    # ========================================================
    # SIDEBAR
    # ========================================================

    def create_sidebar(self):

        sidebar = tk.Frame(
            self.root,
            bg=self.SIDEBAR,
            width=230
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="MAIN MENU",
            font=("Segoe UI", 10, "bold"),
            fg="#6f7d89",
            bg=self.SIDEBAR
        ).pack(
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

        commands = {

            "Dashboard":
                self.create_dashboard,

            "Register Student":
                self.register_student_gui,

            "Start Attendance":
                self.start_face_attendance,

            "Today's Attendance":
                self.show_todays_attendance,

            "Attendance History":
                self.show_attendance_history,

            "Search Attendance":
                self.show_search_attendance,

            "Statistics":
                self.show_statistics,

            "Export Report":
                self.export_report_gui,

            "Registered Students":
                self.show_registered_students
        }

        for name in buttons:

            button = tk.Button(
                sidebar,
                text=name,
                font=("Segoe UI", 10),
                fg="#dce6ee",
                bg=self.BUTTON,
                activeforeground="#ffffff",
                activebackground="#008dcc",
                relief="flat",
                bd=0,
                anchor="w",
                padx=20,
                pady=10,
                cursor="hand2",
                command=commands[name]
            )

            button.pack(
                fill="x",
                padx=12,
                pady=3
            )

    # ========================================================
    # REGISTER STUDENT
    # ========================================================

    def register_student_gui(self):

        window = tk.Toplevel(self.root)

        window.title(
            "Register New Student"
        )

        window.geometry(
            "430x300"
        )

        window.resizable(
            False,
            False
        )

        window.configure(
            bg=self.BG
        )

        window.transient(
            self.root
        )

        window.grab_set()

        tk.Label(
            window,
            text="REGISTER NEW STUDENT",
            font=("Segoe UI", 18, "bold"),
            fg=self.BLUE,
            bg=self.BG
        ).pack(
            pady=(25, 20)
        )

        form = tk.Frame(
            window,
            bg=self.BG
        )

        form.pack(
            fill="x",
            padx=35
        )

        # ----------------------------------------------------
        # STUDENT ID
        # ----------------------------------------------------

        tk.Label(
            form,
            text="Student ID",
            font=("Segoe UI", 10, "bold"),
            fg=self.TEXT,
            bg=self.BG
        ).pack(
            anchor="w"
        )

        id_entry = tk.Entry(
            form,
            font=("Segoe UI", 11),
            bg="#16212b",
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="flat"
        )

        id_entry.pack(
            fill="x",
            ipady=8,
            pady=(5, 15)
        )

        # ----------------------------------------------------
        # STUDENT NAME
        # ----------------------------------------------------

        tk.Label(
            form,
            text="Student Name",
            font=("Segoe UI", 10, "bold"),
            fg=self.TEXT,
            bg=self.BG
        ).pack(
            anchor="w"
        )

        name_entry = tk.Entry(
            form,
            font=("Segoe UI", 11),
            bg="#16212b",
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="flat"
        )

        name_entry.pack(
            fill="x",
            ipady=8,
            pady=(5, 20)
        )

        # ----------------------------------------------------
        # START REGISTRATION
        # ----------------------------------------------------

        # ----------------------------------------------------
        # START REGISTRATION
        # ----------------------------------------------------

        def start_registration():

            student_id = id_entry.get().strip()
            student_name = name_entry.get().strip()

            # =================================================
            # CHECK EMPTY FIELDS
            # =================================================

            if not student_id or not student_name:

                messagebox.showwarning(
                    "Missing Details",
                    "Please enter both Student ID and Student Name.",
                    parent=window
                )

                return

            # =================================================
            # CHECK DUPLICATE STUDENT ID
            # =================================================

            people_before = self.read_registered_people()

            existing_ids = {

                str(
                    person.get(
                        "student_id",
                        ""
                    )
                ).strip().lower()

                for person in people_before
            }

            if student_id.lower() in existing_ids:

                messagebox.showwarning(
                    "Already Registered",
                    f"Student ID {student_id} is already registered.",
                    parent=window
                )

                return

            # =================================================
            # CLOSE REGISTRATION FORM
            # =================================================

            window.destroy()

            self.root.update_idletasks()

            # =================================================
            # SEND GUI INPUT TO BACKEND
            # =================================================

            import builtins
            import io
            import contextlib

            original_input = builtins.input

            # -------------------------------------------------
            # Replace backend input() with GUI values
            # -------------------------------------------------

            def gui_input(prompt=""):

                prompt_text = str(prompt).lower()

                if "student id" in prompt_text:
                    return student_id

                if "name" in prompt_text:
                    return student_name

                return student_id

            # =================================================
            # RUN BACKEND REGISTRATION
            # =================================================

            try:

                builtins.input = gui_input

                # Use the tested backend
                import smart_face_attendance_before_gui

                # Capture backend terminal output
                output_buffer = io.StringIO()

                with contextlib.redirect_stdout(output_buffer):

                    smart_face_attendance_before_gui.register_person()

                # Get captured output
                result = output_buffer.getvalue()

                # =================================================
                # CHECK DUPLICATE FACE
                # =================================================

                if "REGISTRATION REJECTED" in result:

                    existing_id = "Unknown"
                    existing_name = "Unknown"
                    match_score = "Unknown"
                    threshold = "0.60"

                    for line in result.splitlines():

                        if "Existing Student ID" in line:

                            existing_id = (
                                line.split(":", 1)[1].strip()
                            )

                        elif "Existing Name" in line:

                            existing_name = (
                                line.split(":", 1)[1].strip()
                            )

                        elif "Face Match Score" in line:

                            match_score = (
                                line.split(":", 1)[1].strip()
                            )

                        elif "Required Threshold" in line:

                            threshold = (
                                line.split(":", 1)[1].strip()
                            )

                    # Format threshold
                    try:

                        threshold = f"{float(threshold):.2f}"

                    except:

                        pass

                    # Show duplicate warning
                    messagebox.showwarning(

                        "Registration Rejected",

                        "This face is already registered.\n\n"
                        f"Existing Student: "
                        f"{existing_id} - {existing_name}\n"
                        f"Match Score: {match_score}\n"
                        f"Required Threshold: {threshold}",

                        parent=self.root
                    )

                    return

                # =================================================
                # CHECK WHETHER STUDENT WAS SAVED
                # =================================================

                people_after = self.read_registered_people()

                registered = any(

                    str(
                        person.get(
                            "student_id",
                            ""
                        )
                    ).strip().lower()
                    ==
                    student_id.lower()

                    for person in people_after
                )

                # =================================================
                # REGISTRATION SUCCESSFUL
                # =================================================

                if registered:

                    messagebox.showinfo(

                        "Registration Successful",

                        f"{student_name} ({student_id}) "
                        "registered successfully.\n\n"
                        "Face samples have been saved "
                        "for recognition.",

                        parent=self.root
                    )

                    self.create_dashboard()

                # =================================================
                # REGISTRATION NOT COMPLETED
                # =================================================

                else:

                    messagebox.showwarning(

                        "Registration Not Completed",

                        "The student was not saved.\n\n"
                        "Possible reasons:\n\n"
                        "• Camera was cancelled\n"
                        "• Face was not detected\n"
                        "• 5 samples were not captured\n"
                        "• The face is already registered",

                        parent=self.root
                    )

            # =================================================
            # ERROR
            # =================================================

            except Exception as error:

                messagebox.showerror(

                    "Registration Error",

                    "Could not register the student.\n\n"
                    f"{error}",

                    parent=self.root
                )

            # =================================================
            # RESTORE ORIGINAL INPUT
            # =================================================

            finally:

                builtins.input = original_input

        # ----------------------------------------------------
        # BUTTON
        # ----------------------------------------------------

        tk.Button(

            window,

            text="START CAMERA REGISTRATION",

            command=start_registration,

            font=(
                "Segoe UI",
                10,
                "bold"
            ),

            fg="#ffffff",

            bg="#008dcc",

            activebackground=self.BLUE,

            activeforeground="#ffffff",

            relief="flat",

            bd=0,

            cursor="hand2",

            pady=10

        ).pack(

            fill="x",

            padx=35
        )

        id_entry.focus_set()

    # ========================================================
    # START FACE ATTENDANCE
    # ========================================================

    def start_face_attendance(self):

        try:

            import smart_face_attendance_before_gui

            smart_face_attendance_before_gui.start_attendance()

            self.create_dashboard()

        except Exception as error:

            messagebox.showerror(

                "Attendance Error",

                "Could not start face attendance.\n\n"
                f"{error}"
            )

    # ========================================================
    # TODAY'S ATTENDANCE
    # ========================================================

    def show_todays_attendance(self):

        today = datetime.now().strftime(
            "%Y-%m-%d"
        )

        self.clear_content()

        self.page_title(
            "Today's Attendance",
            f"Attendance for {today}"
        )

        tree = self.make_tree(

            (
                "Student ID",
                "Name",
                "Time",
                "Status"
            ),

            (
                170,
                250,
                170,
                150
            )
        )

        total_present = 0

        for row in self.read_attendance():

            if (
                row.get(
                    "Date",
                    ""
                ).strip()
                ==
                today
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
                    ==
                    "present"

                ):

                    total_present += 1

        tk.Label(

            self.content,

            text=f"Total Present: {total_present}",

            font=(
                "Segoe UI",
                13,
                "bold"
            ),

            fg=self.GREEN,

            bg=self.BG

        ).pack(

            anchor="w",

            padx=35,

            pady=20
        )

    # ========================================================
    # ATTENDANCE HISTORY
    # ========================================================

    def show_attendance_history(self):

        self.clear_content()

        self.page_title(

            "Attendance History",

            "Complete attendance records"
        )

        tree = self.make_tree(

            (
                "Date",
                "Student ID",
                "Name",
                "Time",
                "Status"
            ),

            (
                140,
                160,
                240,
                150,
                150
            )
        )

        records = self.read_attendance()

        for row in records:

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

        tk.Label(

            self.content,

            text=(
                f"Total Attendance Records: "
                f"{len(records)}"
            ),

            font=(
                "Segoe UI",
                13,
                "bold"
            ),

            fg=self.GREEN,

            bg=self.BG

        ).pack(

            anchor="w",

            padx=35,

            pady=20
        )

    # ========================================================
    # SEARCH ATTENDANCE
    # ========================================================

    def show_search_attendance(self):

        self.clear_content()

        self.page_title(

            "Search Attendance",

            "Search by Student ID, Name, or Date"
        )

        search_frame = tk.Frame(

            self.content,

            bg=self.BG
        )

        search_frame.pack(

            fill="x",

            padx=35,

            pady=(0, 15)
        )

        entry = tk.Entry(

            search_frame,

            font=(
                "Segoe UI",
                12
            ),

            bg="#151e27",

            fg="#ffffff",

            insertbackground="#ffffff",

            relief="flat"
        )

        entry.pack(

            side="left",

            fill="x",

            expand=True,

            ipady=9,

            padx=(0, 10)
        )

        tree = self.make_tree(

            (
                "Date",
                "Student ID",
                "Name",
                "Time",
                "Status"
            ),

            (
                140,
                160,
                240,
                150,
                150
            )
        )

        result_label = tk.Label(

            self.content,

            text="Enter a value and click Search",

            font=(
                "Segoe UI",
                11
            ),

            fg=self.MUTED,

            bg=self.BG
        )

        result_label.pack(

            anchor="w",

            padx=35,

            pady=10
        )

        def perform_search():

            term = entry.get().strip().lower()

            for item in tree.get_children():

                tree.delete(item)

            if not term:

                result_label.config(

                    text=(
                        "Please enter Student ID, "
                        "Name, or Date."
                    )
                )

                return

            results = []

            for row in self.read_attendance():

                student_id = row.get(
                    "Student ID",
                    ""
                ).lower()

                name = row.get(
                    "Name",
                    ""
                ).lower()

                date = row.get(
                    "Date",
                    ""
                ).lower()

                if (

                    term in student_id
                    or
                    term in name
                    or
                    term in date

                ):

                    results.append(row)

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

            result_label.config(

                text=(
                    f"Matching Records: "
                    f"{len(results)}"
                ),

                fg=(
                    self.GREEN
                    if results
                    else self.MUTED
                )
            )

        tk.Button(

            search_frame,

            text="SEARCH",

            command=perform_search,

            font=(
                "Segoe UI",
                10,
                "bold"
            ),

            fg="#ffffff",

            bg="#008dcc",

            activebackground=self.BLUE,

            activeforeground="#ffffff",

            relief="flat",

            padx=22,

            pady=9,

            cursor="hand2"

        ).pack(

            side="right"
        )

        entry.bind(

            "<Return>",

            lambda event:
            perform_search()
        )

        entry.focus_set()

    # ========================================================
    # STATISTICS
    # ========================================================

    def show_statistics(self):

        self.clear_content()

        self.page_title(

            "Attendance Statistics",

            "Current registration and attendance overview"
        )

        people = self.read_registered_people()

        records = self.read_attendance()

        today = datetime.now().strftime(
            "%Y-%m-%d"
        )

        registered_ids = {

            str(
                person.get(
                    "student_id",
                    ""
                )
            ).strip()

            for person in people

            if str(
                person.get(
                    "student_id",
                    ""
                )
            ).strip()
        }

        today_present_ids = set()

        for row in records:

            student_id = row.get(
                "Student ID",
                ""
            ).strip()

            if (

                row.get(
                    "Date",
                    ""
                ).strip()
                ==
                today

                and

                student_id in registered_ids

                and

                row.get(
                    "Status",
                    ""
                ).strip().lower()
                ==
                "present"

            ):

                today_present_ids.add(
                    student_id
                )

        total_students = len(
            registered_ids
        )

        total_records = len(
            records
        )

        today_present = len(
            today_present_ids
        )

        not_marked = max(

            total_students
            -
            today_present,

            0
        )

        percentage = (

            (
                today_present
                /
                total_students
            )
            *
            100

            if total_students

            else 0
        )

        cards = tk.Frame(

            self.content,

            bg=self.BG
        )

        cards.pack(

            fill="x",

            padx=35,

            pady=25
        )

        values = [

            (
                "TOTAL STUDENTS",
                total_students
            ),

            (
                "TOTAL RECORDS",
                total_records
            ),

            (
                "PRESENT TODAY",
                today_present
            ),

            (
                "NOT MARKED",
                not_marked
            ),

            (
                "TODAY'S RATE",
                f"{percentage:.1f}%"
            )
        ]

        for title, value in values:

            card = tk.Frame(

                cards,

                bg=self.PANEL,

                height=125
            )

            card.pack(

                side="left",

                fill="both",

                expand=True,

                padx=5
            )

            card.pack_propagate(
                False
            )

            tk.Label(

                card,

                text=title,

                font=(
                    "Segoe UI",
                    9,
                    "bold"
                ),

                fg="#7f8d99",

                bg=self.PANEL

            ).pack(

                anchor="w",

                padx=15,

                pady=(18, 5)
            )

            tk.Label(

                card,

                text=str(value),

                font=(
                    "Segoe UI",
                    24,
                    "bold"
                ),

                fg=self.BLUE,

                bg=self.PANEL

            ).pack(

                anchor="w",

                padx=15
            )

        latest = (
            records[-1]
            if records
            else None
        )

        recent = tk.Frame(

            self.content,

            bg=self.PANEL
        )

        recent.pack(

            fill="x",

            padx=35,

            pady=10
        )

        tk.Label(

            recent,

            text="MOST RECENT ATTENDANCE",

            font=(
                "Segoe UI",
                13,
                "bold"
            ),

            fg=self.TEXT,

            bg=self.PANEL

        ).pack(

            anchor="w",

            padx=25,

            pady=(20, 10)
        )

        if latest:

            latest_text = (

                f"Student ID : "
                f"{latest.get('Student ID', '')}\n"

                f"Name       : "
                f"{latest.get('Name', '')}\n"

                f"Date       : "
                f"{latest.get('Date', '')}\n"

                f"Time       : "
                f"{latest.get('Time', '')}\n"

                f"Status     : "
                f"{latest.get('Status', '')}"
            )

        else:

            latest_text = (
                "No attendance records found."
            )

        tk.Label(

            recent,

            text=latest_text,

            font=(
                "Consolas",
                10
            ),

            fg="#aebbc6",

            bg=self.PANEL,

            justify="left"

        ).pack(

            anchor="w",

            padx=25,

            pady=(0, 20)
        )

    # ========================================================
    # EXPORT REPORT
    # ========================================================

    def export_report_gui(self):

        records = self.read_attendance()

        if not records:

            messagebox.showwarning(

                "Export Report",

                "No attendance records are available "
                "to export."
            )

            return

        file_path = filedialog.asksaveasfilename(

            title="Save Attendance Report",

            defaultextension=".csv",

            initialfile="attendance_report.csv",

            filetypes=[

                (
                    "CSV files",
                    "*.csv"
                ),

                (
                    "All files",
                    "*.*"
                )
            ]
        )

        if not file_path:
            return

        fieldnames = [

            "Date",
            "Student ID",
            "Name",
            "Time",
            "Status"
        ]

        try:

            with open(

                file_path,

                "w",

                newline="",

                encoding="utf-8"

            ) as file:

                writer = csv.DictWriter(

                    file,

                    fieldnames=fieldnames
                )

                writer.writeheader()

                for row in records:

                    writer.writerow({

                        "Date":
                            row.get(
                                "Date",
                                ""
                            ),

                        "Student ID":
                            row.get(
                                "Student ID",
                                ""
                            ),

                        "Name":
                            row.get(
                                "Name",
                                ""
                            ),

                        "Time":
                            row.get(
                                "Time",
                                ""
                            ),

                        "Status":
                            row.get(
                                "Status",
                                ""
                            )
                    })

            messagebox.showinfo(

                "Export Successful",

                "Attendance report exported successfully.\n\n"

                f"Records: {len(records)}\n"

                f"File: {file_path}"
            )

        except OSError as error:

            messagebox.showerror(

                "Export Error",

                "Could not save the attendance report.\n\n"
                f"{error}"
            )

    # ========================================================
    # REGISTERED STUDENTS
    # ========================================================

    def show_registered_students(self):

        self.clear_content()

        self.page_title(

            "Registered Students",

            "Students registered for face recognition"
        )

        tree = self.make_tree(

            (
                "Student ID",
                "Name"
            ),

            (
                250,
                350
            )
        )

        people = self.read_registered_people()

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

        tk.Label(

            self.content,

            text=(
                f"Total Registered Students: "
                f"{len(people)}"
            ),

            font=(
                "Segoe UI",
                13,
                "bold"
            ),

            fg=self.GREEN,

            bg=self.BG

        ).pack(

            anchor="w",

            padx=35,

            pady=20
        )

    # ========================================================
    # DASHBOARD
    # ========================================================

    def create_dashboard(self):

        self.clear_content()

        today = datetime.now().strftime(
            "%Y-%m-%d"
        )

        people = self.read_registered_people()

        records = self.read_attendance()

        registered_ids = {

            str(
                person.get(
                    "student_id",
                    ""
                )
            ).strip()

            for person in people

            if str(
                person.get(
                    "student_id",
                    ""
                )
            ).strip()
        }

        present_ids = set()

        for row in records:

            student_id = row.get(
                "Student ID",
                ""
            ).strip()

            if (

                row.get(
                    "Date",
                    ""
                ).strip()
                ==
                today

                and

                student_id in registered_ids

                and

                row.get(
                    "Status",
                    ""
                ).strip().lower()
                ==
                "present"

            ):

                present_ids.add(
                    student_id
                )

        total_students = len(
            registered_ids
        )

        present_today = len(
            present_ids
        )

        not_marked = max(

            total_students
            -
            present_today,

            0
        )

        percentage = (

            (
                present_today
                /
                total_students
            )
            *
            100

            if total_students

            else 0
        )

        tk.Label(

            self.content,

            text="Dashboard",

            font=(
                "Segoe UI",
                26,
                "bold"
            ),

            fg=self.TEXT,

            bg=self.BG

        ).pack(

            anchor="w",

            padx=35,

            pady=(30, 5)
        )

        tk.Label(

            self.content,

            text=(
                "Smart attendance monitoring  •  "
                f"{today}"
            ),

            font=(
                "Segoe UI",
                11
            ),

            fg=self.MUTED,

            bg=self.BG

        ).pack(

            anchor="w",

            padx=35
        )

        cards_frame = tk.Frame(

            self.content,

            bg=self.BG
        )

        cards_frame.pack(

            fill="x",

            padx=35,

            pady=30
        )

        values = [

            (
                "TOTAL STUDENTS",
                total_students
            ),

            (
                "PRESENT TODAY",
                present_today
            ),

            (
                "NOT MARKED",
                not_marked
            ),

            (
                "ATTENDANCE",
                f"{percentage:.1f}%"
            )
        ]

        for title, value in values:

            self.create_card(

                cards_frame,

                title,

                str(value)
            )

        system_frame = tk.Frame(

            self.content,

            bg=self.PANEL
        )

        system_frame.pack(

            fill="x",

            padx=35,

            pady=10
        )

        tk.Label(

            system_frame,

            text="SYSTEM STATUS",

            font=(
                "Segoe UI",
                13,
                "bold"
            ),

            fg=self.TEXT,

            bg=self.PANEL

        ).pack(

            anchor="w",

            padx=25,

            pady=(20, 10)
        )

        tk.Label(

            system_frame,

            text="● SYSTEM ACTIVE",

            font=(
                "Segoe UI",
                11,
                "bold"
            ),

            fg=self.GREEN,

            bg=self.PANEL

        ).pack(

            anchor="w",

            padx=25,

            pady=5
        )

        tk.Label(

            system_frame,

            text=(

                "Detection Engine : YuNet\n"

                "Recognition Engine: SFace\n"

                "Storage           : JSON + CSV"

            ),

            font=(
                "Consolas",
                10
            ),

            fg="#aebbc6",

            bg=self.PANEL,

            justify="left"

        ).pack(

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

            bg=self.PANEL,

            width=150,

            height=120
        )

        card.pack(

            side="left",

            fill="both",

            expand=True,

            padx=6
        )

        card.pack_propagate(
            False
        )

        tk.Label(

            card,

            text=title,

            font=(
                "Segoe UI",
                8,
                "bold"
            ),

            fg="#7f8d99",

            bg=self.PANEL

        ).pack(

            anchor="w",

            padx=18,

            pady=(18, 5)
        )

        tk.Label(

            card,

            text=value,

            font=(
                "Segoe UI",
                22,
                "bold"
            ),

            fg=self.BLUE,

            bg=self.PANEL

        ).pack(

            anchor="w",

            padx=18
        )


# ============================================================
# START GUI
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = AttendanceGUI(
        root
    )

    root.mainloop()