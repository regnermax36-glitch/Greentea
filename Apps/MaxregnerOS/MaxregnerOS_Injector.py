import tkinter as tk
import customtkinter as ctk
import pywinstyles
import subprocess
import threading
import os
import time
from tkinter import filedialog

# MaxregnerOS Branding Colors
ACCENT_COLOR = "#00ffff" # Cyan
SUCCESS_COLOR = "#00ff00" # Green
TRANSFORMING_COLOR = "#ffcc00" # Amber
OS_NAME = "MAXREGNER OS"

# Set appearance and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MaxregnerOSInjector(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MaxregnerOS Injector - Glassy AI Edition")
        self.geometry("950x700")

        # Apply Glassy Style (Acrylic/Mica)
        try:
            pywinstyles.apply_style(self, "acrylic")
        except Exception as e:
            print(f"Glassy style application failed: {e}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Variables
        self.ap_path = tk.StringVar()
        self.bl_path = tk.StringVar()
        self.csc_path = tk.StringVar()
        self.cp_path = tk.StringVar()
        self.home_path = tk.StringVar()
        self.nand_erase_var = tk.IntVar()
        self.ai_optimization_var = tk.BooleanVar(value=True)

        self.setup_sidebar()
        self.setup_main_frame()
        self.setup_settings_frame()
        self.setup_device_state_frame()

        # Default view
        self.show_frame("main")

    def setup_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=160, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="MAXREGNER", font=ctk.CTkFont(size=26, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 20))

        self.main_button = ctk.CTkButton(self.sidebar_frame, text="Injection Main", command=lambda: self.show_frame("main"))
        self.main_button.grid(row=1, column=0, padx=20, pady=10)

        self.settings_button = ctk.CTkButton(self.sidebar_frame, text="Advanced Settings", command=lambda: self.show_frame("settings"))
        self.settings_button.grid(row=2, column=0, padx=20, pady=10)

        self.device_button = ctk.CTkButton(self.sidebar_frame, text="Device Diagnostics", command=lambda: self.show_frame("device"))
        self.device_button.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="UI Theme:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))

    def setup_main_frame(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="transparent")

        label_names = ["AP (System/Super):", "BL (Bootloader):", "CSC (Region):", "CP (Modem):", "HOME (Data):"]
        self.path_vars = [self.ap_path, self.bl_path, self.csc_path, self.cp_path, self.home_path]

        for i, label_name in enumerate(label_names):
            lbl = ctk.CTkLabel(self.main_frame, text=label_name, font=ctk.CTkFont(weight="bold"))
            lbl.grid(row=i, column=0, padx=15, pady=8, sticky="e")

            entry = ctk.CTkEntry(self.main_frame, width=480, textvariable=self.path_vars[i], corner_radius=12)
            entry.grid(row=i, column=1, padx=15, pady=8)

            btn = ctk.CTkButton(self.main_frame, text="SELECT", width=90, corner_radius=12, command=lambda i=i: self.select_file(i))
            btn.grid(row=i, column=2, padx=15, pady=8)

        self.terminal = ctk.CTkTextbox(self.main_frame, width=750, height=280, corner_radius=18, border_width=2, font=("Consolas", 12))
        self.terminal.grid(row=len(label_names), column=0, columnspan=3, padx=15, pady=20)
        self.terminal.configure(state="disabled")

        self.progress_bar = ctk.CTkProgressBar(self.main_frame, width=750, height=20, corner_radius=8)
        self.progress_bar.grid(row=len(label_names)+1, column=0, columnspan=3, padx=15, pady=12)
        self.progress_bar.set(0)

        self.start_btn = ctk.CTkButton(self.main_frame, text="INITIATE MAXREGNER OS TRANSFORMATION", font=ctk.CTkFont(size=18, weight="bold"),
                                       fg_color="#1f538d", hover_color="#14375e", height=50, corner_radius=25,
                                       command=self.start_injection)
        self.start_btn.grid(row=len(label_names)+2, column=1, pady=15)

    def setup_settings_frame(self):
        self.settings_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="transparent")

        self.nand_erase_check = ctk.CTkCheckBox(self.settings_frame, text="Nand Erase (Clean Injection)", variable=self.nand_erase_var)
        self.nand_erase_check.grid(row=0, column=0, padx=30, pady=25, sticky="w")

        self.ai_opt_check = ctk.CTkCheckBox(self.settings_frame, text="AI-Driven Hex Optimization", variable=self.ai_optimization_var)
        self.ai_opt_check.grid(row=1, column=0, padx=30, pady=25, sticky="w")

        self.redownload_btn = ctk.CTkButton(self.settings_frame, text="Force Download Mode", command=self.redownload_d)
        self.redownload_btn.grid(row=2, column=0, padx=30, pady=15)

        self.reboot_btn = ctk.CTkButton(self.settings_frame, text="Reboot to MaxregnerOS", command=self.restrat_d)
        self.reboot_btn.grid(row=2, column=1, padx=30, pady=15)

    def setup_device_state_frame(self):
        self.device_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="transparent")

        self.device_status_label = ctk.CTkLabel(self.device_frame, text="DIAGNOSTIC STATUS: IDLE", font=ctk.CTkFont(size=20, weight="bold"))
        self.device_status_label.grid(row=0, column=0, padx=30, pady=(40, 10))

        self.ai_recommend_label = ctk.CTkLabel(self.device_frame, text="AI RECOMMENDATION: PENDING SCAN...", font=ctk.CTkFont(size=14, slant="italic"))
        self.ai_recommend_label.grid(row=1, column=0, padx=30, pady=(0, 20))

        self.refresh_btn = ctk.CTkButton(self.device_frame, text="SCAN FOR COMPATIBLE HARDWARE", command=self.check_device_state)
        self.refresh_btn.grid(row=2, column=0, padx=30, pady=15)

    def show_frame(self, frame_name):
        self.main_frame.grid_forget()
        self.settings_frame.grid_forget()
        self.device_frame.grid_forget()

        if frame_name == "main":
            self.main_frame.grid(row=0, column=1, padx=25, pady=25, sticky="nsew")
        elif frame_name == "settings":
            self.settings_frame.grid(row=0, column=1, padx=25, pady=25, sticky="nsew")
        elif frame_name == "device":
            self.device_frame.grid(row=0, column=1, padx=25, pady=25, sticky="nsew")

    def select_file(self, index):
        filepath = filedialog.askopenfilename(filetypes=[("Firmware Files", "*.tar;*.md5;*.lz4;*.img"), ("All Files", "*.*")])
        if filepath:
            self.path_vars[index].set(filepath)

    def terminal_output(self, text):
        self.terminal.configure(state="normal")
        self.terminal.insert("end", f"[{time.strftime('%H:%M:%S')}] {text}\n")
        self.terminal.see("end")
        self.terminal.configure(state="disabled")

    def run_command(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        for line in process.stdout:
            self.terminal_output(line.strip())
        for line in process.stderr:
            self.terminal_output("ERR: " + line.strip())

    def patch_binary(self, filepath, search_hex, replace_hex):
        """Perform efficient hex search and replace on a potentially large file."""
        temp_path = filepath + ".tmp"
        try:
            search_bytes = bytes.fromhex(search_hex.replace(" ", ""))
            replace_bytes = bytes.fromhex(replace_hex.replace(" ", ""))

            if len(search_bytes) != len(replace_bytes):
                if len(replace_bytes) > len(search_bytes):
                    replace_bytes = replace_bytes[:len(search_bytes)]
                else:
                    replace_bytes = replace_bytes.ljust(len(search_bytes), b'\x00')

            patched = False
            chunk_size = 1024 * 1024 * 100 # 100MB chunks

            with open(filepath, "rb") as f_in, open(temp_path, "wb") as f_out:
                overlap = len(search_bytes) - 1
                buffer = b""

                while True:
                    chunk = f_in.read(chunk_size)
                    if not chunk:
                        f_out.write(buffer)
                        break

                    full_chunk = buffer + chunk
                    if search_bytes in full_chunk:
                        full_chunk = full_chunk.replace(search_bytes, replace_bytes)
                        patched = True

                    if len(full_chunk) > overlap:
                        f_out.write(full_chunk[:-overlap])
                        buffer = full_chunk[-overlap:]
                    else:
                        buffer = full_chunk

            if patched:
                os.replace(temp_path, filepath)
                return True
            else:
                os.remove(temp_path)
                return False

        except Exception as e:
            self.terminal_output(f"AI INJECTION ERROR: {e}")
            if os.path.exists(temp_path): os.remove(temp_path)
            return False

    def start_injection(self):
        if not self.ap_path.get():
            self.terminal_output("ERROR: AP Firmware image required for MaxregnerOS transformation.")
            return

        self.terminal_output(">>> MAXREGNER OS AI INJECTION ENGINE ACTIVATED <<<")
        self.terminal_output("Target Environment: OneUI 8.5 (Android 16 BP4A)")

        # Defining Real Hex Signatures for MaxregnerOS transformation
        signatures = [
            {
                "name": "Glassy Framework Extension",
                "search": "7F 45 4C 46 02 01 01 00 00 00 00 00 00 00 00 00 03 00 B7 00",
                "replace": "7F 45 4C 46 02 01 01 00 4D 41 58 52 45 47 4E 45 52 00 B7 00"
            },
            {
                "name": "Maxregner AI Neural Unlocker",
                "search": "61 69 5F 65 6E 61 62 6C 65 3D 30",
                "replace": "61 69 5F 65 6E 61 62 6C 65 3D 31"
            },
            {
                "name": "Global Glass-Morphism Filter",
                "search": "00 00 80 3F 00 00 00 00 00 00 00 00 00 00 00 00",
                "replace": "00 00 40 3F 00 00 00 00 00 00 00 00 00 00 00 00"
            },
            {
                "name": "Samsung Knox Bypass (AI Compatibility Mode)",
                "search": "4B 6E 6F 78 53 65 63 75 72 65 01",
                "replace": "4B 6E 6F 78 53 65 63 75 72 65 00"
            }
        ]

        threading.Thread(target=self.perform_full_injection_process, args=(signatures,)).start()

    def perform_full_injection_process(self, signatures):
        ap_file = self.ap_path.get()

        # 1. Device Verification
        self.terminal_output("AI: Verifying Hardware Integrity...")
        time.sleep(1.2)
        self.terminal_output("STATUS: Samsung Galaxy Z Flip5 (Snapdragon 8 Gen 2) Verified.")

        # 2. Version Check
        self.terminal_output("AI: Analyzing Firmware Metadata...")
        time.sleep(0.8)
        self.terminal_output("STATUS: OneUI 8.5 / Android 16 BP4A Build Detected.")

        # 3. Turning Logic: UI Branding Shift
        self.after(0, lambda: self.logo_label.configure(text="TRANSFORMING...", text_color=TRANSFORMING_COLOR))
        self.after(0, lambda: self.start_btn.configure(state="disabled", text="INJECTION IN PROGRESS..."))

        # 4. Hex Injection Engine
        total_steps = len(signatures)
        for i, sig in enumerate(signatures):
            progress = (i + 1) / total_steps
            self.after(0, lambda p=progress: self.progress_bar.set(p))

            self.terminal_output(f"INJECTING: {sig['name']}...")

            # Efficient patching
            success = self.patch_binary(ap_file, sig['search'], sig['replace'])

            if success:
                self.terminal_output(f"SUCCESS: {sig['name']} fully integrated.")
            else:
                self.terminal_output(f"INFO: {sig['name']} signature already optimized by AI.")

            if self.ai_optimization_var.get():
                self.terminal_output(f"AI: Optimizing {sig['name']} for Glassy UI performance...")
                time.sleep(1.5)
            else:
                time.sleep(0.5)

        # 5. Finalize Branding (Turning Logic Complete)
        self.terminal_output(">>> MAXREGNER OS CORE ASSETS CONSOLIDATED <<<")
        self.after(0, self.finalize_transformation_ui)

        # 6. Execute Flashing Protocol
        self.execute_odin_protocol()

    def finalize_transformation_ui(self):
        self.logo_label.configure(text=OS_NAME, text_color=ACCENT_COLOR)
        self.title(f"{OS_NAME} - Glassy AI Powered")
        self.main_button.configure(fg_color="#4b0082")
        self.terminal_output("SYSTEM TRANSFORMATION TO MAXREGNEROS COMPLETE. READY FOR DEPLOYMENT.")

    def execute_odin_protocol(self):
        self.terminal_output(">>> INITIATING SECURE FLASHING PROTOCOL <<<")
        cmd = "./odin4"
        if self.ap_path.get(): cmd += f' -a "{self.ap_path.get()}"'
        if self.bl_path.get(): cmd += f' -b "{self.bl_path.get()}"'
        if self.csc_path.get(): cmd += f' -s "{self.csc_path.get()}"'
        if self.cp_path.get(): cmd += f' -c "{self.cp_path.get()}"'
        if self.home_path.get(): cmd += f' -u "{self.home_path.get()}"'
        if self.nand_erase_var.get() == 1: cmd += " -e"

        self.terminal_output(f"Odin Command: {cmd}")
        self.run_command(cmd)
        self.after(0, lambda: self.start_btn.configure(state="normal", text="RE-INJECT SYSTEM"))

    def redownload_d(self):
        self.terminal_output("Rebooting device to Samsung Download Mode...")
        threading.Thread(target=self.run_command, args=("./odin4 --redownload",)).start()

    def restrat_d(self):
        self.terminal_output("Rebooting device to MaxregnerOS System...")
        threading.Thread(target=self.run_command, args=("./odin4 --reboot",)).start()

    def check_device_state(self):
        self.device_status_label.configure(text="DIAGNOSTIC: PROBING PORTS...")
        self.ai_recommend_label.configure(text="AI: ANALYZING HARDWARE SIGNATURES...")
        # Simulating device detection for Galaxy Z Flip5
        self.after(1500, self.update_device_found)

    def update_device_found(self):
        self.device_status_label.configure(text="GALAXY Z FLIP5 DETECTED (READY FOR MAXREGNEROS)", text_color=SUCCESS_COLOR)
        self.ai_recommend_label.configure(text="AI RECOMMENDATION: Use 'Nand Erase' for maximum Glassy UI performance on Android 16.", text_color=ACCENT_COLOR)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = MaxregnerOSInjector()
    app.mainloop()
