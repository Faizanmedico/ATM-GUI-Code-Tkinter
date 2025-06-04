import tkinter as tk
from tkinter import messagebox, scrolledtext
import datetime

class ATM:
    """Simulates the backend logic of an ATM."""
    def __init__(self):
        # In a real application, this would be loaded from a database or secure file.
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
            self.pin_attempts = 0 # Reset attempts on successful login
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

        if not isinstance(amount, (int, float)) or amount <= 0:
            return False, "Invalid amount. Please enter a positive number."

        if self.accounts[self.current_account_number]["balance"] >= amount:
            self.accounts[self.current_account_number]["balance"] -= amount
            self.record_transaction("Withdrawal", -amount) # Store as negative for withdrawal
            return True, f"Withdrawal successful. New balance: ${self.accounts[self.current_account_number]['balance']:.2f}"
        else:
            return False, "Insufficient funds."

    def deposit(self, amount):
        if not self.current_account_number:
            return False, "Please log in first."

        if not isinstance(amount, (int, float)) or amount <= 0:
            return False, "Invalid amount. Please enter a positive number."

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

class ATM_GUI:
    """Handles the Tkinter GUI for the ATM."""
    def __init__(self, master):
        self.master = master
        master.title("Python Tkinter ATM")
        master.geometry("800x600") # Set a fixed size for consistency
        master.resizable(False, False) # Disable resizing

        self.atm_backend = ATM()
        self.current_input = tk.StringVar()
        self.current_input.set("") # Stores digits entered via keypad

        self.screen_message = tk.StringVar()
        self.screen_message.set("Welcome! Please insert your card (Enter Account Number).")

        self.setup_ui()
        self.current_state = "ACCOUNT_ENTRY" # State machine for ATM flow

    def setup_ui(self):
        # --- Screen Area ---
        screen_frame = tk.Frame(self.master, bg="lightgray", bd=5, relief="sunken")
        screen_frame.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.screen_label = tk.Label(screen_frame, textvariable=self.screen_message,
                                     font=("Arial", 14), bg="lightgray", wraplength=450, justify="left")
        self.screen_label.pack(pady=10, padx=10, fill="both", expand=True)

        self.input_display = tk.Label(screen_frame, textvariable=self.current_input,
                                      font=("Arial", 16, "bold"), bg="white", bd=2, relief="sunken", anchor="e")
        self.input_display.pack(pady=5, padx=10, fill="x")

        # --- Side Action Buttons (Simplified) ---
        self.action_buttons_frame = tk.Frame(self.master)
        self.action_buttons_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        self.action_buttons_right_frame = tk.Frame(self.master)
        self.action_buttons_right_frame.grid(row=0, column=3, padx=10, pady=10, sticky="ns")

        # Example action buttons - adjust as needed
        actions_left = ["Balance", "Withdraw", "Deposit", "History"]
        self.left_buttons = []
        for i, text in enumerate(actions_left):
            btn = tk.Button(self.action_buttons_frame, text=f">>{text}", font=("Arial", 12), width=10, height=2,
                            command=lambda t=text: self.handle_side_action(t))
            btn.pack(pady=5)
            self.left_buttons.append(btn)

        # Right side buttons - for navigation/selection if needed (not active initially)
        actions_right = ["<< Back", "<< Next", "<< Option3", "<< Option4"]
        self.right_buttons = []
        for i, text in enumerate(actions_right):
            btn = tk.Button(self.action_buttons_right_frame, text=text, font=("Arial", 12), width=10, height=2, state=tk.DISABLED)
            btn.pack(pady=5)
            self.right_buttons.append(btn)
        self.disable_action_buttons()


        # --- Keypad Area ---
        keypad_frame = tk.Frame(self.master, bd=2, relief="groove", padx=10, pady=10)
        keypad_frame.grid(row=1, column=1, columnspan=3, padx=10, pady=10)

        buttons = [
            '1', '2', '3',
            '4', '5', '6',
            '7', '8', '9',
            'CLEAR', '0', 'ENTER'
        ]

        row_val = 0
        col_val = 0
        for button_text in buttons:
            if button_text == 'CLEAR':
                btn = tk.Button(keypad_frame, text=button_text, font=("Arial", 14), bg="orange", fg="white",
                                command=self.clear_input, width=8, height=2)
            elif button_text == 'ENTER':
                btn = tk.Button(keypad_frame, text=button_text, font=("Arial", 14), bg="green", fg="white",
                                command=self.process_input, width=8, height=2)
            else:
                btn = tk.Button(keypad_frame, text=button_text, font=("Arial", 14, "bold"),
                                command=lambda b=button_text: self.append_input(b), width=8, height=2)

            btn.grid(row=row_val, column=col_val, padx=5, pady=5)
            col_val += 1
            if col_val > 2:
                col_val = 0
                row_val += 1

        # --- Special ATM Buttons (CANCEL) ---
        cancel_btn = tk.Button(keypad_frame, text="CANCEL", font=("Arial", 14), bg="red", fg="white",
                               command=self.confirm_cancel, width=8, height=2)
        # Position CANCEL button strategically (e.g., next to or below ENTER)
        # We'll place it in its own row for visual separation, as in typical ATMs
        cancel_btn.grid(row=row_val, column=0, columnspan=3, pady=10) # Centered below other buttons

        # Configure column weights to make the screen area expand
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_rowconfigure(0, weight=1) # Allow screen to take up space

    def append_input(self, digit):
        current_text = self.current_input.get()
        # Limit input length if necessary (e.g., for PINs or amounts)
        if self.current_state == "PIN_ENTRY" and len(current_text) < 4: # PIN is 4 digits
             self.current_input.set(current_text + "*") # Mask PIN
             self.actual_pin_input += digit # Store actual digits
        elif self.current_state == "ACCOUNT_ENTRY" and len(current_text) < 9: # Account is 9 digits
            self.current_input.set(current_text + digit)
        elif self.current_state in ["WITHDRAW_AMOUNT", "DEPOSIT_AMOUNT"]:
            # Allow decimals for amounts
            if digit == '.' and '.' in current_text:
                return # Don't allow multiple decimals
            self.current_input.set(current_text + digit)


    def clear_input(self):
        self.current_input.set("")
        if self.current_state == "PIN_ENTRY":
            self.actual_pin_input = ""

    def process_input(self):
        entered_value = self.current_input.get()
        actual_value = entered_value # For non-PIN inputs

        if self.current_state == "ACCOUNT_ENTRY":
            account_num = entered_value
            if account_num:
                self.screen_message.set("Please enter your PIN:")
                self.current_input.set("")
                self.actual_pin_input = "" # To store the unmasked PIN
                self.temp_account_num = account_num # Store it temporarily
                self.current_state = "PIN_ENTRY"
            else:
                self.screen_message.set("Account number cannot be empty. Please try again.")

        elif self.current_state == "PIN_ENTRY":
            pin = self.actual_pin_input # Use the unmasked PIN
            if pin:
                success, message = self.atm_backend.validate_pin(self.temp_account_num, pin)
                self.screen_message.set(message)
                self.current_input.set("")
                self.actual_pin_input = ""

                if success:
                    self.current_state = "MAIN_MENU"
                    self.display_main_menu()
                    self.enable_action_buttons()
                else:
                    if "Card blocked" in message:
                        messagebox.showerror("Error", message)
                        self.reset_atm() # Reset or exit after card blocked
                    else:
                        # Stay in PIN_ENTRY for more attempts
                        self.screen_message.set(f"{message}\nPlease enter your PIN again:")
            else:
                self.screen_message.set("PIN cannot be empty. Please try again.")

        elif self.current_state == "WITHDRAW_AMOUNT":
            try:
                amount = float(entered_value)
                success, message = self.atm_backend.withdraw(amount)
                self.screen_message.set(message)
                self.current_input.set("")
                if success:
                    self.display_main_menu() # Go back to main menu
                else:
                    # Stay on withdrawal input if error, or go back to main menu
                    self.screen_message.set(f"{message}\nEnter amount to withdraw or CANCEL:")
            except ValueError:
                self.screen_message.set("Invalid amount. Please enter a number.")
                self.current_input.set("")

        elif self.current_state == "DEPOSIT_AMOUNT":
            try:
                amount = float(entered_value)
                success, message = self.atm_backend.deposit(amount)
                self.screen_message.set(message)
                self.current_input.set("")
                if success:
                    self.display_main_menu() # Go back to main menu
                else:
                     self.screen_message.set(f"{message}\nEnter amount to deposit or CANCEL:")
            except ValueError:
                self.screen_message.set("Invalid amount. Please enter a number.")
                self.current_input.set("")

    def display_main_menu(self):
        self.screen_message.set("Select an option using the side buttons:")
        self.current_input.set("")
        self.current_state = "MAIN_MENU"

    def handle_side_action(self, action):
        if self.current_state != "MAIN_MENU":
            self.screen_message.set("Please complete the current action or CANCEL.")
            return

        if action == "Balance":
            balance = self.atm_backend.get_balance()
            self.screen_message.set(f"Your current balance is: ${balance:.2f}\n\nSelect another option.")
            self.current_input.set("")
        elif action == "Withdraw":
            self.screen_message.set("Enter amount to withdraw, then press ENTER:")
            self.current_input.set("")
            self.current_state = "WITHDRAW_AMOUNT"
        elif action == "Deposit":
            self.screen_message.set("Enter amount to deposit, then press ENTER:")
            self.current_input.set("")
            self.current_state = "DEPOSIT_AMOUNT"
        elif action == "History":
            history = self.atm_backend.get_transaction_history()
            history_text = "\n".join(history) if history else "No transactions yet."
            # Use a message box or a dedicated scrollable screen area for history
            messagebox.showinfo("Transaction History", history_text)
            self.screen_message.set("Select another option.") # Go back to main menu after showing history
            self.current_input.set("")

    def confirm_cancel(self):
        if messagebox.askyesno("Confirm Cancel", "Do you want to cancel the current operation and log out?"):
            self.reset_atm()

    def reset_atm(self):
        self.atm_backend.logout()
        self.current_state = "ACCOUNT_ENTRY"
        self.screen_message.set("Thank you for using the ATM. Please insert your card (Enter Account Number).")
        self.current_input.set("")
        self.temp_account_num = ""
        self.actual_pin_input = ""
        self.disable_action_buttons()


    def enable_action_buttons(self):
        for btn in self.left_buttons:
            btn.config(state=tk.NORMAL)
        # You might enable right buttons depending on context
        # for btn in self.right_buttons:
        #     btn.config(state=tk.NORMAL)

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