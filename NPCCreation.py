import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.simpledialog import askstring
import pyperclip  # Import the pyperclip library

class SQLQueryCreator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TrinityCore NPC Creator")
        self.geometry("800x500")
        self.resizable(width=False, height=False)

        # Load Database Connection Configuration
        self.load_db_config()

        self.create_widgets()

        self.connection = None

    def create_widgets(self):
        self.entry_labels = [
            "entry",
            "modelid1",
            "name",
            "subname",
            "minlevel",
            "maxlevel",
        ]

        self.entries = {}
        for i, label in enumerate(self.entry_labels):
            ttk.Label(self, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            self.entries[label] = ttk.Entry(self)
            self.entries[label].grid(row=i, column=1, padx=5, pady=5, sticky="w")

        # Create a dropdown menu for unit_class
        ttk.Label(self, text="unit_class").grid(row=len(self.entry_labels), column=0, padx=5, pady=5, sticky="w")
        ## Show both options in dropdown menu
        self.unit_class_options = ["Warrior(Health Only)", "Warrior(Health Only)", "Mage(Health & Mana)"]
        self.unit_class_var = tk.StringVar()
        self.unit_class_dropdown = ttk.OptionMenu(self, self.unit_class_var, *self.unit_class_options, command=self.update_options)
        self.unit_class_dropdown = ttk.OptionMenu(self, self.unit_class_var, *self.unit_class_options)
        self.unit_class_dropdown.grid(row=len(self.entry_labels), column=1, padx=5, pady=5, sticky="w")




        self.create_button = ttk.Button(self, text="Create Query", command=self.create_query)
        self.create_button.grid(row=len(self.entry_labels) + 1, column=1, padx=5, pady=10, sticky="e")

        self.copy_button = ttk.Button(self, text="Copy Query", command=self.copy_query)
        self.copy_button.grid(row=len(self.entry_labels) + 1, column=0, padx=5, pady=10, sticky="w")

        self.search_button = ttk.Button(self, text="Search ModelID1", command=self.search_modelid1)
        self.search_button.grid(row=len(self.entry_labels) + 1, column=2, padx=5, pady=10, sticky="w")

        self.result_tree = ttk.Treeview(self, columns=("ModelID1", "Name"), show="headings")
        self.result_tree.heading("ModelID1", text="ModelID1")
        self.result_tree.heading("Name", text="Name")
        self.result_tree.grid(row=len(self.entry_labels) + 2, columnspan=3, padx=10, pady=5)

        # Create the main menu
        main_menu = tk.Menu(self)
        self.config(menu=main_menu)

        # Create the "Database" menu
        database_menu = tk.Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="SETTINGS", menu=database_menu)

        # Add "Configure" option to the "Database" menu
        database_menu.add_command(label="Configure", command=self.configure_database)

    def create_query(self):
        query_template = self.generate_query()

        try:
            self.execute_query(query_template)
        except ValueError as err:
            messagebox.showerror("Error", f"Error: {err}")

    def execute_query(self, query):
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            cursor.close()
            self.connection.close()
            messagebox.showinfo("Success", "Query executed and data inserted into the database.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
            if self.connection:
                self.connection.rollback()

    def test_connection(self):
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            messagebox.showinfo("Success", "Successfully connected to the database.")
            self.connection.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
            if self.connection:
                self.connection.rollback()

    def copy_query(self):
        query = self.generate_query()
        pyperclip.copy(query)
        messagebox.showinfo("Query Copied", "The SQL query has been copied to the clipboard.")

    def generate_query(self):
        values = [self.entries[label].get() for label in self.entry_labels]

        # Ensure the list has enough elements
        while len(values) < 13:
            values.append("")  # Add empty strings for missing elements

        # Handle empty value for IconName

        # Wrap the name value with single quotes
        values[2] = f"'{values[2]}'"
        values[3] = f"'{values[3]}'"

        # Determine the unit_class value based on the selection
        if self.unit_class_var.get() == "Warrior(Health Only)":
            unit_class_value = 1
        else:
            unit_class_value = 2

        # Create a modified query template with placeholders
        query_template = (
            f"INSERT INTO `creature_template` "
            f"(`entry`, `difficulty_entry_1`, `difficulty_entry_2`, `difficulty_entry_3`, "
            f"`KillCredit1`, `KillCredit2`, `modelid1`, `modelid2`, `modelid3`, `modelid4`, "
            f"`name`, `subname`, `IconName`, `gossip_menu_id`, `minlevel`, `maxlevel`, "
            f"`exp`, `faction`, `npcflag`, `speed_walk`, `speed_run`, `scale`, `rank`, "
            f"`dmgschool`, `BaseAttackTime`, `RangeAttackTime`, `BaseVariance`, `RangeVariance`, "
            f"`unit_class`, `unit_flags`, `unit_flags2`, `dynamicflags`, `family`, `type`, "
            f"`type_flags`, `lootid`, `pickpocketloot`, `skinloot`, `PetSpellDataId`, `VehicleId`, "
            f"`mingold`, `maxgold`, `AIName`, `MovementType`, `HoverHeight`, `HealthModifier`, "
            f"`ManaModifier`, `ArmorModifier`, `DamageModifier`, `ExperienceModifier`, `RacialLeader`, "
            f"`movementId`, `RegenHealth`, `mechanic_immune_mask`, `spell_school_immune_mask`, "
            f"`flags_extra`, `ScriptName`, `VerifiedBuild`) VALUES "
            f"({values[0]}, 0, 0, 0, 0, 0, {values[1]}, 0, 0, 0, {values[2]}, {values[3]}, NULL, "
            f"0, {values[4]}, {values[5]}, 0, 35, 0, 1, 1.14286, 1, 0, 0, 2000, 2000, 1, 1, {unit_class_value}, 512, 2048, 0, "
            f"0, 7, 0, 0, 0, 0, 0, 0, 0, 0, '', 0, 1, 1.02, 1, 1, 1, 1, 0, 0, 1, 0, 0, 66, '', 12340);"
        )

        return query_template

    def search_modelid1(self):
        search_keyword = askstring("Search ModelID1", "Enter a keyword to search for:")
        if search_keyword is None:
            return

        try:
            self.connection = mysql.connector.connect(**self.db_config)
            cursor = self.connection.cursor()

            # Execute the SQL query to select modelid1 and name from creature_template
            query = f"SELECT modelid1, name FROM creature_template WHERE name LIKE '%{search_keyword}%'"
            cursor.execute(query)

            # Clear the Treeview
            self.result_tree.delete(*self.result_tree.get_children())

            # Fetch all the rows returned by the query
            results = cursor.fetchall()

            # Display the results in the Treeview
            for row in results:
                modelid1, name = row
                self.result_tree.insert("", "end", values=(modelid1, name))

            cursor.close()
            self.connection.close()

            # Scroll to the top of the table
            self.result_tree.yview_moveto(0)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
            if self.connection:
                self.connection.rollback()

    def configure_database(self):
        # Create a new Toplevel window for configuration
        config_window = tk.Toplevel(self)
        config_window.title("Database Configuration")
        config_window.geometry("400x250")
        config_window.resizable(width=False, height=False)

        ttk.Label(config_window, text="Database Configuration").grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        # Access the entry_labels list from the main app
        self.host_entry = ttk.Entry(config_window)
        self.host_entry.grid(row=1, column=1, padx=10, pady=5)
        self.host_entry.insert(tk.END, self.db_config["host"])

        self.port_entry = ttk.Entry(config_window)
        self.port_entry.grid(row=2, column=1, padx=10, pady=5)
        self.port_entry.insert(tk.END, self.db_config["port"])

        self.user_entry = ttk.Entry(config_window)
        self.user_entry.grid(row=3, column=1, padx=10, pady=5)
        self.user_entry.insert(tk.END, self.db_config["user"])

        self.password_entry = ttk.Entry(config_window)
        self.password_entry.grid(row=4, column=1, padx=10, pady=5)
        self.password_entry.insert(tk.END, self.db_config["password"])

        self.database_entry = ttk.Entry(config_window)
        self.database_entry.grid(row=5, column=1, padx=10, pady=5)
        self.database_entry.insert(tk.END, self.db_config["database"])

        ttk.Button(config_window, text="Save", command=lambda: self.save_configuration(config_window)).grid(
            row=6, column=0, columnspan=2, padx=10, pady=5
        )

    def save_configuration(self, config_window):
        # Get the updated values from the entries
        host = self.host_entry.get()
        port = self.port_entry.get()
        user = self.user_entry.get()
        password = self.password_entry.get()
        database = self.database_entry.get()

        # Update the database configuration dictionary
        self.db_config["host"] = host
        self.db_config["port"] = port
        self.db_config["user"] = user
        self.db_config["password"] = password
        self.db_config["database"] = database

        # Close the configuration window
        config_window.destroy()
        save_db_config = messagebox.askyesno("Save Configuration", "Would you like to save the configuration?")
        if save_db_config:
            self.save_db_config()
        test_connection = messagebox.askyesno("Test Connection", "Would you like to test the connection?")
        if test_connection:
            self.test_connection()

    def save_db_config(self):
        try:
            with open("config.txt", "w") as file:
                for key, value in self.db_config.items():
                    file.write(f"{key}={value}\n")
            print("Configuration saved to 'config.txt'")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")

    def load_db_config(self):
        try:
            with open("config.txt", "r") as file:
                self.db_config = {}
                for line in file:
                    key, value = line.strip().split("=")
                    self.db_config[key] = value
        except FileNotFoundError:
            # If the config file doesn't exist, use the default config
            self.db_config = {
                "host": "localhost",
                "port": 3306,
                "user": "root",
                "password": "ascent",
                "database": "world",  # Replace this with your actual database name
            }
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {e}")

    def update_options(self, selection):
        if selection == "Mage(Health & Mana)":
            self.unit_class_var.set(self.unit_class_options[1])
        else:
            self.unit_class_var.set(self.unit_class_options[0])

if __name__ == "__main__":
    app = SQLQueryCreator()
    app.mainloop()
