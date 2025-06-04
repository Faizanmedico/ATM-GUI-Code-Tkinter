
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import datetime

# --- Backend Logic ---
class ATM:
    """Simulates the backend logic of an ATM."""
    def __init__(self):
        self.accounts = {
            "123456789": {"pin": "1234", "balance": 1500.00, "transactions": []},
            "987654321": {"pin": "4321", "balance": 750.00, "transactions": []},
        }
        self.current_account_number = None
        self.max_pin_attempts = 3
        self.pin_attempts = 0

    def validate_pin(self, account_num, pin):
        if account_num not in self.accounts:
            return False, "Account not found."

        if self.accounts[account_num]["pin"] == pin:
            self.current_account_number = account_num
            self.pin_attempts = 0
            return True, "Login successful!"
        else:
            self.pin_attempts += 1
            remaining_attempts = self.max_pin_attempts - self.pin_attempts
            if remaining_attempts > 0:
                return False, f"Incorrect PIN. {remaining_attempts} attempts remaining."
            else:
                return False, "Too many incorrect PIN attempts. Card blocked."

    def get_balance(self):
        if self.current_account_number:
            return self.accounts[self.current_account_number]["balance"]
        return None

    def record_transaction(self, type, amount):
        if self.current_account_number:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.accounts[self.current_account_number]["transactions"].append(
                f"{timestamp} - {type}: ${amount:.2f}"
            )

    def withdraw(self, amount):
        if not self.current_account_number:
            return False, "Please log in first."
        try:
            amount = float(amount)
        except ValueError:
            return False, "Invalid amount. Please enter a valid number."

        if amount <= 0:
            return False, "Withdrawal amount must be positive."

        if self.accounts[self.current_account_number]["balance"] >= amount:
            self.accounts[self.current_account_number]["balance"] -= amount
            self.record_transaction("Withdrawal", -amount)
            return True, f"Withdrawal successful. New balance: ${self.accounts[self.current_account_number]['balance']:.2f}"
        else:
            return False, "Insufficient funds."

    def deposit(self, amount):
        if not self.current_account_number:
            return False, "Please log in first."
        try:
            amount = float(amount)
        except ValueError:
            return False, "Invalid amount. Please enter a valid number."

        if amount <= 0:
            return False, "Deposit amount must be positive."

        self.accounts[self.current_account_number]["balance"] += amount
        self.record_transaction("Deposit", amount)
        return True, f"Deposit successful. New balance: ${self.accounts[self.current_account_number]['balance']:.2f}"

    def get_transaction_history(self):
        if self.current_account_number:
            return self.accounts[self.current_account_number]["transactions"]
        return []

    def logout(self):
        self.current_account_number = None
        self.pin_attempts = 0

