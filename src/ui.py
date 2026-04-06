import customtkinter as ctk
from tkinter import messagebox
import pystray
from PIL import Image
import threading
import asyncio
import sys
import os
import uuid
from typing import Optional
from src.security import load_credentials, clear_credentials
from src.config import settings, Theme

class ModernAgentUI(ctk.CTk):
    def __init__(self, agent_worker):
        super().__init__()
        self.agent = agent_worker
        self.agent.status_callback = self.update_status
        self.title("TRAE Mobile Agent")
        self.geometry("480x780")
        self.set_window_icon()
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=Theme.BG_BASE)
        self.protocol("WM_DELETE_WINDOW", self.hide_window)
        self.bind("<Unmap>", self.on_minimize)
        self.create_widgets()
        self.check_initial_state()
        self.tray_icon = None
        self.setup_tray()

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.main_frame = ctk.CTkFrame(self, fg_color=Theme.BG_BASE, corner_radius=0)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.pack(pady=(40, 20), fill="x")
        self.logo_label = ctk.CTkLabel(self.header_frame, text="TRAE", font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=32, weight="bold"), text_color=Theme.BRAND_GREEN)
        self.logo_label.pack()
        self.subtitle_label = ctk.CTkLabel(self.header_frame, text="MOBILE AGENT", font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=12, weight="bold"), text_color=Theme.TEXT_SECONDARY)
        self.subtitle_label.pack()
        self.info_button = ctk.CTkButton(self.main_frame, text="i", width=25, height=25, corner_radius=12, fg_color="transparent", border_width=1, border_color=Theme.BORDER_SUBTLE, text_color=Theme.TEXT_SECONDARY, font=ctk.CTkFont(family=Theme.FONT_MONO, size=14, weight="bold"), hover_color=Theme.BG_SECONDARY, command=self.show_info_popup)
        self.info_button.place(relx=0.95, rely=0.03, anchor="ne")
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=20)

    def set_window_icon(self):
        try:
            icon_ico = os.path.join(os.path.dirname(__file__), "..", "TRAE_Mobile.ico")
            icon_png = os.path.join(os.path.dirname(__file__), "..", "TRAE_Mobile.png")
            if os.path.exists(icon_ico):
                self.iconbitmap(icon_ico)
            elif os.path.exists(icon_png):
                img = Image.open(icon_png)
                photo = ctk.CTkImage(light_image=img, dark_image=img)
                self.iconphoto(False, photo._light_image)
        except Exception:
            pass

    def show_info_popup(self):
        info_text = ("TRAE Mobile Agent\n\nVersion: 1.0.0\nAuthor: HighMark [ Marco N. ]\nCompany: YecoAI\nWebsite: https://trae-mobile.yecoai.com\n\nPackage: com.yecoai.traemobile\n© 2026 YecoAI - All Rights Reserved")
        messagebox.showinfo("Application Info", info_text)

    def check_initial_state(self):
        creds = load_credentials()
        if creds:
            token = creds.get("access_token")
            self.agent.current_association_id = creds.get("association_id")
            self.show_status_view()
            self.start_agent_thread(token)
        else:
            self.show_pairing_view()

    def show_pairing_view(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        card = ctk.CTkFrame(self.content_frame, fg_color=Theme.BG_SECONDARY, corner_radius=16, border_width=1, border_color=Theme.BORDER_SUBTLE)
        card.pack(fill="both", expand=True, pady=10)
        self.pairing_label = ctk.CTkLabel(card, text="Pairing Code", font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=16, weight="bold"), text_color=Theme.TEXT_DEFAULT)
        self.pairing_label.pack(pady=(30, 5))
        self.pairing_desc = ctk.CTkLabel(card, text="Enter the code from your mobile app", font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=12), text_color=Theme.TEXT_MUTED)
        self.pairing_desc.pack(pady=(0, 20))
        self.pairing_entry = ctk.CTkEntry(card, placeholder_text="XXXXXX", width=220, height=50, justify="center", font=ctk.CTkFont(family=Theme.FONT_MONO, size=24, weight="bold"), fg_color=Theme.BG_BASE, border_color=Theme.BORDER_SUBTLE, text_color=Theme.BRAND_GREEN)
        self.pairing_entry.pack(pady=10)
        self.pairing_entry.bind("<KeyRelease>", self.force_caps_pairing)
        self.pair_button = ctk.CTkButton(card, text="Verify Code", command=self.handle_pairing, fg_color=Theme.BRAND_GREEN, hover_color=Theme.BRAND_GREEN_HOVER, text_color=Theme.BG_BASE, font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=14, weight="bold"), height=45, corner_radius=8)
        self.pair_button.pack(pady=(30, 30), padx=40, fill="x")

    def force_caps_pairing(self, event):
        current_text = self.pairing_entry.get()
        self.pairing_entry.delete(0, "end")
        self.pairing_entry.insert(0, current_text.upper())

    def handle_pairing(self):
        code = self.pairing_entry.get().strip()
        if not code: return
        self.pair_button.configure(state="disabled", text="Verifying...")
        device_id = str(uuid.uuid4())
        def run_pairing():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            assoc_id = loop.run_until_complete(self.agent.start_pairing(code, device_id))
            if assoc_id:
                self.after(0, lambda: self.show_otp_view(assoc_id))
            else:
                self.after(0, lambda: self.pair_button.configure(state="normal", text="Verify Code"))
                self.after(0, lambda: self.update_status_msg("Pairing failed. Check code.", is_error=True))
        threading.Thread(target=run_pairing, daemon=True).start()

    def show_otp_view(self, assoc_id):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        card = ctk.CTkFrame(self.content_frame, fg_color=Theme.BG_SECONDARY, corner_radius=16, border_width=1, border_color=Theme.BORDER_SUBTLE)
        card.pack(fill="both", expand=True, pady=10)
        self.otp_label = ctk.CTkLabel(card, text="Security Code (OTP)", font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=16, weight="bold"), text_color=Theme.TEXT_DEFAULT)
        self.otp_label.pack(pady=(30, 5))
        self.otp_desc = ctk.CTkLabel(card, text="Enter the 6-digit OTP from your app", font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=12), text_color=Theme.TEXT_MUTED)
        self.otp_desc.pack(pady=(0, 20))
        self.otp_entry = ctk.CTkEntry(card, placeholder_text="000000", width=220, height=50, justify="center", font=ctk.CTkFont(family=Theme.FONT_MONO, size=24, weight="bold"), fg_color=Theme.BG_BASE, border_color=Theme.BORDER_SUBTLE, text_color=Theme.BRAND_GREEN)
        self.otp_entry.pack(pady=10)
        self.confirm_button = ctk.CTkButton(card, text="Confirm OTP", command=lambda: self.handle_otp(assoc_id), fg_color=Theme.BRAND_GREEN, hover_color=Theme.BRAND_GREEN_HOVER, text_color=Theme.BG_BASE, font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=14, weight="bold"), height=45, corner_radius=8)
        self.confirm_button.pack(pady=(30, 30), padx=40, fill="x")

    def handle_otp(self, assoc_id):
        otp = self.otp_entry.get().strip()
        if not otp: return
        self.confirm_button.configure(state="disabled", text="Confirming...")
        def run_confirm():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            token = loop.run_until_complete(self.agent.confirm_otp(assoc_id, otp))
            if token:
                self.after(0, lambda: self.show_status_view(is_first_setup=True))
                self.after(0, lambda: self.start_agent_thread(token))
            else:
                self.after(0, lambda: self.confirm_button.configure(state="normal", text="Confirm OTP"))
                self.after(0, lambda: self.update_status_msg("OTP invalid.", is_error=True))
        threading.Thread(target=run_confirm, daemon=True).start()

    def show_status_view(self, is_first_setup=False):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        card = ctk.CTkFrame(self.content_frame, fg_color=Theme.BG_SECONDARY, corner_radius=16, border_width=1, border_color=Theme.BORDER_SUBTLE)
        card.pack(fill="both", expand=True, pady=10)
        self.anim_frame = ctk.CTkFrame(card, fg_color="transparent")
        self.anim_frame.pack(pady=(30, 0))
        self.status_indicator = ctk.CTkLabel(self.anim_frame, text="●", text_color=Theme.BRAND_GREEN, font=ctk.CTkFont(size=48))
        self.status_indicator.pack()
        self.status_text = ctk.CTkLabel(card, text="Connection Active", font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=20, weight="bold"), text_color=Theme.TEXT_DEFAULT)
        self.status_text.pack(pady=(10, 5))
        self.status_subtext = ctk.CTkLabel(card, text="Everything is working correctly", font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=13), text_color=Theme.BRAND_GREEN)
        self.status_subtext.pack(pady=(0, 20))
        if is_first_setup:
            self.phone_msg_frame = ctk.CTkFrame(card, fg_color=Theme.BG_BASE, corner_radius=12, border_width=1, border_color=Theme.BRAND_GREEN)
            self.phone_msg_frame.pack(padx=30, fill="x", pady=10)
            ctk.CTkLabel(self.phone_msg_frame, text="IMPORTANT", font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=10, weight="bold"), text_color=Theme.BRAND_GREEN).pack(pady=(10, 0))
            ctk.CTkLabel(self.phone_msg_frame, text="Click 'Done' on your Mobile App\nto complete the setup", font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=13, weight="bold"), text_color=Theme.TEXT_DEFAULT).pack(pady=(5, 15))
            self.after(10000, self.hide_phone_message)
        bg_instructions = ctk.CTkLabel(card, text="You can now close or minimize this window.\nThe agent will continue to run in the background.", font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=11), text_color=Theme.TEXT_SECONDARY, justify="center")
        bg_instructions.pack(pady=(20, 5), padx=20)
        kill_switch_info = ctk.CTkLabel(card, text="EMERGENCY STOP: Move mouse + 5 clicks in 3s", font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=10, weight="bold"), text_color=Theme.ERROR_RED, justify="center")
        kill_switch_info.pack(pady=(0, 10), padx=20)
        info_frame = ctk.CTkFrame(card, fg_color=Theme.BG_BASE, corner_radius=8)
        info_frame.pack(padx=30, fill="x", pady=(20, 10))
        self.id_label = ctk.CTkLabel(info_frame, text="AGENT ID", font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=10, weight="bold"), text_color=Theme.TEXT_MUTED)
        self.id_label.pack(pady=(10, 0))
        self.id_val = ctk.CTkLabel(info_frame, text=str(self.agent.current_association_id or 'N/A'), font=ctk.CTkFont(family=Theme.FONT_MONO, size=12), text_color=Theme.BRAND_GREEN)
        self.id_val.pack(pady=(0, 10))
        self.disconnect_button = ctk.CTkButton(card, text="Disconnect", fg_color="transparent", text_color=Theme.ERROR_RED, hover_color=Theme.BG_BASE, border_width=1, border_color=Theme.ERROR_RED, command=self.confirm_disconnect, height=35, corner_radius=8)
        self.disconnect_button.pack(pady=(20, 20), padx=60, fill="x")
        self.animate_status()

    def confirm_disconnect(self):
        if messagebox.askyesno("Confirm Disconnect", "Are you sure you want to disconnect? This will stop the current session."):
            if messagebox.askyesno("Final Confirmation", "WARNING: This will permanently delete the local association. You will need a new pairing code to reconnect. Proceed?"):
                self.handle_disconnect()

    def animate_status(self):
        def pulse():
            if not hasattr(self, 'status_indicator'): return
            try:
                colors = [Theme.BRAND_GREEN, Theme.BRAND_GREEN_HOVER, "#ffffff", Theme.BRAND_GREEN_HOVER]
                for color in colors:
                    if not self.agent._running: break
                    self.status_indicator.configure(text_color=color)
                    time.sleep(0.5)
                if self.agent._running:
                    self.after(100, pulse)
            except Exception:
                pass
        import time
        threading.Thread(target=pulse, daemon=True).start()

    def hide_phone_message(self):
        try:
            if hasattr(self, 'phone_msg_frame') and self.phone_msg_frame.winfo_exists():
                self.phone_msg_frame.destroy()
        except Exception:
            pass

    def handle_disconnect(self):
        clear_credentials()
        self.agent.stop()
        self.show_pairing_view()

    def update_status(self, msg: str):
        if hasattr(self, 'status_text'):
            self.status_text.configure(text=msg)
            if "Connected" in msg:
                self.status_indicator.configure(text_color=Theme.BRAND_GREEN)
                self.status_subtext.configure(text="Everything is working correctly")
            elif "lost" in msg or "retrying" in msg:
                self.status_indicator.configure(text_color="orange")
                self.status_subtext.configure(text="Connection issue, trying to reconnect")
            else:
                self.status_indicator.configure(text_color=Theme.TEXT_MUTED)
                self.status_subtext.configure(text="Agent is offline")

    def update_status_msg(self, msg: str, is_error=False):
        if hasattr(self, 'subtitle_label'):
            self.subtitle_label.configure(text=msg.upper(), text_color=Theme.ERROR_RED if is_error else Theme.TEXT_SECONDARY)

    def start_agent_thread(self, token):
        def run_agent():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            threading.Thread(target=self.agent.start_kill_switch, args=(loop,), daemon=True).start()
            loop.run_until_complete(self.agent.run(token))
        threading.Thread(target=run_agent, daemon=True).start()

    def setup_tray(self):
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "..", "TRAE_Mobile.png")
            if not os.path.exists(icon_path):
                image = Image.new('RGB', (64, 64), color=(50, 240, 140))
            else:
                image = Image.open(icon_path)
        except Exception:
            image = Image.new('RGB', (64, 64), color=(50, 240, 140))
        menu = pystray.Menu(pystray.MenuItem("Show", self.show_window), pystray.MenuItem("Exit", self.exit_app))
        self.tray_icon = pystray.Icon("trae_agent", image, "TRAE Mobile Agent", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def hide_window(self):
        self.withdraw()
        if self.tray_icon:
            self.tray_icon.notify("Agent is running in the background", "TRAE Mobile Agent")

    def on_minimize(self, event):
        if self.state() == 'iconic':
            self.hide_window()

    def show_window(self, icon=None, item=None):
        self.after(0, self.deiconify)

    def exit_app(self, icon=None, item=None):
        self.agent.stop()
        if self.tray_icon:
            self.tray_icon.stop()
        self.quit()
        sys.exit(0)