# --- GUI Class ---
class ATM_GUI:
    def __init__(self, master):
        self.master = master
        master.title("Modern Tkinter ATM")
        master.geometry("900x650")
        master.resizable(False, False)
        master.configure(bg="#2c3e50")

        self.atm_backend = ATM()
        self.current_input_str = tk.StringVar()
        self.current_input_str.set("")

        self.screen_message_str = tk.StringVar()
        self.screen_message_str.set("Welcome to Sultan Bank! Please insert your card (Enter Account Number).")

        self.setup_styles()
        self.setup_ui()
        self.current_state = "ACCOUNT_ENTRY"
        self.temp_account_num = ""
        self.actual_pin_input = ""

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        self.font_large = ("Helvetica Neue", 16, "bold")
        self.font_medium = ("Helvetica Neue", 12)
        self.font_screen_text = ("Consolas", 18, "bold")

        style.configure("Screen.TFrame", background="#34495e", relief="groove", borderwidth=4)
        style.configure("Screen.TLabel", background="#34495e", foreground="#ecf0f1", font=self.font_large)
        style.configure("InputDisplay.TLabel", background="#ecf0f1", foreground="#2c3e50", 
                        font=self.font_screen_text, borderwidth=2, relief="sunken", anchor="e")

        style.configure("TButton", font=("Helvetica Neue", 14), background="#7f8c8d", 
                        foreground="#ecf0f1", relief="raised", borderwidth=3, padding=10)
        style.map("TButton",
                background=[('active', '#95a5a6')],
                foreground=[('disabled', '#bdc3c7')])

        style.configure("Green.TButton", background="#2ecc71", foreground="white")
        style.map("Green.TButton", background=[('active', '#27ae60')])

        style.configure("Orange.TButton", background="#f39c12", foreground="white")
        style.map("Orange.TButton", background=[('active', '#e67e22')])

        style.configure("Red.TButton", background="#e74c3c", foreground="white")
        style.map("Red.TButton", background=[('active', '#c0392b')])

        style.configure("Side.TButton", font=("Helvetica Neue", 12, "bold"), 
                        background="#3498db", foreground="white", relief="raised", borderwidth=2, padding=8)
        style.map("Side.TButton",
                background=[('active', '#2980b9')],
                foreground=[('disabled', '#bdc3c7')])

    def setup_ui(self):
        self.master.grid_columnconfigure(0, weight=0)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_columnconfigure(3, weight=0)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=0)

        # Screen Area
        screen_outer_frame = ttk.Frame(self.master, style="Screen.TFrame")
        screen_outer_frame.grid(row=0, column=1, columnspan=2, padx=20, pady=20, sticky="nsew")

        screen_inner_frame = ttk.Frame(screen_outer_frame, style="Screen.TFrame")
        screen_inner_frame.pack(fill="both", expand=True, padx=15, pady=15)

        self.screen_label = ttk.Label(screen_inner_frame, textvariable=self.screen_message_str,
                                    style="Screen.TLabel", wraplength=480, justify="left")
        self.screen_label.pack(pady=10, fill="both", expand=True)

        self.input_display = ttk.Label(screen_inner_frame, textvariable=self.current_input_str,
                                     style="InputDisplay.TLabel")
        self.input_display.pack(pady=(0, 10), padx=5, fill="x")

        # Side Action Buttons
        self.action_buttons_left_frame = tk.Frame(self.master, bg=self.master.cget('bg'))
        self.action_buttons_left_frame.grid(row=0, column=0, padx=15, pady=20, sticky="ns")

        self.action_buttons_right_frame = tk.Frame(self.master, bg=self.master.cget('bg'))
        self.action_buttons_right_frame.grid(row=0, column=3, padx=15, pady=20, sticky="ns")

        actions_left = ["Balance", "Withdraw", "Deposit", "History"]
        self.left_buttons = []
        for text in actions_left:
            btn = ttk.Button(self.action_buttons_left_frame, text=f">>{text}", style="Side.TButton",
                            command=lambda t=text: self.handle_side_action(t))
            btn.pack(pady=12, fill="x")
            self.left_buttons.append(btn)

        actions_right = ["<< Back", "<< Print", "<< Other", "<< Exit"]
        self.right_buttons = []
        for text in actions_right:
            if text == "<< Exit":
                cmd = self.confirm_cancel
            else:
                cmd = lambda t=text: self.handle_right_action(t)
            btn = ttk.Button(self.action_buttons_right_frame, text=text, style="Side.TButton", command=cmd)
            btn.pack(pady=12, fill="x")
            self.right_buttons.append(btn)
        self.disable_action_buttons()

        # Keypad Area
        keypad_frame = tk.Frame(self.master, bg="#34495e", bd=4, relief="ridge", padx=20, pady=20)
        keypad_frame.grid(row=1, column=0, columnspan=4, padx=20, pady=20, sticky="ew")

        keypad_buttons = [
            ('1', 'TButton'), ('2', 'TButton'), ('3', 'TButton'),
            ('4', 'TButton'), ('5', 'TButton'), ('6', 'TButton'),
            ('7', 'TButton'), ('8', 'TButton'), ('9', 'TButton'),
            ('CLEAR', 'Orange.TButton'), ('0', 'TButton'), ('ENTER', 'Green.TButton')
        ]

        for i, (text, style_name) in enumerate(keypad_buttons):
            row = i // 3
            col = i % 3
            
            if text == 'ENTER':
                cmd = lambda: self.process_input()
            elif text == 'CLEAR':
                cmd = self.clear_input
            else:
                cmd = lambda b=text: self.append_input(b)
                
            btn = ttk.Button(keypad_frame, text=text, style=style_name, command=cmd)
            btn.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

        cancel_btn = ttk.Button(keypad_frame, text="CANCEL", style="Red.TButton", command=self.confirm_cancel)
        cancel_btn.grid(row=4, column=0, columnspan=3, pady=15, padx=8, sticky="ew")

        for i in range(3):
            keypad_frame.grid_columnconfigure(i, weight=1)
        for i in range(4):
            keypad_frame.grid_rowconfigure(i, weight=1)

    def append_input(self, digit):
        current_text = self.current_input_str.get()
        if self.current_state == "PIN_ENTRY":
            if len(self.actual_pin_input) < 4:
                self.current_input_str.set(current_text + "*")
                self.actual_pin_input += digit
        elif self.current_state == "ACCOUNT_ENTRY":
            if len(current_text) < 9:
                self.current_input_str.set(current_text + digit)
        elif self.current_state in ["WITHDRAW_AMOUNT", "DEPOSIT_AMOUNT"]:
            if digit == '.' and '.' in current_text:
                return
            self.current_input_str.set(current_text + digit)

    def clear_input(self):
        self.current_input_str.set("")
        if self.current_state == "PIN_ENTRY":
            self.actual_pin_input = ""

    def process_input(self):
        entered_display_value = self.current_input_str.get()

        if self.current_state == "ACCOUNT_ENTRY":
            account_num = entered_display_value
            if account_num.strip() and account_num.isdigit() and len(account_num) == 9:
                self.screen_message_str.set("Please enter your 4-digit PIN:")
                self.current_input_str.set("")
                self.actual_pin_input = ""
                self.temp_account_num = account_num
                self.current_state = "PIN_ENTRY"
            else:
                self.screen_message_str.set("Invalid account number. Please enter a 9-digit number.")
                self.current_input_str.set("")

        elif self.current_state == "PIN_ENTRY":
            pin = self.actual_pin_input
            if pin.strip() and pin.isdigit() and len(pin) == 4:
                success, message = self.atm_backend.validate_pin(self.temp_account_num, pin)
                self.screen_message_str.set(message)
                self.current_input_str.set("")
                self.actual_pin_input = ""

                if success:
                    self.current_state = "MAIN_MENU"
                    self.display_main_menu()
                    self.enable_action_buttons()
                else:
                    if "Card blocked" in message:
                        messagebox.showerror("ATM Error", message)
                        self.reset_atm()
                    else:
                        self.screen_message_str.set(f"{message}\nPlease enter your PIN again:")
            else:
                self.screen_message_str.set("PIN must be 4 digits. Please try again.")
                self.actual_pin_input = ""

        elif self.current_state == "WITHDRAW_AMOUNT":
            amount_str = entered_display_value
            if not amount_str:
                self.screen_message_str.set("Amount cannot be empty. Enter amount to withdraw or CANCEL:")
                return
            try:
                amount = float(amount_str)
                success, message = self.atm_backend.withdraw(amount)
                self.screen_message_str.set(message)
                self.current_input_str.set("")
                if success:
                    self.display_main_menu()
                else:
                    self.screen_message_str.set(f"{message}\nEnter amount to withdraw or CANCEL:")
            except ValueError:
                self.screen_message_str.set("Invalid amount. Please enter a number.")
                self.current_input_str.set("")

        elif self.current_state == "DEPOSIT_AMOUNT":
            amount_str = entered_display_value
            if not amount_str:
                self.screen_message_str.set("Amount cannot be empty. Enter amount to deposit or CANCEL:")
                return
            try:
                amount = float(amount_str)
                success, message = self.atm_backend.deposit(amount)
                self.screen_message_str.set(message)
                self.current_input_str.set("")
                if success:
                    self.display_main_menu()
                else:
                    self.screen_message_str.set(f"{message}\nEnter amount to deposit or CANCEL:")
            except ValueError:
                self.screen_message_str.set("Invalid amount. Please enter a number.")
                self.current_input_str.set("")

    def display_main_menu(self):
        self.screen_message_str.set("Login successful!\n\nSelect an option using the side buttons:")
        self.current_input_str.set("")
        self.current_state = "MAIN_MENU"

    def handle_side_action(self, action):
        if self.current_state != "MAIN_MENU":
            self.screen_message_str.set("Please complete the current action or CANCEL to return.")
            return

        if action == "Balance":
            balance = self.atm_backend.get_balance()
            self.screen_message_str.set(f"Your current balance is: ${balance:.2f}\n\nSelect another option.")
            self.current_input_str.set("")
        elif action == "Withdraw":
            self.screen_message_str.set("Enter amount to withdraw, then press ENTER:")
            self.current_input_str.set("")
            self.current_state = "WITHDRAW_AMOUNT"
        elif action == "Deposit":
            self.screen_message_str.set("Enter amount to deposit, then press ENTER:")
            self.current_input_str.set("")
            self.current_state = "DEPOSIT_AMOUNT"
        elif action == "History":
            history = self.atm_backend.get_transaction_history()
            history_text = "\n".join(history) if history else "No transactions yet."
            messagebox.showinfo("Transaction History", history_text)
            self.screen_message_str.set("Transaction history viewed.\n\nSelect another option.")
            self.current_input_str.set("")

    def handle_right_action(self, action):
        if action == "<< Back":
            if self.current_state != "MAIN_MENU":
                self.display_main_menu()
                self.screen_message_str.set("Operation cancelled. Select another option.")
                self.current_input_str.set("")
            else:
                self.screen_message_str.set("You are already at the main menu.")
        elif action == "<< Print":
            messagebox.showinfo("Print", "Printing receipt...")
        elif action == "<< Other":
            messagebox.showinfo("Other Options", "No other options available yet.")

    def confirm_cancel(self):
        if messagebox.askyesno("Confirm Cancellation", "Do you want to cancel the current operation and log out?"):
            self.reset_atm()

    def reset_atm(self):
        self.atm_backend.logout()
        self.current_state = "ACCOUNT_ENTRY"
        self.screen_message_str.set("Thank you for using the ATM. Please insert your card (Enter Account Number).")
        self.current_input_str.set("")
        self.temp_account_num = ""
        self.actual_pin_input = ""
        self.disable_action_buttons()

    def enable_action_buttons(self):
        for btn in self.left_buttons:
            btn.config(state=tk.NORMAL)
        for btn in self.right_buttons:
            btn.config(state=tk.NORMAL)

    def disable_action_buttons(self):
        for btn in self.left_buttons:
            btn.config(state=tk.DISABLED)
        for btn in self.right_buttons:
            btn.config(state=tk.DISABLED)

# --- Main execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ATM_GUI(root)
    root.mainloop()
